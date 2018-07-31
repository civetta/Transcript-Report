import pandas as pd
from openpyxl import Workbook
import numpy
from transcript_filter import filtered_transcripts
from creat_transcript_df import create_transcript_df
import os


def find_transcript_data(row):
    teach_handle = row['teacher_handle'].strip()
    stud_handle = row['student_handle'].strip()
    transcript = row['transcript'].strip()
    trans_df = create_transcript_df(row, teach_handle, stud_handle, transcript)
    frt_loc = trans_df.Teacher_Response.first_valid_index()
    frt = trans_df.Teacher_Response[frt_loc]
    art = trans_df.Teacher_Response.mean()
    vocab = trans_df.vocab_count.sum()
    #Find Rest of Data Needed in Lead Summary
    return trans_df.to_dict(), frt, art, vocab


"""Input Variables"""
num_transcripts = 2
desired_num_interactions = 3
os.system('attrib +H *.pyc /S') #Hides .pyc file in direcory
df = pd.read_csv('data_source/RawPeriscope.csv')
date = pd.read_csv('data_source/date2.csv')


"""Calling Functions"""
df = filtered_transcripts(df, num_transcripts, desired_num_interactions)
teacher_real_names = df.name
unique_teacher_names = list(set(teacher_real_names))
"""Creating a DF for each teacher and then going through each row to create
an individual Transcript DF."""
df['transcript_info'], df['frt'], df['art'], df['vocab'] = zip(*df.apply(find_transcript_data, axis=1))
df = df.apply(find_transcript_data, axis=1)





"""team_data = {}
for teachername in unique_teacher_names:
    teacher_df = df[(df.name == teachername)]
    teacher_df = teacher_df.reset_index(drop=True)
    wb = Workbook()
    rt_ws = wb.create_sheet("Response Time", 0)
    ws = wb.create_sheet("Transcripts", 0)
    for index, row in teacher_df.iterrows():
        trans_df = create_transcript_df(row, teacher_df, teachername, wb, ws, rt_ws)
        frt_loc = trans_df.Teacher_Response.first_valid_index()
        frt = trans_df.Teacher_Response[frt_loc]"""




