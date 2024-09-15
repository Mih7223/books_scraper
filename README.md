# books_scraper
1/## Installation des dépendances

Ce projet nécessite plusieurs bibliothèques Python pour fonctionner correctement. Vous pouvez installer toutes les dépendances à l'aide du fichier `requirements.txt`.

### Étapes pour installer les dépendances :

1. Assurez-vous d'avoir Python installé sur votre machine.
2. Créez un environnement virtuel (recommandé) :
   ```bash
   python -m venv venv
   
 3.Activez l'environnement virtuel :

Sous Windows :
 ```bash
venv\Scripts\activate

 4.Installez les dépendances en utilisant le fichier requirements.txt:
pip install -r requirements.txt

2/## Exécution du script

Une fois les dépendances installées, vous pouvez exécuter le script principal pour scraper le site Books to Scrape.

### Pour exécuter le script :
1. Ouvrez un terminal ou une invite de commandes.
2. Assurez-vous que l'environnement virtuel est activé (si utilisé).
3. Exécutez le script en utilisant la commande suivante :
   ```bash
   python scraper.py

3/###  **Description du fonctionnement du script**
Le script est divisé en plusieurs phases pour extraire les données du site Books to Scrape et les organiser.

### Phase 1 : Scraping d'un livre
Le script commence par scraper un seul livre donné en récupérant ses détails (titre, prix, disponibilité, etc.). Cela permet de vérifier le bon fonctionnement du scraping avant de passer à des catégories plus larges.

### Phase 2 : Scraping d'une catégorie entière
Ensuite, le script récupère tous les livres d'une catégorie spécifique. Pour chaque livre, les informations sont extraites et sauvegardées dans un fichier CSV propre à cette catégorie.

### Phase 3 : Scraping de toutes les catégories
Dans cette phase, le script scrape automatiquement toutes les catégories du site, en générant un fichier CSV distinct pour chaque catégorie. Cela permet de bien organiser les données extraites.

### Phase 4 : Téléchargement des images
Lors du scraping de chaque livre, le script télécharge également l'image associée et la sauvegarde dans un dossier dédié, nommé par catégorie. Cela permet d'associer facilement les images aux données des livres.

### Structure des fichiers générés :
- Les fichiers CSV sont stockés dans le répertoire racine du projet.
- Les images sont sauvegardées dans un dossier `images/`, organisé par sous-dossier correspondant aux catégories des livres.

4/##Voici la structure des fichiers et dossiers générés par le script :
/mon-projet-de-scraping/ │ ├── scraper.py # Code principal du scraping ├── requirements.txt # Liste des dépendances ├── README.md # Fichier d'explication ├── .gitignore # Exclusion des fichiers CSV et images ├── images/ # Dossier contenant les images des livres (généré automatiquement) ├── categorie1.csv # Fichier CSV généré pour la catégorie 1 ├── categorie2.csv # Fichier CSV généré pour la catégorie 2 └── ... # Autres fichiers CSV pour les différentes catégories
