import os
from dotenv import load_dotenv

load_dotenv()

def is_running_on_render():
    return os.environ.get("RENDER", "").strip().lower() in ("true", "1", "yes")


def get_db_connection():

    if is_running_on_render():
      import psycopg
      onRender = True
      print("✅ Running inside Render environment")
      db_url = os.environ.get("DB_URL_INTERNAL")

    elif not is_running_on_render() and "DEV" == os.getenv("FLASK_APP"):
      import psycopg2
      onRender = False
      print("🧩 Local environment detected")
      db_url = os.getenv("EXTERNAL_DB_URL")

    else:
      import psycopg2
      onRender = False
      print("Github Test environment detected")
      db_url = os.getenv("EXTERNAL_DB_URL")

#    RENDER = os.getenv("RENDER", "")  os.getenv NOT supported on render
    if not db_url:
        print("❌ Missing PostgreSQL environment variable")
        return None

    try:
        if onRender:
          conn = psycopg.connect(db_url)
        else:
          conn = psycopg2.connect(db_url)

        print("✅ Connected to PostgreSQL database!!")
        return conn
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        return None



if __name__ == "__main__":
   get_db_connection()
