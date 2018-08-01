"""The purpose of this program is to taken input of a csv file of 1000< transcripts, and return x amount of transcripts per teacher, with each
transcript being over 600 characters long, and having no form of the word "talk" in them and transpose them in an easy to read format.
The first step is to realize what teachers are in the CSV file, which I do with find_teacher_name. They I take the csv file and manipulate it in
string form, identifying the start of each transcript by placing a &&& there. Then I turn it into an array.
In array form I filter out all of the "bad" transcripts and make it a "clean array".
Then I run it through a function that returns a random set of x amount of transcripts per teacher from the cleaned out array. I 
Finally I do some final formatting so each transcript is it's own row."""
from random import shuffle
import re

def find_teacher_names(csv_list):
    """#This function is given an input of the csv file, and finds all of the teachers names.
    #CSV File => List of unique Teacher Names in the CSV File"""
    teacher_names = [row[1] for row in csv_list]
    return list(set(teacher_names[1:]))

def clean_up(csv_list,transcript_Number):
    """This functions take the csv file and returns an array of transcript strings that are
    greater than 600 characters and don't have different variations of the word "Talk" in them, in the first 600 characters.
    """
    clean_Array=[]
    talk_string='Talk|voice|speak|spek|talkk|taalk|tack'
    for row in csv_list:
        i=row[2]
        line=i.splitlines()
        if len(i)>200 and i.count('talk')<=1 and len(re.findall(talk_string,i,re.IGNORECASE))<=1 and len(re.findall("Ms.|Mrs.|Mr.|Miss ",i)) >=2:
            """Checks to make sure there is an @ in each line and there are no empty strings"""
    
            if len(line)!=len(re.findall('@',i)):
                continue
            if str(row[5])!='yes':
                if int(row[4])>3:
                    clean_Array.append(row[1]+" LESSON SPLIT "+row[3]+"--Whiteboard Used"+" LESSON SPLIT2 "+row[2])
                else:
                    clean_Array.append(row[1]+" LESSON SPLIT "+row[3]+" LESSON SPLIT2 "+row[2])
    return clean_Array

def transcripts_per_teacher(transcripts,teacher_Names,transcript_Number):
    """#This functions returns x transcripts per teachers in the list.
    #Clean_Array list =>x Transcripts Per Teacher Array"""
    transcript_by_teacher = {}
    for name in teacher_Names:
        matching = [s for s in transcripts if name in s]
        print name +" has " + str(len(matching)) + " transcripts that are over 600 characters and does not have the word talk in them"
        if len(matching) < transcript_Number:
            print "There is not enough transcripts that match the criteria for " + name
            team_lead_name = raw_input('\n''Please restart the calculator and try again with another csv file')
        transcript_by_teacher[name] = matching[0:transcript_Number+10]
    return transcript_by_teacher


def get_filtered_teacher_transcripts(csv_list,transcript_Number):
    """This function takes the csv_list, and the transcript number ands run them
    through all of the other scripts above to get us the final result of Teacher:Transcripts
    dictionary."""
    teacher_Names = find_teacher_names(csv_list)
    transcripts = clean_up(csv_list,transcript_Number)
    shuffle(transcripts)
    tran_dict=transcripts_per_teacher(transcripts,teacher_Names,transcript_Number)
    return tran_dict
        
