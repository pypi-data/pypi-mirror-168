from wiliot.system_network_tools.packet_monitor import PacketMonitor

from bokeh.plotting import curdoc
from bokeh.models.widgets import Button, Div, DataTable, TableColumn
from bokeh.layouts import column, row
from bokeh.models import Column, ColumnDataSource
import sys

user_configs = {'user_name': '<USER-NAME>@wiliot.com', 'user_pass': '<PASSWORD>', 'owner_id': 'wiliot-ops',
                'env': ''}
# graph params:
global bokeh_doc, unique_tags_title_div, stop_button, table_title_div, table_col, data_table
try:
    monitor = PacketMonitor(user_configs=user_configs)
except Exception as e:
    print(e)
    sys.exit()


def init_graph():
    global bokeh_doc, unique_tags_title_div, stop_button, table_title_div, table_col, data_table, monitor
    # init the graph:
    bokeh_doc = curdoc()

    # unique tag log:
    unique_tags_title_div = Div(text='', width=300, height=30,
                                style={'font-size': '150%', 'color': 'blue', 'font-weight': 'bold'})
    unique_tags_title_div.text = 'Number of Unique Tags:'

    # Button to stop the server
    stop_button = Button(label="Stop", button_type="success")
    stop_button.on_click(monitor.stop_monitor)
    # Summary table:
    table_title_div = Div(text='', width=300, height=30,
                          style={'font-size': '200%', 'color': 'black', 'font-weight': 'bold'})
    table_title_div.text = 'Summary:'
    table_col = [TableColumn(field=k, title=k) for k in monitor.tags.keys()]
    data_table = DataTable(columns=table_col, source=ColumnDataSource(monitor.tags))

    # log the results:
    print('You can type "http://localhost:5006/packet_monitor" in your browser to see the results')


def run_graph():
    global bokeh_doc, unique_tags_title_div, stop_button, table_title_div, table_col, data_table, monitor
    # run continuously
    bokeh_doc.title = "Wiliot Monitor"
    bokeh_doc.add_root(row([column([unique_tags_title_div, table_title_div, data_table,
                                    Column(stop_button, align="center")])]))
    bokeh_doc.add_periodic_callback(plot_callback, 50)


def update_table():
    global bokeh_doc, unique_tags_title_div, stop_button, table_title_div, table_col, data_table, monitor
    data_table.source.data = monitor.tags


def update_unique_tags():
    global bokeh_doc, unique_tags_title_div, stop_button, table_title_div, table_col, data_table, monitor
    unique_tags_title_div.text = 'Number of Unique Tags: {}'.format(len(monitor.tags['tag_id']))


def plot_callback():
    update_table()
    update_unique_tags()


# run graph:
init_graph()
run_graph()
