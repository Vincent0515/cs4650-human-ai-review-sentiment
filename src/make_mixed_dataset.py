from __future__ import annotations

from pathlib import Path

import pandas as pd


def main() -> None:
    human = pd.read_csv("data/human_reviews.csv")
    ai = pd.read_csv("data/ai_reviews.csv")
    mixed = pd.concat([human, ai], ignore_index=True)
    mixed = mixed.sample(frac=1, random_state=42).reset_index(drop=True)

    output = Path("data/mixed_reviews.csv")
    output.parent.mkdir(parents=True, exist_ok=True)
    mixed.to_csv(output, index=False)
    print(f"Saved {len(mixed)} mixed reviews to {output}")
    print(mixed.groupby(["source", "label"]).size().to_string())


if __name__ == "__main__":
    main()
