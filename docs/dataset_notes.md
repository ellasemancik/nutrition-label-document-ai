# Dataset Notes and Error Analysis

## Dataset expansion

I started with 6 nutrition label images (label_01 through label_06). I then used `src/import_labels.py` to download 94 more images from Open Food Facts, bringing the collection to 100 images total.

The importer saves each image in its own numbered folder under `data/raw/`. It also creates `data/import_manifest.jsonl`, which records information like the label number, product barcode, source URL, and image hash. This helps me keep track of where the images came from and avoid downloading duplicates.

The 94 downloaded images are stored locally and are not uploaded to GitHub. They still need to be checked and manually annotated before I can use them in the accuracy benchmark.

For now, the results below only cover labels 02–06. Label 01 was kept as a difficult example but was not part of that benchmark. The current average field accuracy is 76.36% across those 5 labels, **not** across all 100 images.

## Original label testing

### label 01

file: label_01.png

This one ended up being a pretty bad first example. The label is curved around the container and the text is small. It was useful though, because it showed pretty quickly that just throwing an image into OCR does not always work very well.

Some of the problems: curved label, small text, multiple columns, packaging text around the nutrition facts, numbers getting confused with letters

I kept it as more of a difficult example instead of trying to make it the main baseline.

### label 02

Much cleaner than label 01. This one has both per serving and per container columns so I also made a cropped version with just the per serving side.

Threshold 140 ended up working best for the cropped version.

Mostly worked well.

Calories got completely missed by OCR and the serving size got cut off.

Everything else was pretty good.

accuracy: 72.73%

### label 03

Harder two column label. This one caused a lot of OCR issues even though it looks pretty readable to a person.

Definitely the hardest one so far.

The two column layout seems to mess with Tesseract a lot. Some field names disappeared and some numbers were read wrong.

Examples: sodium 55mg became 56mg, 22g sometimes became 229, serving size lost the closing parenthesis, some field names and values ended up separated

Tested multiple threshold values and Tesseract PSM modes.

I tested thresholds 100, 140 and 180.

I also tested Tesseract PSM 6 and 11.

PSM 11 has been the best result so far for this label.

accuracy: 45.45%

### label 04

Pretty clean label and OCR worked well on most of it.

This one did really well.

Main issue was total sugars. 19g got read as 199.

accuracy: 90.91%

### label 05

Best label so far. Clean image and the pipeline got all 11 fields correct.

Basically perfect.

All 11 fields matched the ground truth.

accuracy: 100%

### label 06

Mostly clean but OCR made a few number mistakes like turning 23g into 239.

OCR mistakes were mostly numbers.

23g became 239

1g became ig

21g became 219

I left those values as missing instead of trying to guess what OCR meant.

accuracy: 72.73%
