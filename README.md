# whisper_quantitative_analysis

## Overview
This repository contains code and data for automated scraping of the mobile app Whisper. The app is meant to be run in an Android Studio AVD. Appium and MITMproxy are used to interact with the app and (e.g. scrolling) scrape content by parsing the raw network data. The data consists of 23,516 unique Whisper posts collected from April 13, 2023 through June 17, 2023. Names, exact post IDs, usernames, account names, phone numbers, in the Whisper data are omitted in the data. Labels are provided for the 6,695 records with ground-truth annotations.


## Repository Structure

- `code/`: scripts used for data collection.
- `data/`: dataset (including records with/without ground-truth labels)

## Llama2 Model

The trained Llama2 model (Google Drive link):
[Trained Llama2 Model](https://drive.google.com/your-llama2-model-link)
