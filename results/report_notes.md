# Report Notes

## Dataset

- Human reviews: 100 Amazon Reviews 2023 `All_Beauty` reviews
- AI-generated reviews: 100 Amazon-style beauty product reviews
- Mixed set: 200 total reviews
- Binary labels only:
  - `1-2 stars = negative`
  - `4-5 stars = positive`
  - `3 stars = removed`

## Results

| Model | Dataset | Accuracy | Precision | Recall | F1 |
|---|---:|---:|---:|---:|---:|
| DistilBERT SST-2 | AI | 0.930 | 1.000 | 0.860 | 0.925 |
| DistilBERT SST-2 | Human | 0.850 | 0.889 | 0.800 | 0.842 |
| DistilBERT SST-2 | Mixed | 0.890 | 0.943 | 0.830 | 0.883 |
| Twitter RoBERTa | AI | 1.000 | 1.000 | 1.000 | 1.000 |
| Twitter RoBERTa | Human | 0.939 | 0.939 | 0.939 | 0.939 |
| Twitter RoBERTa | Mixed | 0.970 | 0.969 | 0.969 | 0.969 |

Twitter RoBERTa produced a few neutral predictions. These were excluded from binary metric calculation:

- AI: 1 neutral prediction
- Human: 2 neutral predictions
- Mixed: 3 neutral predictions

## Initial Interpretation

In this small experiment, both pretrained models performed well on AI-generated reviews. Twitter RoBERTa performed best overall. DistilBERT had lower performance on human reviews than AI reviews, likely because real human reviews often contain mixed sentiment, informal writing, spelling issues, or star ratings that do not perfectly match the review text.

## Error Analysis Ideas

Several human review errors appear to come from mixed sentiment. For example, some negative-rated reviews include positive phrases such as "smells wonderful" or praise one part of a gift set, while still giving an overall negative rating. Some positive-rated reviews contain complaints about price, product thickness, skin irritation, or effort required, causing the model to predict negative.

For the report, include 3-5 examples from `results/errors.csv` and explain whether the error was caused by mixed sentiment, rating/text mismatch, or ambiguous wording.

## Limitations

- The sample size is small because the project is time constrained.
- Only one product category, `All_Beauty`, was used.
- AI-generated reviews were generated in a controlled style, so they may be clearer than real AI spam reviews.
- The experiment uses binary sentiment only and removes neutral reviews.
- Star ratings are used as ground-truth sentiment labels, but star ratings do not always perfectly match review text.
