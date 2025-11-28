import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
df=pd.read_csv('hospitalManagement.csv')
html = """
<div class="patient">
  <h2>Patient Name: Priya Verma</h2>
  <p>Age: 34</p>
  <p>Gender: F</p>
  <p>Diagnosis: Typhoid</p>
  <p>Bill Amount: 9500</p>
  <p>Admission Date: 2025-07-10</p>
  <p>Discharge Date: 2025-07-15</p>
</div>
"""
soup = BeautifulSoup(html, 'lxml')
name = soup.find('h2').get_text().split(':',1)[1].strip()
patient_info = {'Name': name}
for p in soup.find_all('p'):
    text = p.get_text()
    if ':' in text:
        key, val = text.split(':', 1)
        patient_info[key.strip().lower()] = val.strip()

new_row = {
    'Patient_ID': int(df['Patient_ID'].max()) + 1 if not df.empty else 1,
    'Name': patient_info.get('name', patient_info.get('patient name', name)),
    'Age': int(patient_info.get('age', 0)),
    'Gender': patient_info.get('gender', ''),
    'Diagnosis': patient_info.get('diagnosis', ''),
    'Bill (INR)': float(patient_info.get('bill amount', 0.0)),
    'Admission_Date': pd.to_datetime(patient_info.get('admission date', None)),
    'Discharge_Date': pd.to_datetime(patient_info.get('discharge date', None))
}
new_df = pd.DataFrame([new_row])
df = pd.concat([df, new_df], ignore_index=True)
print("\nUpdated dataset (last rows):")
print(df.tail())
df.to_csv('hospital_patients_updated.csv', index=False)
print("\nSaved to hospital_patients_updated.csv")