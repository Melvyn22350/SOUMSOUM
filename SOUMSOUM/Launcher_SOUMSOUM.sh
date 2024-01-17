#!/bin/bash

# Récupérer le répertoire du script
script_directory="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Utiliser le chemin complet pour lancer Start.py
python3 "$script_directory/SOUMSOUM_Software/Start.py"
