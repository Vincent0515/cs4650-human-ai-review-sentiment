# Sentiment Analysis on Human vs AI Product Reviews

This is a small evaluation project for comparing pretrained sentiment analysis models on human-written Amazon reviews and AI-generated Amazon-style reviews.

The project uses existing pretrained sentiment models. It does not train a new model.

## Project Structure

```text
data/
  ai_reviews.csv
  human_reviews.csv
  mixed_reviews.csv
results/
  errors.csv
  metrics.csv
  predictions.csv
  report_notes.md
src/
  create_ai_reviews.py
  make_mixed_dataset.py
  prepare_human_reviews.py
  run_sentiment_models.py
EXPERIMENT_GUIDE.md
requirements.txt
```

For a detailed explanation of the experiment, current results, and how teammates can extend the project, read `EXPERIMENT_GUIDE.md`.

## Setup

Use Python 3.10 or newer. From the project root:

### macOS / Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

### Windows PowerShell

```bash
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

If `py` is not available on Windows, use:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

## Run the Experiment

1. Sample 50 positive and 50 negative human reviews from Amazon Reviews 2023. The script streams the Hugging Face `All_Beauty.jsonl` file and stops after collecting enough examples:

```bash
python src/prepare_human_reviews.py
```

2. Create 50 positive and 50 negative AI-generated reviews:

```bash
python src/create_ai_reviews.py
```

3. Combine human and AI reviews:

```bash
python src/make_mixed_dataset.py
```

4. Run pretrained sentiment models:

```bash
python src/run_sentiment_models.py
```

The first model run downloads pretrained models from Hugging Face, so it requires internet access.

Outputs are saved in `results/`:

- `predictions.csv`
- `metrics.csv`
- `errors.csv`

## Current Results

The current run produced these main results:

| Model | Dataset | Accuracy | F1 |
|---|---:|---:|---:|
| DistilBERT SST-2 | AI | 0.930 | 0.925 |
| DistilBERT SST-2 | Human | 0.850 | 0.842 |
| DistilBERT SST-2 | Mixed | 0.890 | 0.883 |
| Twitter RoBERTa | AI | 1.000 | 1.000 |
| Twitter RoBERTa | Human | 0.939 | 0.939 |
| Twitter RoBERTa | Mixed | 0.970 | 0.969 |

Full metrics are in `results/metrics.csv`.

## Dataset Design

- Human reviews: Amazon Reviews 2023, Hugging Face `raw/review_categories/All_Beauty.jsonl`
- AI reviews: 100 generated Amazon-style beauty product reviews
- Binary sentiment only
- Label mapping:
  - 1-2 stars: `negative`
  - 4-5 stars: `positive`
  - 3 stars: removed

## Models

- `distilbert-base-uncased-finetuned-sst-2-english`
- `cardiffnlp/twitter-roberta-base-sentiment-latest`

## Report Notes

In the final report, describe this as a small balanced sample due to time constraints. The results can support initial observations, but larger datasets and more categories would be needed for stronger conclusions.

## Troubleshooting

If imports fail, make sure the virtual environment is activated and install dependencies with:

```bash
python -m pip install -r requirements.txt
```

On Tianhong's local Windows machine, the working interpreter used for the original run was:

```powershell
C:\Users\tianh\miniforge3\python.exe
```

Example local command:

```powershell
C:\Users\tianh\miniforge3\python.exe src/run_sentiment_models.py
```
