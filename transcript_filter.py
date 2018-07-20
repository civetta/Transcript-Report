import numpy as np
import re
import pandas as pd

"""The purpose of this module is to take the original teacher periscope csv
file and create two new columns. One is the character length of the transcript
and the other is to see if it a talk sessions or not. Then using these columns
as a filter it creates a new dataframe. This dataframe returns 
a number of sessions per teacherm which is decided by the user and stored
under variable num_transcripts, this number is usually 50. Then it uses 
the talk boolean to return only sessions that are not considered "talk" and are
above the session length number which is stored as variable 
"session_length"""


def talk_boolean(df):
    """Looks for sessions where a student/or a teacher ever uses the word 
    "talk, tack,etc, then declares it a talk session, true or false. It's 
    done this way so if a kid changes it to a talk session mid session it still
    counts as a talk session."""
    transcript = (df.transcript).split('/n')
    student_handle = df.student_handle
    if student_handle is not None:
        for line in transcript:
                if student_handle in line:
                    print line
                    talk_string = 'Talk|voice|speak|spek|talkk|taalk|tack'
                    if re.search(talk_string, line, re.IGNORECASE) is not None:
                        return True


def find_handles(i):
    i = i.split('\n')
    student_handle = None
    teacher_handle = None
    for line in i:
        if line is not "":
            if "Server" not in line:
                a = re.search('((Mrs|Miss|Mr|Ms).*)@ \[', line)
                if a is None:
                    student_handle = line[:line.index('@')]
                else:
                    teacher_handle = a.group(1)
        if teacher_handle is not None and student_handle is not None:
            return teacher_handle, student_handle
    return teacher_handle, student_handle

def active_session(i):
    transcript = i.transcript
    teacher_handle = i.teacher_handle
    student_handle = i.student_handle
    if teacher_handle is not None:
        if student_handle is not None:
            teacher = re.findall(teacher_handle, transcript)
            student = re.findall(student_handle, transcript)
            if len(student)>1 and len(teacher)>1:
                return True
    return False

def filter(df, num_transcripts, char_length):
    """Creates an empty data frame and then for each teacher
    finds num_transcripts number of transcripts that meet the criteriea
    and appends them onto the empty dataframe called transcripts. 
    In the end there should been num_transcripts amount of random transcripts
    that are above the char_length and talk_boolean is False"""
    transcripts = pd.DataFrame()
    teacher_real_names = df.name
    unique_teacher_names = list(set(teacher_real_names))
    for teachername in unique_teacher_names:
        teacher_df = df[(df.name == teachername)]
        teacher_df = teacher_df.query('active_session==True')
        teacher_df = teacher_df.query('talk_boolean==False')
        try:
            teacher_df = teacher_df.sample(n=num_transcripts)
        except ValueError:
            print teachername +"does not have enough transcripts that meet the criteria, try again"
        teacher_df = teacher_df.reset_index()
        transcripts = transcripts.append(teacher_df)
    transcripts = transcripts.reset_index(drop=True)
    return transcripts


def filtered_transcripts(df, char_length, num_transcripts):
    """Replaces all of the empty transcripts as None, then it calls the 
    talk boolean function to create the talk boolean column. After that 
    it creates the session_char_length column which is short for 
    session character length. This is just the number of characters in 
    the transcripts. Used for filtering"""
    df['transcript'].replace('', np.nan, inplace=True)
    df.dropna(subset=['transcript'], inplace=True)
    df['teacher_handle'], df['student_handle'] = zip(*df['transcript'].map(find_handles))
    df['active_session'] = df.apply(active_session, axis=1)
    df['talk_boolean'] = df.apply(talk_boolean, axis=1)
    df = filter(df, num_transcripts, char_length)
    return df