from random import random
from bokeh.layouts import column, layout, widgetbox
from bokeh.models import Button
from bokeh.palettes import RdYlBu3, Viridis6
from bokeh.plotting import figure, curdoc
from bokeh.io import output_file, show
from bokeh.models.widgets import Dropdown
from bokeh.models import NumeralTickFormatter, HoverTool, ColumnDataSource, CustomJS, LinearAxis, Range1d
from bokeh.models.annotations import Title
import numpy as np
import pandas as pd
from pymongo import MongoClient
from datetime import datetime
import datetime as dt
import time

#INPUT VARIABLES - GLOBAL
end_days = 0
end_hours = 0
end_mins = 0
current_time = True
now = dt.datetime.utcnow()

#DEFINE EMPTY LISTS
time_str_list1 = []
metric_list1 = []
time_str_list2 = []
metric_list2 = []

#DEFINE MONGODB CONNECTION
connect = MongoClient('mongodb://192.168.0.53/')

#DROPDOWN WIDGETS
menu_days = [("0", "0"), ("1", "1"), ("2", "2"), ("3", "3"), ("4", "4"), ("5", "5"), ("6", "6"), ("7", "7"), ("8", "8"), ("9", "9"),("10", "10"), ("11", "11"), ("12", "12"), ("13", "13"), ("14", "14"), ("15", "15"), ("16", "16"), ("17", "17"), ("18", "18"), ("19", "19"), ("20", "20"), ("21", "21"), ("22", "22"), ("23", "23"), ("24", "24"), ("25", "25"), ("26", "26"), ("27", "27"), ("28", "28"), ("29", "29"), ("30", "30"), ("60", "60"), ("90", "90"),("120", "120"), ("365", "365")]
dropdown_days = Dropdown(label="Days Back", button_type="warning", menu=menu_days, value="0")

menu_hours = [("0", "0"), ("1", "1"), ("2", "2"), ("3", "3"), ("4", "4"), ("5", "5"), ("6", "6"), ("7", "7"), ("8", "8"), ("9", "9"), ("10", "10"), ("11", "11"), ("12", "12"), ("13", "13"), ("14", "14"), ("15", "15"), ("16", "16"), ("17", "17"), ("18", "18"), ("19", "19"), ("20", "20"), ("21", "21"), ("22", "22"), ("23", "23")]
dropdown_hours = Dropdown(label="Hours Back", button_type="warning", menu=menu_hours, value="0")

menu_mins = [("0", "0"), ("1", "1"), ("2", "2"), ("3", "3"), ("4", "4"), ("5", "5"), ("6", "6"), ("7", "7"), ("8", "8"), ("9", "9"), ("10", "10"), ("11", "11"), ("12", "12"), ("13", "13"), ("14", "14"), ("15", "15"), ("16", "16"), ("17", "17"), ("18", "18"), ("19", "19"), ("20", "20"), ("21", "21"), ("22", "22"), ("23", "23"), ("24", "24"), ("25", "25"), ("26", "26"), ("27", "27"), ("28", "28"), ("29", "29"), ("30", "30"), ("31", "31"), ("32", "32"), ("33", "33"), ("34", "34"), ("35", "35"), ("36", "36"), ("37", "37"), ("38", "38"), ("39", "39"), ("40", "40"), ("41", "41"), ("42", "42"), ("43", "43"), ("44", "44"), ("45", "45"), ("46", "46"), ("47", "47"), ("48", "48"), ("49", "49"), ("50", "50"), ("51", "51"), ("52", "52"), ("53", "53"), ("54", "54"), ("55", "55"), ("56", "56"), ("57", "57"), ("58", "58"), ("59", "59")]
dropdown_mins = Dropdown(label="Minutes Back", button_type="warning", menu=menu_mins, value="0")

menu_coll1 = [("traffic_rate", "traffic_rate"), ("traffic_rate_dennett", "traffic_rate_dennett"), ("server_response_popper", "server_response_popper"), ("network_delay", "network_delay"), ("network_delay_viavidotcom", "network_delay_viavidotcom"), ("skyrouter_response", "skyrouter_response"), ("viavidotcom_response", "viavidotcom_response"), ("popper_cpu", "popper_cpu"), ("dennett_cpu", "dennett_cpu"), ("dennett_free_memory", "dennett_free_memory"), ("dennett_disk_used",  "dennett_disk_used"), ("hyp1_cpu", "hyp1_cpu"), ("hyp1_free_memory", "hyp1_free_memory"), ("hyp1_disk_used", "hyp1_disk_used"), ("rochester_temp", "rochester_temp")]
dropdown_coll1 = Dropdown(label="Metric1", button_type="warning", menu=menu_coll1, value="traffic_rate")

