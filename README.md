# SOUMSOUM ERP - Gestion de la Production

Bienvenue dans le système ERP (Enterprise Resource Planning) de SOUMSOUM, conçu pour évoluer vers une organisation 4.0 en intégrant un ERP afin de planifier efficacement la production de nos télévisions de luxe.

## Aperçu du Projet

Notre entreprise a entrepris un ambitieux projet visant à moderniser nos opérations en mettant en œuvre un système ERP. Cette partie spécifique du projet, appelée Gestion de la Production, se concentre sur la surveillance et la mise à jour des ordres de fabrication.

## Fonctionnalités Principales

- **Affichage des Ordres de Fabrication:** Visualisez les détails essentiels tels que l'ID de l'ordre, la référence du produit, la date prévue, la quantité produite et le stock du produit.
  
- **Mise à Jour de la Quantité Produite:** Modifiez la quantité produite d'un ordre de fabrication en temps réel.

- **Visualisation des Produits:** Cliquez sur un ID d'ordre pour afficher l'image associée au produit.

- **Déconnexion Sécurisée:** Terminez votre session en toute sécurité à l'aide du bouton "Déconnexion".

## Autres Programmes

### Page de Connexion

- **Fonctionnalités :** Authentification sécurisée, connexion aux modules de production et logistique.

### Application Logistique

- **Fonctionnalités :** Affichage du stock des articles, mise à jour du stock, visualisation des images des articles.

### Application Production

- **Fonctionnalités :** Surveillance et mise à jour des ordres de fabrication, déconnexion sécurisée.

## Configuration Requise

Assurez-vous de configurer correctement les paramètres du serveur Odoo avant d'utiliser ce programme.

## Installation du Docker

1. Aller sur le site internet portainer.io http://localhost:9000

2. Aller dans l'onglet "stacks" puis cliquez sur "add stack"

3. Mettez un nom à votre stack puis cliquez sur web editor et écrivez ce script :

version: '2'
services :
  web:
    image: odoo:15
    depends_on:
      - mydb
    ports:
      - "8069:8069"
    environment:
     - HOST=mydb
     - USER=odoo
     - PASSWORD=myodoo
  mydb: 
     image: postgres:13
     environment:
       - POSTGRES_DB=postgres
       - POSTGRES_PASSWORD=myodoo
       - POSTGRES_USER=odoo
     

## Installation du Serveur ERP sur une machine virtuelle Linux :
Une fois le Docker créer vous pouvez récuperer un backup du serveur ERP.

1. Clonez ce référentiel sur un terminal linux si se n'est pas déjà fait:
Utilisez la commande cd pour vous déplacer dans le répertoire ou vous souhaitez l'installer.

```bash
cd Nom/De/Votre/Repertoire
```

Utilisez la commande git clone pour cloner le dépôt :

```bash
git clone https://github.com/Melvyn22350/SOUMSOUM

```

2. Ouvrez Le serveur ERP Odoo sur un navigateur avec ce lien : http://adresse_ip_de_votre_serveur_contenant_le_docker:8069  exemple : http://172.31.11.79:8069;

3. Une fois sur le site, sélectionner "Gestion des bases de données" puis "Restore Database";

4. Ecrivez le Master Password (MSIR5) cliquez sur parcourir et selectionner le fichier suivant : /home/user/Nom_De_Votre_Repertoire/SOUMSOUM_2024-01-17_10-50-05.zip, puis affecter un nom à votre Database, celui-ci doit être "SOUMSOUM";

5. Une fois le Backup réaliser, connecter vous à l'aide de vos identifiant.

## Installation du Serveur ERP sur une machine virtuelle Windows :

1. Installer le logiciel git bash depuis ce lien si se n'est pas déjà fait:

https://git-scm.com/download/win

sélectionner 64-bit Git for Windows Setup.

Une fois télécharger, pour l'installation appuyez uniquement sur Next et laisser les choix par défaut.

2. Ouvrir Git Bash afin de récupérer les fichiers nécessaires au fonctionnement de l'application :

 Utilisez la commande cd pour vous déplacer dans le répertoire ou vous souhaitez l'installer.

```bash
cd Nom/De/Votre/Repertoire
```

Utilisez la commande git clone pour cloner le dépôt :

```bash
git clone https://github.com/Melvyn22350/SOUMSOUM

```

