from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
from app.services.invoice_service import InvoiceService
import logging
from pathlib import Path

from app.core.firebase import get_firestore

logger = logging.getLogger(__name__)

router = APIRouter()
invoice_service = InvoiceService()


# Pydantic models for request validation
class BuyerConsignee(BaseModel):
    id: str
    name: str
    gstin: str
    address: Optional[str] = None
    email: Optional[str] = None
    panNumber: Optional[str] = None
    phone: Optional[str] = None


class InvoiceItem(BaseModel):
    item_id: str
    name: str
    hsn: str
    uom: str
    quantity: float
    rate: float
    gst_percentage: float
    amount: float


class InvoiceTotals(BaseModel):
    subtotal: float
    sgst: float
    cgst: float
    round_off: float
    rounded_total: int
    total: float
    amount_in_words: Optional[str] = None


class CreateInvoiceRequest(BaseModel):
    invoice_date: str
    po_number: Optional[str] = None
    buyer: BuyerConsignee
    consignee: BuyerConsignee
    items: List[InvoiceItem]
    totals: InvoiceTotals


@router.get("/preview-invoice-number")
def get_preview_invoice_number():
    """
    Get a preview invoice number for the form.
    This is used when the add invoice page loads.

    NOTE: This ONLY previews the next invoice number.
    The counter is NOT incremented here - it will be incremented when the invoice is actually created.

    """
    try:
        result = invoice_service.get_invoice_number_preview()
        return result
    except Exception as e:
        logger.error(f"Error getting preview invoice number: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/")
def create_invoice(invoice_request: CreateInvoiceRequest):
    """
    Create a new invoice.

    Request body should contain:
    - invoice_date: Date of invoice (YYYY-MM-DD)
    - po_number: PO number (optional)
    - buyer: Buyer details with id, name, gstin
    - consignee: Consignee details with id, name, gstin
    - items: Array of invoice items
    - totals: Invoice totals (subtotal, sgst, cgst, round_off, total)

    Returns:
    - Created invoice with ID and invoice_number
    """
    try:
        # Convert request to dict
        invoice_data = invoice_request.model_dump()

        # Create invoice
        result = invoice_service.create_invoice(invoice_data)

        return {
            "success": True,
            "message": "Invoice created successfully",
            "data": result,
        }
    except Exception as e:
        logger.error(f"Error creating invoice: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))


# ---------------------------
# Get All invoices and sort by date descending
# ---------------------------
@router.get("/")
def get_all_invoices():
    db = get_firestore()
    invoices_ref = db.collection("invoices")
    # Create_at field is inside meta
    invoices = invoices_ref.order_by("meta.created_at", direction="DESCENDING").stream()
    return {"invoices": [doc.to_dict() for doc in invoices]}


@router.get("/{invoice_id}")
def get_invoice(invoice_id: str):
    """
    Get a specific invoice by ID.

    Args:
        invoice_id: The invoice document ID

    Returns:
        Invoice document with all details
    """
    try:
        db = get_firestore()
        invoice_ref = db.collection("invoices").document(invoice_id)
        invoice_doc = invoice_ref.get()

        if not invoice_doc.exists:
            raise HTTPException(status_code=404, detail="Invoice not found")

        return {
            "success": True,
            "data": invoice_doc.to_dict(),
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching invoice: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/{invoice_id}")
def update_invoice(invoice_id: str, invoice_request: CreateInvoiceRequest):
    """
    Update an existing invoice.

    Args:
        invoice_id: The invoice document ID
        invoice_request: Updated invoice data

    Returns:
        Updated invoice document
    """
    try:
        db = get_firestore()
        invoice_ref = db.collection("invoices").document(invoice_id)
        invoice_doc = invoice_ref.get()

        if not invoice_doc.exists:
            raise HTTPException(status_code=404, detail="Invoice not found")

        # Prepare updated data
        from datetime import datetime, timezone

        invoice_data = invoice_request.model_dump()
        invoice_data["meta"] = {
            "created_at": invoice_doc.to_dict().get("meta", {}).get("created_at"),
            "updated_at": datetime.now(timezone.utc),
        }

        # Update the invoice
        invoice_ref.update(invoice_data)

        logger.info(f"Invoice updated: {invoice_id}")

        return {
            "success": True,
            "message": "Invoice updated successfully",
            "data": {**invoice_doc.to_dict(), **invoice_data},
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating invoice: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/{invoice_id}")
def delete_invoice(invoice_id: str):
    """
    Delete an invoice by ID.

    Args:
        invoice_id: The invoice document ID

    Returns:
        Success message
    """
    try:
        db = get_firestore()
        invoice_ref = db.collection("invoices").document(invoice_id)
        invoice_doc = invoice_ref.get()

        if not invoice_doc.exists:
            raise HTTPException(status_code=404, detail="Invoice not found")

        # Delete the invoice
        invoice_ref.delete()

        logger.info(f"Invoice deleted: {invoice_id}")

        return {
            "success": True,
            "message": "Invoice deleted successfully",
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting invoice: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{invoice_id}/pdf")
async def get_invoice_pdf(invoice_id: str, download: bool = False):
    """
    Generate and return PDF for an invoice using WeasyPrint

    Args:
        invoice_id: The invoice document ID

    Returns:
        PDF file as bytes
    """
    try:
        from fastapi.responses import StreamingResponse
        from jinja2 import Environment, FileSystemLoader
        from weasyprint import HTML, CSS

        # Get invoice from Firestore
        db = get_firestore()
        invoice_ref = db.collection("invoices").document(invoice_id)
        invoice_doc = invoice_ref.get()

        if not invoice_doc.exists:
            raise HTTPException(status_code=404, detail="Invoice not found")

        invoice_data = invoice_doc.to_dict()

        # Company details (same as in React template)
        company_details = {
            "name": "SPM ENGINEERING",
            "address": "347, SANGANUR ROAD, GANAPATHY, COIMBATORE",
            "gstin": "33AFHPE4773N1Z6",
            "state": "Tamil Nadu",
            "state_code": "33",
        }

        # Prepare data for template
        template_data = {
            "company": company_details,
            "invoice": invoice_data,
        }

        # Setup Jinja2 environment with absolute path
        backend_root = Path(__file__).resolve().parents[3]
        template_dir = backend_root / "app" / "templates"
        template_name = "SPM_bill.html"

        if not (template_dir / template_name).exists():
            raise HTTPException(
                status_code=500,
                detail=f"Template not found: {template_name} in {template_dir}",
            )

        env = Environment(loader=FileSystemLoader(str(template_dir)))
        template = env.get_template(template_name)

        # Render HTML from Jinja2 template
        html_content = template.render(template_data)

        # Get CSS
        css_path = template_dir / "spm_bill.css"
        css = CSS(string=css_path.read_text(encoding="utf-8"))

        # Generate PDF using WeasyPrint
        pdf_bytes = HTML(string=html_content).write_pdf(stylesheets=[css])

        filename = f"invoice_{invoice_data.get('invoice_number', 'document')}.pdf"
        disposition = "attachment" if download else "inline"

        # Return PDF
        return StreamingResponse(
            iter([pdf_bytes]),
            media_type="application/pdf",
            headers={
                "Content-Disposition": f'{disposition}; filename="{filename}"'
            },
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error generating PDF: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error generating PDF: {str(e)}")
