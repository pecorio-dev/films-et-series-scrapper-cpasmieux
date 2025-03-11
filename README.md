# FilmScraper

**FilmScraper** est un script Python qui permet de scraper le site [cpasmieux.ad/filmstreaming](https://www.cpasmieux.ad/filmstreaming/) pour extraire des informations détaillées sur les films en streaming. Le script récupère pour chaque film le titre, l'URL de l'image, les liens de streaming (provenant de services comme Uqload, Netu, Filmoon ou DoodStream) ainsi que des détails complémentaires tels que les genres, la date de sortie, les acteurs et la description.

## Fonctionnalités

- **Scraping des pages de films**  
  Parcourt les pages du site pour récupérer les films (20 films par page par défaut).

- **Extraction des données filmographiques**  
  Pour chaque film, le script extrait :
  - Le titre
  - L'URL de l'image (facultatif)
  - Les liens de streaming
  - Les détails du film (genres, date de sortie, acteurs, description)

- **Multithreading**  
  Utilisation de `ThreadPoolExecutor` pour traiter les films en parallèle et accélérer le processus de scraping.

- **Sauvegarde de la progression**  
  La progression est sauvegardée dans un fichier `progression.json` pour permettre de reprendre le scraping en cas d'interruption.

- **Sauvegarde des résultats**  
  Les informations extraites sont enregistrées dans un fichier JSON (`film_data_results.json`).

- **Utilisation d'un VPN**  
  En cas de blocage ou de limitation lors du scraping, il est recommandé d'utiliser un VPN. Le script vous invite à vous connecter et à relancer le traitement en appuyant sur Enter.

- **Référence à d'autres scripts**  
  Pour obtenir l'ensemble des outils d'automatisation (comme le clonage des liens Uqload), consultez le dépôt [uqload-auto-clone](https://github.com/votre-utilisateur/uqload-auto-clone) (remplacez l'URL par celle de votre dépôt).

## Prérequis

- **Python 3.x**
- **Modules Python :**
  - `requests`
  - `lxml`
  - `concurrent.futures` (inclus dans Python 3)
- **Accès Internet**  
  (Utilisation éventuelle d'un VPN pour contourner les restrictions ou blocages)

## Installation

1. **Cloner le dépôt :**

   ```bash
   git clone https://github.com/votre-utilisateur/filmscraper.git
   cd filmscraper
   ```

2. **Installer les dépendances :**

   ```bash
   pip install requests lxml
   ```

## Utilisation

Pour lancer le scraping, exécutez simplement le script :

```bash
python filmscraper.py
```

Le script parcourt les pages du site [cpasmieux.ad/filmstreaming](https://www.cpasmieux.ad/filmstreaming/), extrait les informations des films et sauvegarde les résultats dans le fichier `film_data_results.json`. La progression est enregistrée dans `progression.json`.

## Personnalisation

- **Nombre de pages à scraper :**  
  Vous pouvez modifier la variable `total_pages` dans la classe `FilmScraper` pour ajuster le nombre de pages à analyser.

- **Chemin du fichier résultat :**  
  Le fichier de résultats est défini par le paramètre `result_file` lors de l'initialisation de la classe. Vous pouvez le modifier selon vos besoins.

## Remarques

- **Utilisation d'un VPN :**  
  Si vous rencontrez des blocages ou limitations lors du scraping, connectez-vous à un VPN et relancez le script ou appuyez sur Enter lorsque le script vous le demande pour reprendre le traitement.

- **Autres scripts d'automatisation :**  
  Pour accéder à l'ensemble des outils (par exemple, pour le clonage automatique des liens Uqload), consultez le dépôt [uqload-auto-clone](https://github.com/votre-utilisateur/uqload-auto-clone).

## Contribution

Les contributions sont les bienvenues ! Si vous souhaitez améliorer ce projet ou corriger un bug, n'hésitez pas à ouvrir une issue ou à soumettre une pull request.

## Licence

Ce projet est sous licence [MIT](LICENSE).

