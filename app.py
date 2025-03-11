import os
import json
import requests
from lxml import html
from concurrent.futures import ThreadPoolExecutor, as_completed
import time

class FilmScraper:
    def __init__(self, result_file='film_data_results.json'):
        self.base_url = "https://www.cpasmieux.ad/filmstreaming/"
        self.total_pages = 961            # Nombre total de pages à scraper
        self.films_per_page = 20          # Films par page (pour le calcul de progression)
        self.total_films_scraped = 0      # Compteur des films récupérés
        self.current_page = 1             # Commencer à la première page
        self.result_file = result_file    # Fichier pour stocker les résultats
        self.is_scraping = False          # État du scraping
        self.progress = {'value': 0}      # Valeur de la barre de progression
        self.films = []                   # Liste de films à sauvegarder

    def update_status(self, status):
        print(status)

    def update_counter(self):
        print(f"Films scraped: {self.total_films_scraped}")

    def save_progress(self):
        with open('progression.json', 'w', encoding='utf-8') as f:
            json.dump({'last_page': self.current_page, 'total_scraped': self.total_films_scraped}, f, indent=4)

    def save_results(self):
        """Sauvegarde l'ensemble des films dans un fichier JSON valide."""
        with open(self.result_file, 'w', encoding='utf-8') as f:
            json.dump(self.films, f, indent=4, ensure_ascii=False)

    def scrape_films(self):
        self.is_scraping = True

        for page_num in range(self.current_page, self.total_pages + 1):
            page_url = f"{self.base_url}{page_num}/"
            self.update_status(f"Scraping page: {page_url}")

            films_on_page = self.get_film_info(page_url)
            self.films.extend(films_on_page)
            self.total_films_scraped += len(films_on_page)
            self.current_page = page_num + 1
            self.save_progress()

            # Mise à jour de la barre de progression
            self.progress['value'] = (self.total_films_scraped / (self.films_per_page * self.total_pages)) * 100
            self.update_counter()

            if self.total_films_scraped >= self.films_per_page * self.total_pages:
                break

        self.save_results()
        self.update_status("Scraping terminé")
        self.is_scraping = False

    def get_film_info(self, page_url):
        films_data = []
        try:
            response = requests.get(page_url, timeout=10)
            if response.status_code != 200:
                self.update_status(f"Erreur lors de la récupération de la page: {page_url}")
                return []
            tree = html.fromstring(response.content)
            movie_items = tree.xpath('//div[contains(@class, "movie-item2")]')
            if not movie_items:
                self.update_status(f"Aucun film trouvé sur la page {page_url}.")
                return []

            # Traiter chaque film en parallèle avec 200 threads
            with ThreadPoolExecutor(max_workers=200) as executor:
                futures = {executor.submit(self.process_movie_item, item): item for item in movie_items}
                for future in as_completed(futures):
                    film = future.result()
                    if film:
                        films_data.append(film)
            return films_data
        except Exception as e:
            self.update_status(f"Erreur lors du scraping de la page {page_url}: {e}")
            return []

    def process_movie_item(self, movie_item):
        try:
            # Extraction du titre (attribut alt de l'image)
            title_list = movie_item.xpath('.//div[@class="mi2-img"]/img/@alt')
            film_title = title_list[0].strip() if title_list else "Titre inconnu"

            # Extraction de l'URL de l'image
            img_src = movie_item.xpath('.//div[@class="mi2-img"]/img/@src')
            film_image_url = "https://www.cpasmieux.ad" + img_src[0].strip() if img_src else ""

            # Extraction du lien vers la page du film
            link_list = movie_item.xpath('.//a[@class="mi2-in-link"]/@href')
            film_link = "https://www.cpasmieux.ad" + link_list[0].strip() if link_list else ""

            # Récupération des liens de streaming et des détails
            film_stream_links = self.get_stream_links(film_link)
            film_details = self.get_film_details(film_link)

            film_data = {
                "title": film_title,
                "image_url": film_image_url,
                "genres": film_details.get('genres', []),
                "release_date": film_details.get('release_date', "Date non disponible"),
                "actors": film_details.get('actors', []),
                "description": film_details.get('description', "Description non disponible"),
                "links": film_stream_links
            }
            self.update_status(f"Film traité : {film_title}")
            self.update_counter()
            return film_data
        except Exception as e:
            self.update_status(f"Erreur lors du traitement d'un film: {e}")
            return None

    def get_stream_links(self, film_url):
        stream_links = []
        try:
            response = requests.get(film_url, timeout=10)
            if response.status_code != 200:
                self.update_status(f"Erreur lors de la récupération de la page du film: {film_url}")
                return []
            tree = html.fromstring(response.content)
            player_list = tree.xpath('//div[contains(@class, "lien") and contains(@class, "fx-row")]')
            for player in player_list:
                service_name_list = player.xpath('.//span[contains(@class, "serv")]/text()')
                service_name = service_name_list[0].strip() if service_name_list else ""
                data_url_list = player.xpath('./@data-url')
                data_url = data_url_list[0].strip() if data_url_list else ""
                if service_name in ['Uqload', 'Netu', 'Filmoon', 'DoodStream']:
                    stream_links.append({'service': service_name, 'url': data_url})
        except Exception as e:
            self.update_status(f"Erreur lors de l'extraction des liens de streaming pour {film_url}: {e}")
        return stream_links

    def get_film_details(self, film_url):
        film_details = {
            'genres': [],
            'release_date': "Date non disponible",
            'actors': [],
            'description': "Description non disponible"
        }
        try:
            response = requests.get(film_url, timeout=10)
            if response.status_code != 200:
                self.update_status(f"Erreur lors de la récupération des détails du film: {film_url}")
                return film_details
            tree = html.fromstring(response.content)
            details_list = tree.xpath('//li[contains(@class, "details-f")]')
            for detail in details_list:
                detail_text = detail.text_content()
                if "Genre:" in detail_text:
                    genres = detail.xpath('.//a/text()')
                    film_details['genres'] = [genre.strip() for genre in genres if genre.strip()]
                elif "Date de sortie:" in detail_text:
                    release_date_list = detail.xpath('.//span/text()')
                    film_details['release_date'] = release_date_list[0].strip() if release_date_list else "Date non disponible"
                elif "Acteurs:" in detail_text:
                    actors = detail.xpath('.//a/text()')
                    film_details['actors'] = [actor.strip() for actor in actors if actor.strip()]
            desc_parts = tree.xpath('//p[@class="full-desc"]/following-sibling::p[1]//text()')
            if desc_parts:
                film_details['description'] = " ".join([part.strip() for part in desc_parts if part.strip()])
        except Exception as e:
            self.update_status(f"Erreur lors de l'extraction des détails pour {film_url}: {e}")
        return film_details

if __name__ == "__main__":
    scraper = FilmScraper()
    scraper.scrape_films()
