from datetime import datetime
from dateutil import parser
import re

def extract_months(durations):
    current_date = datetime.now()
    results = []
    
    for duration in durations:
        duration = duration.strip()
        
        # Standard year range (e.g., "2020-2024", "2020 to 2024")
        match = re.match(r"(\d{4})\s*(?:-|–|to)\s*(\d{4}|Present|Ongoing)", duration, re.IGNORECASE)
        if match:
            start_year = int(match.group(1))
            end_year = current_date.year if match.group(2).lower() in ["present", "ongoing"] else int(match.group(2))
            months = (end_year - start_year) * 12
            results.append(f"{months} months")
            continue

        # Flexible full date parsing (e.g., "10 Dec 2018 to 5 Nov 2024", "12 Sep 2020 - Present", "Sep 2023 - Ongoing")
        match = re.match(r"([\w\s\d,]+?)\s*(?:-|–|to)\s*([\w\s\d,]+)", duration, re.IGNORECASE)
        if match:
            try:
                start_date = parser.parse(match.group(1), dayfirst=True)
                end_date_raw = match.group(2).strip().lower()
                end_date = current_date if end_date_raw in ["present", "ongoing"] else parser.parse(match.group(2), dayfirst=True)
                months = (end_date.year - start_date.year) * 12 + (end_date.month - start_date.month)
                results.append(f"{months} months")
                continue
            except Exception:
                pass

        # MM/DD/YYYY date ranges (e.g., "05/13/2020 - 06/16/2021")
        match = re.match(r"(\d{2}/\d{2}/\d{4})\s*(?:-|–|to)\s*(\d{2}/\d{2}/\d{4}|Present|Ongoing)", duration, re.IGNORECASE)
        if match:
            start_date = datetime.strptime(match.group(1), "%m/%d/%Y")
            end_date = current_date if match.group(2).lower() in ["present", "ongoing"] else datetime.strptime(match.group(2), "%m/%d/%Y")
            months = (end_date.year - start_date.year) * 12 + (end_date.month - start_date.month)
            results.append(f"{months} months")
            continue
        
        # Numeric Year & Month format (e.g., "11 2024 to 12 2025")
        match = re.match(r"(\d{1,2})\s*(\d{4})\s*(?:-|–|to)\s*(\d{1,2})\s*(\d{4}|Present|Ongoing)", duration, re.IGNORECASE)
        if match:
            start_month, start_year = int(match.group(1)), int(match.group(2))
            end_month, end_year = (current_date.month, current_date.year) if match.group(4).lower() in ["present", "ongoing"] else (int(match.group(3)), int(match.group(4)))
            months = (end_year - start_year) * 12 + (end_month - start_month)
            results.append(f"{months} months")
            continue

        # Numeric year-based durations (e.g., "5 years", "4+ years", "Minimum 3 years")
        match = re.search(r"(\d+)\s*(?:\+|\s*(?:years?|yrs?))", duration, re.IGNORECASE)
        if match:
            years = int(match.group(1)) * 12
            results.append(f"{years} months")
            continue

        # Flexible expressions (e.g., "At least 3 years 6 months")
        match = re.match(r"(At least|Minimum|More than|Over|Up to|Approximately|Around)\s+(\d+)\s*(year|years|yr|yrs)(?:\s*(\d+)\s*(month|months))?", duration, re.IGNORECASE)
        if match:
            base_years = int(match.group(2)) * 12
            base_months = int(match.group(4)) if match.group(4) else 0
            total_months = base_years + base_months
            results.append(f"{total_months} months")
            continue

        # Ranges like "Between 3 and 5 years"
        match = re.match(r"(Between|From)\s+(\d+)\s*(year|years|yr|yrs)\s*(?:and|to)\s*(\d+)\s*(year|years|yr|yrs)", duration, re.IGNORECASE)
        if match:
            min_years = int(match.group(2)) * 12
            max_years = int(match.group(4)) * 12
            avg_months = (min_years + max_years) // 2
            results.append(f"{avg_months} months")
            continue

        # Ranges like "3 to 5 years", "2-4 yrs"
        match = re.match(r"(\d+)\s*(?:to|-)\s*(\d+)\s*(year|years|yr|yrs)", duration, re.IGNORECASE)
        if match:
            min_years = int(match.group(1)) * 12
            max_years = int(match.group(2)) * 12
            avg_months = (min_years + max_years) // 2
            results.append(f"{avg_months} months")
            continue
    
    return results


