import requests
from bs4 import BeautifulSoup
import time  # For adding delay between requests

# Function to scrape website content
def scrape_website(session, url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    try:
        response = session.get(url, headers=headers, timeout=10)  # Request website with headers
        response.raise_for_status()  # Raise an exception for HTTP errors
        soup = BeautifulSoup(response.text, 'html.parser')  # Parse HTML content
        text_content = soup.get_text(separator=' ', strip=True)  # Extract text
        return text_content
    except requests.exceptions.SSLError as ssl_err:
        print(f"SSL error occurred when scraping {url}: {ssl_err}")
    except requests.exceptions.RequestException as req_err:
        print(f"Request error occurred when scraping {url}: {req_err}")
    except Exception as e:
        print(f"An unexpected error occurred when scraping {url}: {e}")
    return None  # Return None if there was an error

# Function to search for the query in the scraped data
def answer_query(query, scraped_data):
    results = []
    query = query.lower()  # Convert query to lowercase for case-insensitive comparison
    for url, content in scraped_data.items():
        if query in content.lower():  # Check if the query is in the content
            results.append((url, content))  # Add matching URL and content to results
    return results

# Example usage
urls = [
    "https://www.uchicago.edu/",
    "https://www.washington.edu/",
    "https://www.stanford.edu/",
    "https://und.edu/"
]

# Create a session and scrape data from the URLs
with requests.Session() as session:
    scraped_data = {}
    for url in urls:
        content = scrape_website(session, url)  # Scrape the website content
        if content:
            print(f"Successfully scraped content from {url}")
            scraped_data[url] = content
        else:
            print(f"Failed to scrape content from {url}")

        time.sleep(2)  # Add a small delay to avoid overwhelming the server

    # User query input
    user_query = input("Enter your query: ")
    
    # Find matching results
    results = answer_query(user_query, scraped_data)

    if results:
        print("\nResults found:")
        for url, content in results:
            # Display the first 200 characters to avoid overloading the user
            print(f"\nFrom {url}:\n{content[:200]}...")  # Display a truncated version of the content
    else:
        print("No results found for your query.")
