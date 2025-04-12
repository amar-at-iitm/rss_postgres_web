import os
import time
import feedparser
import requests
import psycopg2
import logging
from urllib.parse import urlparse


# Loading environment variables
RSS_FEED_URL = os.getenv("RSS_FEED_URL", "https://www.thehindu.com/news/national/?service=rss")
POLL_INTERVAL = int(os.getenv("POLL_INTERVAL", "600"))

DB_USER = os.getenv("DB_USER", "admin")
DB_PASS = os.getenv("DB_PASS", "admin")
DB_NAME = os.getenv("DB_NAME", "rss_feed")
DB_HOST = os.getenv("DB_HOST", "db")
DB_PORT = os.getenv("DB_PORT", "5432")

IMAGE_DIR = "./images"

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

# Ensure image directory exists
os.makedirs(IMAGE_DIR, exist_ok=True)

def download_image(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            filename = os.path.join(IMAGE_DIR, urlparse(url).path.split("/")[-1])
            with open(filename, "wb") as file:
                file.write(response.content)
            return filename
        else:
            logger.warning(f"Failed to download image from {url}")
            return None
    except Exception as e:
        logger.error(f"Error downloading image: {e}")
        return None

def insert_article(title, timestamp, link, image, tags, summary):
    try:
        conn = psycopg2.connect(
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASS,
            host=DB_HOST,
            port=DB_PORT
        )
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO news_articles (title, publication_timestamp, weblink, image, tags, summary)
            VALUES (%s, %s, %s, %s, %s, %s)
            ON CONFLICT (title) DO NOTHING;
        """, (title, timestamp, link, image, tags, summary))
        
        conn.commit()
        cursor.close()
        conn.close()
        logger.info(f"Inserted article: {title}")
    except Exception as e:
        logger.error(f"Database insertion failed: {e}")

def fetch_and_store():
    logger.info("Fetching news articles...")
    feed = feedparser.parse(RSS_FEED_URL)
    
    for entry in feed.entries:
        title = entry.get("title", "No Title")
        timestamp = entry.get("published", None)
        link = entry.get("link", "")
        summary = entry.get("summary", "")
        tags = [tag["term"] for tag in entry.get("tags", [])]
        image = None

        if "media_content" in entry:
            image_url = entry["media_content"][0].get("url", "")
            if image_url:
                image = download_image(image_url)
        
        if title and link:
            insert_article(title, timestamp, link, image, tags, summary)

def main():
    while True:
        fetch_and_store()
        logger.info(f"Sleeping for {POLL_INTERVAL} seconds...")
        time.sleep(POLL_INTERVAL)

if __name__ == "__main__":
    main()
