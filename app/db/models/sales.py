from sqlalchemy import Column, Integer, Float, Date, ForeignKey
from sqlalchemy.orm import relationship
from app.db.database import Base
from app.db.models.employee import Employee


class Sales(Base):
    __tablename__ = "sales"

    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey("employees.id"))
    total_sales = Column(Float, nullable=False)
    sales_target = Column(Float, nullable=False)
    date = Column(Date, nullable=False)

    employee = relationship("Employee", back_populates="sales")

    def __repr__(self):
        return f"<Sales(id={self.id}, employee_id={self.employee_id}, total_sales={self.total_sales}, sales_target={self.sales_target}, date={self.date})>"
