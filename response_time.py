import pandas as pd
import re
import numpy as np
from datetime import datetime, timedelta, time


def time_stamps(i):
    transcript = i.split('\n')
    teacher_transcript = []
    start = False
    for line in transcript:
        if '@' in line:
            line = line[:line.index('Z]:')+1]
            match = re.match(r"(.*)\[(\d{4}-\d{2}-\d{2})T(\d{2}:\d{2}:\d{2})", line)
            time_stamp = match.group(1)+" "+match.group(2)+" "+match.group(3)
            teacher_transcript.append(time_stamp)
            if start is False:
                start_date = match.group(2)
                start_time = match.group(3)
                start = True
        else:
            continue
    start_id = round_to_nearest_whole_minutes(start_time, start_date)
    start_id = start_id.strip()
    return teacher_transcript, start_id, match.group(2)+" "+match.group(3)[:-3]


def round_to_nearest_whole_minutes(start_time, start_date):
    minutes = int(start_time[-5:-3])
    hour = int(start_time[0:2])
    tm = time(hour, minutes, 0)
    tm = tm.strftime("%H:%M:%S")
    start_date = start_date.strip()
    return start_date+" "+tm


def find_difference(old_stamp, new_stamp):
    old_stamp = old_stamp[old_stamp.index('@')+2:]
    new_stamp = new_stamp[new_stamp.index('@')+2:]
    new = datetime.strptime(old_stamp, " %Y-%m-%d %H:%M:%S")
    old = datetime.strptime(new_stamp, " %Y-%m-%d %H:%M:%S") 
    delta = old-new
    return timedelta.total_seconds(delta)


def session_length(i):
    lister = list(i)
    delta = find_difference(lister[0],lister[-1])
    return delta   


def find_rt(i):
    time_stamp = list(i.time_stamps)
    student_found = False
    student_line = None
    teacher_line = None
    student_handle = i.student_handle
    teacher_handle = i.teacher_handle
    art_list = []
    marked_timestamps = []
    old_line = None
    if student_handle is not None:
        for line in time_stamp:
            marked_stamp = line
            if student_found is False:
                if student_handle in line:
                    student_found = True
                    student_line = line
            if student_found is True:
                if teacher_handle in line:
                    teacher_line = line
                    marked_stamp = marked_stamp + '--TR'
            if teacher_line is not None and student_line is not None:
                delta = find_difference(student_line, teacher_line)
                marked_stamp = marked_stamp+"--"+str(delta)
                art_list.append(delta)
                student_found = False
                student_line = None
                teacher_line = None
            if old_line is not None:
                delta = find_difference(old_line, line)
                marked_stamp = marked_stamp+"--"+str(delta)
            if old_line is None:
                marked_stamp = marked_stamp +"--0"
            old_line = line
            marked_timestamps.append(marked_stamp)
    if len(art_list)>0:
        return art_list, art_list[0], np.mean(art_list),marked_timestamps
    else:
        return art_list, None, None, None


def date_time(i):
    time = str(i['time'])
    time = datetime.strptime(time, "%I:%M:%S %p").strftime("%H:%M:%S")
    date = str(i['date'])
    date = datetime.strptime(date, "%m/%d/%Y").strftime("%Y-%m-%d")
    return date + " "+time




    

def response_times(df):
    df['time_stamps'], df['start_id'], df['end_date_time'] =  zip(*df['transcript'].map(time_stamps))
    df['session_length'] = df['time_stamps'].apply(session_length)
    df['rt_list'], df['frt'], df['art'], df['marked_timestamps'] = zip(*df.apply(find_rt, axis=1))
    return df