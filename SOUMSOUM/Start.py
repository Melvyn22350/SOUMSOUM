import xmlrpc.client
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import subprocess
import base64
import sys
from io import BytesIO
import platform
import ctypes
from ctypes import wintypes
import os



# Obtenir le chemin complet du script
chemin_script = os.path.abspath(os.path.realpath(__file__))
print(chemin_script)

# Obtenir le chemin du répertoire parent
repertoire_parent = os.path.dirname(chemin_script)
print(repertoire_parent)

subprocess.Popen([sys.executable, f'{repertoire_parent}//Page_De_Connexion.py'])

def main():


    main()
