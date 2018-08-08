from openpyxl import Workbook
from openpyxl.styles import Font, colors, Alignment, PatternFill
from openpyxl.utils.dataframe import dataframe_to_rows
from openpyxl.utils import get_column_letter
import pandas as pd


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
    if wb_boolean is True:
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
        if '--MARK GREEN' in line:
            line = line.replace('--MARK GREEN', "")
            active_cell.font =  Font(color='00A563',bold=True)
        if "--GREY OUT" in line:
            line = line.replace('--GREY OUT', "")
            grayFill = PatternFill("solid", fgColor="efefef")
            active_cell.fill = grayFill
        active_cell.alignment =  active_cell.alignment.copy(wrapText=True) 
        active_cell.value = line
         
        