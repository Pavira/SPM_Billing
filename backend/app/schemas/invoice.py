from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class InvoiceItemBase(BaseModel):
    item_id: str
    quantity: float
    rate: float
    hsn_sac: Optional[str] = None
    gst_percentage: float
    uom: str


class InvoiceBase(BaseModel):
    invoice_number: str
    customer_id: str
    invoice_date: datetime
    due_date: datetime
    items: List[InvoiceItemBase]
    subtotal: float
    sgst: float
    cgst: float
    round_off: float = 0
    rounded_total: Optional[int] = None
    total: float
    amount_in_words: Optional[str] = None
    notes: Optional[str] = None


class InvoiceCreate(InvoiceBase):
    pass


class InvoiceUpdate(BaseModel):
    invoice_number: Optional[str] = None
    customer_id: Optional[str] = None
    invoice_date: Optional[datetime] = None
    due_date: Optional[datetime] = None
    items: Optional[List[InvoiceItemBase]] = None
    subtotal: Optional[float] = None
    sgst: Optional[float] = None
    cgst: Optional[float] = None
    round_off: Optional[float] = None
    rounded_total: Optional[int] = None
    total: Optional[float] = None
    amount_in_words: Optional[str] = None
    notes: Optional[str] = None


class Invoice(InvoiceBase):
    id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
