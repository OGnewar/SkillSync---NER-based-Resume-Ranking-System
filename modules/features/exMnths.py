from datetime import datetime
import re

def extract_months(durations):
    current_year = datetime.now().year
    current_month = datetime.now().month
    results = []
    
    for duration in durations:
        duration = duration.strip()
        
        # Year ranges (e.g., "2020-2024", "2020 to 2024")
        match = re.match(r"(\d{4})\s*(?:-|–|to)\s*(\d{4}|Present|Ongoing)", duration, re.IGNORECASE)
        if match:
            start_year = int(match.group(1))
            end_year = current_year if match.group(2).lower() in ["present", "ongoing"] else int(match.group(2))
            months = (end_year - start_year) * 12
            results.append(f"{months} months")
            continue
        
        # Full date ranges (e.g., "Nov 10, 2020 - Dec 10, 2021")
        match = re.match(r"(\w+ \d{1,2}, \d{4})\s*(?:-|–|to)\s*(\w+ \d{1,2}, \d{4}|Present|Ongoing)", duration, re.IGNORECASE)
        if match:
            start_date = datetime.strptime(match.group(1), "%b %d, %Y")
            end_date = datetime.now() if match.group(2).lower() in ["present", "ongoing"] else datetime.strptime(match.group(2), "%b %d, %Y")
            months = (end_date.year - start_date.year) * 12 + (end_date.month - start_date.month)
            results.append(f"{months} months")
            continue
        
        # MM/DD/YYYY date ranges (e.g., "05/13/2020 - 06/16/2021")
        match = re.match(r"(\d{2}/\d{2}/\d{4})\s*(?:-|–|to)\s*(\d{2}/\d{2}/\d{4}|Present|Ongoing)", duration, re.IGNORECASE)
        if match:
            start_date = datetime.strptime(match.group(1), "%m/%d/%Y")
            end_date = datetime.now() if match.group(2).lower() in ["present", "ongoing"] else datetime.strptime(match.group(2), "%m/%d/%Y")
            months = (end_date.year - start_date.year) * 12 + (end_date.month - start_date.month)
            results.append(f"{months} months")
            continue
        
        # Numeric Year & Month format (e.g., "11 2024 to 12 2025")
        match = re.match(r"(\d{1,2})\s*(\d{4})\s*(?:-|–|to)\s*(\d{1,2})\s*(\d{4}|Present|Ongoing)", duration, re.IGNORECASE)
        if match:
            start_month, start_year = int(match.group(1)), int(match.group(2))
            end_month, end_year = (current_month, current_year) if match.group(4).lower() in ["present", "ongoing"] else (int(match.group(3)), int(match.group(4)))
            months = (end_year - start_year) * 12 + (end_month - start_month)
            results.append(f"{months} months")
            continue
        
        # General duration terms (e.g., "3 years", "4+ years", "2 years 4 months", "a decade")
        '''match = re.match(r"(\d+|a|an)\s*(year|years|yr|yrs|decade|decades)(?:\s*(\d+)\s*(month|months))?", duration, re.IGNORECASE)
        if match:
            years = 10 if match.group(1) in ["a", "an"] and "decade" in match.group(2).lower() else (int(match.group(1)) * 12 if "decade" not in match.group(2).lower() else int(match.group(1)) * 120)
            months = int(match.group(3)) if match.group(3) else 0
            results.append(f"{years + months} months")
            continue'''
        
        # Extract numeric year-based durations (e.g., "5 years", "4+ years", "Minimum 3 years")
        match = re.search(r"(\d+)\s*(?:\+|\s*(?:years?|yrs?))", duration, re.IGNORECASE)
        if match:
            years = int(match.group(1)) * 12  # Convert years to months
            results.append(f"{years} months")
            continue

        # NEW: Flexible experience terms (e.g., "At least 3 years", "More than 5 years", "Over 2 years", "Minimum 4 years")
        match = re.match(r"(At least|Minimum|More than|Over|Up to|Approximately|Around)\s+(\d+)\s*(year|years|yr|yrs)(?:\s*(\d+)\s*(month|months))?", duration, re.IGNORECASE)
        if match:
            base_years = int(match.group(2)) * 12  # Convert years to months
            base_months = int(match.group(4)) if match.group(4) else 0
            total_months = base_years + base_months
            results.append(f"{total_months} months")
            continue

        # NEW: Ranges like "Between 3 and 5 years", "From 2 to 4 years"
        match = re.match(r"(Between|From)\s+(\d+)\s*(year|years|yr|yrs)\s*(?:and|to)\s*(\d+)\s*(year|years|yr|yrs)", duration, re.IGNORECASE)
        if match:
            min_years = int(match.group(2)) * 12
            max_years = int(match.group(4)) * 12
            avg_months = (min_years + max_years) // 2  # Approximate average
            results.append(f"{avg_months} months")
            continue

        # NEW: "3 to 5 years", "2-4 yrs"
        match = re.match(r"(\d+)\s*(?:to|-)\s*(\d+)\s*(year|years|yr|yrs)", duration, re.IGNORECASE)
        if match:
            min_years = int(match.group(1)) * 12
            max_years = int(match.group(2)) * 12
            avg_months = (min_years + max_years) // 2
            results.append(f"{avg_months} months")
            continue
    
    return results
