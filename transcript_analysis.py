import pandas as pd
import numpy as np
from creat_transcript_df import create_transcript_df


def find_transcript_data(row):
    """This is the funcntion that finds all of the interesting data about 
    each transcript. I wrote comments on each part for future refrence"""
    #Calls create_transcript_df which creates a df for each transcript.
    trans_df = create_transcript_df(
        row, row['teacher_handle'].strip(), 
        row['student_handle'].strip(), row['transcript'].strip())
    #Finds the first response time and defines it as the First Response Time (FRT)
    rt, frt = rt_data(trans_df)
    student_response, teacher_response = response_lengths(trans_df)
    #vocab = the total number of vocab words used in the transcript.
    vocab_list = np.asarray([item for sublist in trans_df.vocab.values for item in sublist])
    session_length_secs = (trans_df.Time_Stamps.iloc[-1] - trans_df.Time_Stamps.iloc[0]).seconds
    
    #Finding student to teacher ratio, round to nearest hundreth.
    exchange_ratio = round(trans_df.Student_Bool.sum()/float((trans_df['Student_Bool']==False).sum()),2)
    #returns all of the data found above, place in new columns under plain df.
    return trans_df.to_dict(), frt, rt, trans_df.vocab_count.sum(), vocab_list, trans_df.approp_count.sum(), session_length_secs, student_response, teacher_response, exchange_ratio


def rt_data(trans_df):
    frt_loc = trans_df.Teacher_Response.first_valid_index()
    frt = trans_df.Teacher_Response[frt_loc]
    #RT is short for response time. Looks through lost, drops empty ones
    rt = trans_df.dropna(subset=['Teacher_Response']).Teacher_Response.values.astype('timedelta64[s]')
    return rt,frt
    
def response_lengths(trans_df):
    #Represents the average response length (as in character length)
    student_response = trans_df[trans_df.Student_Bool].Line_Char_Length.mean()
    teacher_response = trans_df[~trans_df.Student_Bool].Line_Char_Length.mean()
    return student_response, teacher_response

