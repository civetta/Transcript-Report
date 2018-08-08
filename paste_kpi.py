from openpyxl.utils.dataframe import dataframe_to_rows
from openpyxl.utils import get_column_letter
import pandas as pd
import numpy as np
from openpyxl.chart import BarChart, Series, Reference



def paste_kpi(teacher_rt, teacher_frt, team_rt, team_frt, rt_ws, row_in_ytd):
    kpi_dict = {'Statistics':['Median',"Max","Min","Average"],
    'Teacher FRT':[np.median(teacher_frt), teacher_frt.max(),teacher_frt.min(), teacher_frt.mean()],
    'Team FRT':[np.median(team_frt),team_frt.max(),team_frt.min(), team_frt.mean()],
    'Teacher ART':[np.median(teacher_rt),teacher_rt.max(),teacher_rt.min(), teacher_rt.mean()],
    'Team ART':[np.median(team_rt),team_rt.max(),team_rt.min(), team_rt.mean()]}
    kpi_table = pd.DataFrame(kpi_dict)
    kpi_table = kpi_table[['Statistics', 'Teacher FRT', 'Team FRT','Teacher ART', 'Team ART']]
    rows = dataframe_to_rows(kpi_table, index=False)
    for r_idx, row in enumerate(rows, 1):
        for c_idx, value in enumerate(row, 1):
            rt_ws.column_dimensions[get_column_letter(c_idx)].width = int(30)
            try:
                #Converting nanoseconds into regular seconds.
                value = value/1e9
            except TypeError:
                value = value
            rt_ws.cell(row=r_idx, column=c_idx, value=value)
    create_box_chart(rt_ws)
    rt_ws.cell(row=6, column=1, value="YTD Session Taught")
    rt_ws.cell(row=6, column=2, value=int(row_in_ytd['sessionCount']))
    rt_ws.cell(row=7, column=1, value="YTD Avg Session Length (minutes)")
    rt_ws.cell(row=7, column=2, value=round(float((row_in_ytd['averageSessionTime'])/60), 2))

def create_box_chart(rt_ws):
    chart1 = BarChart()
    chart1.type = "col"
    chart1.style = 10
    chart1.title = "FRT Comparison"
    chart1.y_axis.title = 'Seconds'
    chart1.width = 10

    data = Reference(rt_ws, min_col=2, min_row=1, max_row=5, max_col=3)
    cats = Reference(rt_ws, min_col=1, min_row=2, max_row=5)
    chart1.add_data(data, titles_from_data=True)
    chart1.set_categories(cats)
    chart1.shape = 4
    rt_ws.add_chart(chart1, "A10")

    chart2 = BarChart()
    chart2.type = "col"
    chart2.style = 10
    chart2.title = "ART Comparison"
    chart2.y_axis.title = 'Seconds'
    chart2.width = 10

    data = Reference(rt_ws, min_col=4, min_row=1, max_row=5, max_col=5)
    cats = Reference(rt_ws, min_col=1, min_row=2, max_row=5)
    chart2.add_data(data, titles_from_data=True)
    chart2.set_categories(cats)
    chart2.shape = 4
    rt_ws.add_chart(chart2, "C10")