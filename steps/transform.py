import pandas as pd
from datetime import datetime, timezone

def transform(raw_data):
    records = []
    for city, d in raw_data.items():
        try:
            records.append({
                "city":       city,
                "country":    d["sys"]["country"],
                "temperature":d["main"]["temp"],
                "humidity":   d["main"]["humidity"],
                "wind_speed": d["wind"]["speed"],
                "pressure":   d["main"]["pressure"],
                "description":d["weather"][0]["description"],
                "lat":        d["coord"]["lat"],
                "lon":        d["coord"]["lon"],
                "recorded_at": datetime.fromtimestamp(
                    d["dt"], tz=timezone.utc
                ).strftime("%Y-%m-%d %H:%M:%S")
            })
        except Exception as e:
            print(f"  Transform error {city}: {e}")

    df = pd.DataFrame(records)
    # Outlier removal
    df = df[(df["temperature"] >= -100) & (df["temperature"] <= 60)]
    print(f"  Clean rows: {len(df)}")
    return df