#!/bin/bash

# Récupérer le répertoire du script
script_directory="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Changer de répertoire vers le répertoire du script
cd "$script_directory/SOUMSOUM_Software/"

# Utiliser le chemin relatif pour lancer Start.py
python3 Start.py
