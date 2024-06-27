import requests
from bs4 import BeautifulSoup
import re
import os

def fetch_text(url):
    response = requests.get(url, verify=False)  # Disable SSL verification
    response.encoding = 'utf-8'  # Set correct encoding to prevent Chinese garble
    return response.text

def save_texts(texts, page_number):
    if not os.path.exists('texts'):
        os.makedirs('texts')
    for idx, text in enumerate(texts):
        if len(text) > 5:  # Only save texts longer than 5 characters
            file_path = f"texts/page_{page_number}_quote_{idx + 1}.txt"
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(text)

def crawl_website(base_url, start_page, end_page):
    for page in range(start_page, end_page + 1):
        # Adjust the URL format if pages include sub-sections like 1, 1_2, etc.
        url = f"{base_url}{page}.html"
        print(f"Fetching {url}")
        html_content = fetch_text(url)
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Find the div with id 'chaptercontent' and class 'Readarea ReadAjax_content'
        content_div = soup.find('div', {'id': 'chaptercontent', 'class': 'Readarea ReadAjax_content'})
        if content_div:
            text_content = content_div.get_text(separator='\n')
            
            # Extract text inside Chinese quotes
            chinese_quotes = re.findall(r'“([^”]*)”', text_content)
            save_texts(chinese_quotes, page)
        else:
            print("No text found on page")

# Call the function
base_url = 'https://34c138647d418d8bb571cc.bq16.cc/book/11710/'  # Adjust base URL as necessary
start_page = 1  # Adjust start page number as necessary
end_page = 4482  # Adjust end page number as necessary
crawl_website(base_url, start_page, end_page)
