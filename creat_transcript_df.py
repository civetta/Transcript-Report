from openpyxl import Workbook
import pandas as pd
import re
from marked_lines import create_marked_lines
from paste_transcript import paste_transcript
from datetime import datetime, timedelta, time


def create_transcript_df(row, df, teachername, wb, ws, rt_ws):
    teach_handle = row['teacher_handle'].strip()
    stud_handle = row['student_handle'].strip()
    lesson_name = row['lesson_name'].strip()
    wb_count = row['wb_message_count']
    
    def handle_bool(x):
        if x == stud_handle:
            return True
        if x == teach_handle:
            return False 

    transcript = row['transcript'].split('\n')
    trans_df = pd.DataFrame({'Transcript': transcript})        
    trans_df['Handle'] = trans_df['Transcript'].map(lambda x: x[:x.index('@')].strip())
    trans_df['Student_Bool'] = trans_df.Handle.map(handle_bool)
    trans_df['Time_Stamps'] = trans_df.Transcript.map(create_timestamp)
    trans_df['Line_Char_Length'] = trans_df.Transcript.map(lambda x: len(x))
    trans_df['rt'] = trans_df.Time_Stamps.diff().dt.total_seconds().fillna(0)
    #trans_df = teacher_response(trans_df)
    #trans_df = create_marked_lines(trans_df)
    #paste_transcript(ws, trans_df, wb_count, lesson_name)
    #wb.save('teacher_sheets/'+teachername+'.xlsx')"""


def create_timestamp(line):
    time = line[:line.index('Z]:')+1]
    match = re.match(r"(.*)\[(\d{4}-\d{2}-\d{2})T(\d{2}:\d{2}:\d{2})", time)
    time_stamp = match.group(2)+" "+match.group(3)
    time_stamp = datetime.strptime(time_stamp, "%Y-%m-%d %H:%M:%S")
    return time_stamp


def teacher_response(trans_df):
    rt_times = []
    student_bool = trans_df['Student_Bool']
    timestamps = trans_df['Time_Stamps']
    student_idx = None
    for idx, user_type in enumerate(student_bool):
        if user_type is True and student_idx is None:
            student_idx = idx
        if user_type is False and student_idx is not None:
            rt_times.append(timestamps[idx] - timestamps[student_idx])
            student_idx = None
        else:
            rt_times.append(None)
    {'Teacher_Response': rt_times}        
    return trans_df
