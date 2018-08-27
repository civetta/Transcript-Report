# -*- coding: cp1252 -*-
#pulls html and checks for http errors. 
import requests, datetime, time, random

def get_data():

    #Set the request parameters
    token = "41a6672c6981848a474a11ee0f18820f6f0c5b009a8ccb675c1ed44c351ca914d86cd47fa6348279ffc748d7266bf47ceea1470276a6c232a370fefff2f1a3608039ff35ef40a73a1bdf5022edcae2a9939c1cb1248c91abb61d47138b6eeab6304deb4ab35323f7cf88c3009cb32ee6cd7ba16776714e1e2f309bcfc8291291"
    url = 'http://live-teaching.thinkthroughmath.com/admin/dashboard?token='
    url_token = "%s%s"%(url,token)
    
    #Set proper headers
    headers = {"Accept":"application/json"}
     
    #Do the HTTP request
    #might need a try, except exception here
    response = requests.get( url_token, headers=headers )
     
    #Check for HTTP codes other than 200
    if response.status_code != 200: 
        print('Status:', response.status_code, 'Headers:', response.headers, 'Error Response:',response.json())
        exit()

    #Decode the JSON response into a dictionary and use the data
    #admin_data is a dict with keys:
    #[u'ytdTeam', u'hourlyTeacher', u'recentTeam', u'hourlyTeam', u'ytdTeacher']
    admin_data = response.json()
    return admin_data

## SEE WHERE THIS DIFFERS FROM DUSTINS STUFF, SOMETHING IS OFF HERE. 
