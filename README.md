# Nutrition Label Document Intelligence

This project takes nutrition label images and turns the information into structured JSON data.

It uses Tesseract OCR to read text from an image. Python then extracts nutrition fields, checks the values, calculates a confidence score, and saves the results as JSON. I also compare the output with manually entered answers to see what the pipeline gets right and where it struggles.

Right now it extracts 11 fields: servings per container, serving size, calories, total fat, saturated fat, cholesterol, sodium, total carbohydrates, dietary fiber, total sugars, and protein.

The general pipeline is: Image → preprocessing → OCR → field extraction → validation → confidence score → JSON

## Dataset

I started with 6 nutrition label images and expanded the collection to 100. The 94 additional images were downloaded from Open Food Facts using a Python importer (`src/import_labels.py`). The importer saves the images in numbered folders and records their source information in `data/import_manifest.jsonl`.

The downloaded images are kept locally and are not included in this GitHub repository. The manifest is included so I can track where the images came from. The new labels still need to be reviewed and annotated before they can be used for accuracy testing.

## Current results

So far, I have benchmarked 5 of the original labels (02–06) against manually entered ground truth. Label 01 is kept as a difficult example because its text wraps around a container.

| Label | Field accuracy |
| --- | ---: |
| 02 | 72.73% |
| 03 | 45.45% |
| 04 | 90.91% |
| 05 | 100% |
| 06 | 72.73% |

**Average field accuracy: 76.36% across these 5 labels.** This is not a benchmark of all 100 images.

I have also tested different preprocessing thresholds and Tesseract page segmentation modes. Two-column layouts and small OCR number mistakes have been some of the biggest problems so far.

The project includes unit tests, saved OCR outputs, ground truth JSON files, validation rules, confidence scoring, and end-to-end benchmarking. More details about the original labels and their errors are in `docs/dataset_notes.md`.

## Next steps

Review the imported images, create ground truth annotations for more labels, and rerun the benchmark on a larger set to see how well the pipeline handles different label layouts.
