import requests
from requests.auth import HTTPBasicAuth
from bs4 import BeautifulSoup

# Replace with your Confluence API endpoint and details
CONFLUENCE_BASE_URL = "https://your-domain.atlassian.net/wiki"
PAGE_ID = "123456789"  # The page ID for the Confluence page you want to scrape
USERNAME = "your-email@example.com"  # Your Atlassian email
API_TOKEN = "your-api-token"  # Your API token generated from Atlassian

# Atlassian API endpoint for Confluence page content (REST API v2)
CONFLUENCE_API_URL = f"{CONFLUENCE_BASE_URL}/rest/api/content/{PAGE_ID}?expand=body.storage"

# Step 1: Make a request to get the Confluence page content
response = requests.get(
    CONFLUENCE_API_URL,
    auth=HTTPBasicAuth(USERNAME, API_TOKEN)  # Use basic authentication with API token
)

# Step 2: Check if the request was successful
if response.status_code == 200:
    print("Successfully accessed Confluence page.")
else:
    print(f"Failed to access Confluence page. Status code: {response.status_code}")
    exit()

# Step 3: Parse the JSON response to extract the page content
page_data = response.json()
page_content_html = page_data['body']['storage']['value']  # The raw HTML content of the page

# Step 4: Use BeautifulSoup to parse and scrape the HTML content
soup = BeautifulSoup(page_content_html, 'html.parser')

# Extracting the text content (or any specific HTML element)
page_text_content = soup.get_text()

# Example: If you want to pass the content to another function
def process_confluence_content(content):
    # Placeholder for processing logic
    print("Processing Confluence content...")
    print(content)

# Step 5: Process the scraped content
process_confluence_content(page_text_content)