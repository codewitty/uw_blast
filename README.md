# BLAST Web Query Application

This is a simple web application built using FastAPI that allows users to submit nucleotide BLAST (blastn) queries against the NCBI database and retrieve results asynchronously. 

---

## Features

- **Submit BLAST queries**: Enter a valid FASTA sequence and submit it as a background job.
- **View results**: Results are displayed in a tabular format on the web interface.

---

## Prerequisites

Ensure the following are installed on your system:

- Python 3.8+
- pip (Python package manager)

---

## Installation

1. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

---

## Running the Application

1. Start the FastAPI server:
   ```bash
   uvicorn app:app --reload
   ```

2. Open your browser and navigate to:
   ```
   http://127.0.0.1:8000
   ```

---

## File Structure

- **`app.py`**: The main FastAPI application file.
- **`templates/index.html`**: The front-end template for submitting and viewing BLAST results.
- **`static/`**: (Optional) Directory for hosting additional static files like CSS or JavaScript.
- **`jobs`**: In-memory store for tracking query statuses.

---

## Usage Instructions

1. Open the application in your browser.
2. Paste a valid FASTA sequence in the text area and click **Run BLAST**.
3. Wait for the query to process (a loading screen will display during the process).
4. View the results in a tabular format once completed.

---
