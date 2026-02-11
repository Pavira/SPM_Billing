"""
Utility functions for invoice generation and management
"""

from datetime import datetime
from typing import Tuple


def get_current_financial_year() -> str:
    """
    Get the current Indian financial year.
    Indian FY runs from April 1 to March 31.

    Example:
        - Date between Apr 1, 2025 – Mar 31, 2026 → "2025-2026"

    Returns:
        str: Financial year in format "YYYY-YYYY"
    """
    today = datetime.now()
    current_year = today.year
    current_month = today.month

    # If current date is on or after April 1, FY starts this calendar year
    if current_month >= 4:
        fy_start = current_year
        fy_end = current_year + 1
    # If current date is before April 1, FY started last calendar year
    else:
        fy_start = current_year - 1
        fy_end = current_year

    return f"{fy_start}-{fy_end}"


def format_invoice_number(inv_no: int, financial_year: str) -> str:
    """
    Format the invoice number according to the pattern: INV/YY-YY/XXXX

    Args:
        inv_no: Invoice sequence number (integer)
        financial_year: Financial year in format "YYYY-YYYY"

    Returns:
        str: Formatted invoice number (e.g., "INV/25-26/0001")
    """
    # Extract last two digits from both years
    years = financial_year.split("-")
    fy_short = f"{years[0][-2:]}-{years[1][-2:]}"

    # Zero-pad invoice number to 4 digits
    inv_seq = str(inv_no).zfill(4)

    return f"INV/{fy_short}/{inv_seq}"
