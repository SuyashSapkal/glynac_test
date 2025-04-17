from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from jose import JWTError, jwt
from datetime import datetime, timedelta, timezone
from app.db.database import get_db
from app.db.models.employee import Employee

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


# JWT token generator
def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.now(tz=timezone.utc) + (
        expires_delta or timedelta(minutes=30)
    )  # You can make this configurable in your settings
    to_encode.update({"exp": expire})
    return jwt.encode(
        to_encode, "SECRET_KEY", algorithm="HS256"
    )  # Make sure to use your real secret key


# Auth route
@router.post("/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    # Query the employee by email
    employee = db.query(Employee).filter(Employee.email == form_data.username).first()

    if not employee:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    # Compare the passwords (in a real application, hash and check)
    if form_data.password != employee.password:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    # Create and return the JWT token
    access_token = create_access_token(data={"sub": employee.email})
    return {"access_token": access_token, "token_type": "bearer"}


# Dependency to get the current user
def get_current_user(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            token, "SECRET_KEY", algorithms=["HS256"]
        )  # Use your secret key and algorithm
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        # Get the user by email from the database
        user = db.query(Employee).filter(Employee.email == email).first()
        if user is None:
            raise credentials_exception
        return user
    except JWTError:
        raise credentials_exception
