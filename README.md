# whisper_quantitative_analysis

## Overview
This repository contains code and data for automated scraping of the mobile app Whisper. The app is meant to be run in an Android Studio AVD. Appium and MITMproxy are used to interact with the app and (e.g. scrolling) scrape content by parsing the raw network data. The data consists of 23,516 unique Whisper posts collected from April 13, 2023 through June 17, 2023. Names, exact post IDs, usernames, account names, phone numbers, in the Whisper data are omitted in the data. Labels are provided for the 6,695 records with ground-truth annotations.


These are meant to be used with (1) the data we scraped; (2) our ground-truth annotations for a subset of the data; (3) our trained model; and (4) code we used to scrape data.
This repository contains code and data for the quantitative analysis of Whisper. The analysis includes various metrics and models to evaluate the performance and accuracy of Whisper.

## Repository Structure

- `code/`: scripts used for data collection.
- `data/`: dataset (including records with/without ground-truth labels)

## Llama2 Model

The trained Llama2 model (Google Drive link):
[Trained Llama2 Model](https://drive.google.com/your-llama2-model-link)
