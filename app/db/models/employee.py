from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey
from app.db.database import Base
from sqlalchemy.orm import relationship


class Employee(Base):
    __tablename__ = "employees"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, index=True)
    last_name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    phone_number = Column(String)
    department_id = Column(Integer, ForeignKey("departments.id"))
    department = Column(String)
    position = Column(String)
    date_joined = Column(Date)
    salary = Column(Float)

    department = relationship("Department", back_populates="employees")
    sales = relationship("Sales", back_populates="employee")
    attendance = relationship("Attendance", back_populates="employee")
    leave = relationship("Leave", back_populates="employee")

    def __repr__(self):
        return f"<Employee(id={self.id}, first_name={self.first_name}, last_name={self.last_name}, email={self.email}, position={self.position})>"
