import os
import sys
import subprocess
import time

def restart_program():
    print("Attente de 1 seconde avant de redémarrer...")
    # Attends 1 seconde avant de redémarrer
    time.sleep(1)

    try:
        # Obtient le chemin absolu du fichier actuel
        current_file_path = os.path.abspath(__file__)

        print("Redémarrage du programme...")
        # Relance le programme en utilisant subprocess.run
        subprocess.run([sys.executable, current_file_path])
    except Exception as e:
        print(f"Erreur lors du redémarrage du programme : {e}")

if __name__ == "__main__":
    # Ajoutons une protection pour éviter la répétition indésirable
    restart_count = int(os.environ.get("RESTART_COUNT", 0))
    
    if restart_count < 5:  # ajustez le nombre maximal de redémarrages si nécessaire
        print(f"Redémarrage n°{restart_count + 1}")
        os.environ["RESTART_COUNT"] = str(restart_count + 1)
        restart_program()
    else:
        print("Nombre maximal de redémarrages atteint. Arrêt du programme.")
