# rss-to-postgres-web: RSS feed to PostgreSQL to Web

This Project is a containerized web application aggregating news articles from an RSS feed, storing them in a PostgreSQL database, and displaying them on a web interface. The application consists of three Docker services:

1. **Database Service (PostgreSQL)** - Stores the news articles.
2. **RSS Scraper Service (Python)** - Fetches news from an RSS feed and stores it in the database.
3. **Web Application Service (Flask)** - Displays the news articles on a web interface.

## Features
- Fetches news articles periodically (Every 10 minutes) from an RSS feed.
- Stores news articles in a PostgreSQL database.
- Displays news articles with title, image, and summary.
- Clicking on the title or image opens the original news link in a new tab.
- Containerized setup using Docker Compose.

## Project Structure
```
assign_4/
├── app/
│   ├── images/                 # Stored news images
│   ├── dockerfile              
│   ├── main.py                 # Fetches & Stores RSS Feed 
│   ├── requirements.txt
├── web/
│   ├── app.py                   # Flask web application
│   ├── templates/index.html     # HTML templates
│   ├── requirements.txt                
│   ├── dockerfile
├── .dockerignore
├── dockerfile
├── init.sql
├── docker-compose.yml          # Docker Compose configuration
├── .env                        # Environment variables
└── README.md                   # Project documentation
```

## Usage
### Build and Run the Project
1. Clone the repository and navigate to the project directory.
2. Run the following command to build and start the containers:
   ```bash
   docker-compose up --build -d
   ```
3. Access the web application at [localhost:8080](http://localhost:8080).

### Stop the Containers
To stop the containers, run:
```bash
docker-compose down
```
### Environment Variables
The application uses a `.env` file to configure the database and RSS feed:
```
DB_USER=admin
DB_PASS=admin
DB_NAME=rss_feed
DB_HOST=db
DB_PORT=5432
POLL_INTERVAL=600
RSS_FEED_URL=https://www.thehindu.com/feeder/default.rss
# RSS_FEED_URL=https://timesofindia.indiatimes.com/rssfeeds/1221656.cms
# RSS_FEED_URL=https://feeds.feedburner.com/NDTV-LatestNews
# RSS_FEED_URL=https://www.indiatoday.in/rss/1206578
# RSS_FEED_URL=https://indianexpress.com/feed/
```
It is set to get RSS Feed from **thehindu.com**. To get feeds from other news websites, comment out that website and put others in the comments. The rest of the things will be taken care of.

### `main.py`
main.py script that performs the following functions:

1. Fetch RSS Feeds
   The default RSS feed URL is The Hindu National News.
2. Download Images:
   It uses the requests library to download images from news articles and saves images in the ./images directory.
3. Insert Articles into the Database:
   Uses psycopg2 to connect to a PostgreSQL database.
   Stores the news article details such as:
  - Title
  - Publication timestamp
  - Web link
  - Image file path
  - Tags
  - Summary<br>
  It uses an `INSERT INTO ... ON CONFLICT DO NOTHING` statement to avoid duplicate entries.

4. Continuous Data Fetching:
  Runs in a loop to fetch and store news articles periodically based on the configured poll interval (default 600 seconds).


### `app.py`
The `app.py` is a Flask-based web application that serves as the frontend for our news feed system. 
It runs as a Docker container alongside the database and news-fetching service, making it easy to manage using Docker Compose. 
It performs the following functions:

1. Data Retrieval: Connects to the PostgreSQL database to fetch news articles, including the title, publication timestamp, web link, image path, and summary.

2. Web Display: Renders a clean, responsive HTML page to display the news articles with the following structure:

- Title: Clickable and opens the original news article in a new tab.
- Summary: A brief description of the news content.
- Publication Timestamp: Displayed to indicate when the news was published.
3. Data Filtering: Supports date-based filtering to show articles from specific dates, with a default of showing today's news.
