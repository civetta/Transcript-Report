import pandas as pd
import re
from marked_lines import create_marked_lines
from datetime import datetime
import numpy as np

"""Takes each transcripts and makes a dataframe out of each of them called
 trans_df (transcript dataframe). With this it figures out the RT (response time)
 It also figures out the response time between each line,
teacher response time to a student specifically, and 
 creates an rt_paste which is a hybrid of those together and is pasted in the 
 transcript-report so teachers can see Their Response times to a student as 
 well as other response times. """



def create_transcript_df(row, teach_handle, stud_handle, transcript):
    """Creates several new columns for each transcript. They are then zipped up
    and sent back up and used for overall transcript analysis. For example 
    using the Student_Bool (true or false student) and the Line_Char_Length
    column, we can figure out the average character length a student 
    sends vs average character length a teacher sends"""
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
    trans_df.to_csv('Trans_df.csv')
    return trans_df


def create_timestamp(line):
    """Makes timestamps easier to read"""
    time = line[:line.index('Z]:')+1]
    match = re.match(r"(.*)\[(\d{4}-\d{2}-\d{2})T(\d{2}:\d{2}:\d{2})", time)
    time_stamp = match.group(2)+" "+match.group(3)
    time_stamp = datetime.strptime(time_stamp, "%Y-%m-%d %H:%M:%S")
    return time_stamp


def teacher_response(trans_df):
    """Figures out the teachers respones time to a student. Teacher response
    time is defined as the length of time it takes for a teacher to response
    to the students first message."""
    rt_times = []
    student_bool = trans_df['Student_Bool']
    timestamps = trans_df['Time_Stamps']
    student_idx = None
    for idx, user_type in enumerate(student_bool):
        if user_type is True and student_idx is None:
            student_idx = idx
        if user_type is False and student_idx is not None:
            delta = (timestamps[idx] - timestamps[student_idx]).total_seconds()
            rt_times.append(delta)
            student_idx = None
        else:
            rt_times.append(None) 
    trans_df["Teacher_Response"] = rt_times
    return trans_df