import pandas as pd


def rt_df(mt, student_handle):
    rt_df = {'TimeStamps': [],
            'ResponseTimes': [],
            'TR': [],
            'SFR': [],
            'TFR': [],}
    for line in mt:
        TR = False
        line_list = line.split('--')
        time_stamp = str(line_list[0])
        if len(line_list) == 2:
            RT = line_list[1]
        else:
            RT = line_list[-1]
        if 'TR' in line_list:
            TR = True
        rt_df['TimeStamps'].append(time_stamp)
        rt_df['ResponseTimes'].append(RT)
        rt_df['TR'].append(TR)
        rt_df['SFR'].append(False)
        rt_df['TFR'].append(False)
    for i, elem in enumerate(rt_df['TimeStamps']):
        if student_handle in elem:
            SFR_location = i
            break
    rt_df['SFR'][SFR_location] = True
    TFR_location = rt_df['TR'].index(True)
    rt_df['TFR'][TFR_location] = True 
    rt_df['TR'][TFR_location] = False

    rt_df = pd.DataFrame(rt_df)   
    rt_df = rt_df.reset_index(drop=True)
    return rt_df
    