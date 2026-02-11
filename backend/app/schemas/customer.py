from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class CustomerBase(BaseModel):
    name: str
    email: str
    phone: Optional[str] = None
    address: Optional[str] = None
    gstin: Optional[str] = None


class CustomerCreate(CustomerBase):
    pass


class CustomerUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    gstin: Optional[str] = None


class Customer(CustomerBase):
    id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
