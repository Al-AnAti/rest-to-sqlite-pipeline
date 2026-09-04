import sqlite3
import requests
from pathlib import Path

script_dir = Path(__file__).resolve().parent
url = "https://jsonplaceholder.typicode.com/posts"

def fetch_data(url: str) -> list:
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        print(f"Total number or records retrieved: {len(data)}")
        print(f"First record title is: {data[0]['title']}")
        return data
    except requests.exceptions.HTTPError as err:
        if response.status_code == 404: print("URL NOT FOUND")
        elif response.status_code >= 500: print("SERVER ERROR")
        raise err
        

def insert_data(db_path: Path, data: list):
    with sqlite3.connect(db_path) as db:
        cursor = db.cursor()
        cursor.execute("""
            create table if not exists posts (
                userId integer,
                id integer primary key,
                title text,
                body text
            );      
        """)

        for post in data:
            cursor.execute(
                "insert or ignore into posts (userId, id, title, body) values (?, ?, ?, ?)",
                (post['userId'], post['id'], post['title'], post['body'])
            )


if __name__ == "__main__":
    db = script_dir / "api_data.db"
    data = fetch_data(url)
    insert_data(db, data)

