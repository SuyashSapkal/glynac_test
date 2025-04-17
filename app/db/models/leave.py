from sqlalchemy import Column, Integer, Date, String, ForeignKey
from sqlalchemy.orm import relationship
from app.db.database import Base
from app.db.models.employee import Employee


class Leave(Base):
    __tablename__ = "leave"

    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey("employees.id"))
    leave_type = Column(String, nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    status = Column(String, nullable=False)  # E.g., "Approved", "Pending", "Rejected"

    employee = relationship("Employee", back_populates="leave")

    def __repr__(self):
        return f"<Leave(id={self.id}, employee_id={self.employee_id}, leave_type={self.leave_type}, start_date={self.start_date}, end_date={self.end_date}, status={self.status})>"
