from bs4 import BeautifulSoup
import requests
import os 

def amazon_monitor_urls(base_url): 

    headers = ({'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
                            'Accept-Language': 'en-US, en;q=0.5'})

    # Send HTTP request
    response = requests.get(base_url, headers=headers)

    # Check if the request was sucessful
    if response.status_code == 200: 
        soup = BeautifulSoup(response.text, 'html.parser')

        # Looking for top 10 links that have a product code
        product_dive = soup.find_all('div', {'data-asin': True}, limit=30)

        # Find all product containers
        urls = []

        for div in product_dive: 

            # Extract product URL
            a_tag = div.find('a', {'class': 'a-link-normal'})
            if a_tag and 'href' in a_tag.attrs:
                product_url = f"{a_tag['href']}"

                # Append the product url to list
                urls.append(product_url) 

        return urls
    else: 
        print(f"Error: Unable to fetch page. Status code {response.status_code}")
        return []
    
def save_urls(urls, filename): 

    # Check if file exists and remove it if it does 
    if os.path.exists(filename): 
        os.remove(filename)

    # Open file in write mode, which will create a new file
    with open(filename, 'w') as file: 
        for url in urls: 
            file.write(url + '\n')

base_url = 'https://www.amazon.com/s?k=monitor&i=computers&crid=2S5B46217DT6&sprefix=monito%2Ccomputers%2C101&ref=nb_sb_ss_pltr-xclick_1_6'
product_urls = amazon_monitor_urls(base_url)

if product_urls: 
    save_urls(product_urls, 'urls.txt')