import requests
from bs4 import BeautifulSoup
import urllib.parse
import argparse
import os

# COLORS
R = "\033[31m"
G = "\033[32m"
Y = "\033[33m"
B = "\033[34m"
P = "\033[35m"
C = "\033[35m"
W = "\033[37m"
BGR = "\033[41m"
BGG = "\033[42m"
BGY = "\033[43m"
BGB = "\033[44m"
BGP = "\033[45m"
BGC = "\033[46m"
NE = "\033[0m"

def clear():
    os.system("clear")

def fetch_results(query, page_number=1):
    # Encode the query
    encoded_query = urllib.parse.quote_plus(query)

    # Google Search URL
    start = (page_number - 1) * 10  # Google results per page are 10
    url = f'https://www.google.com/search?q={encoded_query}&start={start}'

    # Set up headers to simulate a real browser request
    headers = {
        'User-Agent': 'Mozilla/5.0 (compatible; ScoutJet; +http://www.scoutjet.com/)'
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

def parse_pages(pages_str):
    pages = set()
    for part in pages_str.split(','):
        if '-' in part:
            start, end = map(int, part.split('-'))
            pages.update(range(start, end + 1))
        else:
            pages.add(int(part))
    return sorted(pages)

def main():
    # Set up command-line argument parsing
    parser = argparse.ArgumentParser(description='Scrape Google search results.')
    parser.add_argument('-q', '--query', type=str, required=True, help='The search query.')
    parser.add_argument('-p', '--pages', type=str, default='1', help='The pages to scrape (e.g., "1,2,3" or "1-3").')

    args = parser.parse_args()

    pages = parse_pages(args.pages)
    all_results = []

    # Clear the terminal screen
    clear()

    # Print the banner once
    print(f"   ______     ______     ______       ")
    print(f"  /\  ___\   /\  __ \   /\  ___\      ")
    print(f"  \ \ \__ \  \ \  __<   \ \___  \     ")
    print(f"   \ \_____\  \ \_\ \_\  \/\_____\    ")
    print(f"    \/_____/   \/_/\/_/   \/_____/    ")
    print()
    print(f"      {BGG}GOOGLE SEARCH SERPING TOOL{NE}     ")
    print()

    # Display fetching message for the range or list of pages
    if len(pages) == 1:
        print(f"Fetching results for query: {args.query} (Page {pages[0]})")
    else:
        pages_str = ','.join(map(str, pages))
        print(f"Fetching results for query: {args.query} (Pages {pages_str})")
    print('-----------------------------------------------------------------------------')

    # Fetch and display results for each page
    for page in pages:
        results = fetch_results(args.query, page)
        all_results.extend(results)

    display_results(all_results)

if __name__ == "__main__":
    main()
