from flask import Flask
from markdown import markdown
from html_sanitizer import Sanitizer

def render_filter(text: str) -> str:
    """
    Jinja filter to render markdown text

    Args:
        text (str): The text to render

    Returns:
        str: Sanitized HTML of the rendered markdown
    """
    
    sanitizer = Sanitizer()
    return sanitizer.sanitize(markdown(text, extensions=["extra"]))
    

def register_filters(app: Flask) -> None:
    """
    Registers filters for the Jinja environment

    Args:
        app (Flask): The Flask application to register the filters to
    """
    app.jinja_env.filters["render"] = render_filter