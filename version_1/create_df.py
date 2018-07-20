    
    date['start_id'] = date.apply(date_time, axis=1)
    big = pd.merge(df, date, on='start_id', how='left')
    return big