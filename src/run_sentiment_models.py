from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd
from sklearn.metrics import accuracy_score, precision_recall_fscore_support
from tqdm import tqdm
from transformers import pipeline


MODELS = {
    "distilbert_sst2": "distilbert-base-uncased-finetuned-sst-2-english",
    "twitter_roberta": "cardiffnlp/twitter-roberta-base-sentiment-latest",
}


DATASETS = {
    "human": "data/human_reviews.csv",
    "ai": "data/ai_reviews.csv",
    "mixed": "data/mixed_reviews.csv",
}


def normalize_prediction(label: str) -> str:
    value = label.strip().lower()
    if value in {"positive", "pos", "label_2"}:
        return "positive"
    if value in {"negative", "neg", "label_0"}:
        return "negative"
    if value in {"neutral", "label_1"}:
        return "neutral"
    raise ValueError(f"Unknown model label: {label}")


def predict_dataset(model_key: str, model_name: str, dataset_name: str, csv_path: str) -> list[dict]:
    classifier = pipeline("sentiment-analysis", model=model_name, truncation=True)
    df = pd.read_csv(csv_path)
    results = []

    for _, row in tqdm(df.iterrows(), total=len(df), desc=f"{model_key}/{dataset_name}"):
        prediction = classifier(str(row["text"]))[0]
        results.append(
            {
                "model": model_key,
                "dataset": dataset_name,
                "text": row["text"],
                "source": row["source"],
                "true_label": row["label"],
                "predicted_label": normalize_prediction(prediction["label"]),
                "score": prediction["score"],
            }
        )

    return results


def compute_metrics(predictions: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for (model, dataset), group in predictions.groupby(["model", "dataset"]):
        filtered = group[group["predicted_label"].isin(["positive", "negative"])].copy()
        dropped = len(group) - len(filtered)

        y_true = filtered["true_label"]
        y_pred = filtered["predicted_label"]
        precision, recall, f1, _ = precision_recall_fscore_support(
            y_true,
            y_pred,
            average="binary",
            pos_label="positive",
            zero_division=0,
        )
        rows.append(
            {
                "model": model,
                "dataset": dataset,
                "accuracy": accuracy_score(y_true, y_pred),
                "precision": precision,
                "recall": recall,
                "f1": f1,
                "num_examples": len(filtered),
                "neutral_or_dropped_predictions": dropped,
            }
        )
    return pd.DataFrame(rows).sort_values(["model", "dataset"])


def main() -> None:
    parser = argparse.ArgumentParser(description="Run pretrained sentiment models on review datasets.")
    parser.add_argument("--model", choices=list(MODELS), action="append")
    args = parser.parse_args()

    model_keys = args.model or list(MODELS)
    all_results = []
    for model_key in model_keys:
        for dataset_name, csv_path in DATASETS.items():
            all_results.extend(
                predict_dataset(model_key, MODELS[model_key], dataset_name, csv_path)
            )

    output_dir = Path("results")
    output_dir.mkdir(parents=True, exist_ok=True)

    predictions = pd.DataFrame(all_results)
    predictions.to_csv(output_dir / "predictions.csv", index=False)

    metrics = compute_metrics(predictions)
    metrics.to_csv(output_dir / "metrics.csv", index=False)
    print(metrics.to_string(index=False))

    errors = predictions[
        predictions["predicted_label"].isin(["positive", "negative"])
        & (predictions["true_label"] != predictions["predicted_label"])
    ]
    errors.to_csv(output_dir / "errors.csv", index=False)
    print(f"Saved predictions, metrics, and errors to {output_dir}")


if __name__ == "__main__":
    main()
