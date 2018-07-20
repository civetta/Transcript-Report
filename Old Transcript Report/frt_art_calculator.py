import numpy as np
from random import shuffle
from create_time_list import time_difference
from datetime import datetime
import re

"""Finding the Logic
1) Create an array called "Reponse Times
2) Find the Teacher Name
3) Going through each transcript which is a list of lists [name,response time][name,response time]
4) If teacher name is not in First item in transcript and it's not automated message, then it's the student
5) X equals current mini list [name, response time]. So if teacher user_name"""
def identify_teacher_response_time(transcript,teacher_name,teacher_rt_list):
    #Teacher First Response is Defined as the first time a teacher responds to a child. So we need to find the student first response first.
    student_found=False
    length=0
    session_response_times=[]
    student_first_found=0
    teacher_first_found=0
    #Find True Difference Between Student and Teacher Response Times that are not the FRT and list them in the Excel in Transcript[0][1]
    while length< len(transcript):
        x=transcript[length][0]
        if teacher_name not in x and "AUTOMATED MESSAGE" not in x and student_found==False:
            student_found=True
            student_time=x
            if student_first_found==0:
                student_first_found=x
                transcript[length][0]="GREEN "+transcript[length][0]
        if student_found==True and teacher_name in x:
            teacher_time=x
            session_response_times.append(time_difference(student_time,teacher_time))
            transcript[length][1]=time_difference(student_time,teacher_time)
            transcript[length][0]="BOLD "+transcript[length][0]
            student_found=False
            if teacher_first_found==0:
                transcript[length][1]=time_difference(student_first_found,teacher_time)
                transcript[length][0]=transcript[length][0].replace("BOLD","BLUE")
                teacher_first_found=1
        else:
            length=length+1
            continue
        length=length+1
    teacher_rt_list.append(session_response_times)
    return teacher_rt_list
    
            

def find_rt(teacher_transcripts):
    teacher_rt_list=[]
    for i in teacher_transcripts:
        teacher_name=find_teacher_username(i)
        identify_teacher_response_time(i,teacher_name,teacher_rt_list)
    return teacher_rt_list


def session_length(time_list,num):
    total=0
    for x in time_list:
        time1=x[0][0]
        time2=x[-1][0]
        time2 = time2[time2.index('@')+2:]
        time1 = time1[time1.index('@')+2:]
        datetime1 = datetime.strptime(time1, '%H:%M:%S')
        datetime2 = datetime.strptime(time2, '%H:%M:%S')
        difference = str(datetime2 - datetime1)
        if "-1" in difference:
            difference=difference[difference.index(',')+2:]
        h, m, s = difference.split(':')
        difference = int(h) * 3600 + int(m) * 60 + int(s)
        total=total+difference
    return total/float(num)

def find_teacher_username(transcript):
    for i in transcript:
        i=i[0]
        name_string=i[:i.index('@')]
        if re.match("Ms.|Mrs.|Mr.|Miss ",name_string):
            return name_string
    

def find_teacher_frt(rt_list):
    FRT=[]
    for transcript in rt_list:
        if len(transcript)>0:
            h, m, s = transcript[0].split(':')
            FR = int(h) * 3600 + int(m) * 60 + int(s)
            FRT.append(FR)
    FRT=sorted(FRT)
    return FRT

def find_teacher_ART(rt_list):
    ART=[]
    for transcript in rt_list:
        for transaction in transcript:
            h, m, s = transaction.split(':')
            AR = int(h) * 3600 + int(m) * 60 + int(s)
            ART.append(AR)
    ART=sorted(ART)
    return ART
        

def find_team_FRT(teacher_dict,teacher_names):
    frt=[]
    for i in teacher_names:
        response=teacher_dict[i]
        for transcript in response:
             try:
                 h, m, s = transcript[0].split(':')
                 FR = int(h) * 3600 + int(m) * 60 + int(s)
                 frt.append(FR)
             except:
                 continue
    FRT=sorted(frt)
    return FRT

def find_team_ART(teacher_dict,teacher_names):
    art=[]
    for i in teacher_names:
        response=teacher_dict[i]
        for transcript in response:
            for transaction in transcript:
                h, m, s = transaction.split(':')
                FR = int(h) * 3600 + int(m) * 60 + int(s)
                art.append(FR)
    ART=sorted(art)
    return ART
            
        
        
        
        
            
            
    
            
        