2. Ouvrez Le serveur ERP Odoo sur un navigateur avec ce lien : http://adresse_ip_de_votre_serveur_contenant_le_docker:8069  exemple : http://172.31.11.79:8069;

3. Une fois sur le site, sélectionner "Gestion des bases de données" puis "Restore Database";

4. Ecrivez le Master Password (MSIR5) cliquez sur parcourir et selectionner le fichier suivant : C:\Users\usrafpi.AFPI_BRUZ.000\Nom_De_Votre_Repertoire\SOUMSOUM_2024-01-17_10-50-05.zip, puis affecter un nom à votre Database, celui-ci doit être "SOUMSOUM";

5. Une fois le Backup réaliser, connecter vous à l'aide de vos identifiant.

## Installation du Desktop sur linux

1. Clonez ce référentiel sur un terminal linux si se n'est pas déjà fait:
Utilisez la commande cd pour vous déplacer dans le répertoire ou vous souhaitez l'installer.

```bash
cd Nom/De/Votre/Repertoire
```

Utilisez la commande git clone pour cloner le dépôt :

```bash
git clone https://github.com/Melvyn22350/SOUMSOUM

```

2. Installez les bibliothèques nécessaires avec la commande suivante sur linux:

```bash
pip install pillow
```

3. Installer la version de python3.9 ou supérieur avec la commande sur linux :

```bash
sudo apt install python3.9
```

4. Mettez à jour python3.9 avec la commande sur linux :

```bash
sudo apt upgrade python3.9
```

5. Sur un terminal, rendre le fichier "Launcher_SOUMSOUM.sh" éxecutable depuis cette commande :

```bash
chmod +x /Chemin/De/Votre/Fichier/Launcher_SOUMSOUM.sh
```

6. Sur le bureau, faite un clique droit puis sélecionner "créer un nouveau" puis séléctionner "lien vers un emplacement (URL)...",
ensuite appeller le raccourci comme vous le souhaitez et mettez le lien de l'emplacement du fichier "Laucnher_SOUMSOUM.sh" dans le champ "Nouveau lien vers un emplacement (URL)"

7. Lancer le Launcher depuis le raccourci bureau et connectez vous à l'aide de vos identifiants du serveur ERP ainsi que votre mot de passe associé.

  
## Installation du Desktop pour Windows :

1. Installer le logiciel git bash depuis ce lien :

https://git-scm.com/download/win

sélectionner 64-bit Git for Windows Setup.

Une fois télécharger, pour l'installation appuyez uniquement sur Next et laisser les choix par défaut.

2. Ouvrir Git Bash afin de récupérer les fichiers nécessaires au fonctionnement de l'application :

 Utilisez la commande cd pour vous déplacer dans le répertoire ou vous souhaitez l'installer.

```bash
cd Nom/De/Votre/Repertoire
```

Utilisez la commande git clone pour cloner le dépôt :

```bash
git clone https://github.com/Melvyn22350/SOUMSOUM

```

3. Installer Python via l'invité de commande :

```bash
python3
```
Microsoft store s'ouvre puis cliquez sur obtenir.

4. Verifier si l'installation s'est bien passée en marquant "python --version" dans l'invité de commande

5. Installer Pillow et pip via l'invité de commande grace à cette commande :

```bash
python3 -m pip install --upgrade pip
```

```bash
python3 -m pip install --upgrade Pillow
```
6. Aller chercher l'emplacement du dossier que vous venez de cloner, rentrez dans le dossier SOUMSOUM puis effectuer un clique droit sur "Launcher_SOUMSOUM.sh" et séléctionner créer un raccourci et glisser le sur le bureau.

7. Lancer le Launcher depuis le raccourci bureau et connectez vous à l'aide de vos identifiants du serveur ERP ainsi que votre mot de passe associé.


## Guide de l'Utilisateur

Consultez le tableau d'affichage pour obtenir un aperçu complet des ordres de fabrication. Cliquez sur un ID d'ordre pour visualiser l'image du produit associé. Utilisez les champs dédiés pour mettre à jour la quantité produite.

## Contact

Pour toute question ou assistance, veuillez contacter notre équipe informatique à l'adresse tech_support@soumsoum.com.

Merci d'avoir choisi SOUMSOUM ERP pour votre gestion de la production. Nous sommes engagés à fournir des solutions innovantes pour stimuler la croissance de votre entreprise.