menu_coll2 = [("traffic_rate", "traffic_rate"), ("traffic_rate_dennett", "traffic_rate_dennett"), ("server_response_popper", "server_response_popper"), ("network_delay", "network_delay"), ("network_delay_viavidotcom", "network_delay_viavidotcom"), ("skyrouter_response", "skyrouter_response"), ("viavidotcom_response", "viavidotcom_response"), ("popper_cpu", "popper_cpu"), ("dennett_cpu", "dennett_cpu"), ("dennett_free_memory", "dennett_free_memory"), ("dennett_disk_used",  "dennett_disk_used"), ("hyp1_cpu", "hyp1_cpu"), ("hyp1_free_memory", "hyp1_free_memory"), ("hyp1_disk_used", "hyp1_disk_used"), ("rochester_temp", "rochester_temp")]
dropdown_coll2 = Dropdown(label="Metric2", button_type="warning", menu=menu_coll2, value="traffic_rate")

graph1_title = "Choose From The Menu Items Above"
graph2_title = ""

#EMPTY GRAPHS
graph1 = figure(x_axis_type="datetime", title=graph1_title, plot_width=1700, plot_height=300)
graph2 = figure(x_axis_type="datetime", title=graph2_title, plot_width=1700, plot_height=300)

graph1_source = ColumnDataSource(data={'Time':[], 'Metric':[]})
graph2_source = ColumnDataSource(data={'Time':[], 'Metric':[]})

graph1.line(source=graph1_source, x='Time', y='Metric', color='navy', alpha=0.9, line_width=2)
graph2.line(source=graph2_source, x='Time', y='Metric', color='navy', alpha=0.9, line_width=2)

graph1.left[0].formatter.use_scientific = False
graph1.yaxis[0].formatter = NumeralTickFormatter(format='0,0.00')

graph2.left[0].formatter.use_scientific = False
graph2.yaxis[0].formatter = NumeralTickFormatter(format='0,0.00')

graph1.title.text_font_size='13pt'
graph1.title.text_color='navy'

graph2.title.text_font_size='13pt'
graph2.title.text_color='navy'

def refresh_graphs(attr, old, new):
#TIME SELECTION
    start_days = int(dropdown_days.value)
    start_hours = int(dropdown_hours.value)
    start_mins = int(dropdown_mins.value)

    days_back_start = dt.timedelta(days=start_days)
    #print('days_back_start ', days_back_start)
    hours_back_start = dt.timedelta(hours=start_hours)
    #print('hours_back_start ', hours_back_start)
    mins_back_start = dt.timedelta(minutes=start_mins)
    #print('mins_back_start ', mins_back_start)
    total_back_start = days_back_start + hours_back_start + mins_back_start
    total_ago_start = now - total_back_start
    total_ago_start_iso = total_ago_start.isoformat()
    total_ago_start_iso_str = str(total_ago_start_iso)

    days_back_end = dt.timedelta(days=end_days)
    hours_back_end = dt.timedelta(hours=end_hours)
    mins_back_end = dt.timedelta(minutes=end_mins)
    total_back_end = days_back_end + hours_back_end + mins_back_end
    total_ago_end = now - total_back_end
    total_ago_end_iso = total_ago_end.isoformat()
    total_ago_end_iso_str = str(total_ago_end_iso)

