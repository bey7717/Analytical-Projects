import sqlite3
import csv
from tabulate import tabulate


DB = r'C:\Users\bey77\OneDrive\Desktop\Projects\data_analysis\er_wait_time_project\database.db'
CSV = r'C:\Users\bey77\OneDrive\Desktop\Projects\data_analysis\er_wait_time_project\ER Wait Time Dataset.csv'

conn = sqlite3.connect(DB)
cur = conn.cursor()

cur.execute("DROP TABLE IF EXISTS er;")


cur.execute('''
CREATE TABLE er (
  visit_id TEXT,
  patient_id TEXT,
  hospital_id TEXT,
  hospital_name TEXT,
  region TEXT,
  visit_date DATE,
  day_of_week TEXT,
  season TEXT,
  time_of_day TEXT,
  urgency_level TEXT,
  nurse_to_patient_ratio INTEGER,
  specialist_availability INTEGER,
  facility_size_beds INTEGER,
  time_to_registration_min INTEGER,
  time_to_triage_min INTEGER,
  time_to_medical_professional_min INTEGER,
  total_wait_time_min INTEGER,
  patient_outcome TEXT,
  patient_satisfaction INTEGER
);
''')


data_to_insert = []

with open(CSV, 'r', encoding='utf-8-sig') as file:
    reader = csv.DictReader(file)
    reader.fieldnames = [h.strip().replace(" ", "_").replace("(", "").replace(")", "").replace("-", "_").lower() 
                         for h in reader.fieldnames]

    for row in reader:
        record = (
            row['visit_id'], 
            row['patient_id'], 
            row['hospital_id'], 
            row['hospital_name'], 
            row['region'], 
            row['visit_date'], 
            row['day_of_week'], 
            row['season'], 
            row['time_of_day'], 
            row['urgency_level'], 
            row['nurse_to_patient_ratio'], 
            row['specialist_availability'], 
            row['facility_size_beds'], 
            row['time_to_registration_min'], 
            row['time_to_triage_min'], 
            row['time_to_medical_professional_min'], 
            row['total_wait_time_min'], 
            row['patient_outcome'], 
            row['patient_satisfaction']
        )
        data_to_insert.append(record)

query = "INSERT INTO er VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
cur.executemany(query, data_to_insert)
conn.commit()

# testing to see if dataset works
# cur.execute("SELECT COUNT(hospital_name) as count FROM er LIMIT 5")
# rows = cur.fetchall()
# col = [description[0] for description in cur.description]
# print(tabulate(rows, headers=col, tablefmt='grid'))


# does a lower nurse-to-patient ratio actually lead to faster care?
# cur.execute("SELECT nurse_to_patient_ratio, " \
# "COUNT(*) as total_visits, " \
# "ROUND(AVG(patient_satisfaction), 2) as avg_patient_satisfaction, " \
# "ROUND(AVG(total_wait_time_min), 2) as avg_wait_time " \
# "FROM er " \
# "GROUP BY nurse_to_patient_ratio " \
# "ORDER BY nurse_to_patient_ratio ")
# rows = cur.fetchall()
# col = [description[0] for description in cur.description]
# print(tabulate(rows, headers=col, tablefmt='grid'))

# peak volume and how that affects satisfaction 
# cur.execute("SELECT time_of_day, " \
# "specialist_availability, " \
# "ROUND(AVG(patient_satisfaction), 2) as avg_patient_satisfaction, " \
# "ROUND(AVG(total_wait_time_min), 2) as avg_wait_time " \
# "FROM er " \
# "WHERE time_of_day IN ('Morning', 'Afternoon', 'Evening', 'Night') "\
# "GROUP BY time_of_day, specialist_availability " \
# "ORDER BY avg_patient_satisfaction DESC" \
# )
# rows = cur.fetchall()
# col = [description[0] for description in cur.description]
# print(tabulate(rows, headers=col, tablefmt='grid'))


# check to see if the region matters for wait time and patient satifcation
# cur.execute("SELECT region, " \
# "ROUND(AVG(patient_satisfaction), 2) as avg_patient_satisfaction, " \
# "ROUND(AVG(total_wait_time_min), 2) as avg_wait_time " \
# "FROM er " \
# "GROUP BY region " \
# "ORDER BY avg_patient_satisfaction DESC " \
# )
# rows = cur.fetchall()
# col = [description[0] for description in cur.description]
# print(tabulate(rows, headers=col, tablefmt='grid'))





conn.close()
