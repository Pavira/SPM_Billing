from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class ItemBase(BaseModel):
    name: str
    description: Optional[str] = None
    hsn_sac: Optional[str] = None
    uom: str
    rate: float
    gst_percentage: float


class ItemCreate(ItemBase):
    pass


class ItemUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    hsn_sac: Optional[str] = None
    uom: Optional[str] = None
    rate: Optional[float] = None
    gst_percentage: Optional[float] = None


class Item(ItemBase):
    id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
