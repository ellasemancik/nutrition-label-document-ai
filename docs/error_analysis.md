# Error Analysis

## Label 02

Main problems:
- Calories was missed by OCR.
- Serving size was cut off by OCR.
- Most other nutrition fields were extracted correctly.

## Label 03

Main problems:
- OCR struggled with the two-column layout.
- Some field names disappeared completely.
- Some values were misread, such as sodium 55mg becoming 56mg.
- Some values were read with extra digits, such as 22g becoming 229.
- PSM 11 performed better than the other tested OCR settings.

## Label 04

Main problems:
- Total sugars 19g was read as 199.
- The rest of the main nutrition fields were extracted well.

## Current Benchmark

- Label 02: 72.73%
- Label 03: 45.45%
- Label 04: 90.91%
- Average: 69.70%

## Main Failure Types

1. Missing OCR text
2. Incorrect OCR characters or digits
3. Multi-column layout confusion
4. Field name and value separated onto different lines
5. Minor formatting differences