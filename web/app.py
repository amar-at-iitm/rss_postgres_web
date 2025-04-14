from flask import Flask, render_template,send_from_directory, request
import psycopg2
import os
from datetime import date


app = Flask(__name__)


DB_USER = os.getenv("DB_USER", "admin")
DB_PASS = os.getenv("DB_PASS", "admin")
DB_NAME = os.getenv("DB_NAME", "rss_feed")
DB_HOST = os.getenv("DB_HOST", "db")
DB_PORT = os.getenv("DB_PORT", "5432")

def get_articles(filter_date):
    try:
        conn = psycopg2.connect(
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASS,
            host=DB_HOST,
            port=DB_PORT
        )
        cursor = conn.cursor()

        query = """
        SELECT title, publication_timestamp, weblink, image, summary
        FROM news_articles
        WHERE publication_timestamp::date = %s;
        """
        cursor.execute(query, (filter_date,))
        articles = cursor.fetchall()
        cursor.close()
        conn.close()
        return articles
    except Exception as e:
        print(f"Error retrieving articles: {e}")
        return []

@app.route("/", methods=["GET"])
def index():
    filter_date = request.args.get("date", date.today().isoformat())
    articles = get_articles(filter_date)
    return render_template("index.html", articles=articles, filter_date=filter_date)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
