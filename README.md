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

## Installation du Docker et du serveur ERP sur Linux (PC_1)

1. Installer la machine virtuelle PC_1 sur virtual Box, puis démarrer la.

2. Aller sur le site internet portainer.io http://localhost:9000

3. Connectez-vous en tant que admin. Cliquer sur local puis aller dans l'onglet "stacks" puis cliquez sur "add stack"

4. Mettez un nom à votre stack puis cliquez sur web editor et écrivez ce script :

```bash
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

```
Cliquez ensuite sur "deploy the stack" et vérifiez que les deux serveurs sont en running. Le temps de chargement peut parraitre long, attendez un peu le temps que l'image Odoo15 ce créer.

Une fois le Docker créer vous pouvez récuperer un backup du serveur ERP.

5. Collez les fichiers de la clé USB dans un emplacement de votre ordinateur que vous souhaitez.

6. Ouvrez Le serveur ERP Odoo sur un navigateur avec ce lien : http://localhost:8069 ou aller sur le docker que vous venez de créer et cliquer sur "8069" dans la colonne "published ports".

7. Une fois sur le site, sélectionner "Gestion des bases de données" puis "Restore Database";

8. Ecrivez le Master Password (MSIR5) cliquez sur parcourir et selectionner le fichier .ZIP que vous venez de telecharger qui est dans le repertoire NomDeVotreRepertoire/SOUMSOUM, puis affecter un nom à votre Database, celui-ci doit être "SOUMSOUM";
   
9. Modifier les paramètres réseau de votre machine virtuelle pour passer en accès par pont puis valider. Changer l'adresse IP de votre machine virtuelle contenant le docker pour celle ci : 172.31.10.158. Déconnectez vous du réseau wifi sur la machine virtuelle puis reconnectez vous pour qu'il prenne en compte les modification.

## Installation du Desktop sur linux (PC_2)

1. Installer la machine virtuelle PC_2 sur virtual Box, puis démarrer la.

2. Connectez vous au réseau afpicfai_wifi_guests.
  
3. Collez les fichiers de la clé USB dans un emplacement de votre ordinateur que vous souhaitez.
  
4. Installez les bibliothèques nécessaires avec la commande suivante sur linux en utilisant la commande cd pour accedez à l'emplacement du dossier:

```bash
pip install -r requierement_linux.txt
```

5. Sur un terminal, rendre le fichier "Launcher_SOUMSOUM.sh" éxecutable depuis cette commande :

```bash
chmod +x /Chemin/De/Votre/Fichier/Launcher_SOUMSOUM.sh
```

6. Lancer le Launcher présent dans le dossier SOUMSOUM_Software et connectez vous à l'aide de vos identifiants du serveur ERP ainsi que votre mot de passe associé. Les identifiants sont écris à la fin du Read_me.

  
## Installation du Desktop pour Windows (PC_3) :

1. Installer la machine virtuelle PC_3 sur virtual Box, puis démarrer la.

2. Connectez vous au réseau afpicfai_wifi_guests.
  
3. Collez les fichiers de la clé USB dans un emplacement de votre ordinateur que vous souhaitez.
  
4. Installer le logiciel git bash depuis ce lien :

https://git-scm.com/download/win

sélectionner 64-bit Git for Windows Setup.

Une fois télécharger, pour l'installation appuyez uniquement sur Next et laisser les choix par défaut.

5. Ouvrir Git Bash :

Installer Python via l'invité de commande GitBash :

```bash
python3
```
Microsoft store s'ouvre puis cliquez sur obtenir python3.

6. Installez les bibliothèques nécessaires avec la commande suivante sur gitbash:

```bash
pip install -r requierement_windows.txt
```

7. Lancer le Launcher présent dans le dossier SOUMSOUM_Software et connectez vous à l'aide de vos identifiants du serveur ERP ainsi que votre mot de passe associé. Les identifiants sont écris à la fin du Read_me.

## Guide de l'Utilisateur

Consultez le tableau d'affichage pour obtenir un aperçu complet des ordres de fabrication. Cliquez sur un ID d'ordre pour visualiser l'image du produit associé. Utilisez les champs dédiés pour mettre à jour la quantité produite.

Connectez-vous sur la page logistique avec l'identifiant : "log" et le mot de passe "123".

Connectez-vous sur la page production avec l'identifiant : "prod" et le mot de passe "123".

Connectez-vous sur le serveur Odoo en tant que commercial avec l'idendifiant : "commercial" et le mot de passe "123".

Connectez-vous sur le serveur Odoo en tant qu'administrateur avec l'idendifiant : "admin" et le mot de passe "123456789".

## Contact

Pour toute question ou assistance, veuillez contacter notre équipe informatique à l'adresse tech_support@soumsoum.com.

Merci d'avoir choisi SOUMSOUM ERP pour votre gestion de la production. Nous sommes engagés à fournir des solutions innovantes pour stimuler la croissance de votre entreprise.
