# Python + SQL Customer Analytics System

End-to-end customer analytics project using Python, MySQL, SQL, Pandas and Matplotlib.

## Features
- MySQL customer and order database
- CSV data loading
- SQL business analysis
- Customer, product, category and city analysis
- Monthly revenue analysis
- Repeat-customer analysis
- Python/Pandas reporting
- PNG charts
- Excel report

## Project structure
```text
python-sql-customer-analytics/
├── data/
│   ├── customers.csv
│   └── orders.csv
├── sql/
│   ├── database.sql
│   └── analysis_queries.sql
├── src/
│   ├── config.py
│   ├── database.py
│   ├── setup_database.py
│   ├── load_data.py
│   ├── analysis.py
│   └── reports.py
├── reports/
├── visualizations/
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
```

## Setup

### 1. Create environment
```bash
python -m venv venv
venv\Scripts\activate
```

### 2. Install packages
```bash
pip install -r requirements.txt
```

### 3. Configure MySQL
Copy `.env.example` to `.env` and enter your MySQL password.

### 4. Create database and tables
```bash
python src/setup_database.py
```

### 5. Load data
```bash
python src/load_data.py
```

### 6. Run analysis
```bash
python src/analysis.py
```

### 7. Generate charts and Excel report
```bash
python src/reports.py
```

## Resume bullets

**Customer Analytics System | Python, MySQL, SQL, Pandas**

- Developed an end-to-end customer analytics system using Python, MySQL, SQL, and Pandas to analyze customer and order data.
- Designed SQL queries to identify top customers, product performance, monthly revenue, repeat customers, and city-wise sales.
- Automated KPI calculations, data visualizations, and Excel reporting using Python and Pandas.

## Interview explanation

"I built a customer analytics system using Python and MySQL. Customer and order data is stored in MySQL, SQL queries are used for business analysis, and Python retrieves the results with Pandas, performs additional analysis, creates visualizations, and exports an Excel report."

## Future improvements
- FastAPI web API
- RFM customer segmentation
- Power BI dashboard
- Scheduled reporting
- Unit tests
