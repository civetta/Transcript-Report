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
    session_length_secs = (trans_df.Time_Stamps.iloc[-1] - trans_df.Time_Stamps.iloc[0]).seconds
    student_response = trans_df[trans_df.Student_Bool].Line_Char_Length.mean()
    teacher_response = trans_df[~trans_df.Student_Bool].Line_Char_Length.mean()
    return trans_df.to_dict(), frt, art, vocab, session_length_secs, student_response, teacher_response


"""Input Variables"""
num_transcripts = 50
desired_num_interactions = 3
os.system('attrib +H *.pyc /S') #Hides .pyc file in direcory
df = pd.read_csv('data_source/RawPeriscope.csv')
date = pd.read_csv('data_source/date2.csv')


"""Calling Functions"""
df = filtered_transcripts(df, num_transcripts, desired_num_interactions)
"""Creating a DF for each teacher and then going through each row to create
an individual Transcript DF."""
df['transcript_info'], df['frt'], df['art'], df['vocab'], df['session_length_secs'], df['avg_teacher_response_length'], df['avg_student_response_length'] = zip(*df.apply(find_transcript_data, axis=1))
summary = Workbook()
teacher_real_names = df.name
unique_teacher_names = list(set(teacher_real_names))
    for teachername in unique_teacher_names:
        teacher_df = df[(df.name == teachername)]
        
#Paste Everything and be done with the initial part of project






