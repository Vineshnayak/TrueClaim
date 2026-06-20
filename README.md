# TrueClaim

TrueClaim is an automated multi-modal evidence review system built during the **HackerRank Orchestrate** hackathon. It is designed to verify damage claims for various items, including cars, laptops, and packages. 

By analyzing claim conversations, submitted images, user claim histories, and evidence requirements, TrueClaim determines whether the provided visual evidence supports or contradicts a claim, or if further information is required.

## Features
- **Multi-Modal Analysis**: Processes both text and images to generate comprehensive claim evaluations.
- **Automated Verification**: Produces structured verification decisions with explicit justifications, confidence levels, and risk flags.
- **Robust Pipeline**: Incorporates rate-limit handling, local image caching, and a modular architecture for efficient processing.

## Setup

1. Ensure you have Python installed (Python 3.8+ recommended).
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Set up your environment variables by creating a `.env` file in the project root:
   ```env
   GEMINI_API_KEY=your_gemini_key_here
   GROQ_API_KEY=your_groq_key_here
   ```

## Usage

To run the main evaluation pipeline on the dataset:
```bash
python code/main.py --input dataset/claims.csv --output output.csv
```

To run the evaluation module:
```bash
python code/evaluation/main.py
```

## Project Structure
- `code/`: Contains the core application logic and evaluation pipelines.
- `dataset/`: Contains the input claim data, user history, evidence requirements, and images.
- `docs/`: Contains additional documentation and compliance reports.

## Hackathon Context
This project was developed as a submission for the HackerRank Orchestrate hackathon, challenging participants to build robust multi-modal claim verification systems within a 24-hour timeframe.
