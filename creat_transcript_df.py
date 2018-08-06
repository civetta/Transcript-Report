import pandas as pd
import re
from marked_lines import create_marked_lines
from datetime import datetime
import numpy as np


def create_transcript_df(row, teach_handle, stud_handle, transcript):
    def handle_bool(x):
        if x == stud_handle:
            return True
        if x == teach_handle:
            return False 
    transcript = transcript[transcript.index(teach_handle):]
    trans_df = pd.DataFrame({'Transcript': transcript.split('\n')})        
    trans_df['Handle'] = trans_df['Transcript'].map(lambda x: x[:x.index('@')].strip())
    trans_df['Student_Bool'] = trans_df.Handle.map(handle_bool)
    trans_df['Time_Stamps'] = trans_df.Transcript.map(create_timestamp)
    trans_df['Line_Char_Length'] = trans_df.Transcript.map(lambda x: len(x))
    trans_df['rt'] = trans_df.Time_Stamps.diff().fillna(0)
    trans_df = teacher_response(trans_df)
    trans_df['rt_paste'] = trans_df["Teacher_Response"].map(lambda x: str(x)+'-TR' if pd.isnull(x) is False else x)
    trans_df['rt_paste'] = trans_df.rt_paste.combine_first(trans_df.rt)
    trans_df = create_marked_lines(trans_df)
    return trans_df


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
    trans_df["Teacher_Response"] = rt_times
    return trans_df