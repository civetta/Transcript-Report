import pandas as pd
from openpyxl import Workbook
import numpy as np
from transcript_filter import filtered_transcripts
from creat_transcript_df import create_transcript_df
from paste_transcript import paste_transcript
from paste_transcript import paste_response
from paste_kpi import paste_kpi
from dash_data import get_data
import os


def find_transcript_data(row):
    teach_handle = row['teacher_handle'].strip()
    stud_handle = row['student_handle'].strip()
    transcript = row['transcript'].strip()
    trans_df = create_transcript_df(row, teach_handle, stud_handle, transcript)
    frt_loc = trans_df.Teacher_Response.first_valid_index()
    frt = trans_df.Teacher_Response[frt_loc]
    art = trans_df.dropna(subset=['Teacher_Response']).Teacher_Response.values.astype('timedelta64[s]')
    vocab = trans_df.vocab_count.sum()
    session_length_secs = (trans_df.Time_Stamps.iloc[-1] - trans_df.Time_Stamps.iloc[0]).seconds
    student_response = trans_df[trans_df.Student_Bool].Line_Char_Length.mean()
    teacher_response = trans_df[~trans_df.Student_Bool].Line_Char_Length.mean()
    return trans_df.to_dict(), frt, art, vocab, session_length_secs, student_response, teacher_response



"""Input Variables"""
num_transcripts = 50
desired_num_interactions = 3
os.system('attrib +H *.pyc /S') #Hides .pyc file in directory
df = pd.read_csv('data_source/caren.csv')
date = pd.read_csv('data_source/date2.csv')


"""Calling Functions"""
ytd = get_data()
ytd = pd.DataFrame(ytd['ytdTeacher'])
df = filtered_transcripts(df, num_transcripts, desired_num_interactions)
"""Creating a DF for each teacher and then going through each row to create
an individual Transcript DF."""
df['transcript_info'], df['frt'], df['art'], df['vocab'], df['session_length_secs'], df['avg_teacher_response_length'], df['avg_student_response_length'] = zip(*df.apply(find_transcript_data, axis=1))
summary = {
    'Teacher Name': [],'FRT Median': [],'ART Median': [],
    'Avg Teacher Response Length': [], 'Avg Student Response Length': [],
    'Avg Numer of Interactions': [], 'Teacher to Student Ration': [],
    'Avg Session Length(seconds)': [], 'Avg Session Length(minutes)': []
    }
teacher_real_names = df.name
unique_teacher_names = list(set(teacher_real_names))
#Creates a nparray of all of the teachers response times.
team_rt = np.asarray([item for sublist in df.art.values for item in sublist])
team_frt = np.asarray(df.frt.values.astype('timedelta64[s]'))
for teachername in unique_teacher_names:
    row_in_ytd = ytd.loc[ytd['teacherName'] == teachername]
    teacherbook = Workbook()
    ws = teacherbook.create_sheet('Transcripts')
    rt_ws = teacherbook.create_sheet('ART-FRT')
    teacherbook.remove_sheet(teacherbook.get_sheet_by_name('Sheet'))
    teacher_df = df[(df.name == teachername)]
    teacher_rt = np.asarray([item for sublist in teacher_df.art.values for item in sublist])
    teacher_frt = np.asarray(teacher_df.frt.values.astype('timedelta64[s]'))

    paste_kpi(teacher_rt, teacher_frt, team_rt, team_frt, rt_ws, row_in_ytd)
    teacher_df.apply(paste_transcript, args=(ws, ), axis=1)
    teacher_df.apply(paste_response, args=(rt_ws, ), axis=1)
    
    teacherbook.save('teacher_sheets/'+teachername+'.xlsx')





