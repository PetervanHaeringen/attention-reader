# Focuslezer

*Eén zin tegelijk. Het oog mag rusten, de verbeelding krijgt ruimte.*

Focuslezer is een rustige leesapp die telkens één zin centraal stelt. De vorige
zin staat erboven als vervaagd nabeeld; de volgende komt half uit de mist
eronder. De lezer houdt zelf het tempo — klik, spatie of pijltjes.

## Het idee

Bij lezen scant het oog vooruit en terug, soms chaotisch — wie moeizaam leest,
verliest daardoor de plek of laat het begin van een zin los voor het einde
binnen is. Door maar één zin helder te tonen, met de buren als zachte context,
krijgt het oog een *omheining zonder hek*: het mag heen en weer, maar binnen een
kleinere ruimte. De trage overgang tussen zinnen — die meeademt met de lengte
van de zin — traint zachtjes de spanningsboog die ook een lange zin van je
vraagt: het uitstel van begrip verdragen tot het punt valt.

Lezen activeert de verbeelding in plaats van haar te vullen met wat een ander
bedacht heeft, en dat schept een ruimte waarin van alles kan groeien.

## Wat het kan

- **Eén zin centraal**, met de vorige en volgende zacht in de mist eromheen.
- **Een adem die meegroeit** met de lengte van de zin — lange zinnen vervloeien
  langzamer dan korte.
- **Een 'vanzelf'-stand** waarin de zinnen vanzelf komen en het tempo zich naar
  je leesritme voegt: druk vóór de adem en het wordt vlotter, laat een zin
  vanzelf wegademen en het wordt rustiger. Eén toets, en de stilte is de rem.
- **Zelf afstemmen**, weggevouwen achter één knop, met uitleg in gewone taal.
- **Tweetalig** (Engels / Nederlands), met onthouden voorkeur.
- **Je eigen tekst** openen of naar binnen slepen — lokaal en privé, niet naar
  de server.
- **Leespositie onthouden** per boek, in de browser. Geen account, geen database.

## Draaien

```bash
pip install flask
python app.py
```

Open daarna `http://localhost:5001`.

Voor een server (bijv. PythonAnywhere of een eigen machine) draai je het achter
een WSGI-server zoals gunicorn in plaats van de ingebouwde ontwikkelserver.

## Boeken toevoegen

Zet `.txt`-bestanden (UTF-8) in de map `boeken/`. De bestandsnaam zonder `.txt`
wordt de titel. De meegeleverde bibliotheek bestaat uit publiek-domein werk
(zie `boeken/00_inhoud_en_rechten.md`).

Een recente *vertaling* heeft een eigen, jonger auteursrecht van de vertaler —
ook al is het origineel vrij. Wie de publieke collectie uitbreidt, kiest dus
vrije bronnen: [Project Gutenberg](https://www.gutenberg.org) voor Engels,
[DBNL](https://www.dbnl.org) voor Nederlands.

## Hoe het werkt

- `app.py` — Flask. Vindt de boeken, splitst de tekst in zinnen (met zorg voor
  afkortingen en losse koppen), serveert de pagina's. Padtraversal is geblokkeerd.
- `templates/index.html` — de boekenlijst en het openen van eigen tekst.
- `templates/lees.html` — de drie-lagen-leesruimte, de meegroeiende adem, de
  zelfsturende 'vanzelf'-stand en het afstem-paneel.

## Licentie

MIT — gebruik het vrij, bouw erop voort, deel het. De enige voorwaarde is dat
de naamsvermelding en licentietekst meereizen, zodat de oorsprong herkenbaar
blijft. Nieuwe ideeën zijn van harte welkom.
