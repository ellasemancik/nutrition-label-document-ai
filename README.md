# Nutrition Label Document Intelligence

This project takes nutrition label images and turns the information into structured JSON data.

It uses Tesseract OCR to read the text from each image, then Python code extracts specific nutrition fields, checks the values, gives the result a confidence score, and compares the output against manually entered correct answers.

Right now the project extracts: servings per container, serving size, calories, total fat, saturated fat, cholesterol, sodium, total carbohydrates, dietary fiber, total sugars, protein

The general pipeline is: Image → preprocessing → OCR → field extraction → validation → confidence score → JSON

I have also been testing different OCR settings and preprocessing methods to see how they affect accuracy on labels with different layouts and image quality.

Current benchmark across 5 labels: 

Label 02: 72.73%
Label 03: 45.45%
Label 04: 90.91%
Label 05: 100%
Label 06: 72.73%

Average accuracy: 76.36%

The project also includes unit tests, saved OCR outputs, ground truth JSON files, validation rules, confidence scoring, and end-to-end benchmarking.