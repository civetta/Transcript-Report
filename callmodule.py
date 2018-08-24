import pandas as pd
from openpyxl import Workbook
import numpy as np
from transcript_filter import filtered_transcripts
from dash_data import get_data
from create_teacher_df import teacher_df, find_transcript_data
import os

def call_func(num_transcripts, df, desired_num_interactions):
    ytd = get_data()
    ytd = pd.DataFrame(ytd['ytdTeacher'])
    df = filtered_transcripts(df, num_transcripts, desired_num_interactions)
    df.to_csv('After_Filter.csv')
    """Creating a DF for each teacher and then going through each row to create
    an individual Transcript DF."""
    df['transcript_info'], df['frt'], df['art'], df['vocab'], df['session_length_secs'], df['avg_teacher_response_length'], df['avg_student_response_length'] = zip(*df.apply(find_transcript_data, axis=1))
    df.to_csv('After_Transcript_df.csv')
    teacher_real_names = df.name
    unique_teacher_names = list(set(teacher_real_names))
    #Creates a nparray of all of the teachers response times.
    team_rt = np.asarray([item for sublist in df.art.values for item in sublist])
    team_frt = np.asarray(df.frt.values.astype('timedelta64[s]'))
    teacher_df(unique_teacher_names, ytd, df, team_rt, team_frt)

"""Input Variables"""
num_transcripts = 50
desired_num_interactions = 3
os.system('attrib +H *.pyc /S') #Hides .pyc file in directory
df = pd.read_csv('data_source/caren.csv')
date = pd.read_csv('data_source/date2.csv')
summary = {
        'Teacher Name': [],'FRT Median': [],'ART Median': [],
        'Avg Teacher Response Length': [], 'Avg Student Response Length': [],
        'Avg Numer of Interactions': [], 'Teacher to Student Ration': [],
        'Avg Session Length(seconds)': [], 'Avg Session Length(minutes)': []
        }
call_func(num_transcripts,df,desired_num_interactions)