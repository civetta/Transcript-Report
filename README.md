# Transcript-Report    
The purpose of this script is to generate Transcript Reports for teachers.
Each teacher has their own transcript report containing only their transcripts,
and personal Key Performance Indicators (KPI). Only transcripts that meet
certain criteria are used. These criteria's can be edited under User Input Variables.


The input for this script, is a CSV file pulled from the "Live Teaching Data" 
dashboard in Periscope.

The output for this script is a Transcript Report Excel file for each teacher,
and then a summary excel file containing summary KPI information. The summary
excel file is only read by management and contains other data not given to 
teachers in their personal Transcript Reports. This was a desicion by management.

# Known Problems
1) Regex efficiency under marked_lines is poor.

# Modules Descriptions

**CallModule**




**Transcript Filter:** Takes the initial csv file from periscope and finds several things about it.
The teacher and student handle for that transcript. The number of interactions.
If it was a "type session" or not (typing as in the teacher typed instead of 
talked). It then filters the transcripts, finding the desired number of 
transcripts for each teacher (usually this is 50 for transcript reviews).
Then it finds out if it was considered an "active whiteboard" session 
or not, using the whiteboard_count (these numbers represent the number of 
times a teacher interacts with the whiteboard. So a number of at least 3 means a
teacher opened it up, and drew something).

**Create Transcript DF:** Takes each transcripts and makes a dataframe out of each of them called
 trans_df (transcript dataframe). With this it figures out the RT (response time)
 It also figures out the response time between each line,
teacher response time to a student specifically, and 
 creates an rt_paste which is a hybrid of those together and is pasted in the 
 transcript-report so teachers can see Their Response times to a student as 
 well as other response times. 


**Create Teacher Df:** Creates a DF for each teachers transcripts. Then goes
through each transcript in teacher_df and makes another df for each transcript (called trans_df, see Create Transcript DF).
Once create_transcript_df has gone through and analyzed each individual transcript, it zips all of the information back 
up and adds new columns to the teacher_df, with the new data being information about the transcript in that row. 
Then using that information it makes further data. For example using the response time data figured out by
transcript_df, a new column will be added to teacher_df with the median response time of the transcripts in 
the same row. 


**Marked Lines:**
Marked Lines module takes the transcript df as an input. Each row is a line 
in the transcript. It is used to find when vocab is used, appropriate phrases 
are used, and if a teacher talks more than 3 times in row. Then the column
"marked_lines" is updated, which indicators attached to it. For example if 
a teacher used vocab, then --VOCAB is added at the end so that when pasting it
into Openpyxl, the script knows to make that line blue.

**Paste Transcript:**
Pastes transcript information into Transcript worksheet in teacherbook. It 
pastes one line of the transcript into each row. Then looking for the marked lines markers (such as --VOCAB), it formats the cell. For example if there is a
--GREY OUT in the line, it will make the background a light gray.

**Paste KPI:** Pastes the summary data in the KPI worksheet in the teacherbook. It includes
the team FRT, teacher FRT, teacher ART, and Team ART. Then it generates charts
for easy comparison.