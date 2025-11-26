Datenimport und Start der Django-Anwendung

Diese Anleitung beschreibt, wie du die bereitgestellte Excel-Datei in die Django-Anwendung importierst, die Datenbank aktualisierst und anschließend den Server startest.

1. Daten importieren

Führe den folgenden Befehl im Terminal aus. Wichtig: Du musst dich im Verzeichnis befinden, in dem sich die Datei manage.py befindet.

--> python manage.py import_data Flohmarkt_Simulation.xlsx --sheet1 "ZB_Verkäufer2" --sheet2 "ZB_Käufer2"

2. Migrationen erstellen

Erzeuge die benötigten Migrationen mit:

--> python manage.py makemigrations

3. Migrationen anwenden

Führe die erstellten Migrationen aus:

--> python manage.py migrate

4. Server starten

Starte anschließend den Django-Entwicklungsserver:

--> python manage.py runserver
