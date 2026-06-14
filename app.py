"""
Focuslezer — een leesapp die één zin centraal stelt.

De vorige zin doemt op als nabeeld, de volgende zin komt uit de mist.
De lezer houdt zelf het tempo. Niet duwen — het pad van de minste
weerstand naar de juiste plek laten lopen.
"""

import os
import re
import json
from flask import Flask, render_template, request, jsonify, abort

app = Flask(__name__)

BOEKEN_MAP = os.path.join(os.path.dirname(os.path.abspath(__file__)), "boeken")


# ---------------------------------------------------------------------------
# Boeken vinden
# ---------------------------------------------------------------------------
def lijst_boeken():
    """Alle .txt-bestanden in de boekenmap, alfabetisch, zonder extensie als titel."""
    if not os.path.isdir(BOEKEN_MAP):
        return []
    bestanden = [b for b in os.listdir(BOEKEN_MAP) if b.lower().endswith(".txt")]
    bestanden.sort(key=str.lower)
    return bestanden


def veilig_pad(bestandsnaam):
    """
    Geef een veilig, geverifieerd pad terug voor een gekozen boek.
    Voorkomt padtraversal: alleen bestanden die echt in de lijst staan.
    """
    if bestandsnaam not in lijst_boeken():
        return None
    return os.path.join(BOEKEN_MAP, bestandsnaam)


# ---------------------------------------------------------------------------
# Zin-segmentatie
# ---------------------------------------------------------------------------
# Veelvoorkomende afkortingen (NL + EN) die GEEN zinseinde zijn.
AFKORTINGEN = {
    "mr.", "mrs.","mss", "ms.", "dr.", "st.", "prof.", "sr.", "jr.", "vs.", "etc.",
    "nr.", "no.", "blz.", "pag.", "fig.", "c.a.", "b.v.", "bijv.", "enz.", "ev",
    "dhr.", "mevr.", "ing.", "drs.", "mr.", "ir.", "tel.", "a.u.b.", "z.o.z.",
    "i.v.m.", "o.a.", "d.w.z.", "n.a.v.", "t.o.v.", "p.s.",
}


def split_in_zinnen(tekst):
    """
    Splits tekst in zinnen op een manier die geschikt is voor lezen.

    Aanpak: normaliseer witruimte tot enkele spaties (regeleindes binnen
    een alinea horen niet bij de zinsgrens), splits dan op .!? gevolgd
    door witruimte en een hoofdletter/aanhalingsteken — maar niet na een
    bekende afkorting of een losse initiaal.
    """
    # Normaliseer: CRLF -> LF.
    tekst = tekst.replace("\r\n", "\n").replace("\r", "\n")

    # Korte losse regels (titels, koppen, opdrachten) zonder zinseinde-teken
    # zijn eigen eenheden — niet samenvoegen met de eerste echte zin.
    nieuwe_regels = []
    for regel in tekst.split("\n"):
        kaal = regel.strip()
        if kaal and len(kaal) <= 60 and not re.search(r"[.!?\u2026]$", kaal):
            nieuwe_regels.append("\u00b6 " + kaal + " \u00b6")
        else:
            nieuwe_regels.append(regel)
    tekst = "\n".join(nieuwe_regels)

    # Alineagrenzen markeren zodat we ze als zachte pauze kunnen houden.
    tekst = re.sub(r"\n[ \t]*\n+", " \u00b6 ", tekst)   # ¶ = alineagrens
    tekst = re.sub(r"\n+", " ", tekst)
    tekst = re.sub(r"[ \t]+", " ", tekst).strip()

    # Splits op zinseinde-leestekens gevolgd door spatie.
    # We houden het leesteken bij de zin (lookbehind-achtig via capture).
    ruwe_stukken = re.split(r"(?<=[.!?\u2026])\s+", tekst)

    zinnen = []
    buffer = ""
    for stuk in ruwe_stukken:
        stuk = stuk.strip()
        if not stuk:
            continue
        kandidaat = (buffer + " " + stuk).strip() if buffer else stuk

        # Eindigt het op een afkorting of losse initiaal? Dan doorlezen.
        laatste_woord = re.split(r"\s+", kandidaat)[-1]
        kern = laatste_woord.rstrip(".!?\u2026\"')]").lower()
        is_afkorting = kern in AFKORTINGEN
        is_initiaal = bool(re.match(r"^[a-z]$", kern))  # losse letter, bv. "J."

        if (is_afkorting or is_initiaal) and not kandidaat.endswith(("!", "?", "\u2026")):
            buffer = kandidaat
            continue

        buffer = ""
        # Alineamarkers omzetten naar een leesbare zin-scheiding.
        for deel in kandidaat.split(" \u00b6 "):
            deel = deel.replace("\u00b6", "").strip()
            if deel:
                zinnen.append(deel)

    if buffer.strip():
        zinnen.append(buffer.replace("\u00b6", "").strip())

    return zinnen


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------
@app.route("/")
def index():
    return render_template("index.html", boeken=lijst_boeken())


@app.route("/lees")
def lees():
    # Eigen tekst: de tekst zit in de browser (sessionStorage), niet op de
    # server. We tonen dan de leespagina zonder een boek in te lezen; de
    # pagina haalt zelf de tekst op en laat hem segmenteren via /segmenteer.
    if request.args.get("eigen") == "1":
        return render_template(
            "lees.html",
            boek="",
            titel="",
            zinnen_json="",
            aantal=0,
        )

    boek = request.args.get("boek", "")
    pad = veilig_pad(boek)
    if pad is None:
        abort(404)
    with open(pad, "r", encoding="utf-8", errors="replace") as f:
        tekst = f.read()
    zinnen = split_in_zinnen(tekst)
    titel = os.path.splitext(boek)[0]
    return render_template(
        "lees.html",
        boek=boek,
        titel=titel,
        zinnen_json=json.dumps(zinnen, ensure_ascii=False),
        aantal=len(zinnen),
    )


@app.route("/segmenteer", methods=["POST"])
def segmenteer():
    """Voor zelf-geüploade tekst: stuur tekst in, krijg zinnen terug."""
    data = request.get_json(silent=True) or {}
    tekst = data.get("tekst", "")
    return jsonify({"zinnen": split_in_zinnen(tekst)})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=False)
