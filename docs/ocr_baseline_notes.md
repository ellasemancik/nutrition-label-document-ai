# OCR Baseline Notes

## Label 01

### What worked

- Tesseract detected some nutrition words.
- Tesseract detected some numbers.
- The image opened and processed without crashing.

### Problems noticed

- Some words were missed.
- Some numbers were incorrect.
- The curved label made the text harder to read.
- The image text was small.
- The nutrition columns may have been mixed together.

### Baseline conclusion

The first OCR result works as a starting point, but the image needs preprocessing before the results will be reliable.

## Label 02

- Label 02 extracted 8 of 9 target fields.
- Calories was missed because OCR did not capture the value 350.
- The extractor correctly returned null instead of guessing.