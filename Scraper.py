import re
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from Book import Book

class Scraper:
    def __init__(self, url):
        self.url = url
        # Set up the WebDriver options to run headless Chrome for faster execution
        self.chrome_options = Options()
        self.chrome_options.add_argument("--headless")
        # Initialize the Chrome WebDriver using webdriver_manager  
        self.driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=self.chrome_options)

    def scrape_books(self):
        books = []
        try:
            # Make a request to the website
            response = requests.get(self.url)  
            response.raise_for_status() # Raise an exception if the response contains an HTTP error  
            # Parse the HTML content with BeautifulSoup and the 'lxml' parser
            soup = BeautifulSoup(response.text, 'lxml')  
            
            # Select book elements using CSS selector
            book_elements = soup.select('.product_pod')  
            for element in book_elements:
                title = element.h3.a['title'] # Extract the book title
                category = self.get_category(title) # Get the category using Selenium
                rating = self.get_rating(element) # Get the rating
                price = self.get_price(element) # Get the price
                stock = self.get_stock(title) # Get the stock using Selenium
                # Create a Book object and add it to the list
                book = Book(title, category, rating, price, stock)
                books.append(book)
        except requests.exceptions.RequestException as e:
            print(f"Error fetching data from {self.url}: {e}")
        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            self.driver.quit() # Ensure WebDriver is closed
        return books
    
    def get_category(self, title):
        self.driver.get(self.url)
        try:
            # Find book elements by CSS selector
            book_elements = self.driver.find_elements(By.CSS_SELECTOR, "article.product_pod")
            for product in book_elements:
                title_element = product.find_element(By.CSS_SELECTOR, "h3 > a")
                if title_element.get_attribute("title") == title:
                    title_element.click() # Click on the book element
                    # Extract category information from the breadcrumb
                    category_element = self.driver.find_element(By.CSS_SELECTOR, ".breadcrumb li:nth-child(3) a")
                    category_text = category_element.text
                    self.driver.back() # Navigate back to the main page
                    return category_text
        except (ValueError, AttributeError, TypeError):
            print(f"Error fetching category for {title}")
            return "Unknown"

    def get_rating(self, element):
        RATINGLOCATOR = "p.star-rating"
        # Extract the rating class and map it to an integer value
        rating = element.select_one(RATINGLOCATOR).attrs['class'][1].lower()
        ratings = {'one': 1, 'two': 2, 'three': 3, 'four': 4, 'five': 5}
        return ratings.get(rating, 0) # Default to 0 if rating not found

    def get_price(self, element):
        # Extract the price text and remove non-numeric characters (except the decimal point)
        price_text = element.find('p', class_='price_color').text
        price = re.sub(r'[^\d.]', '', price_text)
        try:
            return float(price)
        except ValueError:
            print(f"Error converting price: {price_text}")
            return 0.0
    
    def get_stock(self, title):
        #Use Selenium to get the stock quantity for a book given its title.
        self.driver.get(self.url) 
        try:
            # Find book elements by CSS selector
            book_elements = self.driver.find_elements(By.CSS_SELECTOR, ".product_pod")
            for product in book_elements:
                title_element = product.find_element(By.CSS_SELECTOR, "h3 > a")
                if title_element.get_attribute("title") == title:
                    title_element.click() # Click on the book element
                    # Extract stock information
                    stock_text = self.driver.find_element(By.CLASS_NAME, 'instock.availability').text
                    qt_stock = int(re.search(r'In stock \((\d+) available\)', stock_text).group(1))
                    self.driver.back() # Navigate back to the main page
                    return qt_stock
        except (ValueError, AttributeError, TypeError):
            print(f"Error fetching stock for {title}")
            return 0



if __name__ == "__main__":
    url = "http://books.toscrape.com/"
    scrapper = Scraper(url)
    books = scrapper.scrape_books()
    for book in books:
        print(book.title, book.category, book.rating, book.price, book.stock)

