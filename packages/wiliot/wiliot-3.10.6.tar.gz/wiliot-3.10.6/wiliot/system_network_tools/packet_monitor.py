"""
  Copyright (c) 2016- 2021, Wiliot Ltd. All rights reserved.

  Redistribution and use of the Software in source and binary forms, with or without modification,
   are permitted provided that the following conditions are met:

     1. Redistributions of source code must retain the above copyright notice,
     this list of conditions and the following disclaimer.

     2. Redistributions in binary form, except as used in conjunction with
     Wiliot's Pixel in a product or a Software update for such product, must reproduce
     the above copyright notice, this list of conditions and the following disclaimer in
     the documentation and/or other materials provided with the distribution.

     3. Neither the name nor logo of Wiliot, nor the names of the Software's contributors,
     may be used to endorse or promote products or services derived from this Software,
     without specific prior written permission.

     4. This Software, with or without modification, must only be used in conjunction
     with Wiliot's Pixel or with Wiliot's cloud service.

     5. If any Software is provided in binary form under this license, you must not
     do any of the following:
     (a) modify, adapt, translate, or create a derivative work of the Software; or
     (b) reverse engineer, decompile, disassemble, decrypt, or otherwise attempt to
     discover the source code or non-literal aspects (such as the underlying structure,
     sequence, organization, ideas, or algorithms) of the Software.

     6. If you create a derivative work and/or improvement of any Software, you hereby
     irrevocably grant each of Wiliot and its corporate affiliates a worldwide, non-exclusive,
     royalty-free, fully paid-up, perpetual, irrevocable, assignable, sublicensable
     right and license to reproduce, use, make, have made, import, distribute, sell,
     offer for sale, create derivative works of, modify, translate, publicly perform
     and display, and otherwise commercially exploit such derivative works and improvements
     (as applicable) in conjunction with Wiliot's products and services.

     7. You represent and warrant that you are not a resident of (and will not use the
     Software in) a country that the U.S. government has embargoed for use of the Software,
     nor are you named on the U.S. Treasury Department’s list of Specially Designated
     Nationals or any other applicable trade sanctioning regulations of any jurisdiction.
     You must not transfer, export, re-export, import, re-import or divert the Software
     in violation of any export or re-export control laws and regulations (such as the
     United States' ITAR, EAR, and OFAC regulations), as well as any applicable import
     and use restrictions, all as then in effect

   THIS SOFTWARE IS PROVIDED BY WILIOT "AS IS" AND "AS AVAILABLE", AND ANY EXPRESS
   OR IMPLIED WARRANTIES OR CONDITIONS, INCLUDING, BUT NOT LIMITED TO, ANY IMPLIED
   WARRANTIES OR CONDITIONS OF MERCHANTABILITY, SATISFACTORY QUALITY, NONINFRINGEMENT,
   QUIET POSSESSION, FITNESS FOR A PARTICULAR PURPOSE, AND TITLE, ARE DISCLAIMED.
   IN NO EVENT SHALL WILIOT, ANY OF ITS CORPORATE AFFILIATES OR LICENSORS, AND/OR
   ANY CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY,
   OR CONSEQUENTIAL DAMAGES, FOR THE COST OF PROCURING SUBSTITUTE GOODS OR SERVICES,
   FOR ANY LOSS OF USE OR DATA OR BUSINESS INTERRUPTION, AND/OR FOR ANY ECONOMIC LOSS
   (SUCH AS LOST PROFITS, REVENUE, ANTICIPATED SAVINGS). THE FOREGOING SHALL APPLY:
   (A) HOWEVER CAUSED AND REGARDLESS OF THE THEORY OR BASIS LIABILITY, WHETHER IN
   CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE);
   (B) EVEN IF ANYONE IS ADVISED OF THE POSSIBILITY OF ANY DAMAGES, LOSSES, OR COSTS; AND
   (C) EVEN IF ANY REMEDY FAILS OF ITS ESSENTIAL PURPOSE.
"""
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
    def __init__(self, user_configs, logger_name=None):
        """

        :param user_configs: dict with user_name, user_pass, owner_id, env
        :type user_configs: dict
        """
        self.is_stop = False
        self.tags = {'tag_id': [], 'adv_address': [], 'counter': [], 'last_packet_time': []}
        self.results_lock = threading.Lock()
        # define log:
        if logger_name is None:
            self.logger = logging.getLogger('WiliotMonitor')
            self.set_logger()
        else:
            self.logger = logging.getLogger('WiliotMonitor')

        # connect to the cloud:
        try:
            self.client = Client(oauth_username=user_configs['user_name'], oauth_password=user_configs['user_pass'],
                                 owner_id=user_configs['owner_id'], env=user_configs['env'])
            self.logger.log(logging.INFO, 'Cloud Connection was established')
        except Exception as e:
            raise Exception('Cloud Connection Problem: {}'.format(e))

        # connect to the gw:
        self.GwObj = None
        self.gw_init()
        self.gw_reset_and_config()

    def set_logger(self):
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
        self.GwObj = WiliotGateway(auto_connect=True)
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
        self.GwObj.close_port(is_reset=True)
        for i in range(5):
            time.sleep(1)
            # open GW again
            if self.GwObj.open_port(port=self.GwObj.port, baud=self.GwObj.baud):
                break
        if self.GwObj.connected:
            self.GwObj.start_continuous_listener()
            self.GwObj.write('!set_tester_mode 1', with_ack=True)
            self.GwObj.write('!listen_to_tag_only 0', with_ack=True)
            self.GwObj.config_gw(received_channel=37, time_profile_val=[0, 15],
                                 start_gw_app=True, with_ack=True)
        else:
            e = 'Could NOT reconnect to GW after reset'
            self.logger.log(logging.WARNING, e)
            raise Exception(e)

    def stop_monitor(self):
        self.is_stop = True

    def exit_app(self):
        self.GwObj.close_port(is_reset=True)
        self.GwObj.stop_continuous_listener()
        sys.exit()  # Stop the server

    def start_monitor(self):
        self.logger.log(logging.INFO, "Monitor Start")

        def existing_tag(adva_or_ex_id, time_str_now, new_adva):
            if new_adva:
                ind = self.tags['tag_id'].index(adva_or_ex_id)
                self.tags['adv_address'][ind] = new_adva
            else:
                ind = self.tags['adv_address'].index(adva_or_ex_id)
            self.tags['counter'][ind] += 1
            self.tags['last_packet_time'][ind] = time_str_now

        def new_tag(new_adva, new_ex_id, time_str_now):
            self.tags['adv_address'].append(new_adva)
            self.tags['tag_id'].append(new_ex_id)
            self.tags['counter'].append(1)
            self.tags['last_packet_time'].append(time_str_now)

        while True:
            time.sleep(0)
            try:
                if self.is_stop:
                    self.logger.log(logging.INFO, "Monitor Stop")
                    self.exit_app()
                    return

                # check if there is data to read
                if self.GwObj.is_data_available():
                    packet_list_in = self.GwObj.get_packets(action_type=ActionType.ALL_SAMPLE)
                    for packet in packet_list_in:
                        raw_packet = packet.get_packet_string(process_packet=False, gw_data=False)
                        self.logger.log(logging.INFO, raw_packet)
                        try:
                            adva = packet.packet_data['adv_address']
                            with self.results_lock:
                                time_str = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                                if adva in self.tags['adv_address'] and not packet.is_packet_from_bridge():
                                    existing_tag(adva, time_str, '')
                                else:  # maybe a new tag
                                    payload = raw_packet[16:74]
                                    rsp = self.client.resolve_payload(payload=payload)
                                    ex_id = rsp['externalId']
                                    if ex_id in self.tags['tag_id']:
                                        existing_tag(ex_id, time_str, adva)
                                    else:
                                        new_tag(adva, ex_id, time_str)

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
