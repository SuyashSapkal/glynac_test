import random
from datetime import date, timedelta, datetime
from faker import Faker
from dotenv import load_dotenv
from sqlalchemy.orm import Session
import bcrypt
import csv

from app.db.database import Base, engine, SessionLocal
from app.db.models import employee, department, sales, attendance, leave

# Load .env variables
load_dotenv()

# Initialize Faker
fake = Faker("en_US")

# Create DB tables
Base.metadata.create_all(bind=engine)

# Start DB session
db: Session = SessionLocal()

# Departments
DEPARTMENTS = ["Sales", "Marketing", "Customer Success", "Operations", "HR"]


def seed_departments() -> list[department.Department]:
    dept_objs: list[department.Department] = []
    for dept_name in DEPARTMENTS:
        dept = department.Department(name=dept_name)
        db.add(dept)
        dept_objs.append(dept)
    db.commit()
    return dept_objs


def seed_employees(departments: list[department.Department]) -> list[employee.Employee]:
    employees: list[employee.Employee] = []

    with open("temp.csv", mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["first_name", "last_name", "email", "password"])  # header

        for _ in range(100):
            dept = random.choice(departments)
            first_name = fake.first_name()
            last_name = fake.last_name()
            unique_id = random.randint(1000, 9999)
            email = f"{first_name.lower()}.{last_name.lower()}{unique_id}@example.com"
            raw_password = fake.password(length=10)
            hashed_password = bcrypt.hashpw(raw_password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

            emp = employee.Employee(
                first_name=first_name,
                last_name=last_name,
                email=email,
                department_id=dept.id,
                date_joined=fake.date_between(start_date="-3y", end_date="-30d"),
                password=hashed_password,
            )
            db.add(emp)
            employees.append(emp)

            # Write plain password to CSV
            writer.writerow([first_name, last_name, email, raw_password])

    db.commit()
    return employees



def seed_sales(employees: list[employee.Employee]):
    for emp in employees:
        for _ in range(
            random.randint(5, 15)
        ):  # Random number of sales records for each employee
            year = random.randint(2022, 2024)  # Random year between 2022 and 2024
            month = random.randint(1, 12)  # Random month between 1 and 12
            day = random.randint(1, 28)  # Random day, 28 is safe for all months

            # Create a valid date using the year, month, and day
            sale_date = date(year, month, day)

            s = sales.Sales(
                employee_id=emp.id,
                total_sales=round(random.uniform(1000.0, 20000.0), 2),
                sales_target=round(random.uniform(1000.0, 20000.0), 2),
                date=sale_date,  # Store the full date
            )
            db.add(s)  # Add the sale record to the session

    db.commit()  # Commit all changes to the database


def seed_attendance(employees: list[employee.Employee]):
    for emp in employees:
        for day_offset in range(10):  # last 10 working days
            date_entry = date.today() - timedelta(days=day_offset)
            if date_entry.weekday() < 5:  # Weekday check
                att = attendance.Attendance(
                    employee_id=emp.id,
                    date=date_entry,
                    check_in_time=datetime.strptime(
                        f"{random.randint(8,10)}:{random.randint(0,59)}", "%H:%M"
                    ).time(),
                    check_out_time=datetime.strptime(
                        f"{random.randint(17,19)}:{random.randint(0,59)}", "%H:%M"
                    ).time(),
                    status="Present",
                )
                db.add(att)
    db.commit()


def seed_leaves(employees: list[employee.Employee]):
    for emp in random.sample(employees, k=30):  # ~30 employees with leave
        leave_record = leave.Leave(
            employee_id=emp.id,
            leave_type=random.choice(["Sick Leave", "Vacation", "Personal Leave"]),
            start_date=date.today() - timedelta(days=random.randint(5, 15)),
            end_date=date.today() - timedelta(days=random.randint(1, 4)),
            status=random.choice(["Approved", "Pending", "Rejected"]),
        )
        db.add(leave_record)
    db.commit()


def main():
    print("Seeding database...")
    departments = seed_departments()
    employees = seed_employees(departments)
    seed_sales(employees)
    seed_attendance(employees)
    seed_leaves(employees)
    print("Seeding complete.")


if __name__ == "__main__":
    main()
