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
python -m streamlit run ui/app.py --server.port 8081 --server.address localhost
```

Open your web browser and navigate to `http://localhost:8081` to access the application.

## Features

- Upload your own dataset and DAG file.
- Select from preloaded datasets.
- Enter and execute SQL GROUP-BY queries.
- Visualize causal explanations and interactive bar charts.

## Main Functions

### ui/app.py

1. `main()`: The main function that sets up the Streamlit UI and orchestrates the workflow.
2. `dot_to_list(uploaded_file)`: Converts a DOT file to a list representation of the DAG.
3. `plot_interactive_bar_chart(data, country_column, value_column, title=None)`: Creates an interactive bar chart using Plotly.

### ui/CauSumX.py

1. `cauSumX(df, DAG, ordinal_atts, targetClass, groupingAtt, fds, k, tau, actionable_atts, high, low)`: The main CauSumX algorithm implementation.

### ui/Algorithms.py

1. `filterPatterns(df, groupingAtt, groups)`: Filters patterns based on grouping attributes.
2. `getAllGroups(df_org, atts, t)`: Retrieves all groups from the dataset.
3. `getGroupstreatments(DAG, df, groupingAtt, groups, ordinal_atts, targetClass, ...)`: Gets treatments for groups.

### ui/Utils.py

1. `getAttsVals(atts,df)`: Gets attribute values from the dataframe.
2. `getNextLeveltreatments(treatments_cate, df_g, ordinal_atts, high, low)`: Generates next level treatments.
3. `getCombTreatments(df_g, positives, treatments, ordinal_atts)`: Combines treatments.

### ui/llm_explainer.py

1. `causumx_output_to_natural_language_explanation(causumx_output)`: Converts CauSumX output to natural language explanations.

## How to Run the UI

1. Ensure you have completed the installation steps mentioned above.

2. Activate your virtual environment:
    ```sh
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. Navigate to the project directory:
    ```sh
    cd path/to/causumx
    ```

4. Run the Streamlit application:
    ```sh
    python -m streamlit run ui/app.py --server.port 8081 --server.address localhost
    ```

5. Open your web browser and go to `http://localhost:8081`.

6. Using the UI:
   a. Choose a dataset from the dropdown or upload your own CSV file.
   b. If using your own dataset, upload a corresponding DAG file (in DOT format).
   c. Enter a SQL GROUP BY query in the provided text area.
   d. Adjust the parameters (k and tau) if needed.
   e. Click the "Run CauSumX" button to execute the algorithm.
   f. View the results, including causal explanations and interactive visualizations.

## Troubleshooting

- If you encounter any issues with package dependencies, ensure your virtual environment is activated and all packages in `requirements.txt` are installed.
- For OpenAI API related errors, check that your `.env` file contains a valid API key.

## Contributing

Contributions to improve the UI or extend the functionality of CauSumX are welcome. Please submit pull requests or open issues on the GitHub repository.

Original Paper:
https://dl.acm.org/doi/10.1145/3639328
