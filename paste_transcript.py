from openpyxl import Workbook
from openpyxl.styles import Font, colors, Alignment
from openpyxl.utils.dataframe import dataframe_to_rows
from openpyxl.utils import get_column_letter
#from openpyxl.worksheet.write_only import WriteOnlyCell


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