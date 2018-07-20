import re
from datetime import datetime
import openpyxl
"""The purpose of this module is to create a time list. So it has [Speaker, difference in time from last interaction] format."""

def transcript_clean_up(transcript_list,  teacher_name):
    """This function identifies the first automated message by the teacher after the server notices and labels it AUTOMATED MESSAGE".
    Then it removes everything after the time stamp,  and makes the time stamp easy to read"""
    list_of_transcripts = []
    #So for each transcript in this entire transcript list we do the following things.
    for transcript in transcript_list:
         
         cleaned_transcript = []
         #This takes our big string and splits it up into multiple parts of an array by enter sign
         transcript_split = transcript.splitlines()
         #This Removes that First Server Notice
         if "Server Notice" in transcript_split[1]:
             transcript_split = transcript_split[2:]
         else:
             transcript_split = transcript_split[1:]
         #The first item in the transcript Array that contains the Server Notice is cut down to a more readable lines
         transcript_split[0] = 'AUTOMATED MESSAGE '+transcript_split[0][transcript_split[0].index('@'):]
         #We Iterate through the Transcript Arrays to each interaction. It turns "Mrs Kelly Anne @ 4:00 PM: Hello can you hear me?" into just "Mrs. Kelly Anne @ 4:00 PM
         for item in transcript_split:
            try:
                match =  re.match(r"(.*)\[(\d{4}-\d{2}-\d{2})T(\d{2}:\d{2}:\d{2})", item)
                cleaned_transcript.append(match.group(1)+match.group(3))
            except:
                continue
         #Add's those lists to another list.
         list_of_transcripts.append(cleaned_transcript)
    #This calls the function below to find difference in times.
    time_list = art_frt_organizer(list_of_transcripts,teacher_name)
    return time_list
     



            

def art_frt_organizer(transcript_list, teacher_name):
    """The following function creates a list of couples. [Person Who Spoke, The Time it Took For them To Respones to Last Message]"""
    teacher_list_of_transcripts = []
    #For each Transcript in Transcript_List that looks like [Ms. Kelly-Anne @ 15:07:47, Ms. Kelly-Anne @ 15:07:51, Kennedi @ 15:08:11, Ms. Kelly-Anne @ 15:08:42]
    for transcript in transcript_list:
        transcripter=[[transcript[0],'0:00:00']]
        for item in transcript[1:]:
            difference=time_difference(transcript[transcript.index(item)-1], item)
            couple=[item,difference]
            transcripter.append(couple)
        teacher_list_of_transcripts.append(transcripter)
    return teacher_list_of_transcripts
        
            
        



def time_difference(time1, time2):
    """This finds the difference between two times. If the times happen over the course of 11 to Midnight, it fixes it"""
    if '@' in time2:
        time2 = time2[time2.index('@')+2:]
        time1 = time1[time1.index('@')+2:]
        datetime1 = datetime.strptime(time1, '%H:%M:%S')
        datetime2 = datetime.strptime(time2, '%H:%M:%S')
        difference = datetime2 - datetime1
        difference = str(difference)
        if len(difference)>7:
            difference = difference[-7:]
        return difference
                        



