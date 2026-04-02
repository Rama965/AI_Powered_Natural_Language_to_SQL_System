import sqlite3
import random
from faker import Faker
from datetime import datetime, timedelta

fake = Faker()

conn = sqlite3.connect("clinic.db")
cursor = conn.cursor()


def create_tables():
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS patients(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        first_name TEXT NOT NULL,
        last_name TEXT NOT NULL,
        email TEXT,
        phone TEXT,
        date_of_birth DATE,
        gender TEXT,
        city TEXT,
        registered_date DATE
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS doctors(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        specialization TEXT,
        department TEXT,
        phone TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS appointments(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        patient_id INTEGER,
        doctor_id INTEGER,
        appointment_date DATETIME,
        status TEXT,
        notes TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS treatments(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        appointment_id INTEGER,
        treatment_name TEXT,
        cost REAL,
        duration_minutes INTEGER
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS invoices(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        patient_id INTEGER,
        invoice_date DATE,
        total_amount REAL,
        paid_amount REAL,
        status TEXT
    )
    """)


def insert_doctors():
    specializations = [
        "Dermatology",
        "Cardiology",
        "Orthopedics",
        "General",
        "Pediatrics"
    ]

    doctor_ids = []

    for _ in range(15):
        name = fake.name()
        spec = random.choice(specializations)

        cursor.execute("""
        INSERT INTO doctors(name, specialization, department, phone)
        VALUES (?, ?, ?, ?)
        """, (name, spec, spec + " Dept", fake.phone_number()))

        doctor_ids.append(cursor.lastrowid)

    return doctor_ids


def insert_patients():
    cities = [
        "Hyderabad",
        "Bangalore",
        "Chennai",
        "Mumbai",
        "Delhi",
        "Pune",
        "Vizag",
        "Kolkata"
    ]

    patient_ids = []

    for _ in range(200):

        email = fake.email() if random.random() > 0.2 else None
        phone = fake.phone_number() if random.random() > 0.2 else None

        cursor.execute("""
        INSERT INTO patients(
        first_name,last_name,email,phone,date_of_birth,
        gender,city,registered_date
        )
        VALUES(?,?,?,?,?,?,?,?)
        """, (
            fake.first_name(),
            fake.last_name(),
            email,
            phone,
            fake.date_of_birth(minimum_age=5, maximum_age=80),
            random.choice(["M", "F"]),
            random.choice(cities),
            fake.date_between(start_date="-1y", end_date="today")
        ))

        patient_ids.append(cursor.lastrowid)

    return patient_ids


def insert_appointments(patient_ids, doctor_ids):
    statuses = [
        "Scheduled",
        "Completed",
        "Cancelled",
        "No-Show"
    ]

    appointment_ids = []

    for _ in range(500):

        appointment_date = fake.date_time_between(
            start_date="-12m",
            end_date="now"
        )

        notes = fake.text() if random.random() > 0.3 else None

        cursor.execute("""
        INSERT INTO appointments(
        patient_id,doctor_id,appointment_date,status,notes
        )
        VALUES(?,?,?,?,?)
        """, (
            random.choice(patient_ids),
            random.choice(doctor_ids),
            appointment_date,
            random.choice(statuses),
            notes
        ))

        appointment_ids.append(cursor.lastrowid)

    return appointment_ids


def insert_treatments(appointment_ids):
    treatment_names = [
        "Consultation",
        "X-Ray",
        "MRI",
        "Blood Test",
        "Skin Therapy",
        "Physiotherapy"
    ]

    for appt_id in random.sample(appointment_ids, 350):

        cursor.execute("""
        INSERT INTO treatments(
        appointment_id,treatment_name,cost,duration_minutes
        )
        VALUES(?,?,?,?)
        """, (
            appt_id,
            random.choice(treatment_names),
            random.randint(50, 5000),
            random.randint(10, 120)
        ))


def insert_invoices(patient_ids):

    statuses = ["Paid", "Pending", "Overdue"]

    for _ in range(300):

        total = random.randint(200, 10000)

        paid = total if random.random() > 0.3 else random.randint(0, total)

        status = "Paid" if paid == total else random.choice(statuses)

        cursor.execute("""
        INSERT INTO invoices(
        patient_id,invoice_date,total_amount,
        paid_amount,status
        )
        VALUES(?,?,?,?,?)
        """, (
            random.choice(patient_ids),
            fake.date_between(start_date="-12m", end_date="today"),
            total,
            paid,
            status
        ))


def main():

    create_tables()

    doctor_ids = insert_doctors()

    patient_ids = insert_patients()

    appointment_ids = insert_appointments(patient_ids, doctor_ids)

    insert_treatments(appointment_ids)

    insert_invoices(patient_ids)

    conn.commit()

    print("Created 200 patients")
    print("Created 15 doctors")
    print("Created 500 appointments")
    print("Created 350 treatments")
    print("Created 300 invoices")

    conn.close()


if __name__ == "__main__":
    main()