from typing import Optional

from flask import redirect, session, request
from werkzeug.wrappers import Response

def redirect_with_error(destination: str, error: str) -> Response:
    """
    Redirects to a destination with an error message in the session

    Args:
        destination (str): The destination to redirect to after setting the error
        error (str): The error message to set in the session

    Returns:
        Response: The response to redirect to the destination
    """
    session["error"] = error

    return redirect(destination)

def set_error(error: str) -> None:
    """
    Sets an error message in the session

    Args:
        error (str): The error message to set in the session
    """
    
    session["error"] = error
    
def validate_input(text: str) -> bool:
    """
    Validates the input text

    Args:
        text (str): The text to validate

    Returns:
        bool: Whether the text is valid
    """
    
    if not text: 
        return False
    
    return len(text) > 0 and text.strip() != ""

def validate_request_item(key: str) -> bool:
    """
    Validates the request item

    Args:
        key (str): The key to validate

    Returns:
        bool: Whether the key is valid
    """
    
    if not key in request.form:
        return False
    
    return validate_input(request.form[key])

def attempt_form_item(key: str) -> Optional[str]:
    """
    Attempts to get the form item

    Args:
        key (str): The key to get from the form

    Returns:
        Optional[str]: The form item if it exists, otherwise None
    """
    
    if not key in request.form:
        return None
    
    return request.form[key]