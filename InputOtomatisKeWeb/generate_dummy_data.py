import csv
import random
import pandas as pd
from datetime import datetime, timedelta

# Define possible values for each field
indonesian_names = [
    "Andi", "Budi", "Citra", "Dewi", "Eka", "Fajar", "Gita", "Hadi",
    "Ira", "Joko", "Lina", "Maya", "Nanda", "Oka", "Putri", "Rama",
    "Sari", "Tono", "Umi", "Vina", "Wahyu", "Yuni", "Zain"
]
passwords = ["pass123", "qwerty", "securepass", "letmein", "password1"]
genders = ["female", "male", "other"]
hobbies = ["membaca", "nonton", "tidur"]
jobs = ["pelajar", "mahasiswa", "pns", "swasta", "wiraswasta", "lainnya"]

# Generate random dates between 1980 and 2000
def random_date():
    start_date = datetime(1980, 1, 1)
    end_date = datetime(2000, 12, 31)
    delta = end_date - start_date
    random_days = random.randint(0, delta.days)
    return start_date + timedelta(days=random_days)

# Generate random comments
def random_comment():
    comments = [
        "Ini adalah komentar uji coba.",
        "Hanya mengisi formulir.",
        "Tidak ada komentar.",
        "Formulir ini bagus!",
        "Menunggu hasilnya."
    ]
    return random.choice(comments)

# Generate random filenames
def random_filename():
    return f"foto_{random.randint(1, 1000)}.jpg"

# Generate 500 dummy data entries
dummy_data = []
for i in range(500):
    name = random.choice(indonesian_names)
    password = random.choice(passwords)
    birthdate = random_date()
    comment = random_comment()
    gender = random.choice(genders)
    hobi = random.sample(hobbies, random.randint(1, len(hobbies)))
    job = random.choice(jobs)
    foto = random_filename()

    # Format hobi as a comma-separated string
    hobi_str = ",".join(hobi)

    dummy_data.append([name, password, birthdate, comment, gender, hobi_str, job, foto])

# Convert to DataFrame for better date handling
df = pd.DataFrame(dummy_data, columns=[
    'name', 'password', 'tanggal_lahir', 'comment', 'gender', 'hobi', 'job', 'foto'
])

# Convert dates to string with dd/mm/yyyy format
df['tanggal_lahir'] = df['tanggal_lahir'].dt.strftime('%d/%m/%Y')

# Save to CSV with pipe delimiter
df.to_csv('dummy_data.csv', index=False, sep='|')

print("500 dummy data entries generated successfully!")