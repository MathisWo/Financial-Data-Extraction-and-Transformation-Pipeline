# Financial Data Extraction and Transformation Pipeline

## 🧠 Project Overview

This project implements a Python-based data pipeline that extracts publicly accessible company financial data, cleans and transforms it, and outputs a structured dataset for analytical use.
The pipeline retrieves company profile information and income statements for multiple companies and generates a merged dataset containing financial metrics for the most recent three years.


## 🌐 Data Source

Financial Modeling Prep (FMP)
https://financialmodelingprep.com/

The FMP API is publicly accessible and provides among other data the company profile and financial statement data through a free access tier. A valid API key is required, which can be obtained by signing up for a free account.

Note on Data Availability:
Due to licensing restrictions, the fully generated dataset is not included in this public repository. However, it can be reproduced by running the pipeline with your own API key.


## 🎯 Project Requirements

This project satisfies the following assignment criteria:

✔️ Identify a publicly accessible dataset

✔️ Use Python to extract the data

✔️ Clean and transform the dataset

✔️ Produce a structured output

The task specifies that the final dataset should contain at least 100 companies and no more than 500.


## 📌 Limitations

The FMP free tier includes approximately 100 company ticker symbols.
However:

- some company symbols are duplicates 
- some financial statement endpoints return no data

After filtering invalid or incomplete entries, the final dataset contains 84 companies with fully accessible profiles and financial statements for the last three years. 
Rather than mixing more data sources, this approach prioritizes data integrity and consistency and keeps the pipeline maintainable.


## 📁 Repository Structure
```
.
├── README.md
├── LICENSE
├── requirements.txt
│
├── src/
│   ├── main.py               # Entry point: runs the pipeline
│   ├── extract.py            # API fetching + caching
│   └── transform.py          # Data transformation and data set builder
│
└── data/
    ├── processed/
    │   └──company_financials.csv (generated output - NOT in repo)
    ├── valid_symbols.txt     # List of verified free-tier symbols
    └── raw/                  # Cached raw API responses



```


## ⚙️ How to run the Project

### 1️⃣ Install dependencies
```
pip install -r requirements.txt
```
### 2️⃣ Set up API key
Create a .env file in the project root with the following content:
```
FMP_API_KEY = your_api_key_here
```
### ▶️ Running the Pipeline

Setting the right directory (project folder):

```
cd <YOUR_PROJECT_FOLDER>
```

Creating the final dataset:

```
python -m src.main
```

The output dataset will be saved to:

```
data/processed/company_financials.csv
```


## 📁 Output Dataset Description

Each row represents one company-year combination. Ther are 84 comapnies x 3 years = 252 rows in total. 
Columns include:
| Field                      | Description                             |
| -------------------------- | ----------------------------------------|
| `company_name`             | Full company name                       |
| `symbol`                   | Stock ticker of the company             |
| `country`                  | Headquarters country                    |
| `industry`                 | Industry classification                 |
| `year`                     | Fiscal year of reported financials      |
| `revenue`                  | Reported revenue value                  |
| `currency`                 | Currency or unit of revenue             |
| `gross_profit`             | Revenue minus production costs          |
| `operating_income`         | Gross profit minus operating expenses   |
| `net_income`               | Op. income minus interest - tax         |
| `earnings_per_share`       | Net income divided by outstanding shares|


## 💾 Caching Strategy

To avoid exceeding daily API limits, all raw responses are cached under:

```
data/raw/
```

Profile data is stored as JSON, and financial statements as Python pickles. 
If cached data exists, the pipeline reuses it instead of re-requesting via the API.


## 🛠️ Error Handling

- Empty data from API responses is detected and ignored

- Symbols are then skipped

- The pipeline warns but does not terminate unexpectedly


## 📄 License

This project is intended for educational and evaluation purposes only.
Please do not redistribute data retrieved from FMP's API.


## ✍️ Author

**Mathis Wobst**

M.Sc. Psychologist | Aspiring Data Analyst/Engineer
  
[LinkedIn](https://www.linkedin.com/in/mathis-wobst-b37125360/?locale=en_US)
