import pandas as pd
from openpyxl import Workbook
import numpy as np
from creat_transcript_df import create_transcript_df
from paste_transcript import paste_transcript
from paste_transcript import paste_response
from paste_kpi import paste_kpi

def teacher_df(unique_teacher_names, ytd, df, team_rt, team_frt):
    for teachername in unique_teacher_names:
        row_in_ytd = ytd.loc[ytd['teacherName'] == teachername]
        #Sets up teacherbooks, creates worksheets, deletes default sheet
        teacherbook = Workbook()
        ws = teacherbook.create_sheet('Transcripts')
        rt_ws = teacherbook.create_sheet('ART-FRT')
        teacherbook.remove_sheet(teacherbook.get_sheet_by_name('Sheet'))
        #Creates teacher_df, which is a df of just a single teacher transcripts.
        teacher_df = df[(df.name == teachername)]
        teacher_df = teacher_df.sort_values('lesson_name')
        #Creates a list of teacher response times.
        teacher_rt = np.asarray([item for sublist in teacher_df.art.values for item in sublist])
        #Creates a list of teacher first response times.
        teacher_frt = np.asarray(teacher_df.frt.values.astype('timedelta64[s]'))
        #Pastes everything for each personal teacherbook.
        paste_kpi(teacher_rt, teacher_frt, team_rt, team_frt, rt_ws, row_in_ytd)
        teacher_df.apply(paste_transcript, args=(ws, ), axis=1)
        teacher_df.apply(paste_response, args=(rt_ws, ), axis=1)        
        #saves
        teacherbook.save('teacher_sheets/'+teachername+'.xlsx')


def find_transcript_data(row):
    #Gets variables for each row that will be used.
    teach_handle = row['teacher_handle'].strip()
    stud_handle = row['student_handle'].strip()
    transcript = row['transcript'].strip()
    #Calls create_transcript_df which creates a df for each transcript.
    trans_df = create_transcript_df(row, teach_handle, stud_handle, transcript)
    #Finds the first response time and defines it as the First Response Time (FRT)
    frt_loc = trans_df.Teacher_Response.first_valid_index()
    frt = trans_df.Teacher_Response[frt_loc]
    #RT is short for response time. Looks through lost, drops empty ones
    rt = trans_df.dropna(subset=['Teacher_Response']).Teacher_Response.values.astype('timedelta64[s]')
    #vocab = the total number of vocab words used in the transcript.
    vocab = trans_df.vocab_count.sum()
    session_length_secs = (trans_df.Time_Stamps.iloc[-1] - trans_df.Time_Stamps.iloc[0]).seconds
    #Represents the response length (as in character length)
    student_response = trans_df[trans_df.Student_Bool].Line_Char_Length.mean()
    teacher_response = trans_df[~trans_df.Student_Bool].Line_Char_Length.mean()
    #returns all of the data found above, place in new columns under plain df.
    return trans_df.to_dict(), frt, rt, vocab, session_length_secs, student_response, teacher_response
