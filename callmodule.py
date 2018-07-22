import pandas as pd
from transcript_filter import filtered_transcripts
from create_transcript_df import create_transcript_df
import os

num_transcripts = 50
desired_num_interactions = 3
os.system('attrib +H *.pyc /S') #Hides .pyc file in direcory
df = pd.read_csv('data_source/RawPeriscope.csv')
date = pd.read_csv('data_source/date2.csv')
df = filtered_transcripts(df, num_transcripts, desired_num_interactions)
teacher_real_names = df.name
unique_teacher_names = list(set(teacher_real_names))
for teachername in unique_teacher_names:
    teacher_df = df[(df.name == teachername)]
    teacher_df = teacher_df.reset_index(drop=True)
    for index, row in teacher_df.iterrows():
        create_transcript_df(row, teacher_df, trans_ws, rt_ws, teacherbook, teachername)