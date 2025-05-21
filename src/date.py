from datetime import datetime, timedelta

def get_date_two_weeks_prior(input_date):
    """
    Takes a date string in various formats and returns 
    the date two weeks prior in MM/DD/YYYY format.
    
    Args:
        input_date (str): Date string in various formats
        (e.g., 'MM/DD/YYYY', 'MM-DD-YY', 'MM/DD/YY', 'YYYY-MM-DD')
        
    Returns:
        str: Date two weeks prior in MM/DD/YYYY format,
        or None if parsing fails
    """
    # List of possible date formats to try
    date_formats = [
        '%m/%d/%Y',  # MM/DD/YYYY
        '%m/%d/%y',  # MM/DD/YY
        '%m-%d-%Y',  # MM-DD-YYYY
        '%m-%d-%y',  # MM-DD-YY
        '%Y-%m-%d',  # YYYY-MM-DD (ISO format)
        '%m.%d.%Y',  # MM.DD.YYYY
        '%m.%d.%y',  # MM.DD.YY
        '%m/%d',     # MM/DD (assumes current year)
        '%m-%d'      # MM-DD (assumes current year)
    ]
    
    # Try parsing the date with each format
    for fmt in date_formats:
        try:
            # For formats without year, use current year
            if fmt in ['%m/%d', '%m-%d']:
                current_year = datetime.now().year
                parsed_date = datetime.strptime(f"{input_date}/{current_year}",
                                                '%m/%d/%Y')
            else:
                parsed_date = datetime.strptime(input_date, fmt)
            
            # Calculate two weeks before
            two_weeks_prior = parsed_date - timedelta(weeks=2)
            
            # Return in MM/DD/YYYY format
            return two_weeks_prior.strftime('%m/%d/%Y')
            
        except ValueError:
            continue  # Try the next format
    
    return None  # Return None if no format matched

def main():
    import sys
    
    # Check if a date was provided as a command-line argument
    if len(sys.argv) > 1:
        input_date = ' '.join(sys.argv[1:])
        result = get_date_two_weeks_prior(input_date)
        if result:
            print(result)  # Print only the result
        else:
            print(f"Error: Could not parse the date: {input_date}")
        return
    
    # If no arguments provided, show usage examples
    print("Please provide a date as an argument. For example:")
    print("python date.py 05/19/2025")
    print("\nExample outputs:")
    
    test_dates = [
        '05/19/2025',  # MM/DD/YYYY
        '05/19/25',    # MM/DD/YY
        '2025-05-19',  # YYYY-MM-DD
        '05-19-2025',  # MM-DD-YYYY
        '05/19',       # MM/DD (current year assumed)
        '05-19'        # MM-DD (current year assumed)
    ]
    
    for date_str in test_dates:
        result = get_date_two_weeks_prior(date_str)
        print(f"Input: {date_str:<12} → {result}")

if __name__ == "__main__":
    main()
