from openpyxl import Workbook
import pandas as pd
import re
from marked_lines import create_marked_lines
from paste_transcript import paste_transcript


def create_transcript_df(row, teacher_df, trans_ws, rt_ws, teacherbook, teachername):
    teacherbook = Workbook()
        rt_ws = teacherbook.create_sheet("Response Time", 0)
        trans_ws = teacherbook.create_sheet("Transcripts", 0)
        blank_sheet = teacherbook.get_sheet_by_name('Sheet')
        teacherbook.remove_sheet(blank_sheet)
    teach_handle = row['teacher_handle']
    stud_handle = row['student_handle']
    lesson_name = row['lesson_name']
    wb_count = row['wb_message_count']
    transcript = row['transcript'].split('\n')
    trans_df = create_trandsdf(transcript, teach_handle, stud_handle)
    trans_df = create_marked_lines(trans_df)
    paste_transcript(trans_ws, trans_df, wb_count, lesson_name)
    trans_df.to_csv('Testing.csv')
    teacherbook.save('teacher_sheets/'+teachername+'.xlsx')


def create_trandsdf(transcript, teach_handle, stud_handle):
    """Creates the Transcript Dataframe, and finds the timestamp."""
    trans_df = {
        'Transcript':[], 
        'Time_Stamps':[],
        'Handle':[],
        'Teacher_Bool':[],
        'Student_Bool':[],
        'Line_Char_Length':[]}
    for line in transcript:
        trans_df = fill_in_transdf(trans_df, line, teach_handle, stud_handle)
    trans_df = pd.DataFrame(trans_df)   
    trans_df = trans_df.reset_index(drop=True)
    return trans_df


def fill_in_transdf(trans_df, line, teach_handle, stud_handle):
    """Uses Logic to fill in the transcript dataframe"""
    time_stamp = create_timestamp(line)
    handle = create_handle(line)
    trans_df['Handle'].append(handle)
    trans_df['Transcript'].append(line)
    trans_df['Time_Stamps'].append(time_stamp)
    trans_df['Line_Char_Length'].append(len(line))
    if teach_handle in handle:
        trans_df['Teacher_Bool'].append(True)
        trans_df['Student_Bool'].append(False)
    elif stud_handle in handle:
        trans_df['Teacher_Bool'].append(False)
        trans_df['Student_Bool'].append(True)
    else:
        trans_df['Teacher_Bool'].append(False)
        trans_df['Student_Bool'].append(False)
    return trans_df

def create_timestamp(line):
    """Creates a cleaned up timestamp"""
    time = line[:line.index('Z]:')+1]
    match = re.match(r"(.*)\[(\d{4}-\d{2}-\d{2})T(\d{2}:\d{2}:\d{2})", time)
    time_stamp = match.group(2)+" "+match.group(3)
    return time_stamp

def create_handle(line):
    """Returns only the handle"""
    handle = line[:line.index('@')].strip()
    return handle