#RUN MONGODB QUERIES
    coll1 = dropdown_coll1.value
    print('coll1 ', coll1)
    if coll1 == "traffic_rate" or coll1 == "server_response_popper" or coll1 == "network_delay" or coll1 == "traffic_rate_dennett" or coll1 == "network_delay_viavidotcom":
        db1 = "wire"
        connect_db1 = connect[db1]
        connect_db_coll1 = connect_db1[coll1]
        print('connect_db_coll1 ', connect_db_coll1)
        cursor_connect_db_coll1 = connect_db_coll1.find({'data.results.results.data.intervalData.intervals': {'$gte': total_ago_start_iso_str, '$lt': total_ago_end_iso_str}}, {'data.results.results.data.intervalData.intervals': 1, '_id': 0})
        del time_str_list1[:]
        for dict1 in cursor_connect_db_coll1:
            list1 = dict1['data']['results']['results']
            dict2 = list1[0]
            time1 = dict2['data']['intervalData']['intervals']
            time_str1 = str(time1[0])
            time_str_list1.append(time_str1)

        cursor_connect_db_coll1 = connect_db_coll1.find({'data.results.results.data.intervalData.intervals': {'$gte': total_ago_start_iso_str, '$lt': total_ago_end_iso_str}},{'data.results.results.data.series.fieldData.data.float': 1, '_id': 0})
        del metric_list1[:]
        for dict1 in cursor_connect_db_coll1:
            list2 = dict1['data']['results']['results']
            dict3 = list2[0]
            list3 = dict3['data']['series']
            dict4 = list3[0]
            list4 = dict4['fieldData']
            dict3 = list2[0]
            list3 = dict3['data']['series']
            dict3 = list2[0]
            list3 = dict3['data']['series']
            dict4 = list3[0]
            list4 = dict4['fieldData']
            dict4 = list4[0]
            list5 = dict4['data']
            dict6 = list5[0]
            metric1 = dict6['float']
            metric_list1.append(metric1)

    elif coll1 == "dennett_cpu" or coll1 == "popper_cpu" or coll1 == "dennett_free_memory" or coll1 == "dennett_disk_used" or coll1 == "hyp1_cpu" or coll1 == "hyp1_free_memory" or coll1 == "hyp1_disk_used":
        print('coll1 ', coll1)
        db1 = "device"
        connect_db1 = connect[db1]
        print('connect_db1 ', connect_db1)
        connect_db_coll1 = connect_db1[coll1]
        print('connect_db_coll1 ', connect_db_coll1)
        cursor_connect_db_coll1 = connect_db_coll1.find({'Time': {'$gte': total_ago_start_iso_str, '$lt': total_ago_end_iso_str}})
        del time_str_list1[:]
        listy = list(cursor_connect_db_coll1)
        for n in range(len(listy)):
            item = (listy[n]['Time'])
            time_str_list1.append(item)

        cursor_connect_db_coll1 = connect_db_coll1.find({'Time': {'$gte': total_ago_start_iso_str, '$lt': total_ago_end_iso_str}})
        del metric_list1[:]
        listy = list(cursor_connect_db_coll1)
        for n in range(len(listy)):
            item = (listy[n]['Metric'])
            metric_list1.append(item)

    elif coll1 == "rochester_temp":
        print('coll1 ', coll1)
        db1 = "web"
        connect_db1 = connect[db1]
        print('connect_db1 ', connect_db1)
        connect_db_coll1 = connect_db1[coll1]
        print('connect_db_coll1 ', connect_db_coll1)
        cursor_connect_db_coll1 = connect_db_coll1.find({'Time': {'$gte': total_ago_start_iso_str, '$lt': total_ago_end_iso_str}})
        del time_str_list1[:]
        listy = list(cursor_connect_db_coll1)
        for n in range(len(listy)):
            item = (listy[n]['Time'])
            time_str_list1.append(item)

        cursor_connect_db_coll1 = connect_db_coll1.find({'Time': {'$gte': total_ago_start_iso_str, '$lt': total_ago_end_iso_str}})
        del metric_list1[:]
        listy = list(cursor_connect_db_coll1)
        for n in range(len(listy)):
            item = (listy[n]['Metric'])
            metric_list1.append(item)

    else:
        db1 = "curl"
        connect_db1 = connect[db1]
        connect_db_coll1 = connect_db1[coll1]
        print('connect_db_coll1 ', connect_db_coll1)
        cursor_connect_db_coll1 = connect_db_coll1.find({'Time': {'$gte': total_ago_start_iso_str, '$lt': total_ago_end_iso_str}})
        del time_str_list1[:]
        listy = list(cursor_connect_db_coll1)
        for n in range(len(listy)):
            item = (listy[n]['Time'])
            time_str_list1.append(item)

        cursor_connect_db_coll1 = connect_db_coll1.find({'Time': {'$gte': total_ago_start_iso_str, '$lt': total_ago_end_iso_str}})
        del metric_list1[:]
        listy = list(cursor_connect_db_coll1)
        for n in range(len(listy)):
            item = (listy[n]['Metric'])
            metric_list1.append(item)

    df1 = pd.DataFrame({'Time': time_str_list1})
    df1['Time'] = pd.to_datetime(df1['Time'])
    metric_series1 = pd.Series(metric_list1)
    df1['Metric'] = pd.Series(metric_series1, index=df1.index)
    #print('df1 ', df1)

    coll2 = dropdown_coll2.value
    if coll2 == "traffic_rate" or coll2 == "server_response_popper" or coll2 == "network_delay" or coll2 == "traffic_rate_dennett" or coll2 == "network_delay_viavidotcom":
        db2 = "wire"
        connect_db2 = connect[db2]
        connect_db_coll2 = connect_db2[coll2]
        print('connect_db_coll2 ', connect_db_coll2)
        cursor_connect_db_coll2 = connect_db_coll2.find({'data.results.results.data.intervalData.intervals': {'$gte': total_ago_start_iso_str, '$lt': total_ago_end_iso_str}}, {'data.results.results.data.intervalData.intervals': 1, '_id': 0})
        del time_str_list2[:]
        for dict1 in cursor_connect_db_coll2:
            list1 = dict1['data']['results']['results']
            dict2 = list1[0]
            time1 = dict2['data']['intervalData']['intervals']
            time_str2 = str(time1[0])
            time_str_list2.append(time_str2)

        cursor_connect_db_coll2 = connect_db_coll2.find({'data.results.results.data.intervalData.intervals': {'$gte': total_ago_start_iso_str, '$lt': total_ago_end_iso_str}}, {'data.results.results.data.series.fieldData.data.float': 1, '_id': 0})
        del metric_list2[:]
        for dict1 in cursor_connect_db_coll2:
            list2 = dict1['data']['results']['results']
            dict3 = list2[0]
            list3 = dict3['data']['series']
            dict4 = list3[0]
            list4 = dict4['fieldData']
            dict3 = list2[0]
            list3 = dict3['data']['series']
            dict3 = list2[0]
            list3 = dict3['data']['series']
            dict4 = list3[0]
            list4 = dict4['fieldData']
            dict4 = list4[0]
            list5 = dict4['data']
            dict6 = list5[0]
            metric2 = dict6['float']
            metric_list2.append(metric2)

    elif coll2 == "dennett_cpu" or coll2 == "popper_cpu" or coll2 == "dennett_free_memory" or coll2 == "dennett_disk_used" or coll2 == "hyp1_cpu" or coll2 == "hyp1_free_memory" or coll2 == "hyp1_disk_used":
        db2 = "device"
        connect_db2 = connect[db2]
        connect_db_coll2 = connect_db2[coll2]
        print('connect_db_coll2 ', connect_db_coll2)
        cursor_connect_db_coll2 = connect_db_coll2.find({'Time': {'$gte': total_ago_start_iso_str, '$lt': total_ago_end_iso_str}})
        del time_str_list2[:]
        listy = list(cursor_connect_db_coll2)
        for n in range(len(listy)):
            item = (listy[n]['Time'])
            time_str_list2.append(item)

        cursor_connect_db_coll2 = connect_db_coll2.find({'Time': {'$gte': total_ago_start_iso_str, '$lt': total_ago_end_iso_str}})
        del metric_list2[:]
        listy = list(cursor_connect_db_coll2)
        for n in range(len(listy)):
            item = (listy[n]['Metric'])
            metric_list2.append(item)

    elif coll2 == "rochester_temp":
        db2 = "web"
        connect_db2 = connect[db2]
        connect_db_coll2 = connect_db2[coll2]
        print('connect_db_coll2 ', connect_db_coll2)
        cursor_connect_db_coll2 = connect_db_coll2.find({'Time': {'$gte': total_ago_start_iso_str, '$lt': total_ago_end_iso_str}})
        del time_str_list2[:]
        listy = list(cursor_connect_db_coll2)
        for n in range(len(listy)):
            item = (listy[n]['Time'])
            time_str_list2.append(item)

        cursor_connect_db_coll2 = connect_db_coll2.find({'Time': {'$gte': total_ago_start_iso_str, '$lt': total_ago_end_iso_str}})
        del metric_list2[:]
        listy = list(cursor_connect_db_coll2)
        for n in range(len(listy)):
            item = (listy[n]['Metric'])
            metric_list2.append(item)

    else:
        db2 = "curl"
        connect_db2 = connect[db2]
        connect_db_coll2 = connect_db2[coll2]
        print('connect_db_coll2 ', connect_db_coll2)
        cursor_connect_db_coll2 = connect_db_coll2.find({'Time': {'$gte': total_ago_start_iso_str, '$lt': total_ago_end_iso_str}})
        del time_str_list2[:]
        listy = list(cursor_connect_db_coll2)
        for n in range(len(listy)):
            item = (listy[n]['Time'])
            time_str_list2.append(item)

        cursor_connect_db_coll2 = connect_db_coll2.find({'Time': {'$gte': total_ago_start_iso_str, '$lt': total_ago_end_iso_str}})
        del metric_list2[:]
        listy = list(cursor_connect_db_coll2)
        for n in range(len(listy)):
            item = (listy[n]['Metric'])
            metric_list2.append(item)

    df2 = pd.DataFrame({'Time': time_str_list2})
    df2['Time'] = pd.to_datetime(df2['Time'])

    metric_series2 = pd.Series(metric_list2)
    #print('apex_metric_series2 ', apex_metric_series2)
    df2['Metric'] = pd.Series(metric_series2, index=df2.index)
    #print('df2 ', df2)

