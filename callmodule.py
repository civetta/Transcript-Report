import pandas as pd
from transcript_filter import filtered_transcripts
from test import response_df
import os


os.system('attrib +H *.pyc /S') #Hides .pyc file in direcory
df = pd.read_csv('data_source/Kristin.csv')
date = pd.read_csv('data_source/date2.csv')
df = filtered_transcripts(df, 600, 5)
response_df(df)
#df = response_times(df)
#df = marked_transcripts(df)
#paste_df(df)
#create_summary(df)