#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Run this script first to obtain the token. Credentials.json must be in the same folder first.
To obtain Credentials.json, follow the instructions listed in the following link.
https://developers.google.com/calendar/api/quickstart/python
"""

from __future__ import print_function
import datetime
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from datetime import datetime
from datetime import timedelta
from google.oauth2.credentials import Credentials

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

def main(tokenFile, credentialsFile):
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists(tokenFile):
        creds = Credentials.from_authorized_user_file(tokenFile, SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                credentialsFile, SCOPES)
            creds = flow.run_local_server(port=42424)
        # Save the credentials for the next run
        with open(tokenFile, 'wb') as token:
            pickle.dump(creds, token)

    service = build('calendar', 'v3', credentials=creds)

    # Call the Calendar API
    today = datetime.today()

    # now = (today + timedelta(days = -50)).isoformat() + 'Z' # 'Z' indicates UTC time
    now = (today + timedelta(days = -50)).isoformat() + 'Z' # 'Z' indicates UTC time
    print('Getting the upcoming 10 events')
    events_result = service.events().list(calendarId='primary', timeMin=now,
                                        maxResults=100, singleEvents=True,
                                        orderBy='startTime').execute()
    events = events_result.get('items', [])

    processedEvents = {}

    if not events:
        print('No upcoming events found.')
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        # end = event['end'].get('dateTime', event['start'].get('date'))
        # updated = event['updated']
        # print(start + " | " + " | " + event['summary'])
        # print(start, event['summary'].encode('utf-8'))
        processedEvents[start] = event

    # print(processedEvents)

    today = datetime.today()
    today = today + timedelta(days = -1)

    print(str(today.year)+"-"+str(today.month)+"-"+str(today.day))

    for eventDate in processedEvents: 
        if eventDate.find(str(today.year)+"-"+str(today.month)+"-"+str(today.day)) != -1:
            # print(event, processedEvents[eventDate])
            print(eventDate, processedEvents[eventDate]['summary'].encode('utf-8'))

    return processedEvents

if __name__ == '__main__':
    main()