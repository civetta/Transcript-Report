import pandas as pd 

def response_times(rt_ws, trans_df):
    a=1
    trans_df['rt']=trans_df.Time_Stamps.diff().dt.total_seconds().fillna(0)
    #trans_df['teacher_response'] = trans_df.apply(teacher_response, axis=1)
    


    #print diff_times