from __future__ import annotations

import argparse
import json
from pathlib import Path

import pandas as pd
import requests


DEFAULT_URL = (
    "https://huggingface.co/datasets/McAuley-Lab/Amazon-Reviews-2023/resolve/main/"
    "raw/review_categories/All_Beauty.jsonl"
)


def label_from_rating(rating: float) -> str | None:
    if rating <= 2:
        return "negative"
    if rating >= 4:
        return "positive"
    return None


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Sample human-written Amazon reviews for binary sentiment analysis."
    )
    parser.add_argument("--url", default=DEFAULT_URL)
    parser.add_argument("--per-label", type=int, default=50)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--output", default="data/human_reviews.csv")
    args = parser.parse_args()

    needed = args.per_label
    rows: list[dict[str, str]] = []
    counts = {"positive": 0, "negative": 0}

    response = requests.get(args.url, stream=True, timeout=60)
    response.raise_for_status()

    for raw_line in response.iter_lines(decode_unicode=True):
        if not raw_line:
            continue
        item = json.loads(raw_line)
        label = label_from_rating(float(item["rating"]))
        text = str(item.get("text") or "").strip()
        title = str(item.get("title") or "").strip()

        if label is None or counts[label] >= needed or not text:
            continue

        full_text = f"{title}. {text}" if title else text
        rows.append(
            {
                "text": full_text.replace("\n", " ").strip(),
                "label": label,
                "source": "human",
                "rating": item["rating"],
            }
        )
        counts[label] += 1

        if all(value >= needed for value in counts.values()):
            break

    if not all(value >= needed for value in counts.values()):
        raise RuntimeError(f"Not enough samples collected: {counts}")

    df = pd.DataFrame(rows).sample(frac=1, random_state=args.seed).reset_index(drop=True)
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output, index=False)
    print(f"Saved {len(df)} human reviews to {output}")
    print(df["label"].value_counts().to_string())


if __name__ == "__main__":
    main()
