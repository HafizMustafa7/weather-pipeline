from steps.extract   import fetch_all
from steps.load_s3   import upload_raw
from steps.transform import transform
from steps.load_db   import load

print("=== Weather Pipeline Shuru ===")

print("[1] Data fetch ho raha hai...")
raw = fetch_all()

print("[2] S3 mein save ho raha hai...")
upload_raw(raw)

print("[3] Data transform ho raha hai...")
df = transform(raw)

print("[4] Database mein load ho raha hai...")
load(df)

print("=== Pipeline Complete! ===")