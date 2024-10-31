from flask import Flask, render_template, request, redirect, url_for, flash, abort

from google.oauth2 import service_account
from googleapiclient.discovery import build

import os
import json
from datetime import datetime, timedelta, timezone

app = Flask(__name__)

APP_SECRET_KEY = os.environ.get('SECRET_KEY', None)
SERVICE_ACCOUNT_INFO = os.environ.get('SERVICE_ACCOUNT', None)

if SERVICE_ACCOUNT_INFO and APP_SECRET_KEY is not None:
    envOk = True
else:
    # Check environment Variables
    envOk = False

app.secret_key = APP_SECRET_KEY
# OAuth 2.0 credentials and Google Calendar API setup
SCOPES = ['https://www.googleapis.com/auth/calendar']

#SERVICE_ACCOUNT_FILE = 'api-project-643305102087-f687005d2990.json'
#app.secret_key = 'vmHCePweH6z8g759HFjr'

def get_google_calendar_service():
    '''Anmeldung über Dienstkonto'''
    service_account_info = json.loads(SERVICE_ACCOUNT_INFO)
    credentials = service_account.Credentials.from_service_account_info(
            service_account_info, scopes=SCOPES
    )
    service = build('calendar', 'v3', credentials=credentials)
    return service

'''
def get_google_calendar_service():
    creds = None
    
    token_data = os.getenv('GOOGLE_API_TOKEN')

    if token_data:
        creds = Credentials.from_authorized_user_info(json.loads(token_data))
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
                os.environ['GOOGLE_API_TOKEN'] = creds.to_json()
    else:
        # Starte den OAuth-Flow, falls kein Token vorhanden ist
        flow = InstalledAppFlow.from_client_secrets_file(
            'credentials.json', SCOPES
        )
        creds = flow.run_local_server(port=0)

        # Setze den neuen Token in Umgebungsvariablen
        os.environ['GOOGLE_API_TOKEN'] = creds.to_json()

    service = build('calendar', 'v3', credentials=creds)

    return service
'''
@app.route('/')
def index():
    if not envOk:
        return abort(500)

    return render_template('calendar.html')

@app.route('/test1z')
def test():
    y = json.loads(SERVICE_ACCOUNT_INFO)
    return y


@app.route('/book', methods=['POST'])
def book():
    title = request.form.get('title')
    
    # Konvertiere die Zeitangaben zu ISO 8601 mit Zeitzoneninfo
    start_time = datetime.fromisoformat(request.form.get('start_time')).isoformat() + '+02:00'
    end_time = datetime.fromisoformat(request.form.get('end_time')).isoformat() + '+02:00'
    print(start_time)
    print(end_time)
    if not title or not start_time or not end_time:
        flash('All fields are required!')
        return redirect(url_for('index'))

    try:
        service = get_google_calendar_service()
        event = {
            'summary': title,
            'start': {
                'dateTime': start_time,
            },
            'end': {
                'dateTime': end_time,
            },
        }
        print(event)
        service.events().insert(calendarId='h509f2qea5ioe56lr8gevpj57k@group.calendar.google.com', body=event).execute()
        flash('Booking successful!')
    except Exception as e:
        flash(f'An error occurred: {e}')

    return redirect(url_for('index'))

@app.route('/bookings')
def bookings():
    try:
        service = get_google_calendar_service()
        # Hole die Events der nächsten 10 Tage
        #now = datetime.utcnow().isoformat() + 'Z'  # 'Z' bedeutet UTC-Zeit
        now = datetime.now(timezone.utc).isoformat()

        events_result = service.events().list(
            calendarId='h509f2qea5ioe56lr8gevpj57k@group.calendar.google.com', timeMin=now, maxResults=10, singleEvents=True,
            orderBy='startTime').execute()
        
        events = events_result.get('items', [])

        if not events:
            flash('No upcoming bookings found.')
    
        formatted_events = []
        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            end = event['end'].get('dateTime', event['end'].get('date'))
            
            # Parse die Zeit ins datetime-Objekt und formatiere es
            start_dt = datetime.fromisoformat(start)  # Entfernt das 'Z' für UTC
            end_dt = datetime.fromisoformat(end)

            # Formatiere das Datum in DD.MM.YYYY hh:mm
            event['start']['formatted'] = start_dt.strftime('%d.%m.%Y %H:%M')
            event['end']['formatted'] = end_dt.strftime('%d.%m.%Y %H:%M')
            formatted_events.append(event)

        return render_template('bookings.html', events=formatted_events)

    except Exception as e:
        flash(f'An error occurred: {e}')
        return redirect(url_for('index'))

@app.route('/events')
def get_events():
    try:
        service = get_google_calendar_service()

        # Hol die Events der nächsten 30 Tage
        now = datetime.now(timezone.utc).isoformat()
        future = (datetime.now(timezone.utc) + timedelta(days=30)).isoformat()

        events_result = service.events().list(
            calendarId='h509f2qea5ioe56lr8gevpj57k@group.calendar.google.com', timeMin=now, timeMax=future, singleEvents=True,
            orderBy='startTime').execute()
        events = events_result.get('items', [])

        # Konvertiere die Events in ein Format, das FullCalendar verwenden kann
        calendar_events = []
        for event in events:
            calendar_event = {
                'title': event.get('summary', 'No Title'),
                'start': event['start'].get('dateTime', event['start'].get('date')),
                'end': event['end'].get('dateTime', event['end'].get('date')),
            }
            calendar_events.append(calendar_event)

        return json.dumps(calendar_events)
    except Exception as e:
        return str(e), 500

@app.route('/calendar_view')
def calendar_view():
    return render_template('calendarView.html')

if __name__ == '__main__':
    app.run(debug=True)
