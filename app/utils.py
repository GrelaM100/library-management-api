from fastapi import HTTPException

def validate_serial_number(serial_number: str) -> str:
    """
    Validate that the serial number is a six-digit number.
    
    Args:
        serial_number (str): The serial number to validate.
        
    Returns:
        str: The validated serial number.
        
    Raises:
        HTTPException: If the serial number is not a six-digit number.
    """
    if not serial_number.isdigit() or len(serial_number) != 6:
        raise HTTPException(status_code=400, detail="Serial number must be a six-digit number")
    return serial_number