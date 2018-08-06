from openpyxl import Workbook
from openpyxl.styles import Font, colors, Alignment
from openpyxl.utils.dataframe import dataframe_to_rows
from openpyxl.utils import get_column_letter
from openpyxl.styles import Alignment
import pandas as pd
import numpy as np
from openpyxl.chart import BarChart, Series, Reference

def paste_summary(row, summary_ws):
    ws_row = summary_ws.max_row
    Summary_row = {}


def paste_kpi(teacher_rt, teacher_frt, team_rt, team_frt, rt_ws):
    kpi_dict = {'Statistics':['Median',"Max","Min","Average"],
    'Teacher FRT':[np.median(teacher_frt),teacher_frt.max(),teacher_frt.min(), teacher_frt.mean()],
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
                value=value/1e9
            except TypeError:
                value=value
            rt_ws.cell(row=r_idx, column=c_idx, value=value)
    create_box_chart(rt_ws)


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

#FIGURE OUT ERROR FOR RESPONSE TIME PASTING
def paste_response(row, rt_ws):
    student_handle = row.student_handle
    trans_df = row.transcript_info

    trans_df = pd.DataFrame(trans_df)
    if rt_ws.cell(row=1, column=7).value is None:
        column = 7
    else:
        column = rt_ws.max_column+1
    title = 'Transcript '+(get_column_letter((column-4)/2))
    rt_ws.cell(row=1, column=column).value = title
    rt_ws.cell(row=1, column=column).font = Font(bold=True)
    
    rt_ws.column_dimensions[get_column_letter(column)].width = int(35)
    rt_ws.column_dimensions[get_column_letter(column+1)].width = int(20)
    for_line_in_rt_ws(rt_ws, trans_df, column, student_handle)


def for_line_in_rt_ws(rt_ws, trans_df, column, student_handle):
    FRT = 'Not Found'
    Student_First_Response = "Not Found"

    for row, line in enumerate(trans_df.rt_paste, 0):
        active_cell = rt_ws.cell(row=row+2, column=column+1)
        timestamp_cell = rt_ws.cell(row=row+2, column=column)
        time = line
        if "-TR" in str(time):
            time = time[6:-3]
            if FRT == 'Not Found':
                active_cell.font = Font(color=colors.BLUE,bold=True)
                timestamp_cell.font = Font(color=colors.BLUE,bold=True)
                FRT = 'Found'
            else:
                active_cell.font = Font(bold=True)
                timestamp_cell.font = Font(bold=True)
            active_cell.value = time
        else:
            if Student_First_Response == "Not Found" and student_handle.strip()==trans_df.Handle.loc[row]:
                active_cell.font = Font(color='00A563',bold=True)
                timestamp_cell.font = Font(color='00A563',bold=True)
                Student_First_Response = "Found"
            time = trans_df.rt.loc[row]
            #By making it a string, excel will automatically align it to the left of cell
            active_cell.value = (str(time)[6:])
        stamp = "  "+trans_df.Handle.loc[row]+" "+str(trans_df.Time_Stamps.loc[row])
        timestamp_cell.value = stamp
        
        
        

def paste_transcript(row, ws):
    wb_boolean = row.wb_boolean
    lesson_name = row.lesson_name
    trans_df = row.transcript_info
    trans_df = pd.DataFrame(trans_df)
    if ws.cell(row=1, column=1).value is None:
        column = 1
    else:
        column = ws.max_column+1
    if wb_boolean > 3:
        transcript_title = lesson_name + " -Whiteboard Used"
    else:
        transcript_title = lesson_name
    ws.cell(row=1, column=column, value=transcript_title).font=Font(bold=True)
    ws.column_dimensions[get_column_letter(column)].width = int(70)
    for_line_in_transcript(trans_df, ws, column)



def for_line_in_transcript(trans_df, ws, column):
    for row, line in enumerate(trans_df.marked_lines, 0):
        active_cell = ws.cell(row=row+2, column=column)
        if '-- VOCAB FOUND' in line:
            line = line.replace('-- VOCAB FOUND',"")
            active_cell.font = Font(color="69a1e5",bold=True)
        if '--APPROP FOUND' in line:
            line = line.replace('--APPROP FOUND', "")
            active_cell.font = Font(color="cc79d1",bold=True)
        active_cell.alignment =  active_cell.alignment.copy(wrapText=True)
        active_cell.value = line