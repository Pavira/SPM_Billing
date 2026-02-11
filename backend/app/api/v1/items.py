from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from datetime import datetime, timezone
from app.core.firebase import get_firestore

router = APIRouter()


# ---------------------------
# Schemas
# ---------------------------
class ItemCreate(BaseModel):
    name: str
    hsn_sac: str
    uom: str
    rate: str
    gst_percentage: str
    description: str


class ItemUpdate(BaseModel):
    name: str | None = None
    hsn_sac: str | None = None
    uom: str | None = None
    rate: str | None = None
    gst_percentage: str | None = None
    description: str | None = None


# ---------------------------
# Create Item
# ---------------------------
@router.post("/")
def create_item(payload: ItemCreate):
    try:
        db = get_firestore()
        doc_ref = db.collection("items").document()

        now = datetime.now(timezone.utc)

        doc_ref.set(
            {
                "id": doc_ref.id,
                "name": payload.name,
                "hsn_sac": payload.hsn_sac,
                "uom": payload.uom,
                "rate": payload.rate,
                "gst_percentage": payload.gst_percentage,
                "description": payload.description,
                "is_active": True,
                "created_at": now,
                "updated_at": None,
            }
        )

        return {
            "success": True,
            "item_id": doc_ref.id,
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ---------------------------
# Update Item
# ---------------------------
@router.put("/{item_id}")
def update_item(item_id: str, payload: ItemUpdate):
    db = get_firestore()
    print(item_id)
    doc_ref = db.collection("items").document(item_id)
    doc = doc_ref.get()

    if not doc.exists:
        raise HTTPException(status_code=404, detail="Item not found")

    update_data = {k: v for k, v in payload.model_dump().items() if v is not None}

    update_data["updated_at"] = datetime.now(timezone.utc)

    doc_ref.update(update_data)

    return {"success": True}


# ---------------------------
# Delete Item (Soft Delete)
# ---------------------------
@router.delete("/{item_id}")
def delete_item(item_id: str):
    db = get_firestore()
    doc_ref = db.collection("items").document(item_id)
    doc = doc_ref.get()

    if not doc.exists:
        raise HTTPException(status_code=404, detail="Item not found")

    doc_ref.update(
        {
            "is_active": False,
            "updated_at": datetime.now(timezone.utc),
        }
    )

    return {"success": True}


# ---------------------------
# Get All Items (Active Only) and sort by date descending
# ---------------------------
@router.get("/")
def get_all_items():
    db = get_firestore()
    items_ref = db.collection("items")
    query = items_ref.where("is_active", "==", True).order_by(
        "created_at", direction="DESCENDING"
    )
    docs = query.stream()

    items = []
    for doc in docs:
        item_data = doc.to_dict()
        item_data["item_id"] = doc.id
        items.append(item_data)

    return {"items": items}


# ---------------------------


# ---------------------------
# Get Item by ID
# ---------------------------
@router.get("/{item_id}")
def get_item_by_id(item_id: str):
    db = get_firestore()
    doc_ref = db.collection("items").document(item_id)
    doc = doc_ref.get()

    if not doc.exists:
        raise HTTPException(status_code=404, detail="Item not found")

    item_data = doc.to_dict()
    item_data["id"] = doc.id

    return {"item": item_data}


# ---------------------------
