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
import datetime

from wiliot.system_network_tools.packet_monitor import PacketMonitor
from wiliot.wiliot_testers.offline.offline_utils import WiliotDir

from bokeh.plotting import curdoc
from bokeh.models.widgets import Button, Div, DataTable, TableColumn, TextInput
from bokeh.layouts import column, row
from bokeh.models import Column, ColumnDataSource
import sys
from getpass import getpass
import logging
import os
import pandas as pd


class PlotPacketMonitor(object):
    def __init__(self):
        print("Please run using CLI (command line interface) with the following line at the code location:"
              "bokeh serve --show run_packet_monitor.py")
        user_name = input('Please Enter user name:\n')
        user_pass = getpass('Please Enter Password:\n')
        owner_id = input('Please Enter owner id:\n')
        self.user_configs = {'user_name': user_name, 'user_pass': user_pass, 'owner_id': owner_id, 'env': ''}
        self.logger = logging.getLogger('WiliotMonitor')
        self.set_logger()
        # init monitor
        self.monitor = None
        self.init_monitor()
        # init graph
        self.bokeh_doc = None
        self.unique_tags_title_div = None
        self.stop_button = None
        self.table_title_div = None
        self.table_col = None
        self.data_table = None
        self.num_of_physical_tags = None
        self.log_path = None
        self.log_div = None
        self.save_button = None
        self.init_graph()

    def set_logger(self):
        formatter = logging.Formatter('%(asctime)s,%(msecs)d %(name)s %(levelname)s: %(message)s', '%Y-%m-%d %H:%M:%S')
        stream_handler = logging.StreamHandler()
        stream_handler.setLevel(logging.DEBUG)
        stream_handler.setFormatter(formatter)
        self.logger.addHandler(stream_handler)
        self.logger.setLevel(logging.INFO)

    def init_monitor(self):
        try:
            self.monitor = PacketMonitor(user_configs=self.user_configs, logger_name=self.logger.name)
        except Exception as e:
            self.logger.log(logging.WARNING, e)
            sys.exit()

    def log_results(self):
        if not os.path.isdir(self.log_path.value):
            wiliot_dir = WiliotDir()
            self.log_path.value = os.path.join(wiliot_dir.get_wiliot_root_app_dir(), 'wiliot_monitor')
            if not os.path.isdir(self.log_path.value):
                os.makedirs(self.log_path.value)
        if self.num_of_physical_tags.value == '':
            self.num_of_physical_tags.value = 'X'

        file_path = os.path.join(self.log_path.value, 'wiliot_monitor_{}.csv'.format(
            datetime.datetime.now().strftime("%Y%m%d_%H%M%S")))
        df_title = pd.DataFrame({'summary': ['Received {} unique tags '
                                             'out of {} tags'.format(len(self.monitor.tags['tag_id']),
                                                                     self.num_of_physical_tags.value)]})
        df_title.to_csv(file_path,  index=False)
        df_tags = pd.DataFrame(self.monitor.tags)
        df_tags.to_csv(file_path, mode='a', index=False)
        self.log_div.text = 'data was saved at {}'.format(self.log_path.value)

    def init_graph(self):
        # init the graph:
        self.bokeh_doc = curdoc()

        # unique tag log:
        self.unique_tags_title_div = Div(text='', width=300, height=30,
                                         style={'font-size': '150%', 'color': 'blue', 'font-weight': 'bold'})
        self.unique_tags_title_div.text = 'Number of Unique Tags:'

        # Button to stop the server
        self.stop_button = Button(label="Stop", button_type="danger")
        self.stop_button.on_click(self.monitor.stop_monitor)
        # save to csv
        self.num_of_physical_tags = TextInput(value="", title="number of physical tags")
        self.log_path = TextInput(value="", title="folder directory")
        self.log_div = Div(text='', width=300, height=800, style={'font-size': '100%', 'color': 'black',
                                                                  'font-weight': 'bold'})
        self.save_button = Button(label="Save", button_type="success")
        self.save_button.on_click(self.log_results)
        # Summary table:
        self.table_title_div = Div(text='', width=300, height=30,
                                   style={'font-size': '200%', 'color': 'black', 'font-weight': 'bold'})
        self.table_title_div.text = 'Summary:'
        self.table_col = [TableColumn(field=k, title=k) for k in self.monitor.tags.keys()]
        self.data_table = DataTable(columns=self.table_col, source=ColumnDataSource(self.monitor.tags))

        # log the results:
        self.logger.log(logging.INFO,
                        'You can type "http://localhost:5006/packet_monitor" in your browser to see the results')

    def run_graph(self):
        # run continuously
        self.bokeh_doc.title = "Wiliot Monitor"
        self.bokeh_doc.add_root(row([column([self.unique_tags_title_div, self.table_title_div, self.data_table,
                                             Column(self.stop_button, align="center")]),
                                     column([self.num_of_physical_tags, self.log_path,
                                             self.save_button, self.log_div])]))
        self.bokeh_doc.add_periodic_callback(self.plot_callback, 50)

    def update_table(self):
        self.data_table.source.data = self.monitor.tags

    def update_unique_tags(self):
        self.unique_tags_title_div.text = 'Number of Unique Tags: {}'.format(len(self.monitor.tags['tag_id']))

    def plot_callback(self):
        self.update_table()
        self.update_unique_tags()
        if self.monitor.is_stop:
            self.logger.log(logging.INFO, 'done')
            sys.exit(0)


# run graph:
p = PlotPacketMonitor()
p.run_graph()
