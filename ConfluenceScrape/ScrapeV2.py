import requests
from requests.auth import HTTPBasicAuth
from bs4 import BeautifulSoup

# Replace with your Confluence API endpoint and details
CONFLUENCE_BASE_URL = "https://your-domain.atlassian.net/wiki"
PAGE_ID = "123456789"  # The page ID for the Confluence page you want to scrape
USERNAME = "your-email@example.com"  # Your Atlassian email
API_TOKEN = "your-api-token"  # Your API token generated from Atlassian

# Atlassian API endpoint for Confluence page content (REST API v2)
CONFLUENCE_API_URL = f"{CONFLUENCE_BASE_URL}/rest/api/content/{PAGE_ID}?expand=body.view"

# Step 1: Make a request to get the Confluence page content (rendered view)
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

# Step 3: Parse the JSON response to extract the rendered page content
page_data = response.json()
page_content_html = page_data['body']['view']['value']  # The rendered HTML content of the page

# Step 4: Use BeautifulSoup to parse the HTML content
soup = BeautifulSoup(page_content_html, 'html.parser')

# Step 5: Extract text while preserving basic newlines for paragraphs and block elements
def get_text_with_newlines(soup):
    # Replace <br> with a newline
    for br in soup.find_all("br"):
        br.replace_with("\n")

    # Extract plain text, adding newlines around block-level elements
    block_elements = ['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'li', 'tr', 'td', 'div']

    for tag in soup.find_all(block_elements):
        tag.insert_before("\n")
        tag.insert_after("\n")

    return soup.get_text()

# Extract text with basic newlines preserved
plain_text_with_newlines = get_text_with_newlines(soup)

# Step 6: Pass the plain text content to another function or print it
def process_confluence_content(content):
    # Placeholder for processing logic
    print("Processing plain text Confluence content with newlines:")
    print(content)

# Step 7: Process the extracted plain text
process_confluence_content(plain_text_with_newlines)