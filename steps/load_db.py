import psycopg2, os
from dotenv import load_dotenv
load_dotenv()

def setup_tables(cur):
    cur.execute("""
    CREATE TABLE IF NOT EXISTS dim_city (
        city_id   SERIAL PRIMARY KEY,
        name      VARCHAR(100) UNIQUE,
        country   VARCHAR(10),
        lat       FLOAT,
        lon       FLOAT
    );
    CREATE TABLE IF NOT EXISTS fact_weather (
        id          SERIAL PRIMARY KEY,
        city_id     INT REFERENCES dim_city(city_id),
        temperature FLOAT,
        humidity    INT,
        wind_speed  FLOAT,
        pressure    INT,
        description VARCHAR(100),
        recorded_at TIMESTAMP
    );
    """)

def load(df):
    conn = psycopg2.connect(os.getenv("DATABASE_URL"))
    cur = conn.cursor()
    setup_tables(cur)

    for _, row in df.iterrows():
        # City insert (agar already hai toh skip)
        cur.execute("""
            INSERT INTO dim_city (name, country, lat, lon)
            VALUES (%s,%s,%s,%s)
            ON CONFLICT (name) DO NOTHING
            RETURNING city_id
        """, (row.city, row.country, row.lat, row.lon))
        result = cur.fetchone()
        if not result:
            cur.execute("SELECT city_id FROM dim_city WHERE name=%s", (row.city,))
            result = cur.fetchone()
        city_id = result[0]

        cur.execute("""
            INSERT INTO fact_weather
            (city_id, temperature, humidity, wind_speed, pressure, description, recorded_at)
            VALUES (%s,%s,%s,%s,%s,%s,%s)
        """, (city_id, row.temperature, row.humidity,
              row.wind_speed, row.pressure, row.description, row.recorded_at))

    conn.commit()
    cur.close()
    conn.close()
    print(f"  DB mein {len(df)} rows insert ho gayi")