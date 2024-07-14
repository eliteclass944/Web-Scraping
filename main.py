import csv
from bs4 import BeautifulSoup
from selenium import webdriver

def scrape_daraz(query, pages):
    driver = webdriver.Chrome()
    query = '+'.join(query.split())  # Transform query into Daraz search term
    products = []
    for page in range(1, pages+1):
        driver.get(f"https://www.daraz.pk/catalog/?page={page}&q={query}")
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        general_products_div = soup.find('div', {'data-qa-locator':'general-products'})
        if general_products_div:
            product_grid_item_class = general_products_div.find('div')['class'][0]
            for item_div in soup.findAll('div', class_=product_grid_item_class):
                for item_div in soup.findAll('div', class_=product_grid_item_class):
                    item_div = item_div.findAll('div')[3]
                    item_name = item_div.find('div', id='id-title').text
                    try:
                        item_ratings = item_div.findAll('span')[1].text if '/' in item_div.findAll('span')[
                            1].text else 'N/A'
                        items_sold = item_div.findAll('div')[1].findAll('div')[-1].text
                    except IndexError:
                        item_ratings = '-'
                        items_sold = '-'
                    if item_div.find('div', id='id-price').find('del').text == "":
                        item_original_price = "-"
                    else:
                        item_original_price = item_div.find('div', id='id-price').find('del').text.strip('Rs. ')
                    item_list_price = item_div.find('div', id='id-price').findAll('span')[1].text
                    products.append({
                        'item_name': item_name,
                        'item_ratings': item_ratings,
                        'items_sold': items_sold,
                        'item_list_price': item_list_price,
                        'item_original_price': item_original_price
                    })
        else:
            print("Could not find general products div")
    driver.quit()
    return products
def write_to_csv(products, query):
    file_name = f"daraz-products-{'-'.join(query.split('+'))}.csv"
    with open(file_name, "w", newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Search Term', 'Rating', 'Items Sold', 'Selling Price', 'List Price'])
        for product in products:
            writer.writerow([
                product['item_name'],
                product['item_ratings'],
                product['items_sold'],
                product['item_list_price'],
                product['item_original_price']
            ])

if __name__ == '__main__':
    query = "Rubiks Cube"  # Search term on Daraz
    pages = 2  # Number of pages
    products = scrape_daraz(query, pages)
    write_to_csv(products, 'output.csv')