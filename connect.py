import psycopg2
import pandas as pd

def get_warehouse_data(start_date, end_date):
  conn = psycopg2.connect("dbname='warehouse' user='kellyrichardson'  password='8b3c9XFGLj3FiSnQvzfJx' host='im-warehouse-prod.cfozmy0xza77.us-west-2.rds.amazonaws.com'")
  sql = """SELECT Cast(starterdate.date as date) as "Session_Date",
CAST(starterdate.date as date) + CAST(startertime.time as Time) as "Session Started",
CAST(enddate.date as date) + CAST(endtime.time as Time) as "Session Ended",
teachers.name, transcript, wb_message_count, items.item_number,
math_lessons.lesson_name, live_help_reasons.reason 

    --Lauras's Team
  ,CASE WHEN teachers.id IN (
    152964	--Caren Glowa
    ,270102	--Crystal Boris
    ,548352	--Jamie Weston
    ,5955	--Kay Plinta-Howard
      ,725743	--Marcella Parks
     ,5957	--Melissa Mitchell
    ,725733	--Michelle Amigh
    ,592154	--Stacy Good
    ,723678	--Laura Gardiner
) THEN 'Laura' 
           
--Rachel's Team
WHEN teachers.id IN (
   5962	--Rachel Adams
  ,901687 --Clifton Dukes
  ,5960	--Heather Chilleo
  ,273045	--Hester Southerland
  ,205305	--Kelly-Anne Heyden
  ,723676	--Kimberly Stanek
  ,555127	--Michele Irwin
  ,553281	--Nancy Polhemus
  ,5966	--Juventino Mireles
    ) THEN 'Rachel'


--Melissa's Team
 WHEN teachers.id IN (
    8444	--Melissa Cox
    ,1027651	--Andrew Lowe
   ,983167 -- Emily McKibben
   ,985473 --Erica DeCosta
   ,594225	--Erin Hrncir
    ,997469 --Erin Spiker
   ,555566	--Jennifer Talaski
   ,1027654	--Julie Horne
   ,559642	--Lisa Duran
   ,993319 --Preston Tirey
  
    ) THEN 'Melissa'

--Sara's Team
WHEN teachers.id IN (
  548353	--Sara Watkins
  ,150843	--Alisa Lynch
  ,725737	--Andrea Burkholder
   ,555257	--Angela Miller
  ,274007	--Bill Hubert
  ,188078	--Donita Spencer
   ,896147 --Jessica Connole
  ,587414	--Laura Craig
  ,40394	--Nicole Marsula
  ,1028752 --Rachel Romana
   ,555565	--Veronica Alvarez
   ,5952	--Wendy Bowser
    ) THEN 'Sara'

--Kristin's Team
WHEN teachers.id IN (
    5958	--Kristin Donnelly
  ,280470	--Carol Kish
  ,555126	--Erica Basilone
  ,984490 --Euna Pin
  ,1029083	--Hannah Beus
  ,982757 --Jenni Alexander
  ,1027653	--Jessica Throolin
  ,1027652	--Natasha W/
  ,555128	--Nicole Knisely
  ,6516	--Shannon Stout
    ) THEN 'Kristin'

--Gabby's Team
WHEN teachers.id IN (
   164866	--Gabriela Torres
  ,6515	--Amy Stayduhar
  ,5965	--Audrey Rogers
  ,262061	--Cheri Shively
  ,596811	--Kathryn Montano
 ,1028751 --Karen Henderson
  ,725746	--Lynae Shepp
  ,553279	--Johana Miller
  ,278244	--Meaghan Wright
  ,997470 --Veronica Wyatt
    ) THEN 'Gabby'  
           
ELSE 'n/a'
END AS Team



FROM live_help_facts



left join teachers on live_help_facts.teacher_id = teachers.id
left join items on live_help_facts.item_id = items.id
left join math_lessons on live_help_facts.math_lesson_id = math_lessons.id
left join live_help_reasons on live_help_facts.live_help_reason_id = live_help_reasons.id
left join dates starterdate on live_help_facts.utc_started_date_id = starterdate.id
left join times startertime on live_help_facts.utc_started_time_id = startertime.id
left join dates enddate on live_help_facts.utc_completed_date_id = enddate.id
left join times endtime on live_help_facts.utc_completed_time_id = endtime.id
WHERE email LIKE '%liveteacher%'
and transcript  is not NULL
and Cast(starterdate.date as date) between"""+start_date+""" and"""+end_date

  df = pd.read_sql_query(sql,conn)
  return df

def warehouseyeardata (end_date):
  from datetime import datetime
  end_date = datetime.today().strftime('%Y-%m-%d')
  conn = psycopg2.connect("dbname='warehouse' user='kellyrichardson'  password='8b3c9XFGLj3FiSnQvzfJx' host='im-warehouse-prod.cfozmy0xza77.us-west-2.rds.amazonaws.com'")
  sql ="""with source as (
  
 select teachers.name as name, seconds_of_help as Average_Session_Time, transcript
FROM live_help_facts
left join teachers on live_help_facts.teacher_id = teachers.id
left join dates on live_help_facts.utc_completed_date_id = dates.id

WHERE email LIKE '%liveteacher%'
and Cast(dates.date as Date) between '2019-08-20' and '"""+end_date+"""'
and transcript  is not NULL)

select name, Avg(Average_Session_Time), count(transcript) from source group by name"""
  df = pd.read_sql_query(sql,conn)
  return df
