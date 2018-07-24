import pandas as pd
from openpyxl import Workbook
from transcript_filter import filtered_transcripts
from creat_transcript_df import create_transcript_df
import os


"""Input Variables"""
num_transcripts = 50
desired_num_interactions = 5
os.system('attrib +H *.pyc /S') #Hides .pyc file in direcory
df = pd.read_csv('data_source/RawPeriscope.csv')
date = pd.read_csv('data_source/date2.csv')


"""Calling Functions"""
df = filtered_transcripts(df, num_transcripts, desired_num_interactions)
teacher_real_names = df.name
unique_teacher_names = list(set(teacher_real_names))
"""Creating a DF for each teacher and then going through each row to create
an individual Transcript DF."""
for teachername in unique_teacher_names:
    teacher_df = df[(df.name == teachername)]
    teacher_df = teacher_df.reset_index(drop=True)
    wb = Workbook()
    rt_ws = wb.create_sheet("Response Time", 0)
    ws = wb.create_sheet("Transcripts", 0)
    blank_sheet = wb.get_sheet_by_name('Sheet')
    wb.remove_sheet(blank_sheet)
    for index, row in teacher_df.iterrows():
        create_transcript_df(row, teacher_df, teachername, wb, ws, rt_ws)
