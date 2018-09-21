import pandas as pd
import os.path
import datetime
from openpyxl import Workbook
import numpy as np
from paste_transcript import paste_transcript
from paste_transcript import paste_response
from paste_kpi import paste_kpi
from datetime import datetime


def teacher_df(unique_teacher_names, ytd, df, team_rt, team_frt, summary, lead_name):
    """Creates a df for each teacher and sends it over to all of the paste
    functions to paste into excel"""
    for teachername in unique_teacher_names:
        
        row_in_ytd = ytd.loc[ytd['teacherName'] == teachername]
        teacherbook, ws, rt_ws = create_teacherbook()

        #Creates teacher_df, which is a df of just a single teacher transcripts.
        teacher_df = df[(df.name == teachername)]
        teacher_df = teacher_df.sort_values('lesson_name')

        #Creates a list of teacher response times.
        teacher_rt = np.asarray([item for sublist in teacher_df.art.values for item in sublist])
        teacher_frt = np.asarray(teacher_df.frt.values.astype('timedelta64[s]'))

        #Pastes everything for each personal teacherbook.
        paste_kpi(teacher_rt, teacher_frt, team_rt, team_frt, rt_ws, row_in_ytd)
        teacher_df.apply(paste_transcript, args=(ws, ), axis=1)
        teacher_df.apply(paste_response, args=(rt_ws, ), axis=1)        
        
        #Saves the workbook as an excel doc, under teacher_sheets, using teachername in the title.
        summary = update_summary_data(teacher_df, teacher_rt, teacher_frt, summary, teachername, lead_name)
        
        mydate = datetime.now()
        month = mydate.strftime("%b")
        path = 'C:\Users\kelly.richardson\OneDrive - Imagine Learning Inc\Reports\Transcript Reports'
        file_name = teachername+"_"+month+'-Transcript Report.xlsx'
        save_location = os.path.join(path,lead_name,teachername)
        if not os.path.isdir(save_location):
            os.makedirs (save_location)
        teacherbook.save(save_location+"/"+file_name)
    
    return summary


def create_teacherbook():
    """Sets up teacherbooks, creates worksheets, deletes default sheet"""
    teacherbook = Workbook()
    ws = teacherbook.create_sheet('Transcripts')
    rt_ws = teacherbook.create_sheet('ART-FRT')
    teacherbook.remove_sheet(teacherbook.get_sheet_by_name('Sheet'))
    return teacherbook, ws, rt_ws


def update_summary_data(teacher_df, teacher_rt, teacher_frt, summary, teachername, lead_name):
    """Updates the Summary df which will be saved as a csv file and given to management"""
    teacher_summary = {
    'Name': [teachername],
    'Team': [lead_name],
    'FRT Median': [np.median(teacher_frt)],
    'ART Median': [np.median(teacher_rt)],
    'Math Terms Per Session': [teacher_df.vocab_count.sum()],
    'Appropriate Phrase Per Session' : [teacher_df.approp_count.mean()],
    'Student Response Length': [np.median(teacher_df.avg_student_response_length)],
    'Teacher Response Length': [np.median(teacher_df.avg_teacher_response_length)],
    'Student to Teacher Exchange Ratio': [teacher_df.exchange_ratio.mean()],
    'Average Session Length(minutes)': [round((teacher_df.session_length_secs.mean())/float(60),2)],
    'Average Session Length(seconds)': [teacher_df.session_length_secs.mean()],
    'Date': [datetime.today().strftime('%Y-%m-%d')]}
    teacher_summary = pd.DataFrame(teacher_summary)
    summary =  summary.append(teacher_summary, sort=False)
    return summary