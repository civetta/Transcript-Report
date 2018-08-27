import pandas as pd
from openpyxl import Workbook
import numpy as np
from transcript_filter import filtered_transcripts
from dash_data import get_data
from create_teacher_df import teacher_df
from transcript_analysis import find_transcript_data
import os


def call_func(num_transcripts, df, desired_num_interactions, summary):
    ytd = get_data()
    ytd = pd.DataFrame(ytd['ytdTeacher'])
    df = filtered_transcripts(df, num_transcripts, desired_num_interactions)
    """Creating a DF for each teacher and then going through each row to create
    an individual Transcript DF."""
    df['transcript_info'], df['frt'], df['art'], df['vocab_count'], df['vocab'], df['approp_count'], df['session_length_secs'], df['avg_teacher_response_length'], df['avg_student_response_length'], df['exchange_ratio'] = zip(*df.apply(find_transcript_data, axis=1))
    #------The Original DF Has All of the Columns Nesscary After This Point.
    teacher_real_names = df.name
    unique_teacher_names = list(set(teacher_real_names))
    #Creates a nparray of all of the teachers response times.
    team_rt = np.asarray([item for sublist in df.art.values for item in sublist])
    team_frt = np.asarray(df.frt.values.astype('timedelta64[s]'))
    summary = teacher_df(unique_teacher_names, ytd, df, team_rt, team_frt, summary)
    summary = summary[['Name','Team','FRT Median','ART Median','Math Terms Per Session',
     'Appropriate Phrase Per Session','Student Response Length',
     'Teacher Response Length','Student to Teacher Exchange Ratio',
     'Average Session Length(minutes)',
     'Average Session Length(seconds)','Date']]
    summary.to_csv('Management Summary.csv')
    

"""Input Variables"""
num_transcripts = 50
desired_num_interactions = 0
#os.system('attrib +H *.pyc /S') #Hides .pyc file in directory
df = pd.read_csv('data_source/ds_transcrpts.csv')
summary = pd.DataFrame()

call_func(num_transcripts, df, desired_num_interactions,summary)