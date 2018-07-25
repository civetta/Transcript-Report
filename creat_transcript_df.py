from openpyxl import Workbook
import pandas as pd
import re
from marked_lines import create_marked_lines
from paste_transcript import paste_transcript
from datetime import datetime, timedelta, time


def create_transcript_df(row, teacher_df, teachername, wb, ws, rt_ws):

   
    teach_handle = row['teacher_handle']
    stud_handle = row['student_handle']
    lesson_name = row['lesson_name']
    wb_count = row['wb_message_count']
    transcript = row['transcript'].split('\n')
    trans_df = create_trandsdf(transcript, teach_handle, stud_handle)
    #trans_df = create_marked_lines(trans_df)
    #paste_transcript(ws, trans_df, wb_count, lesson_name)
    #wb.save('teacher_sheets/'+teachername+'.xlsx')


def create_trandsdf(transcript, teach_handle, stud_handle):
    """Creates the Transcript Dataframe, and finds the timestamp."""
    trans_df = {
        'Transcript':[], 
        'Time_Stamps':[],
        'Handle':[],
        'Student_Bool':[],
        'Line_Char_Length':[],
        'Response_Times':[]}
    for line in transcript:
        trans_df = fill_in_transdf(trans_df, line, teach_handle, stud_handle)
    trans_df = teacher_response(trans_df)
    trans_df = pd.DataFrame(trans_df)   
    trans_df = trans_df.reset_index(drop=True)
    trans_df['rt']=trans_df.Time_Stamps.diff().dt.total_seconds().fillna(0)
    return trans_df


def teacher_response(trans_df):
    student_bool = trans_df['Student_Bool']
    timestamps = trans_df['Time_Stamps']
    student_idx = None
    for idx, user_type in enumerate(student_bool):
        if user_type is True and student_idx is None:
            student_idx = idx
        if user_type is False and student_idx is not None:
            trans_df['Response_Times'].append(timestamps[idx] - timestamps[student_idx])
            student_idx = None
        else:
            trans_df['Response_Times'].append(None)
    return trans_df


def fill_in_transdf(trans_df, line, teach_handle, stud_handle):
    """Uses Logic to fill in the transcript dataframe"""
    time_stamp = create_timestamp(line)
    handle = create_handle(line)
    trans_df['Handle'].append(handle)
    trans_df['Transcript'].append(line)
    trans_df['Time_Stamps'].append(time_stamp)
    trans_df['Line_Char_Length'].append(len(line))
    if teach_handle.strip() in handle:
        trans_df['Student_Bool'].append(False)
    elif stud_handle.strip() in handle:
        trans_df['Student_Bool'].append(True)
    else:
        trans_df['Student_Bool'].append(None)
    return trans_df

def create_timestamp(line):
    """Creates a cleaned up timestamp"""
    time = line[:line.index('Z]:')+1]
    match = re.match(r"(.*)\[(\d{4}-\d{2}-\d{2})T(\d{2}:\d{2}:\d{2})", time)
    time_stamp = match.group(2)+" "+match.group(3)
    time_stamp = datetime.strptime(time_stamp, "%Y-%m-%d %H:%M:%S")
    return time_stamp

def create_handle(line):
    """Returns only the handle"""
    handle = line[:line.index('@')].strip()
    return handle