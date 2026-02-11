from datetime import timezone
import logging
from app.core.firebase import get_firestore
from app.utils.invoice_utils import get_current_financial_year, format_invoice_number
from google.cloud import firestore

logger = logging.getLogger(__name__)


class InvoiceService:
    def __init__(self):
        self.db = get_firestore()

    def get_invoice_number_preview(self) -> dict:
        """
        Generate a preview invoice number for display on page load.
        This ONLY reads the current counter and shows a preview.
        The counter is NOT updated here - it will be updated when invoice is actually created.

        Returns:
            dict: Contains invoice_number and financial_year

        Raises:
            Exception: If unable to generate invoice number
        """
        try:
            current_fy = get_current_financial_year()
            count_ref = self.db.collection("Count").document("count")

            # Read current document (no update)
            doc = count_ref.get()

            if not doc.exists:
                # Document doesn't exist, start from 1
                inv_no = 1
                fy = current_fy
            else:
                # Document exists, convert to dict and check financial year
                data = doc.to_dict() or {}
                stored_fy = data.get("fy")
                inv_no = data.get("inv_no", 0)

                if stored_fy == current_fy:
                    # Same FY, show next number (without updating)
                    inv_no += 1
                else:
                    # Different FY, show 1
                    inv_no = 1

                fy = current_fy

            # Format and return invoice number
            invoice_number = format_invoice_number(inv_no, fy)

            logger.info(
                f"Generated preview invoice number: {invoice_number} for FY: {fy}"
            )

            return {
                "invoice_number": invoice_number,
                "financial_year": fy,
                "sequence_number": inv_no,
            }

        except Exception as e:
            logger.error(f"Error generating invoice number: {str(e)}")
            raise Exception(f"Failed to generate invoice number: {str(e)}")

    def increment_invoice_counter(self) -> dict:
        """
        Increment the invoice counter in Firebase when an invoice is actually created.
        Uses Firestore transaction for thread-safe concurrent operations.

        Returns:
            dict: Contains the saved invoice_number, financial_year, and sequence_number

        Raises:
            Exception: If unable to increment counter
        """
        try:
            current_fy = get_current_financial_year()
            count_ref = self.db.collection("Count").document("count")

            # Define and execute transaction function
            transaction = self.db.transaction()

            @firestore.transactional
            def update_in_transaction(transaction):
                # Read current document using transaction
                doc = count_ref.get(transaction=transaction)

                if not doc.exists:
                    # Document doesn't exist, create it with inv_no = 1
                    initial_data = {"inv_no": 1, "fy": current_fy}
                    transaction.set(count_ref, initial_data)
                    inv_no = 1
                    fy = current_fy
                else:
                    # Document exists, convert to dict and check financial year
                    data = doc.to_dict() or {}
                    stored_fy = data.get("fy")
                    inv_no = data.get("inv_no", 0)

                    if stored_fy == current_fy:
                        # Same FY, increment invoice number
                        inv_no += 1
                    else:
                        # Different FY, reset to 1
                        inv_no = 1

                    # Update the document
                    transaction.update(count_ref, {"inv_no": inv_no, "fy": current_fy})
                    fy = current_fy

                return inv_no, fy

            # Execute transaction
            inv_no, fy = update_in_transaction(transaction)

            # Format and return invoice number
            invoice_number = format_invoice_number(inv_no, fy)

            logger.info(f"Incremented invoice counter: {invoice_number} for FY: {fy}")

            return {
                "invoice_number": invoice_number,
                "financial_year": fy,
                "sequence_number": inv_no,
            }

        except Exception as e:
            logger.error(f"Error incrementing invoice counter: {str(e)}")
            raise Exception(f"Failed to increment invoice counter: {str(e)}")

    def create_invoice(self, invoice_data: dict) -> dict:
        """
        Create a new invoice and save it to Firestore.
        Also increments the invoice counter.

        Args:
            invoice_data: Invoice data containing buyer, consignee, items, totals

        Returns:
            dict: Created invoice with ID

        Raises:
            Exception: If unable to create invoice
        """
        try:
            from datetime import datetime
            import uuid

            # Generate invoice ID and number
            # invoice_id = (
            #     f"inv_{datetime.now().strftime('%Y%m%d%H%M%S')}_{uuid.uuid4().hex[:8]}"
            # )

            # Get and increment invoice counter
            current_fy = get_current_financial_year()
            count_ref = self.db.collection("Count").document("count")

            # Define and execute transaction function for creating invoice
            transaction = self.db.transaction()

            @firestore.transactional
            def update_in_transaction(transaction):
                doc = count_ref.get(transaction=transaction)

                if not doc.exists:
                    initial_data = {"inv_no": 1, "fy": current_fy}
                    transaction.set(count_ref, initial_data)
                    inv_no = 1
                else:
                    data = doc.to_dict() or {}
                    stored_fy = data.get("fy")
                    inv_no = data.get("inv_no", 0)

                    if stored_fy == current_fy:
                        inv_no += 1
                    else:
                        inv_no = 1

                    transaction.update(count_ref, {"inv_no": inv_no, "fy": current_fy})

                return inv_no

            # Execute transaction to get next invoice number
            inv_no = update_in_transaction(transaction)

            # Format invoice number
            invoice_number = format_invoice_number(inv_no, current_fy)

            # Save to Firestore
            invoice_id = self.db.collection("invoices").document()
            # Prepare invoice document
            invoice_doc = {
                "id": invoice_id.id,
                "invoice_number": invoice_number,
                "invoice_date": invoice_data.get("invoice_date"),
                "po_number": invoice_data.get("po_number", ""),
                "buyer": invoice_data.get("buyer", {}),
                "consignee": invoice_data.get("consignee", {}),
                "items": invoice_data.get("items", []),
                "totals": invoice_data.get("totals", {}),
                "meta": {
                    "created_at": datetime.now(timezone.utc),
                    "updated_at": None,
                },
            }

            # Save the invoice document
            invoice_id.set(invoice_doc)

            logger.info(f"Invoice created: {invoice_number} with ID: {invoice_id.id}")

            return invoice_doc

        except Exception as e:
            logger.error(f"Error creating invoice: {str(e)}")
            raise Exception(f"Failed to create invoice: {str(e)}")
