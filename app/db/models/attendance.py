from sqlalchemy import Column, Integer, Date, Time, ForeignKey, String
from sqlalchemy.orm import relationship
from app.db.database import Base
from app.db.models.employee import Employee


class Attendance(Base):
    __tablename__ = "attendance"

    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey("employees.id"))
    date = Column(Date, nullable=False)
    check_in_time = Column(Time, nullable=True)
    check_out_time = Column(Time, nullable=True)
    status = Column(String, nullable=True)

    employee = relationship("Employee", back_populates="attendance")

    def __repr__(self):
        return f"<Attendance(id={self.id}, employee_id={self.employee_id}, date={self.date}, check_in_time={self.check_in_time}, check_out_time={self.check_out_time}, status={self.status})>"
