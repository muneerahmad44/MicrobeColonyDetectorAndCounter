# Microbe Colony Detector and Counter

A deep learning-based system for automated detection, classification, and counting of bacterial colonies from petri dish images.

## Overview

This system analyzes petri dish images to detect and classify bacterial colonies into 7 distinct categories. It provides automated colony counting per class along with comprehensive statistics and visualizations.

## Features

- **Multi-class Colony Detection**: Detects and classifies colonies into 7 trained categories
- **Automated Counting**: Counts colonies per class with high accuracy
- **Statistical Analysis**: Generates detailed statistics and visual graphs
- **User-friendly Interface**: Built with Streamlit for easy interaction

## Installation

1. Clone the repository:
```bash
git clone https://github.com/muneerahmad44/MicrobeColonyDetectorAndCounter.git
cd MicrobeColonyDetectorAndCounter
```

2. Install required dependencies:
```bash
pip install -r requirements.txt
```

## Usage

Run the application using Streamlit:
```bash
streamlit run main.py
```

The application will open in your default web browser where you can upload petri dish images for analysis.

## Documentation

- **System Architecture**: [View Flow Diagram](#) *https://github.com/muneerahmad44/MicrobeColonyDetectorAndCounter/blob/main/flow_charts/flowchartcomplete.png*
- **System Results**: [View Results](#) *https://github.com/muneerahmad44/MicrobeColonyDetectorAndCounter/tree/main/system%20results*
- **Model Performance**: [View Fine-tuned Model Metrics](#) *https://github.com/muneerahmad44/MicrobeColonyDetectorAndCounter/tree/main/fine%20tuned%20model%20results*

## How It Works

1. Upload an image of a petri dish
2. The system processes the image using a trained deep learning model
3. Colonies are detected and classified into one of 7 categories
4. Results display:
   - Colony count per class
   - Statistical summaries
   - Visual graphs and charts

## Requirements

See `requirements.txt` for a complete list of dependencies.



## Contact

*muneerahmed.dev@gmail.com*
