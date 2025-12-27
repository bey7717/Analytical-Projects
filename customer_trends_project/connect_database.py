import sqlite3
import csv
from tabulate import tabulate


DB = r'C:\Users\bey77\OneDrive\Desktop\Projects\data_analysis\customer_trends_project\database.db'
CSV = r'C:\Users\bey77\OneDrive\Desktop\Projects\data_analysis\customer_trends_project\customer_shopping_behavior.csv'

# Connect to SQLite
conn = sqlite3.connect(DB)
cur = conn.cursor()

# Drop table if it exists (for clean rebuild)
cur.execute("DROP TABLE IF EXISTS customer;")

# Create table with proper types
cur.execute('''
CREATE TABLE customer (
    customer_id TEXT,
    age INTEGER,
    gender TEXT,
    item_purchased TEXT,
    category TEXT,
    purchase_amount REAL,
    location TEXT,
    size TEXT,
    color TEXT,
    season TEXT,
    review_rating REAL,
    subscription_status TEXT,
    shipping_type TEXT,
    discount_applied_txt TEXT,
    promo_code_used TEXT,
    previous_purchases INTEGER,
    payment_method TEXT,
    frequency_of_purchases TEXT,
    purchase_freq_days INTEGER
)
''')

# Open CSV and normalize headers
with open(CSV, 'r', newline='', encoding='utf-8-sig') as file:
    reader = csv.DictReader(file)
    reader.fieldnames = [h.strip().replace(" ", "_").replace("(", "").replace(")", "").lower() for h in reader.fieldnames]

    for row in reader:
        # Clean text fields
        discount = row['discount_applied'].strip() if row['discount_applied'] else 'No'
        frequency = row['frequency_of_purchases'].strip() if row['frequency_of_purchases'] else None

        # Map frequency to days
        freq_days_map = {
            'Weekly': 7,
            'Fortnightly': 14,
            'Monthly': 30,
            'Quarterly': 90,
            'Annually': 365
        }
        purchase_freq_days = freq_days_map.get(frequency, None)

        # Insert row into table
        cur.execute('''
            INSERT INTO customer (
                customer_id, age, gender, item_purchased, category,
                purchase_amount, location, size, color, season,
                review_rating, subscription_status, shipping_type,
                discount_applied_txt, promo_code_used, previous_purchases,
                payment_method, frequency_of_purchases, purchase_freq_days
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            row['customer_id'], row['age'], row['gender'], row['item_purchased'], row['category'],
            row['purchase_amount_usd'], row['location'], row['size'], row['color'], row['season'],
            row['review_rating'], row['subscription_status'], row['shipping_type'],
            discount, row['promo_code_used'], row['previous_purchases'],
            row['payment_method'], frequency, purchase_freq_days
        ))

# Commit and close connection
conn.commit()


#testing to see if it works
# cur.execute("SELECT customer_id, item_purchased, category, purchase_amount FROM customer LIMIT 5")
# rows = cur.fetchall()
# col = [description[0] for description in cur.description]
# print(tabulate(rows, headers=col, tablefmt='grid'))

# Q1: What is the total revenue generated male vs female customers?
# cur.execute("SELECT gender, SUM(purchase_amount) as total_rev FROM customer GROUP BY gender")
# rows = cur.fetchall()
# col = [description[0] for description in cur.description]
# print(tabulate(rows, headers=col, tablefmt='grid'))


# Q2 Which customers used a discount but still spent more than the average purchase amount?
# cur.execute("SELECT customer_id, purchase_amount FROM customer WHERE discount_applied = 'Yes' AND purchase_amount >= (SELECT AVG(purchase_amount) FROM customer)")
# rows = cur.fetchall()
# col = [description[0] for description in cur.description]
# print(tabulate(rows, headers=col, tablefmt='grid'))


# Q3 What are the top 5 products with the highest average review rating
# cur.execute("SELECT ROUND(AVG(review_rating), 2) as rating, item_purchased FROM customer " \
# "GROUP BY item_purchased ORDER BY (rating) DESC LIMIT 5")
# rows = cur.fetchall()
# col = [description[0] for description in cur.description]
# print(tabulate(rows, headers=col, tablefmt='grid'))

#Q4 compare the average purchase amount between Standard and Express shipping
# cur.execute("SELECT ROUND(AVG(purchase_amount), 2) as avg_revenue, shipping_type " \
# "FROM customer " \
# "WHERE shipping_type IN ('Standard', 'Express') " \
# "GROUP BY shipping_type")
# rows = cur.fetchall()
# col = [description[0] for description in cur.description]
# print(tabulate(rows, headers=col, tablefmt='grid'))

#Q5 Do subscribed customers spend more? 
# Compare average spending and total revenue between subscribers and non-subscribers
# cur.execute("SELECT subscription_status, COUNT(customer_id) as total_customer, ROUND(AVG(purchase_amount), 2) as average_spending, ROUND(SUM(purchase_amount), 0) as total_rev " \
# "FROM customer " \
# "GROUP BY subscription_status " \
# "ORDER BY total_rev, average_spending DESC ")
# rows = cur.fetchall()
# col = [description[0] for description in cur.description]
# print(tabulate(rows, headers=col, tablefmt='grid'))

# Q6 Which 5 products have the highest percentage of purchases with discounts applied?
# cur.execute("SELECT item_purchased, ROUND(100 * SUM(CASE WHEN discount_applied = 'Yes' THEN 1 ELSE 0 END) / COUNT(*), 2) as discount_rate " \
# "FROM customer " \
# "GROUP BY item_purchased " \
# "ORDER BY discount_rate desc " \
# "LIMIT 5")
# rows = cur.fetchall()
# col = [description[0] for description in cur.description]
# print(tabulate(rows, headers=col, tablefmt='grid'))

# Q7 What is the revenue contribution of each age group?
# cur.execute("SELECT CASE "  \
# "WHEN age BETWEEN 18 AND 24 THEN 'Young Adult' " \
# "WHEN age BETWEEN 25 AND 44 THEN 'Adult' " \
# "WHEN age BETWEEN 45 AND 64 THEN 'Middle-age' " \
# "WHEN age BETWEEN 65 AND 120 THEN 'Senior' " \
# "END AS age_group, " \
# "COUNT(*) as total_customers, " \
# "ROUND(AVG(purchase_amount), 2) as avg_spending " \
# "FROM customer " \
# "GROUP by age_group " \
# "ORDER BY age_group DESC")
# rows = cur.fetchall()
# col = [description[0] for description in cur.description]
# print(tabulate(rows, headers=col, tablefmt='grid'))

# cur.execute(
#     "ALTER TABLE customer "
#     "ADD COLUMN purchase_freq_day INTEGER"
# )

# cur.execute("""
#     UPDATE customer
#     SET purchase_freq_day =
#         CASE frequency_of_purchases
#             WHEN 'Weekly' THEN 7
#             WHEN 'Fortnightly' THEN 14
#             WHEN 'Bi-Weekly' THEN 14
#             WHEN 'Monthly' THEN 30
#             WHEN 'Every 3 Months' THEN 90
#             WHEN 'Quarterly' THEN 90
#             WHEN 'Annually' THEN 365
#             ELSE NULL
#         END
# """)
# conn.commit()

# cur.execute("""
#     SELECT frequency_of_purchases, purchase_freq_day
#     FROM customer
#     GROUP BY frequency_of_purchases
# """)
# print(cur.fetchall())

# cur.execute("SELECT discount_applied, COUNT(*) " \
# "FROM customer " \
# "GROUP BY discount_applied ")
# rows = cur.fetchall()
# col = [description[0] for description in cur.description]
# print(tabulate(rows, headers=col, tablefmt='grid'))

# cur.execute("PRAGMA table_info(customer);")
# columns = cur.fetchall()
# for col in columns:
#     print(col)


# cur.execute("ALTER TABLE customer " \
# "ADD COLUMN discount_applied_txt TEXT;")

# cur.execute("""
# UPDATE customer
# SET discount_applied_txt =
#     CASE
#         WHEN discount_applied = 1 THEN 'Yes'
#         WHEN discount_applied = 0 THEN 'No'
#         ELSE 'Yes'  -- or use original CSV value if available
#     END;
#             """)


conn.close()



