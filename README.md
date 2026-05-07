# Sentinel area tiler
In deze _repository_ vind je code om satellietbeeld van [Sentinel](https://browser.dataspace.copernicus.eu/) binnen te halen via hun API, en dat op te knippen in stukjes die geschikt zijn om (bijvoorbeeld) een AI-model te trainen. 

Deze code is geschreven in het kader van een AI-cursus voor journalisten van het [Fonds Bijzondere Journalistieke Projecten](https://fondsbjp.nl/).

## Benodigdheden 
De code is geschreven in Python, gebruik bij voorkeur een moderne versie. We gebruiken hier relatief veel lirbaries, die vind je in `requirements.txt`. Installeer ze bij voorkeur in een _virtual environment_ als `venv` of `conda`. 

Verder heb je om de beelden binnen te halen een _API key/login_ nodig van de Sentinel Hub. [Zie hier hoe je daaraan komt](https://dataspace.copernicus.eu/analyse/apis/sentinel-hub). 

## De scripts 
Met `fetch_area.py` kun je een gebied binnenhalen via de Sentinel Hub API. Let op de volgende variabelen:
- `area_name` bepaalt hoe je bestanden worden opgeslagen etc. 
- `area_bounding_box` is de _bounding box_ van het gebied dat je binnen wilt halen. Gebruik hiervoor het format `[west, zuid, oost, noord]` in EPSG:4326-formaat.
- `tile_size_in_meters` is het formaat van een enkele satelliettegel _in meters_, voor zowel de breedte als de hoogte. Let op: maak dit getal niet te klein of je krijgt een enorm aantal afbeeldingen (1 miljoen is de max hier). 
- `tile_overlap_in_meters` is de overlap van de tegels in meters. Dit wil zeggen dat de code elke tegel zo verschuift dat de stukjes met deze lengte aan de rand bij _beide tegels_ worden meegenomen. Wil je bijvoorbeeld schepen analyseren, dan heb je hiermee minder kans op een "afgeknipt" schip. 

### Sentinel-gegevens
Plaats je Sentinel-login in de `.env` file, die je kunt aanmaken aan de hand van het voorbeeldbestand `.env.example` (commit het origineel nooit!). Hier kun je ook de Sentinel-login inzetten.
