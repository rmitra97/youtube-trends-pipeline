import os
from datetime import datetime
from googleapiclient.discovery import build
from pytrends.request import TrendReq
import pandas as pd

# -----------------------------
# 1. CONFIG / API KEYS
# -----------------------------
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")
REGION_CODE = os.getenv("YOUTUBE_REGION_CODE", "US")  # default US

OUTPUT_DIR = "data"  # folder within repo
os.makedirs(OUTPUT_DIR, exist_ok=True)

# -----------------------------
# 2. YOUTUBE TRENDING FETCH
# -----------------------------
def fetch_youtube_trending():
    if not YOUTUBE_API_KEY:
        raise ValueError("YOUTUBE_API_KEY not set in environment variables.")

    youtube = build("youtube", "v3", developerKey=YOUTUBE_API_KEY)

    request = youtube.videos().list(
        part="snippet,statistics,contentDetails",
        chart="mostPopular",
        maxResults=50,
        regionCode=REGION_CODE,
    )
    response = request.execute()

    df = pd.json_normalize(response["items"])

    # add a run_timestamp column
    df["run_timestamp"] = datetime.utcnow().isoformat()

    # save as date-partitioned file
    date_str = datetime.utcnow().strftime("%Y-%m-%d")
    output_path = os.path.join(OUTPUT_DIR, f"youtube_trending_{date_str}.csv")
    df.to_csv(output_path, index=False)
    print(f"Saved YouTube trending data to {output_path}")


# -----------------------------
# 3. GOOGLE TRENDS FETCH
# -----------------------------
def fetch_google_trends():
    pytrends = TrendReq(hl="en-US", tz=360)

    # you can later swap ["YouTube"] for topic-specific keywords
    pytrends.build_payload(["YouTube"], cat=0, timeframe="now 1-d", geo="US")
    data = pytrends.interest_over_time()

    # add run_timestamp
    data["run_timestamp"] = datetime.utcnow().isoformat()

    date_str = datetime.utcnow().strftime("%Y-%m-%d")
    output_path = os.path.join(OUTPUT_DIR, f"google_trends_{date_str}.csv")
    data.to_csv(output_path)
    print(f"Saved Google Trends data to {output_path}")


# -----------------------------
# 4. MAIN ENTRYPOINT
# -----------------------------
def main():
    print("Starting daily ETL run...")
    fetch_youtube_trending()
    fetch_google_trends()
    print("ETL completed successfully.")


if __name__ == "__main__":
    main()