#TEXT FOR METRIC TITLES INCLUDING UNITS
    if coll1 == 'traffic_rate':
        unit1 = 'bits_per_second'
    elif coll1 == 'traffic_rate_dennett':
        unit1 = 'bits per second'
    elif coll1 == 'network_delay':
        unit1 = 'milliseconds'
    elif coll1 == 'network_delay_viavidotcom':
        unit1 = 'milliseconds'
    elif coll1 == 'popper_cpu':
        unit1 = '%'
    elif coll1 == 'dennett_cpu':
        unit1 = '%'
    elif coll1 == 'server_response_popper':
        unit1 = 'milliseconds'
    elif coll1 == 'dennett_free_memory':
        unit1 = 'KB'
    elif coll1 == 'dennett_disk_used':
        unit1 = '%'
    elif coll1 == 'hyp1_cpu':
        unit1 = "%"
    elif coll1 == 'hyp1_free_memory':
        unit1 = 'KB'
    elif coll1 == 'hyp1_disk_used':
        unit1 = '%'
    elif db1 == 'curl':
        unit1 = 'milliseconds'
    elif coll1 == 'rochester_temp':
        unit1 = 'oC'
    else:
        unit1 = ''
    graph1_title = str(db1) + " " + str(coll1) + " " + str(unit1)
    #print('metric1_title ', metric1_title)

    if coll2 == 'traffic_rate':
        unit2 = 'bits_per_second'
    elif coll2 == 'traffic_rate_dennett':
        unit2 = 'bits per second'
    elif coll2 == 'network_delay':
        unit2 = 'milliseconds'
    elif coll2 == 'network_delay_viavidotcom':
        unit2 = 'milliseconds'
    elif coll2 == 'popper_cpu':
        unit2 = "%"
    elif coll2 == 'dennett_cpu':
        unit2 = "%"
    elif coll2 == 'server_response_popper':
        unit2 = 'milliseconds'
    elif coll2 == 'dennett_free_memory':
        unit2 = 'KB'
    elif coll2 == 'dennett_disk_used':
        unit2 = '%'
    elif coll2 == 'hyp1_cpu':
        unit2 = "%"
    elif coll2 == 'hyp1_free_memory':
        unit2 = 'KB'
    elif coll2 == 'hyp1_disk_used':
        unit2 = '%'
    elif coll2 == 'rochester_temp':
        unit2 = 'oC'
    elif db2 == 'curl':
        unit2 = 'milliseconds'
    else:
        unit2 = ''
    graph2_title = str(db2) + " " + str(coll2) + " " + str(unit2)

#DF TO DICT FOR GRAPHS
    graph1_dict = df1.to_dict('list')
    #print('graph1_dict ', graph1_dict)
    graph1_source.data = graph1_dict
    graph1.title.text = graph1_title
    graph1.add_tools(HoverTool(tooltips=[("Time", "@Time{%d-%m-%Y %H:%M}"), (graph1_title, "@Metric{0,000.000}")], formatters={'Time': 'datetime'}))

    graph2_dict = df2.to_dict('list')
    #print('graph1_dict ', graph1_dict)
    graph2_source.data = graph2_dict
    graph2.title.text = graph2_title
    graph2.add_tools(HoverTool(tooltips=[("Time", "@Time{%d-%m-%Y %H:%M}"), (graph2_title, "@Metric{0,000.000}")], formatters={'Time': 'datetime'}))

dropdown_coll1.on_change('value', refresh_graphs)
dropdown_coll2.on_change('value', refresh_graphs)

dropdown_days.on_change('value', refresh_graphs)
dropdown_hours.on_change('value', refresh_graphs)
dropdown_mins.on_change('value', refresh_graphs)

curdoc().add_root(layout([dropdown_days, dropdown_hours, dropdown_mins], dropdown_coll1, graph1, dropdown_coll2, graph2))
