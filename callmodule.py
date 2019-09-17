import pandas as pd
from datetime import datetime
from openpyxl import Workbook
from datetime import time
import os.path
import numpy as np
from transcript_filter import filtered_transcripts
from dash_data import get_data
from create_teacher_df import teacher_df
from transcript_analysis import find_transcript_data
from connect import get_warehouse_data, warehouseyeardata
import os


pd.options.mode.chained_assignment = None

def call_func(num_transcripts, df, desired_num_interactions, summary, lead_name, debug,yeardata):
    #ytd = get_data()
    #ytd = pd.DataFrame(ytd['ytdTeacher'])
    #ytd = "To Be Replaced"
    df = filtered_transcripts(df, num_transcripts, desired_num_interactions)
    """Creating a DF for each teacher and then going through each row to create
    an individual Transcript DF."""
    df['transcript_info'], df['frt'], df['art'], df['vocab_count'], df['vocab'], df['approp_count'], df['session_length_secs'], df['avg_teacher_response_length'], df['avg_student_response_length'], df['exchange_ratio'], df['has_drag_drop'] = list(zip(*df.apply(find_transcript_data, axis=1)))
    #------The Original DF Has All of the Columns Nesscary After This Point.
    teacher_real_names = df.name
    unique_teacher_names = list(set(teacher_real_names))
    #Creates a nparray of all of the teachers response times.
    team_rt = np.asarray([item for sublist in df.art.values for item in sublist])
    team_frt = np.asarray(df.frt.values.astype('timedelta64[s]'))
    summary = teacher_df(unique_teacher_names, df, team_rt, team_frt, summary, lead_name, debug,yeardata)
    summary = summary[['Name','Team','FRT Median','ART Median','Math Terms Per Session',
     'Appropriate Phrase Per Session','Student Response Length',
     'Teacher Response Length','Student to Teacher Exchange Ratio',
     'Average Session Length(minutes)',
     'Average Session Length(seconds)','Visuals Count','Date']]
    #print summary
    if debug is False:
        save_management(summary)


def save_management(summary):
    print("Starting to Save Management")
    mydate = datetime.now()
    month = mydate.strftime("%b")
    ms_filename = 'Management Summary-'+month+'.csv'
    path = 'C:\\Users\kelly.richardson\OneDrive - Imagine Learning Inc\Reports\Transcript Reports\Management Summaries'
    ms_path = os.path.join(path,ms_filename)
    if combine_management_summaries is False:
        summary.to_csv(ms_path,index=False)
    else:
        ms = pd.read_csv(ms_path)
        ms = ms.append(summary, sort=False, ignore_index=True)
        ms.to_csv(ms_path,index=False)

"""Input Variables"""
#Appends team data to already existing management csv file.
combine_management_summaries = False
num_transcripts = 25
desired_num_interactions = 3
lead_name = "New_Teachers_Fall_2019"
debug = True
start_date = "'2019-09-01'"
end_date = "'2019-09-17'"
#os.system('attrib +H *.pyc /S') #Hides .pyc file in directory
df = get_warehouse_data(start_date, end_date)
yeardata = warehouseyeardata() 
print (df)

summary = pd.DataFrame()

call_func(num_transcripts, df, desired_num_interactions,summary,lead_name, debug, yeardata)