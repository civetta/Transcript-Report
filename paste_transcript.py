from openpyxl import Workbook
from openpyxl.styles import Font, colors, Alignment
from openpyxl.utils.dataframe import dataframe_to_rows
from openpyxl.utils import get_column_letter


def paste_transcript(ws, trans_df, wb_boolean, lesson_name):
    column = ws.max_column+1
    if wb_boolean > 3:
        transcript_title = lesson_name + " -Whiteboard Used"
    else:
        transcript_title = lesson_name
    ws.cell(row=1, column=column, value=transcript_title).font=Font(bold=True)
    ws.column_dimensions[get_column_letter(column)].width = int(70)
    #for_line_in_transcript(trans_df, ws)



def for_line_in_transcript(trans_df, ws):
    for row, line in enumerate(transcript_list, 0):
        active_cell = ws.cell(row=row+2, column=num)
        if '--VOCAB FOUND' in line:
            line = line.replace('--VOCAB FOUND',"")
            active_cell.font = Font(color="69a1e5",bold=True)
        if ' ~APPROPRIATE PHRASE' in line:
            line = line.replace('~APPROPRIATE PHRASE', "")
            active_cell.font = Font(color="cc79d1",bold=True)
        active_cell.alignment =  active_cell.alignment.copy(wrapText=True)
        active_cell.value = line