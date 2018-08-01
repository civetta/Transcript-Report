import numpy as np
import re
import pandas as pd

def active_session(row):
    """Finds the number of times a student spoke followed immedieatly
    by a teacher. This is called an interaction"""
    transcript = row.transcript
    student = row.student_handle
    teacher = row.teacher_handle
    if "." in teacher:
        teacher = teacher.replace(".","\.")
    regex = student+"@.*\n"+teacher +"@"
    matches = re.findall(regex, transcript)
    return len(matches)


def filter(df, num_transcripts, desire_interaction):
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
    find_teacher = r"(\n|^)(?P<FULL>(Mrs|Miss|Mr|Ms)(\s|\.).*(?=@))"
    df['teacher_handle'] = df['transcript'].str.extract(find_teacher).FULL
    df['teacher_handle'].fillna(False,inplace=True)
    df.dropna(subset=['teacher_handle'], inplace=True)
    find_student = r"((\n|^)(?P<FULL>(?!(Ms|Mrs|Miss|Mr|Ms|Server Notice)(\s|\.))[^@]*))"
    df['student_handle'] = df['transcript'].str.extract(find_student).FULL
    df.dropna(subset=['student_handle'], inplace=True)
    return df


def find_type_bool(df):
    find_talk =  r"(\n|^)((?!(Ms|Mrs|Miss|Mr|Ms|Server Notice)(\s|\.)).*((?P<FULL>(?=)(Talk|voice|speak|spek|talkk|taalk|tack))))"
    df['type_boolean'] = df['transcript'].str.extract(find_talk).FULL
    df['type_boolean'].fillna(True, inplace=True)
    return df


def filtered_transcripts(df, num_transcripts, desired_num_interactions):
    df['transcript'].replace('', np.nan, inplace=True)
    
    df.dropna(subset=['transcript'], inplace=True)
    df = find_handles(df)
    df = find_type_bool(df)
    df['number_of_interactions'] = df.apply(active_session, axis=1)
    df['active_session'] = df['number_of_interactions'].map(lambda x: x >= desired_num_interactions)
    df = filter(df, num_transcripts, desired_num_interactions)
    df['wb_boolean'] = df['wb_message_count'].map(lambda x: x>3)
    return df