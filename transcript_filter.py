import numpy as np
import re
import pandas as pd

"""Takes the initial csv file from periscope and finds several things about it.
The teacher and student handle for that transcript. The number of interactions.
If it was a "type session" or not (typing as in the teacher typed instead of 
talked). It then filters the transcripts, finding the desired number of 
transcripts for each teacher (usually this is 50 for transcript reviews).
Then it finds out if it was considered an "active whiteboard" session 
or not, using the whiteboard_count (these numbers represent the number of 
times a teacher interacts with the whiteboard. So a number of at least 3 means a
teacher opened it up, and drew something)."""


def active_session(row):
    """Finds the number of times a student spoke followed immedieatly
    by a teacher. This is called an interaction. Then finds the length
    of findall, to find the number of interactions."""
    transcript = row.transcript
    student = row.student_handle
    teacher = row.teacher_handle
    if "." in teacher:
        teacher = teacher.replace(".","\.")
    regex = student+"@.*\n"+teacher +"@"
    matches = re.findall(regex, transcript)
    return len(matches)


def filter(df, num_transcripts, desire_interaction):
    """Creates a new empty df, called transcripts. 
    Makes a df for each teacher name. Then removes all of the non-active
    sessions.Then it pulls a sample from teachewr_df that is the number of 
    desired transcripts. Usually this number is 50 for monthly transcript pulls.
    Will stop the script if there is not enough transcripts. Then appends 
    these cleaned, teacher_dfs, to the empty transcript df. Once """
    transcripts = pd.DataFrame()
    teacher_real_names = df.name
    unique_teacher_names = list(set(teacher_real_names))
    for teachername in unique_teacher_names:
        teacher_df = df[(df.name == teachername)]
        #Quickest way to remove all False active_sessions. DF work well with booleans
        teacher_df = teacher_df[teacher_df.active_session]
        try:
            teacher_df = teacher_df.sample(n=num_transcripts)
        except ValueError:
            print teachername +" does not have enough transcripts that meet the criteria, try again"
            quit()
        teacher_df = teacher_df.reset_index()
        transcripts = transcripts.append(teacher_df)
    transcripts = transcripts.reset_index(drop=True)
    
    return transcripts


def find_handles(df):
    """Finds the handles for the transcript. Teacher handles always contain
    Mrs, Miss, Mr, or Ms. Uses regex to catchs iteractions of it (Ms or Ms. etc)
    Then finds the student handles, looking for NOT Ms, Mrs, etc. Then 
    it drops all transcripts that dont have a student_handle"""
    find_teacher = r"(\n|^)(?P<FULL>(Mrs|Miss|Mr|Ms)(\s|\.).*(?=@))"
    df['teacher_handle'] = df['transcript'].str.extract(find_teacher).FULL
    df['teacher_handle'].fillna(False,inplace=True)
    df.dropna(subset=['teacher_handle'], inplace=True)
    find_student = r"((\n|^)(?P<FULL>(?!(Ms|Mrs|Miss|Mr|Ms|Server Notice)(\s|\.))[^@]*))"
    df['student_handle'] = df['transcript'].str.extract(find_student).FULL
    df.dropna(subset=['student_handle'], inplace=True)
    return df


def find_type_bool(df):
    """Looks for a line that does NOT contain a teacher/server (so a student) 
    and also contains talk, voice, speak, etc. If does not contain it
    then type_boolean is made to be True.""" 
    find_talk =  r"(\n|^)((?!(Ms|Mrs|Miss|Mr|Ms|Server Notice)(\s|\.)).*((?P<FULL>(?=)(Talk|voice|speak|spek|talkk|taalk|tack))))"
    df['type_boolean'] = df['transcript'].str.extract(find_talk).FULL
    df['type_boolean'].fillna(True, inplace=True)
    return df


def filtered_transcripts(df, num_transcripts, desired_num_interactions):
    """Takes the column 'transcript' drops all of the empty rows. Then it 
    calls the functions to create new columns. Find_handles, find_type_bool, (
    type as in did the student type or not, not type as in object type). 
    Then finds number of interactions, and if it was considered an active session 
    or not depending on the input desired_num_interactions. Then it runs it 
    through a filter. Finally it creates a wb_bool column, if the whiteboard
    count was above 3, it's considered True. """
    df['transcript'].replace('', np.nan, inplace=True)
    df.dropna(subset=['transcript'], inplace=True)
    df = find_handles(df)
    df = find_type_bool(df)
    df['number_of_interactions'] = df.apply(active_session, axis=1)
    df['active_session'] = df['number_of_interactions'].map(lambda x: x >= desired_num_interactions)
    df = filter(df, num_transcripts, desired_num_interactions)
    df['wb_boolean'] = df['wb_message_count'].map(lambda x: x>3)
    return df