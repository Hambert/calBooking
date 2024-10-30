# Flask Calendar Booking Application

Eine Web-Anwendung auf Basis von Python Flask zur Buchung von Kalenderplätzen. Die Anwendung verbindet sich mit Google Kalender über ein Dienstkonto, um Events anzuzeigen, zu erstellen und zu verwalten.
Projektübersicht

## Funktionen:

    Eine Weboberfläche zur Buchung von Terminen im Google Kalender.
    Integration mit Google Kalender API, basierend auf einem Google-Dienstkonto.
    Darstellung aller Buchungen im Kalender-Layout mit FullCalendar.js.

## Voraussetzungen

    Python 3.8 oder höher
    Google Cloud Konto für das Dienstkonto und die API-Authentifizierung
    Flask
    FullCalendar.js (für die Kalender-Darstellung der Buchungen)


## Google Cloud API aktivieren und Dienstkonto erstellen:

    Erstelle ein Google Cloud-Projekt und aktiviere die Google Kalender API.
    Erstelle ein Dienstkonto und lade den JSON-Schlüssel herunter.
    Stelle sicher, dass der Kalender, der verwendet werden soll, mit der E-Mail-Adresse des Dienstkontos geteilt ist.

## Konfigurationsdatei .env erstellen:

    Füge die Dienstkonto-Schlüsseldatei (service_account.json) im Projektverzeichnis ein oder speichere deren Inhalte in einer Umgebungsvariablen.
    Erstelle eine .env-Datei mit dem folgenden Inhalt:

    makefile

    FLASK_SECRET_KEY=your_secret_key
    GOOGLE_SERVICE_ACCOUNT_INFO=JSON_inhalt_des_Dienstkontos


project-folder/
├── templates/
│   ├── calendar.html          # Startseite für Buchungen
│   ├── bookings.html          # Übersicht gebuchter Events
│   └── calendarView.html      # FullCalendar.js-Kalenderansicht
├── static/
│   └── fullcalendar.js        # FullCalendar.js Bibliothek (optional, falls lokal gespeichert)
├── app.py                     # Hauptanwendung
├── requirements.txt           # Python-Abhängigkeiten
└── README.md                  # Diese Datei

# Hauptfunktionen
1. Buchung eines Termins

Die book-Route erlaubt das Erstellen eines Termins im Kalender durch Eingabe von Titel, Start- und Endzeit.
2. Anzeige der Buchungen

Die bookings-Route zeigt eine Liste aller bevorstehenden Buchungen an und formatiert die Start- und Endzeiten im Format DD.MM.YYYY hh:mm.
3. Kalenderansicht mit FullCalendar.js

Die Route /calendar_view zeigt alle Buchungen im Kalenderformat, indem die FullCalendar.js-Bibliothek verwendet wird.
Endpunkte
Route	Beschreibung
/	Startseite zur Eingabe neuer Buchungen
/book	Endpunkt für das Erstellen eines neuen Events
/bookings	Zeigt eine Liste der kommenden Buchungen
/events	API-Endpunkt zum Abrufen der Events im JSON-Format
/calendar_view	Zeigt die Buchungen in der FullCalendar.js-Kalenderansicht
Umgebungsvariablen

Stelle sicher, dass folgende Umgebungsvariablen konfiguriert sind:

    FLASK_SECRET_KEY: Ein geheimer Schlüssel für Flask-Sitzungen.
    GOOGLE_SERVICE_ACCOUNT_INFO: JSON-Inhalt der Dienstkonto-Anmeldeinformationen als Umgebungsvariable (für Vercel oder AWS Lambda).

# Lizenz
