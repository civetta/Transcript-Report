import numpy as np
import re
import pandas as pd

"""Takes the initial csv file from periscope turned into a df, and finds several things about it.
The teacher and student handle for that transcript. The number of interactions.
If it was a "keyboard session" or not (using keyboard instead of talking to the student).
It then filters the transcripts, finding the desired number of 
transcripts for each teacher (usually this is 50 for transcript reviews).
Then it finds out if it was considered an "active whiteboard" session 
or not, using the whiteboard_count (these numbers represent the number of 
times a teacher interacts with the whiteboard. So a number of at least 3 means a
teacher opened it up, and drew something)."""

def filtered_transcripts(df, num_transcripts, desired_num_interactions):
    """Takes the column 'transcript' drops all of the empty rows. Then it 
    calls the functions to create new columns. Find_handles, find_type_bool, (
    type as in did the student type or not, not type as in object type). 
    Then finds number of interactions, and if it was considered an active session 
    or not depending on the input desired_num_interactions. Then it runs it 
    through a filter. Finally it creates a wb_bool column, if the whiteboard
    count was above 3, it's considered True.
    
    df: DataFrame
    num_transcripts: integer
    desired_num_interactions: integer
     """
    df['transcript'].replace('', np.nan, inplace=True)
    df.dropna(subset=['transcript'], inplace=True)
    df = find_handles(df)
    df = find_keyboard_bool(df)
    df['number_of_interactions'] = df.apply(active_session, axis=1)
    df['active_session'] = df['number_of_interactions'].map(lambda x: x >= desired_num_interactions)
    df = filter(df, num_transcripts, desired_num_interactions)
    df['wb_boolean'] = df['wb_message_count'].map(lambda x: x>3)
    return df



def active_session(row):
    """Finds the number of times a student spoke followed immedieatly
    by a teacher. This is called an interaction. Then finds the length
    of findall, to find the number of interactions.
    
    Called using maping. 
    Row: row in dataframe"""
    
    student = row['student_handle']
    teacher = row['teacher_handle']
    if "." in teacher:
        teacher = teacher.replace(".","\.")
    regex = student+"@.*\n"+teacher +"@"
    matches = re.findall(regex, row['transcript'])
    return len(matches)


def find_keyboard_bool(df):
    """Looks for a line that does NOT contain a teacher/server (so a student) 
    and also contains talk, voice, speak, etc. If does not contain it
    then type_boolean is made to be True.""" 
    find_talk =  r"(\n|^)((?!(Ms|Mrs|Miss|Mr|Ms|Server Notice)(\s|\.)).*((?P<FULL>(?=)(Talk|voice|speak|spek|talkk|taalk|tack))))"
    df['keyboard_boolean'] = df['transcript'].str.extract(find_talk,flags = re.IGNORECASE).FULL
    df['keyboard_boolean'].fillna(True, inplace=True)
    df['keyboard_boolean'] =df['keyboard_boolean'].map(lambda x: x is True)
    #Drops all False "typing sessions"
    df = df[df['keyboard_boolean']]
    return df


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
    df['student_handle'] = df['transcript'].str.extract(find_student,).FULL
    df.dropna(subset=['student_handle'], inplace=True)
    return df


def filter(df, num_transcripts, desire_interaction):
    """Creates a new empty df, called filtered_df. 
    Makes a dataframe for each teacher. Then removes all of the non-active
    sessions.Then it pulls a sample from teacher_df that is the number of 
    desired transcripts. If sample cannot be met an error is given but 
    it does not stop the script. Instead, all possible transcripts are 
    used instead of 50. This decision was made by management. 
    Then it appends these cleaned, teacher_dfs, to the empty filtered_df. """
    filtered_df = pd.DataFrame()
    teacher_real_names = df['name']
    unique_teacher_names = list(set(teacher_real_names))
    
    for teachername in unique_teacher_names:
        #creates a df for each teacher only containing their transcripts.
        teacher_df = df[(df.name == teachername)]
        #Quickest way to remove all False active_sessions.
        teacher_df = teacher_df[teacher_df.active_session]
    
        try:
            teacher_df = teacher_df.sample(n=num_transcripts)
        except ValueError:
            print teacher_df.shape
            print"WARNING "+ teachername +" does not have enough transcripts that meet the criteria."
        #Cleans teacher df and appends to final filtered_df
        teacher_df = teacher_df.reset_index()
        filtered_df = filtered_df.append(teacher_df)
    
    filtered_df = filtered_df.reset_index(drop=True)    
    return filtered_df


