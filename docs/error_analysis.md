# Error Analysis

These are just notes on what has been going wrong while testing different labels.

## label 02

Mostly worked well.

Calories got completely missed by OCR and the serving size got cut off.

Everything else was pretty good.

accuracy: 72.73%

## label 03

Definitely the hardest one so far.

The two column layout seems to mess with Tesseract a lot. Some field names disappeared and some numbers were read wrong.

Examples:
- sodium 55mg became 56mg
- 22g sometimes became 229
- serving size lost the closing parenthesis
- some field names and values ended up separated

I tested thresholds 100, 140 and 180.

I also tested Tesseract PSM 6 and 11.

PSM 11 gave the best extraction accuracy so far.

accuracy: 45.45%

## label 04

This one did really well.

Main issue was total sugars. 19g got read as 199.

accuracy: 90.91%

## label 05

Basically perfect.

All 11 fields matched the ground truth.

accuracy: 100%

## label 06

OCR mistakes were mostly numbers.

23g became 239

1g became ig

21g became 219

I left those values as missing instead of trying to guess what OCR meant.

accuracy: 72.73%