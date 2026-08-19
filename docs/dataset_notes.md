# Dataset Notes

label 01

file: label_01.png

This one ended up being a pretty bad first example. The label is curved around the container and the text is small. It was useful though, because it showed pretty quickly that just throwing an image into OCR does not always work very well.

Some of the problems:
- curved label
- small text
- multiple columns
- packaging text around the nutrition facts
- numbers getting confused with letters

I kept it as more of a difficult example instead of trying to make it the main baseline.

label 02

Much cleaner than label 01. This one has both per serving and per container columns so I also made a cropped version with just the per serving side.

Threshold 140 ended up working best for the cropped version.

label 03

Harder two column label. This one caused a lot of OCR issues even though it looks pretty readable to a person.

Tested multiple threshold values and Tesseract PSM modes.

PSM 11 has been the best result so far for this label.

label 04

Pretty clean label and OCR worked well on most of it.

label 05

Best label so far. Clean image and the pipeline got all 11 fields correct.

label 06

Mostly clean but OCR made a few number mistakes like turning 23g into 239.