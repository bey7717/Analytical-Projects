# 📊 Customer Behavior Analytics Dashboard

## Overview
This project is an **end-to-end data analytics pipeline** that transforms raw customer shopping behavior data into an **interactive Power BI dashboard** for business insights.

The workflow covers:
- Data ingestion and cleaning using **Python**
- Storage and transformation using **SQLite**
- Data modeling and visualization using **Power BI**
- Actionable **business insights and recommendations**

The final dashboard provides insights into customer demographics, purchasing behavior, revenue drivers, and subscription impact.

---

## 🧱 Tech Stack

- **Python**: Data cleaning, transformation, and database population
- **SQLite**: Lightweight relational database for structured storage
- **Power BI**: Interactive dashboard and business intelligence
- **CSV Dataset**: Customer shopping behavior data

---

## 📁 Project Structure

```
customer_trends_project/
│
├── customer_shopping_behavior.csv   # Raw dataset
├── database.db                      # SQLite database
├── connect_database.py              # Python ETL script
├── README.md                        # Project documentation
└── PowerBI_Dashboard.pbix           # Power BI report file
```

---

## 🧹 Data Cleaning & Preparation (Python)

Data cleaning and normalization were handled in Python before loading into SQLite.

### Key Cleaning Steps

1. **Standardized Column Names**
   - Converted to lowercase
   - Replaced spaces with underscores
   - Removed special characters

2. **Handled Encoding Issues**
   - Used `utf-8-sig` to properly read CSV headers

3. **Validated Data Types**
   - Ensured numeric fields (age, purchase amount, ratings)
   - Ensured categorical consistency (gender, category, frequency)

4. **Controlled Inserts with `DictReader`**
   - Prevented column misalignment
   - Explicit column mapping during SQL inserts

---

## 🗄️ Database Design (SQLite)

### Core Table: `customer`

The dataset is stored in a single fact-style table optimized for BI querying.

Key fields include:
- `customer_id`
- `age`
- `gender`
- `item_purchased`
- `category`
- `purchase_amount`
- `review_rating`
- `subscription_status`
- `discount_applied`
- `frequency_of_purchases`

---

## 🔄 SQL Transformations

### 1️⃣ Age Group Derivation

Age groups were created using SQL logic (not present in the original CSV):

```sql
CASE
  WHEN age < 18 THEN 'Minor'
  WHEN age BETWEEN 18 AND 25 THEN 'Young Adult'
  WHEN age BETWEEN 26 AND 45 THEN 'Adult'
  WHEN age BETWEEN 46 AND 65 THEN 'Middle-age'
  ELSE 'Senior'
END AS age_group
```

This field is used directly in Power BI for segmentation.

---

### 2️⃣ Purchase Frequency (Days)

Converted text-based frequency into numeric values for analysis:

```sql
UPDATE customer
SET purchase_freq_days =
  CASE frequency_of_purchases
    WHEN 'Weekly' THEN 7
    WHEN 'Fortnightly' THEN 14
    WHEN 'Monthly' THEN 30
    WHEN 'Quarterly' THEN 90
    WHEN 'Annually' THEN 365
  END;
```

This allows trend analysis and numerical aggregation.

---

### 3️⃣ Discount Applied Normalization

Discount indicators were standardized to ensure compatibility with Power BI:

- Converted mixed or boolean-like values into consistent formats
- Verified using `PRAGMA table_info(customer)` and SQL checks

---

## 📐 Data Modeling (Power BI)

- SQLite database connected via **SQLite connector / ODBC**
- Single-table star-like schema optimized for slicing and filtering
- Calculated fields handled either in SQL or Power BI DAX

### Slicers Included
- Subscription Status
- Gender
- Category
- Discount Applied

These slicers dynamically update all visuals.

---

## 📈 Dashboard Features

### KPI Cards
- **Number of Customers**
- **Average Review Rating**
- **Average Purchase Amount**

### Visual Insights
- Sales by Category
- Revenue by Category
- Revenue by Age Group
- Sales by Age Group
- Subscription Status Distribution
- Shipping Type Distribution

The dashboard layout is optimized for executive-level readability.

---

## 💡 Business Insights & Recommendations

### 🔹 1. Middle-Age & Adult Customers Drive Revenue
- These segments generate the highest revenue
- **Recommendation:** Target loyalty programs and premium offers toward ages 26–65

---

### 🔹 2. Clothing Is the Top Revenue Category
- Clothing dominates both sales volume and revenue
- **Recommendation:**
  - Expand clothing SKUs
  - Offer bundled promotions with accessories

---

### 🔹 3. Subscription Penetration Is Low (27%)
- Majority of customers are non-subscribers
- **Recommendation:**
  - Introduce tiered subscription benefits
  - Offer discounts or free shipping for first-time subscribers

---

### 🔹 4. Discounts Influence Purchasing Behavior
- Discount usage correlates with higher purchase frequency
- **Recommendation:**
  - Personalize discount campaigns
  - Avoid blanket discounts to protect margins

---

### 🔹 5. Shipping Preferences Are Balanced
- No dominant shipping method
- **Recommendation:**
  - Maintain diverse shipping options
  - Promote faster shipping for high-value customers

---

## 🚀 Future Enhancements

- Add time-series analysis (monthly trends)
- Build a customer lifetime value (CLV) model
- Predict churn based on frequency and subscription status
- Automate data refresh pipeline

---

## ✅ Conclusion

This project demonstrates a **full analytics lifecycle**:

✔ Raw data → Cleaned with Python
✔ Structured storage with SQLite
✔ SQL-based feature engineering
✔ Interactive Power BI dashboard
✔ Actionable business insights

It is designed to be **scalable, reproducible, and business-ready**.

---

📌 *Dashboard shown above reflects the final output of this pipeline.*

