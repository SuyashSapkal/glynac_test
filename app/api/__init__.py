from fastapi import APIRouter
from app.api import auth, employee, department, sales, attendance, leave

api_router = APIRouter()
api_router.include_router(auth.router, prefix="/auth", tags=["Auth"])
api_router.include_router(employee.router, prefix="/employee", tags=["Employee"])
api_router.include_router(department.router, prefix="/department", tags=["Department"])
api_router.include_router(sales.router, prefix="/sales", tags=["Sales"])
api_router.include_router(attendance.router, prefix="/attendance", tags=["Attendance"])
api_router.include_router(leave.router, prefix="/leave", tags=["leave"])
