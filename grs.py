import requests
from bs4 import BeautifulSoup
import urllib.parse
import argparse
import os

os.system("clear")

def fetch_results(query, page_number=1):
    # Encode the query
    encoded_query = urllib.parse.quote_plus(query)

    # Google Search URL
    start = (page_number - 1) * 10  # Google results per page are 10
    url = f'https://www.google.com/search?q={encoded_query}&start={start}'

    # Set up headers to simulate a real browser request
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    # Send the GET request
    response = requests.get(url, headers=headers)

    # Check if the response was successful
    if response.status_code != 200:
        print("Failed to retrieve data.")
        return []

    # Parse the content with BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find the relevant parts of the Google SERP (e.g., links to results)
    results = soup.find_all('h3')

    # Extract and return titles and URLs
    extracted_results = []
    for result in results:
        a_tag = result.find_parent('a')
        if a_tag:
            title = result.get_text()
            link = a_tag['href']
            extracted_results.append((title, link))

    return extracted_results

def display_results(results):
    # Display extracted results
    if not results:
        print("No results found.")
        return

    for idx, (title, link) in enumerate(results, 1):
        print(f"\033[1;34m{idx}. Title: \033]8;;{link}\a{title}\033]8;;\a\033[0m")  # Clickable link with blue title
        print(f"   Link: {link}")
        print('-----------------------------------------------------------------------------')

def main():
    # Set up command-line argument parsing
    parser = argparse.ArgumentParser(description='Scrape Google search results.')
    parser.add_argument('-q', '--query', type=str, required=True, help='The search query.')
    parser.add_argument('-p', '--page', type=int, default=1, help='The page number to scrape (default: 1).')

    args = parser.parse_args()

    # Fetch results for the specified query and page
    print("       ______  _______     ______ 1.0 ")
    print("     .' ___  ||_   __ \  .' ____ \    ")
    print("    / .'   \_|  | |__) | | (___ \_|   ")
    print("    | |   ____  |  __ /   _.____`.    ")
    print("    \ `.___]  |_| |  \ \_| \____) |   ")
    print("     `._____.'|____| |___|\______.'   ")
    print("       GOOGLE SEARCH SERPING TOOL     ")
    print()
    print(f"Fetching results for query: {args.query} (Page {args.page})")
    print()
    print('-----------------------------------------------------------------------------')
    results = fetch_results(args.query, args.page)
    display_results(results)

if __name__ == "__main__":
    main()
