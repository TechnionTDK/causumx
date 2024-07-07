# CauSumX UI

This project provides a user interface for explaining the causes of aggregate SQL query results using the CauSumX algorithm.

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/nativlevy/causumx
    cd causumx
    ```

2. Create a virtual environment and activate it:
    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. Install the required packages:
    ```sh
    pip install -r requirements.txt
    ```

4. Create a `.env` file with the following content:
    ```env
    OPENAI_API_KEY=sk-...
    ```

## Usage

Run the Streamlit application:
```sh
streamlit run ui/app.py --server.port 8081 --server.address localhost
```

Open your web browser and navigate to `http://localhost:8081` to access the application.

## Features

- Upload your own dataset and DAG file.
- Select from preloaded datasets.
- Enter and execute SQL GROUP-BY queries.
- Visualize causal explanations and interactive bar charts.
