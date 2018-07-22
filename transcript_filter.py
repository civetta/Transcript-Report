import numpy as np
import re
import pandas as pd


def talk_boolean(row):
    student_handle = row['student_handle']
    transcript = row['transcript']
    if student_handle is not None:
        transcript = transcript.split('\n')
        for line in transcript:
                if student_handle in line:
                    talk_string = 'Talk|voice|speak|spek|talkk|taalk|tack'
                    if re.search(talk_string, line, re.IGNORECASE) is not None:
                        return True
        else:
            return False
    return False


def find_handles(transcript):
    """Finds teacher and student handles in the transcript. These are figured
    out for each transcript because teachers can easily change their handles.
    For example I went from Ms. Heyden to Mrs. Richardson"""
    transcript = transcript.split('\n')
    student_handle = None
    teacher_handle = None
    for line in transcript:
        if line is not "":
            if "Server" not in line:
                a = re.search('((Mrs|Miss|Mr|Ms).*)@ \[', line)
                if a is None:
                    student_handle = line[:line.index('@')].strip()
                else:
                    teacher_handle = a.group(1).strip()
        if teacher_handle is not None and student_handle is not None:
            return teacher_handle, student_handle
    return teacher_handle, student_handle


def active_session(row):
    """Finds the number of times a student spoke followed immedieatly
    by a teacher. This is called an interaction"""
    transcript = row.transcript
    teacher_handle = row.teacher_handle
    student_handle = row.student_handle
    interaction_count = 0
    if teacher_handle is not None and student_handle is not None:
        transcript = transcript.split('\n')
        for i in range(len(transcript)-1):
            if '@' in transcript[i] and '@' in transcript[i+1]:
                first = transcript[i][:transcript[i].index('@')+3]
                second = transcript[i+1][:transcript[i+1].index('@')+3]
                if student_handle in first and teacher_handle in second:
                    interaction_count = interaction_count+1
    return interaction_count


def filter(df, num_transcripts, desire_interaction):
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
            print teachername +" does not have enough transcripts that meet the criteria, try again"
            quit()
        teacher_df = teacher_df.reset_index()
        transcripts = transcripts.append(teacher_df)
    transcripts = transcripts.reset_index(drop=True)
    return transcripts


def filtered_transcripts(df, num_transcripts, desired_num_interactions):
    df['transcript'].replace('', np.nan, inplace=True)
    df.dropna(subset=['transcript'], inplace=True)
    df['teacher_handle'], df['student_handle'] = zip(*df['transcript'].map(find_handles))
    df['number_of_interactions'] = df.apply(active_session, axis=1)
    df['active_session'] = df['number_of_interactions'].map(lambda x: x>=desired_num_interactions)
    df['talk_boolean'] = df.apply(talk_boolean, axis=1)
    df['wb_boolean'] = df['wb_message_count'].map(lambda x: x>3)
    df = filter(df, num_transcripts, desired_num_interactions)
    return df