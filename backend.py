import requests
from bs4 import BeautifulSoup
from PIL import Image
from io import BytesIO

# This function will handle downloading images
from PIL import Image
from io import BytesIO
import requests


def parse_query(query):
    if '+' in query:
        keywords = [word.strip().lower() for word in query.split('+')]
        mode = 'OR'
    else:
        keywords = [word.strip().lower() for word in query.split()]
        mode = 'AND'
    return keywords, mode

def download_image(url):
    try:
        # Fix protocol-relative URLs
        if url and url.startswith("//"):
            url = "https:" + url
        elif url and not url.startswith("http"):
            url = "https://" + url.lstrip("/")
        response = requests.get(url, stream=True, timeout=10)
        response.raise_for_status()  # Raise an error for HTTP problems
        return Image.open(BytesIO(response.content))  # Return the PIL Image object
    except Exception as e:
        print(f"Error downloading image: {e}")
        return None

def scrape_images(query):
    print(f"Scraping for: {query}")

    # Parse the query into keywords and mode (AND/OR)
    keywords, mode = parse_query(query)

    # List of websites to scrape
    websites = [
        "https://www.123rf.com/",
        "https://500px.com/",
        "https://www.flickr.com/",
        "https://www.freepik.com/",
        "https://www.lifeofpix.com/",
        "https://www.rawpixel.com/",
        "https://stocksnap.io/",
        "https://burst.shopify.com/",
        "https://www.freeimages.com/",
        "https://commons.wikimedia.org/",
        "https://www.pexels.com/",
        "https://unsplash.com/",
        "https://pixabay.com/",
        "https://picjumbo.com/",
        "https://dreamstime.com/",
    ]

    # Placeholder for storing results
    images = []

    for site in websites:
        try:
            response = requests.get(site)
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')

                # Find all <img> tags
                for img_tag in soup.find_all('img'):
                    # Extract src and alt attributes
                    src = img_tag.get("src")
                    alt = img_tag.get("alt", "").lower()  # Convert to lowercase for matching
                    parent = img_tag.find_parent()
                    nearby_text = parent.get_text(strip=True).lower() if parent else ""  # Lowercase nearby text

                    # Combine alt and nearby text
                    combined_text = f"{alt} {nearby_text}"

                    # Filter based on mode
                    if mode == 'AND':
                        # Match all keywords exactly
                        if all(keyword in combined_text.split() for keyword in keywords):
                            images.append({
                                "src": src,
                                "alt": alt,
                                "nearby_text": nearby_text,
                                "source": site
                            })
                    elif mode == 'OR':
                        # Match any keyword exactly
                        if any(keyword in combined_text.split() for keyword in keywords):
                            images.append({
                                "src": src,
                                "alt": alt,
                                "nearby_text": nearby_text,
                                "source": site
                            })
        except Exception as e:
            print(f"Error scraping {site}: {e}")
    
    return images

""""
# Test the scraping
query = "forest"
images = scrape_images(query)

# Display results
for image in images:
    print(f"Image URL: {image['src']}")
    print(f"Alt Text: {image['alt']}")
    print(f"Nearby Text: {image['nearby_text']}")
    print(f"Source: {image['source']}")
    print("-" * 50)"""