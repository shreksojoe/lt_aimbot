import re

def split_addr():
    address = "ROLL PRODUCTS INC. THE OAKWOOD GROUP26504-OMF-ME-NMORHAN9755 INKSTER RDTAYLOR, MI 48180US"

    # Remove leading company if present
    address = re.sub(r'^ROLL PRODUCTS INC\. ?', '', address, flags=re.IGNORECASE)

    # Extract country (assume US)
    country = "US" if address.endswith("US") else ""
    address = re.sub(r'US$', '', address)

    # Extract state and zip at the end (more specific pattern)
    state_zip_match = re.search(r',\s*([A-Z]{2})\s*(\d{5})$', address)
    if state_zip_match:
        state, zip_code = state_zip_match.groups()
        # Remove the state and zip from address
        address = address[:state_zip_match.start()].strip()
    else:
        state = zip_code = ""

    # Now find the street address with suffix (RD, ST, etc.)
    # This should come before the city
    street_match = re.search(r'(\d{1,5}[-A-Z]*\d*\s+[A-Z\s]+?(?:RD|ST|AVE|BLVD|LN|CT))\s*([A-Z]+)$', address)
    
    if street_match:
        line2 = street_match.group(1).strip()
        city = street_match.group(2).strip()
        line1 = address[:street_match.start()].strip()
    else:
        # Fallback: try to extract city as last word
        city_match = re.search(r'([A-Z]+)$', address)
        if city_match:
            city = city_match.group(1)
            main_address = address[:city_match.start()].strip()
            
            # Try to find street address in remaining text
            street_match2 = re.search(r'(\d{1,5}[-A-Z]*\d*\s+[A-Z\s]+?(?:RD|ST|AVE|BLVD|LN|CT))\s*$', main_address)
            if street_match2:
                line2 = street_match2.group(1).strip()
                line1 = main_address[:street_match2.start()].strip()
            else:
                line1 = main_address
                line2 = ""
        else:
            city = ""
            line1 = address
            line2 = ""

    return {
        "Address Line 1": line1,
        "Address Line 2": line2,
        "City": city,
        "State": state,
        "Zip Code": zip_code,
        "Country": country
    }

print(split_addr())
