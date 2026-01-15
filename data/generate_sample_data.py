#!/usr/bin/env python3
"""
E-Commerce Sample Data Generator
Generates realistic customer transaction data for analysis
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
import os

# Set random seed for reproducibility
np.random.seed(42)
random.seed(42)

class EcommerceDataGenerator:
    def __init__(self, n_customers=1000, n_products=100, n_transactions=5000):
        self.n_customers = n_customers
        self.n_products = n_products
        self.n_transactions = n_transactions
        
        # Product categories and price ranges
        self.categories = [
            'Electronics', 'Clothing', 'Home & Garden', 'Sports', 
            'Books', 'Beauty', 'Toys', 'Food & Beverage'
        ]
        
        self.price_ranges = {
            'Electronics': (50, 2000),
            'Clothing': (15, 200),
            'Home & Garden': (20, 500),
            'Sports': (25, 400),
            'Books': (10, 50),
            'Beauty': (15, 150),
            'Toys': (10, 100),
            'Food & Beverage': (5, 80)
        }
        
    def generate_customers(self):
        """Generate customer data"""
        print("Generating customer data...")
        
        countries = ['USA', 'UK', 'Germany', 'France', 'Canada', 'Australia']
        customer_segments = ['New', 'Regular', 'VIP']
        
        customers = pd.DataFrame({
            'customer_id': [f'CUST_{i:05d}' for i in range(self.n_customers)],
            'registration_date': [datetime(2022, 1, 1) + timedelta(days=random.randint(0, 700)) 
                                 for _ in range(self.n_customers)],
            'country': np.random.choice(countries, self.n_customers),
            'segment': np.random.choice(customer_segments, self.n_customers, 
                                       p=[0.4, 0.45, 0.15])
        })
        
        return customers
    
    def generate_products(self):
        """Generate product catalog"""
        print("Generating product catalog...")
        
        products = []
        for i in range(self.n_products):
            category = random.choice(self.categories)
            min_price, max_price = self.price_ranges[category]
            
            products.append({
                'product_id': f'PROD_{i:05d}',
                'product_name': f'{category} Product {i}',
                'category': category,
                'price': round(random.uniform(min_price, max_price), 2),
                'cost': round(random.uniform(min_price * 0.4, min_price * 0.7), 2)
            })
        
        return pd.DataFrame(products)
    
    def generate_transactions(self, customers, products):
        """Generate transaction data"""
        print("Generating transaction data...")
        
        transactions = []
        start_date = datetime(2023, 1, 1)
        end_date = datetime(2024, 12, 31)
        
        # Customer purchase behavior (some customers buy more)
        customer_weights = np.random.exponential(scale=1.5, size=len(customers))
        customer_weights = customer_weights / customer_weights.sum()
        
        for i in range(self.n_transactions):
            customer_id = np.random.choice(customers['customer_id'], p=customer_weights)
            product = products.sample(1).iloc[0]
            
            # Random date
            trans_date = start_date + timedelta(
                days=random.randint(0, (end_date - start_date).days),
                hours=random.randint(0, 23),
                minutes=random.randint(0, 59)
            )
            
            # Quantity (most buy 1, some buy more)
            quantity = np.random.choice([1, 2, 3, 4, 5], p=[0.7, 0.15, 0.08, 0.05, 0.02])
            
            # Discount (80% no discount, 20% have discount)
            discount = 0 if random.random() > 0.2 else round(random.uniform(0.05, 0.3), 2)
            
            # Calculate totals
            subtotal = product['price'] * quantity
            discount_amount = subtotal * discount
            total_amount = round(subtotal - discount_amount, 2)
            
            transactions.append({
                'transaction_id': f'TXN_{i:06d}',
                'customer_id': customer_id,
                'product_id': product['product_id'],
                'transaction_date': trans_date,
                'quantity': quantity,
                'unit_price': product['price'],
                'discount_pct': discount,
                'total_amount': total_amount
            })
        
        return pd.DataFrame(transactions)
    
    def add_data_quality_issues(self, df, missing_rate=0.02):
        """Add realistic data quality issues"""
        print("Adding realistic data quality issues...")
        
        df_copy = df.copy()
        
        # Add some missing values
        for col in df_copy.columns:
            if col not in ['transaction_id', 'customer_id', 'product_id']:
                mask = np.random.random(len(df_copy)) < missing_rate
                df_copy.loc[mask, col] = np.nan
        
        # Add some duplicates (1% of records)
        n_duplicates = int(len(df_copy) * 0.01)
        duplicates = df_copy.sample(n_duplicates)
        df_copy = pd.concat([df_copy, duplicates], ignore_index=True)
        
        return df_copy
    
    def generate_all(self, output_dir='data/raw', clean_dir='data/processed'):
        """Generate all data and save to files"""
        print("="*60)
        print("E-Commerce Data Generator")
        print("="*60)
        
        # Create directories if they don't exist
        os.makedirs(output_dir, exist_ok=True)
        os.makedirs(clean_dir, exist_ok=True)
        
        # Generate data
        customers = self.generate_customers()
        products = self.generate_products()
        transactions = self.generate_transactions(customers, products)
        
        # Save clean versions
        print(f"\nSaving clean data to {clean_dir}/...")
        customers.to_csv(f'{clean_dir}/customers.csv', index=False)
        products.to_csv(f'{clean_dir}/products.csv', index=False)
        transactions.to_csv(f'{clean_dir}/transactions.csv', index=False)
        
        # Add data quality issues for raw data
        transactions_raw = self.add_data_quality_issues(transactions)
        
        # Save raw versions
        print(f"Saving raw data (with quality issues) to {output_dir}/...")
        customers.to_csv(f'{output_dir}/customers_raw.csv', index=False)
        products.to_csv(f'{output_dir}/products_raw.csv', index=False)
        transactions_raw.to_csv(f'{output_dir}/transactions_raw.csv', index=False)
        
        print("\n" + "="*60)
        print("Data Generation Complete!")
        print("="*60)
        print(f"\nGenerated:")
        print(f"  - {len(customers)} customers")
        print(f"  - {len(products)} products")
        print(f"  - {len(transactions)} transactions")
        print(f"  - {len(transactions_raw)} raw transactions (including duplicates)")
        print(f"\nFiles saved to:")
        print(f"  - {output_dir}/ (raw data with quality issues)")
        print(f"  - {clean_dir}/ (clean data for comparison)")
        
if __name__ == '__main__':
    # Generate sample data
    generator = EcommerceDataGenerator(
        n_customers=1000,
        n_products=100,
        n_transactions=5000
    )
    generator.generate_all()
