import requests
from bs4 import BeautifulSoup
import re
import os

def fetch_text(url):
    try:
        response = requests.get(url, verify=False)  # Disable SSL verification for simplicity
        response.raise_for_status()  # Raise an exception for 4XX or 5XX errors
        response.encoding = 'utf-8'  # Set correct encoding to prevent character issues
        return response.text
    except requests.exceptions.HTTPError as err:
        print(f"HTTP error occurred: {err} - URL: {url}")
        return None

def save_texts(texts, page_number, sub_page):
    if not os.path.exists('texts'):
        os.makedirs('texts')
    for idx, text in enumerate(texts):
        if len(text) > 5:  # Only save texts longer than 5 characters
            file_path = f"texts/page_{page_number}_{sub_page}_quote_{idx + 1}.txt"
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(text)

def crawl_sub_pages(base_url, main_page):
    sub_page = 1
    while True:
        url = f"{base_url}{main_page}" + (f"_{sub_page}" if sub_page > 1 else "") + ".html"
        print(f"Fetching {url}")
        html_content = fetch_text(url)
        if html_content is None:
            break  # Exit loop if page does not exist

        soup = BeautifulSoup(html_content, 'html.parser')
        content_div = soup.find('div', {'id': 'chaptercontent', 'class': 'Readarea ReadAjax_content'})
        if content_div:
            text_content = content_div.get_text(separator='\n')
            chinese_quotes = re.findall(r'“([^”]*)”', text_content)
            if chinese_quotes:
                save_texts(chinese_quotes, main_page, sub_page)
                sub_page += 1  # Move to the next sub-page only if quotes were found
            else:
                print(f"No quotes found on {url}, moving to next index.")
                break  # Exit if no quotes are found
        else:
            print("No text content found on page, moving to next index.")
            break  # Exit if no content div is found

def crawl_website(base_url, start_page, end_page):
    for page in range(start_page, end_page + 1):
        crawl_sub_pages(base_url, page)

# Adjust the base URL, start, and end pages as necessary
base_url = 'https://da6fa9c20a9a60a17ca0b.bq16.cc/book/37330/'
start_page = 1
end_page = 1821
crawl_website(base_url, start_page, end_page)
