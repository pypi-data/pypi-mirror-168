from wiliot.gateway_api.gateway import WiliotGateway, ActionType
from wiliot.cloud_apis.security import security
from wiliot.cloud_apis.api_client import WiliotCloudError
import requests
from uuid import uuid4
import json

import threading
import logging
import time
import datetime

import sys


class Client:
    def __init__(self, oauth_username, oauth_password, owner_id, env=''):
        self.owner_id = owner_id
        self.env = env+"/" if env != '' else ''
        api_path = "https://api.wiliot.com/{env}v1/".format(env=self.env)
        self.base_path = api_path + "owner/{owner}/".format(owner=owner_id)
        self.headers = {
            "accept": "application/json",
            "Content-Type": "application/json"
        }
        self.auth_obj = security.WiliotAuthentication(api_path, oauth_username, oauth_password)
        self.headers["Authorization"] = self.auth_obj.get_token()

    def resolve_payload(self, payload):
        """
        Resolve a tag's payload
        :param payload: valid Wiliot tag payload starting with the manufacturer ID
        :return: A dictionary from the returned JSON
        """
        now_ts = int(datetime.datetime.now().timestamp())
        payload = {
            'timestamp': now_ts,
            'packets': [
                {
                    'timestamp': now_ts,
                    'payload': payload
                }
            ],
            'gatewayType': 'cli',
            'gatewayId': str(uuid4())
        }
        res = self._post("resolve", payload)
        return res['data'][0]

    def _post(self, path, payload):
        response = requests.post(self.base_path + path, headers=self.headers, data=json.dumps(payload))
        if int(response.status_code/100) != 2:
            raise WiliotCloudError(response.text)
        message = response.json()
        return message


class PacketMonitor(object):
    def __init__(self, user_configs):
        """

        :param user_configs: dict with user_name, user_pass, owner_id, env
        :type user_configs: dict
        """
        self.is_stop = False
        self.tags = {'tag_id': [], 'counter': [], 'last_packet_time': []}
        self.results_lock = threading.Lock()
        # define log:
        self.logger = logging.getLogger('WiliotMonitor')
        self.set_logger()
        # connect to the cloud:
        try:
            self.client = Client(oauth_username=user_configs['user_name'], oauth_password=user_configs['user_pass'],
                                 owner_id=user_configs['owner_id'], env=user_configs['env'])
        except Exception as e:
            raise Exception('Cloud Connection Problem: {}'.format(e))

        # connect to the gw:
        self.GwObj = None
        self.gw_init()
        self.gw_reset_and_config()

    def set_logger(self, log_path=None, tester_name='tester'):
        ''' Sets the logger if doesn't exist from main code - INFO level
        3 loggers declared
        self.logger - our main for packet
        self.results_logger - for results
        self.gw_logger - for GW logging'''
        formatter = logging.Formatter('\x1b[36;20m%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                                      '%H:%M:%S')
        stream_handler = logging.StreamHandler()
        stream_handler.setLevel(logging.DEBUG)
        stream_handler.setFormatter(formatter)
        self.logger.addHandler(stream_handler)
        self.logger.setLevel(logging.DEBUG)

    def gw_init(self):
        """
        initialize gw and the data listener thread
        """
        self.GwObj = WiliotGateway(auto_connect=True, logger_name=self.logger.name,
                                   lock_print=threading.Lock())
        try:
            if self.GwObj.connected:
                self.GwObj.reset_buffer()
                self.GwObj.start_continuous_listener()

                data_handler_listener = threading.Thread(target=self.start_monitor, args=())
                data_handler_listener.start()
            else:
                raise Exception('gateway was not detected, please check connection')
        except Exception as e:
            self.logger.log(logging.WARNING, e)
            raise e

    def gw_reset_and_config(self):
        """
        reset gw and config it to tester mode
        """
        self.GwObj.reset_gw()
        time.sleep(2)
        self.GwObj.write('!enable_brg_mgmt 0', with_ack=True)
        self.GwObj.config_gw(received_channel=37, time_profile_val=[0, 15],
                             start_gw_app=True, with_ack=True)

    def stop_monitor(self):
        self.is_stop = True

    def exit_app(self):
        self.GwObj.close_port(is_reset=True)
        self.GwObj.stop_continuous_listener()
        self.GwObj._port_listener_thread.join()
        sys.exit()  # Stop the server

    def start_monitor(self):
        print("Monitor Start")
        consecutive_exception_counter = 0
        while True:
            time.sleep(0)
            try:
                if self.is_stop:
                    print("Monitor Stop")
                    self.exit_app()
                    return

                # check if there is data to read
                if self.GwObj.is_data_available():
                    packet_list_in = self.GwObj.get_packets(action_type=ActionType.ALL_SAMPLE)
                    for packet in packet_list_in:
                        raw_packet = packet.get_packet_string(process_packet=False, gw_data=False)
                        try:
                            payload = raw_packet[16:74]
                            rsp = self.client.resolve_payload(payload=payload)
                            ex_id = rsp['externalId']
                            with self.results_lock:
                                time_str = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                                if ex_id in self.tags['tag_id']:
                                    ind = self.tags['tag_id'].index(ex_id)
                                    self.tags['counter'][ind] += 1
                                    self.tags['last_packet_time'][ind] = time_str
                                else:  # new tag
                                    self.tags['tag_id'].append(ex_id)
                                    self.tags['counter'].append(1)
                                    self.tags['last_packet_time'].append(time_str)

                        except Exception as e:
                            raise Exception('could not resolve payload ({})'.format(e))
            except Exception as e:
                self.logger.log(logging.WARNING, 'got exception during monitor: {}'.format(e))

    def present_results(self):
        with self.results_lock:
            print(' *********************************** ')
            print('number of unique tags: {}\nlist of tags:'.format(len(self.tags['tag_id'])))
            for i in range(len(self.tags['tag_id'])):
                row = {}
                for k, v in self.tags.items():
                    row[k] = v[i]
                print(row)


if __name__ == '__main__':
    user_configs = {'user_name': '<USER-NAME>@wiliot.com', 'user_pass': '<PASSWORD>', 'owner_id': 'wiliot-ops',
                    'env': ''}

    monitor = PacketMonitor(user_configs=user_configs)
    for i in range(10):
        time.sleep(1)
        monitor.present_results()
    monitor.stop_monitor()
    print('exit')
