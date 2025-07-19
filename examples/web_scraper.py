#!/usr/bin/env python3

import json
import time
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup


def scrape_website(url):
    """Simple web scraper example using requests and BeautifulSoup."""

    # Make request with headers to avoid being blocked
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()

        # Parse HTML content
        soup = BeautifulSoup(response.content, 'html.parser')

        # Extract basic information
        title = soup.find('title')
        title_text = title.get_text().strip() if title else "No title found"

        # Find all links
        links = []
        for link in soup.find_all('a', href=True):
            href = link['href']
            absolute_url = urljoin(url, href)
            link_text = link.get_text().strip()
            if link_text:
                links.append({
                    'url': absolute_url,
                    'text': link_text
                })

        # Extract meta description
        meta_desc = soup.find('meta', attrs={'name': 'description'})
        description = meta_desc.get('content', '') if meta_desc else ''

        return {
            'url': url,
            'title': title_text,
            'description': description,
            'links_count': len(links),
            'links': links[:10],  # First 10 links only
            'scraped_at': time.time()
        }

    except requests.RequestException as e:
        print(f"Error scraping {url}: {e}")
        return None

def main():
    """Main function to demonstrate the scraper."""

    # Example URLs to scrape
    urls = [
        "https://httpbin.org/html",
        "https://example.com",
    ]

    results = []

    for url in urls:
        print(f"Scraping: {url}")
        result = scrape_website(url)

        if result:
            results.append(result)
            print(f"✓ Title: {result['title']}")
            print(f"✓ Links found: {result['links_count']}")
        else:
            print("✗ Failed to scrape")

        # Be polite to servers
        time.sleep(1)

    # Save results to JSON file
    with open('scrape_results.json', 'w') as f:
        json.dump(results, f, indent=2)

    print("\nScraping complete! Results saved to scrape_results.json")
    print(f"Total sites scraped: {len(results)}")

if __name__ == "__main__":
    main()
