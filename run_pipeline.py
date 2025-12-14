import random
import pandas as pd
from src.pipeline import process_request

df = pd.read_csv("data/prompts.csv")

for text in df["text"]:
    route = random.choice(["qa", "summary", "analysis"])
    process_request(
        text,
        route=route,
        price_per_1k=0.002,
        cache_hit_rate=0.0
    )

print("✅ Pipeline run completed.")