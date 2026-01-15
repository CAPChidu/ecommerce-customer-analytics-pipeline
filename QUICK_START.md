# 🚀 Quick Start Guide

## Run the Complete Data Analytics Pipeline

This guide will help you get the project up and running in minutes!

---

## 💻 Prerequisites

Make sure you have:
- **Python 3.9+** installed
- **pip** (Python package manager)
- **Git** (to clone the repository)

---

## ⚡ Quick Setup (5 minutes)

### Step 1: Clone the Repository
```bash
git clone https://github.com/CAPChidu/ecommerce-customer-analytics-pipeline.git
cd ecommerce-customer-analytics-pipeline
```

### Step 2: Create Virtual Environment
```bash
# Create virtual environment
python -m venv venv

# Activate it
# On Windows:
venv\Scripts\activate

# On Mac/Linux:
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Generate Sample Data
```bash
python data/generate_sample_data.py
```

**Output:** This creates realistic e-commerce data in:
- `data/raw/` - Raw data with quality issues (duplicates, missing values)
- `data/processed/` - Clean data for comparison

---

## 📊 What You Get

After running the data generator, you'll have:

**✅ 1,000 customers** with realistic profiles
**✅ 100 products** across 8 categories
**✅ 5,000+ transactions** spanning 2 years
**✅ Real data quality issues** (missing values, duplicates)

---

## 🔍 Next Steps: Analyze the Data

Once data is generated, you can:

### Option 1: Run Python Scripts (Command Line)
```bash
# Coming soon: Analysis scripts
python src/analysis/customer_segmentation.py
python src/analysis/sales_trends.py
```

### Option 2: Use Jupyter Notebooks (Interactive)
```bash
# Launch Jupyter
jupyter notebook

# Then open notebooks in this order:
# 1. notebooks/01_data_exploration.ipynb
# 2. notebooks/02_data_cleaning.ipynb
# 3. notebooks/03_customer_analysis.ipynb
```

### Option 3: Load Data for Your Own Analysis
```python
import pandas as pd

# Load the generated data
customers = pd.read_csv('data/processed/customers.csv')
products = pd.read_csv('data/processed/products.csv')
transactions = pd.read_csv('data/processed/transactions.csv')

# Start analyzing!
print(f"Total customers: {len(customers)}")
print(f"Total revenue: ${transactions['total_amount'].sum():,.2f}")
```

---

## 📊 Sample Analysis You Can Perform

### Customer Segmentation (RFM Analysis)
```python
import pandas as pd
from datetime import datetime

# Load data
transactions = pd.read_csv('data/processed/transactions.csv')
transactions['transaction_date'] = pd.to_datetime(transactions['transaction_date'])

# Calculate RFM metrics
today = transactions['transaction_date'].max()

rfm = transactions.groupby('customer_id').agg({
    'transaction_date': lambda x: (today - x.max()).days,  # Recency
    'transaction_id': 'count',  # Frequency
    'total_amount': 'sum'  # Monetary
}).rename(columns={
    'transaction_date': 'Recency',
    'transaction_id': 'Frequency',
    'total_amount': 'Monetary'
})

print(rfm.head())
print(f"\nTop 10% of customers by revenue: ${rfm['Monetary'].quantile(0.9):,.2f}+")
```

### Sales Trends Over Time
```python
import matplotlib.pyplot as plt

# Monthly sales trend
transactions['month'] = pd.to_datetime(transactions['transaction_date']).dt.to_period('M')
monthly_sales = transactions.groupby('month')['total_amount'].sum()

plt.figure(figsize=(12, 6))
monthly_sales.plot(kind='line', marker='o')
plt.title('Monthly Sales Trend')
plt.xlabel('Month')
plt.ylabel('Total Sales ($)')
plt.grid(True)
plt.tight_layout()
plt.savefig('reports/figures/monthly_sales.png')
print("Chart saved to reports/figures/monthly_sales.png")
```

### Product Category Performance
```python
# Merge transactions with products
products = pd.read_csv('data/processed/products.csv')
merged = transactions.merge(products, on='product_id')

# Category performance
category_sales = merged.groupby('category').agg({
    'total_amount': 'sum',
    'transaction_id': 'count'
}).rename(columns={
    'total_amount': 'Revenue',
    'transaction_id': 'Units_Sold'
})

print("\nCategory Performance:")
print(category_sales.sort_values('Revenue', ascending=False))
```

---

## 🛠️ Project Structure

```
ecommerce-customer-analytics-pipeline/
├── data/
│   ├── raw/                    # Raw data (with quality issues)
│   ├── processed/              # Clean data
│   └── generate_sample_data.py # Data generator script (✅ RUNS!)
│
├── notebooks/                  # Jupyter notebooks (coming soon)
├── src/                        # Python modules (coming soon)
├── reports/                    # Generated reports
├── requirements.txt            # Python dependencies
└── README.md                   # Full documentation
```

---

## ❓ Troubleshooting

### Issue: "ModuleNotFoundError"
**Solution:** Make sure you installed dependencies:
```bash
pip install -r requirements.txt
```

### Issue: "Permission denied" when running scripts
**Solution:** Make the script executable:
```bash
chmod +x data/generate_sample_data.py
```

### Issue: Data files not generated
**Solution:** Check that the script completed successfully:
```bash
python data/generate_sample_data.py
# Look for "Data Generation Complete!" message
```

---

## 🎓 What This Project Teaches

By exploring this project, you'll learn:

✅ How to generate realistic sample data for analysis
✅ Data cleaning techniques (handling missing values, duplicates)
✅ Customer segmentation using RFM analysis
✅ Sales trend analysis and visualization
✅ Product performance analysis
✅ Statistical analysis for business insights
✅ Creating data pipelines from scratch

---

## 📞 Need Help?

- **Issues:** Open an issue on GitHub
- **Questions:** Check the main README.md
- **Contact:** Connect via LinkedIn

---

## ⏭️ Next: Explore the Notebooks

Once you've generated data, explore the Jupyter notebooks for guided analysis:

1. **Data Exploration** - Understand your dataset
2. **Data Cleaning** - Handle quality issues
3. **Customer Analysis** - Segment customers
4. **Sales Analysis** - Identify trends
5. **Business Recommendations** - Translate insights to action

**Get Started:**
```bash
jupyter notebook
```

Then navigate to the `notebooks/` folder!

---

**⭐ Star this repo if you find it helpful!**
