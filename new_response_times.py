import pandas as pd 
import datetime

def response_times(trans_df):
    trans_df['Response_Times'] = trans_df.apply(create_response_times axis=1)


def create_response_times(row):
    

def find_difference(old_stamp, new_stamp):
    old_stamp = old_stamp[old_stamp.index('@')+2:]
    new_stamp = new_stamp[new_stamp.index('@')+2:]
    new = datetime.strptime(old_stamp, " %Y-%m-%d %H:%M:%S")
    old = datetime.strptime(new_stamp, " %Y-%m-%d %H:%M:%S") 
    delta = old-new
    return timedelta.total_seconds(delta)