import requests
from requests.exceptions import ConnectTimeout, RequestException
from bs4 import BeautifulSoup
import csv
import os
import time

# Ajouter les headers pour simuler une requête depuis un navigateur
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:130.0) Gecko/20100101 Firefox/130.0'
}

# Phase 1 : Scraping d'un seul livre
def scrape_single_product(product_url, folder='images', retries=3):
    """
    Scraper les détails d'un seul produit (livre).
    """
    for attempt in range(retries):
        try:
            response = requests.get(product_url, timeout=30, headers=HEADERS)
            response.encoding = "ISO-8859-1"  # Définir l'encodage
            response.raise_for_status()
            break
        except ConnectTimeout:
            print(f"Timeout pour {product_url}. Tentative {attempt + 1} de {retries}")
            time.sleep(5)
        except RequestException as e:
            print(f"Erreur: {e}")
            return None
    else:
        return None

    soup = BeautifulSoup(response.text, 'html.parser')

    # Extraire les données du livre
    product_page_url = product_url
    upc = soup.find('th', string='UPC').find_next('td').text
    title = soup.find('h1').text
    price_incl_tax = soup.find('th', string='Price (incl. tax)').find_next('td').text
    price_excl_tax = soup.find('th', string='Price (excl. tax)').find_next('td').text
    number_available = soup.find('th', string='Availability').find_next('td').text
    product_description = soup.find('meta', {'name': 'description'})['content'].strip()
    category = soup.find('ul', class_='breadcrumb').find_all('a')[-2].text
    review_rating = soup.find('p', class_='star-rating')['class'][1]
    image_url = "https://books.toscrape.com/" + soup.find('img')['src']

    # Phase 4 : Téléchargement de l'image du livre
    download_image(image_url, folder)

    return {
        'product_page_url': product_page_url,
        'universal_product_code': upc,
        'title': title,
        'price_including_tax': price_incl_tax,
        'price_excluding_tax': price_excl_tax,
        'number_available': number_available,
        'product_description': product_description,
        'category': category,
        'review_rating': review_rating,
        'image_url': image_url
    }

# Phase 2 : Scraping d'une catégorie entière
def get_category_books(category_url):
    """
    Récupérer toutes les URLs des livres d'une catégorie.
    """
    try:
        response = requests.get(category_url, headers=HEADERS)
        response.encoding = "ISO-8859-1"  # Définir l'encodage
        response.raise_for_status()
    except RequestException as e:
        print(f"Erreur lors de la connexion à {category_url}: {e}")
        return []

    soup = BeautifulSoup(response.text, 'html.parser')

    # Récupérer les URLs des livres
    book_urls = []
    books = soup.find_all('h3')
    for book in books:
        link = book.find('a')['href']
        book_url = 'https://books.toscrape.com/catalogue/' + link.replace('../../../', '')
        book_urls.append(book_url)

    # Gestion de la pagination
    next_page = soup.find('li', class_='next')
    while next_page:
        next_page_url = category_url.replace('index.html', next_page.find('a')['href'])
        try:
            response = requests.get(next_page_url, headers=HEADERS)
            response.encoding = "ISO-8859-1"
            response.raise_for_status()
        except RequestException as e:
            print(f"Erreur lors de la connexion à {next_page_url}: {e}")
            break

        soup = BeautifulSoup(response.text, 'html.parser')
        books = soup.find_all('h3')
        for book in books:
            link = book.find('a')['href']
            book_url = 'https://books.toscrape.com/catalogue/' + link.replace('../../../', '')
            book_urls.append(book_url)
        next_page = soup.find('li', class_='next')

    return book_urls

# Phase 2 : Fonction pour scraper une catégorie entière
def scrape_category(category_url, folder='images', filename='category_books.csv'):
    """
    Scraper tous les livres d'une catégorie et sauvegarder dans un CSV.
    """
    book_urls = get_category_books(category_url)

    # Créer un dossier pour la catégorie
    category_name = category_url.split('/')[-2]
    category_folder = os.path.join(folder, category_name)
    if not os.path.exists(category_folder):
        os.makedirs(category_folder)

    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)

        # Écrire l'en-tête
        writer.writerow(['Titre', 'Description', 'Détails'])

        # Scraper chaque livre dans la catégorie
        for url in book_urls:
            book_data = scrape_single_product(url, folder=category_folder)
            if book_data is None:
                continue

            writer.writerow([book_data['title'], book_data['product_description']])
            writer.writerow(['Détails du produit'])
            writer.writerow(['URL de la page du produit', book_data['product_page_url']])
            writer.writerow(['UPC', book_data['universal_product_code']])
            writer.writerow(['Prix TTC', book_data['price_including_tax']])
            writer.writerow(['Prix HT', book_data['price_excluding_tax']])
            writer.writerow(['Disponibilité', book_data['number_available']])
            writer.writerow(['Catégorie', book_data['category']])
            writer.writerow(['Évaluation', book_data['review_rating']])
            writer.writerow(['URL de l\'image', book_data['image_url']])
            writer.writerow([])  # Ligne vide pour séparation

    print(f"Les résultats de la catégorie ont été enregistrés dans '{filename}'.")

# Phase 3 : Scraping de toutes les catégories
def get_all_categories():
    """
    Récupérer toutes les catégories disponibles sur le site.
    """
    url = 'https://books.toscrape.com/index.html'
    try:
        response = requests.get(url, headers=HEADERS)
        response.encoding = "ISO-8859-1"  # Définir l'encodage
        response.raise_for_status()
    except RequestException as e:
        print(f"Erreur lors de la connexion au site: {e}")
        return {}

    soup = BeautifulSoup(response.text, 'html.parser')
    categories = soup.find('ul', class_='nav-list').find('ul').find_all('a')
    category_urls = {}
    for category in categories:
        category_name = category.text.strip()
        category_url = 'https://books.toscrape.com/' + category['href']
        category_urls[category_name] = category_url

    return category_urls

# Phase 3 : Scraper toutes les catégories et générer un CSV pour chaque catégorie
def scrape_all_categories():
    """
    Scraper toutes les catégories disponibles et générer un fichier CSV pour chaque.
    """
    categories = get_all_categories()
    for category_name, category_url in categories.items():
        filename = f'{category_name.replace(" ", "_").lower()}.csv'
        scrape_category(category_url, filename=filename)

# Phase 4 : Téléchargement des images
def download_image(image_url, folder='images'):
    """
    Télécharger une image de produit et la sauvegarder localement.
    """
    if not os.path.exists(folder):
        os.makedirs(folder)

    image_name = os.path.basename(image_url)
    image_path = os.path.join(folder, image_name)

    response = requests.get(image_url, headers=HEADERS)
    response.encoding = "ISO-8859-1"  # Définir l'encodage
    with open(image_path, 'wb') as f:
        f.write(response.content)
    print(f"Image téléchargée: {image_path}")

# Lancer les phases dans l'ordre croissant

# Phase 1 : Scraper un seul livre
print("Phase 1 : Scraping d'un seul livre")
product_url = 'https://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html'
scrape_single_product(product_url)

# Phase 2 : Scraper une catégorie entière
print("Phase 2 : Scraping d'une catégorie entière")
category_url = 'https://books.toscrape.com/catalogue/category/books/science_22/index.html'
scrape_category(category_url, filename='science_books.csv')

# Phase 3 : Scraper toutes les catégories
print("Phase 3 : Scraping de toutes les catégories")
scrape_all_categories()

print("Fin du projet.")
