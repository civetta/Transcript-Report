from openpyxl import Workbook
from openpyxl.styles import Font, colors, Alignment
from openpyxl.utils.dataframe import dataframe_to_rows
from openpyxl.utils import get_column_letter
from openpyxl.styles import Alignment
#from openpyxl.worksheet.write_only import WriteOnlyCell


def paste_response(rt_ws, trans_df):
    if rt_ws.cell(row=1, column=6).value is None:
        column = 6
    else:
        column = rt_ws.max_column+1
    title = 'Transcript '+(get_column_letter((column-4)/2))
    rt_ws.cell(row=1, column=column).value = title
    rt_ws.cell(row=1, column=column).font = Font(bold=True)
    FRT = 'Not Found'
    rt_ws.column_dimensions[get_column_letter(column)].width = int(35)
    rt_ws.column_dimensions[get_column_letter(column+1)].width = int(20)
    
    for row, line in enumerate(trans_df.Teacher_Response, 0):
        active_cell = rt_ws.cell(row=row+2, column=column+1)
        timestamp_cell = rt_ws.cell(row=row+2, column=column)
        time = line
        if line != 'None':
            if FRT == 'Not Found':
                active_cell.font = Font(color=colors.BLUE,bold=True)
                timestamp_cell.font = Font(color=colors.BLUE,bold=True)
                FRT = 'Found'
            else:
                active_cell.font = Font(bold=True)
                timestamp_cell.font = Font(bold=True)
        else:
            time = trans_df.rt.loc[row]
        stamp = "  "+trans_df.Handle.loc[row]+" "+str(trans_df.Time_Stamps.loc[row])
        timestamp_cell.value = stamp
        active_cell.value = time
        
            


def paste_transcript(ws, trans_df, wb_boolean, lesson_name):
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
    for row, line in enumerate(trans_df.marked_line, 0):
        active_cell = ws.cell(row=row+2, column=column)
        if '-- VOCAB FOUND' in line:
            line = line.replace('-- VOCAB FOUND',"")
            active_cell.font = Font(color="69a1e5",bold=True)
        if '--APPROP FOUND' in line:
            line = line.replace('--APPROP FOUND', "")
            active_cell.font = Font(color="cc79d1",bold=True)
        active_cell.alignment =  active_cell.alignment.copy(wrapText=True)
        active_cell.value = line