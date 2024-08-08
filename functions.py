import httpx
import json
from bs4 import BeautifulSoup

def calculate(exp):
    result = eval(exp)
    return result

def search_web(que):
    response = httpx.get("https://en.wikipedia.org/w/api.php", params={
        "action": "query",
        "list": "search",
        "srsearch": que,
        "format": "json"
    }).json()["query"]["search"][0]["snippet"]

    soup = BeautifulSoup(response, 'html.parser').get_text()
    return soup

import io
import contextlib

def run_code(code):
    # A string stream to capture the outputs of exec
    output = io.StringIO() 
    # Create a limited global namespace
    safe_globals = {
        "__builtins__": {
            "print": print,
            "range": range,
            "len": len,
            "int": int,
            # Add more built-ins as needed
        },
        # You can add other safe functions or variables here
    }
    
    try:
        # Redirect stdout to the StringIO object
        with contextlib.redirect_stdout(output):  
            # Execute the code with limited globals
            exec(code, globals())
    except Exception as e:
        # If an error occurs, capture it as part of the output
        print(f"Error: {e}", file=output)  
    return output.getvalue()


