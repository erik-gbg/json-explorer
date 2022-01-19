# JSON Explorer

JSON Explorer låter dig organisera en JSON-fil (vilken som helst) i grupperingar, som trädstruktur, för en bättre överblick. Att användas för analys av innehåll och datakvalitet. Användargränssnittet är byggt med PySimpleGUI. 

## Demo

Starta JSON Explorer utan argument: `python json_explorer.py`

För Windows-användare finns en körbar json_explorer.exe inklusive demo att ladda ner här: https://github.com/erik-gbg/json-explorer/releases/

Välj ett scenario från menyn, vänta på att JSON-filen laddats, sedan kan du bläddra runt och undersöka datat. [Det skapas ett menyval för varje konfigurationsfil (.cfg) i katalogen ./resources.]

Exemplen i demon körs på en JSON-fil med publicerade platsannonser (pb.json) som laddats ner med JobStream i januari 2022.

## Från kommandoraden med argument

    $ python json_explorer.py <konfigurationsfil>.cfg <JSON-fil>.json

## Konfiguration

Konfigurationsfilens syntax är enligt Python-modulen ConfigParser. Grupperingar, filter m.m. definieras med Python-uttryck som lambda-funktioner. Lambda-funktionerna identifierar fält i JSON-filen och processar dem.

## Installation

Installera Python-paket med: `pip install -r requirements.txt`

Krav: Python 3.8+  

