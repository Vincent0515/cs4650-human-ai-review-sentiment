# Experiment Guide

This guide explains what the first version of the experiment does, how to run it, and how to interpret the current results.

## What This Project Does

This project evaluates whether pretrained sentiment analysis models behave differently on human-written Amazon product reviews and AI-generated Amazon-style reviews.

The task is binary sentiment classification:

- `positive`
- `negative`

We do not train a new model. We use existing Hugging Face sentiment models and compare their predictions against our labels.

## First Version Dataset

The first version uses a small balanced dataset:

| Source | Positive | Negative | Total |
|---|---:|---:|---:|
| Human Amazon reviews | 50 | 50 | 100 |
| AI-generated reviews | 50 | 50 | 100 |
| Mixed dataset | 100 | 100 | 200 |

Human reviews come from Amazon Reviews 2023:

```text
McAuley-Lab/Amazon-Reviews-2023
raw/review_categories/All_Beauty.jsonl
```

For human reviews, star ratings are mapped to sentiment labels:

```text
1-2 stars -> negative
4-5 stars -> positive
3 stars -> removed
```

AI reviews are stored in `data/ai_reviews.csv`. They are generated Amazon-style beauty product reviews with controlled positive or negative sentiment.

## Files and What They Do

```text
src/prepare_human_reviews.py
```

Streams the `All_Beauty` Amazon Reviews 2023 file from Hugging Face and saves 50 positive and 50 negative human reviews to:

```text
data/human_reviews.csv
```

```text
src/create_ai_reviews.py
```

Creates 50 positive and 50 negative AI-generated reviews and saves them to:

```text
data/ai_reviews.csv
```

```text
src/make_mixed_dataset.py
```

Combines human and AI reviews into:

```text
data/mixed_reviews.csv
```

```text
src/run_sentiment_models.py
```

Runs the pretrained sentiment models on the human, AI, and mixed datasets. It saves:

```text
results/predictions.csv
results/metrics.csv
results/errors.csv
```

## How To Run

Install dependencies first:

```bash
python -m pip install -r requirements.txt
```

Then run:

```bash
python src/prepare_human_reviews.py
python src/create_ai_reviews.py
python src/make_mixed_dataset.py
python src/run_sentiment_models.py
```

The first and fourth commands require internet access:

- `prepare_human_reviews.py` streams Amazon Reviews 2023 from Hugging Face.
- `run_sentiment_models.py` downloads pretrained Hugging Face models the first time it runs.

## Models Used

The first version uses two pretrained sentiment models:

| Short Name | Hugging Face Model |
|---|---|
| DistilBERT SST-2 | `distilbert-base-uncased-finetuned-sst-2-english` |
| Twitter RoBERTa | `cardiffnlp/twitter-roberta-base-sentiment-latest` |

## First Version Results

The current results are:

| Model | Dataset | Accuracy | Precision | Recall | F1 |
|---|---:|---:|---:|---:|---:|
| DistilBERT SST-2 | AI | 0.930 | 1.000 | 0.860 | 0.925 |
| DistilBERT SST-2 | Human | 0.850 | 0.889 | 0.800 | 0.842 |
| DistilBERT SST-2 | Mixed | 0.890 | 0.943 | 0.830 | 0.883 |
| Twitter RoBERTa | AI | 1.000 | 1.000 | 1.000 | 1.000 |
| Twitter RoBERTa | Human | 0.939 | 0.939 | 0.939 | 0.939 |
| Twitter RoBERTa | Mixed | 0.970 | 0.969 | 0.969 | 0.969 |

Twitter RoBERTa can output `neutral`. Since this experiment is binary, neutral predictions are excluded from binary metric calculation:

| Dataset | Neutral Predictions |
|---|---:|
| AI | 1 |
| Human | 2 |
| Mixed | 3 |

## How To Read the Result

In this first version, both models perform well on AI-generated reviews.

DistilBERT performs better on AI reviews than on human reviews:

```text
AI F1:    0.925
Human F1: 0.842
```

Twitter RoBERTa performs best overall:

```text
AI F1:    1.000
Human F1: 0.939
Mixed F1: 0.969
```

One likely reason is that the AI-generated reviews are clearer and more direct. Human reviews often include mixed sentiment, informal language, spelling issues, and star ratings that do not perfectly match the written text.

## Error Analysis

Use this file for error analysis:

```text
results/errors.csv
```

Useful patterns to look for:

- Human reviews with mixed sentiment, such as a negative review that still says something positive.
- Positive star ratings where the text contains complaints.
- Negative star ratings where the review praises some part of the product.
- AI negative reviews that use polite or mild wording.

For the final report, choose 3-5 examples from `results/errors.csv` and explain why each example was misclassified.

## How To Extend the Experiment

To change the sample size, use:

```bash
python src/prepare_human_reviews.py --per-label 100
```

If you increase the human review sample size, also update `src/create_ai_reviews.py` or replace `data/ai_reviews.csv` so the AI dataset stays balanced.

To run only one model:

```bash
python src/run_sentiment_models.py --model distilbert_sst2
python src/run_sentiment_models.py --model twitter_roberta
```

## Limitations

- This is a small sample because the project is time constrained.
- Only one Amazon category, `All_Beauty`, is used.
- AI reviews are generated in a controlled style and may be easier to classify than real AI spam.
- The experiment removes neutral sentiment.
- Star ratings are used as labels, but star ratings and review text do not always match perfectly.
