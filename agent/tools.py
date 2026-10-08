from datetime import datetime, date
from utils.decorator import tool 

@tool
def get_current_time() -> str:
    """Get the current time"""
    return datetime.now().strftime("%H:%M:%S")

@tool 
def do_division( a : float , b : float  )-> float:
    """divides two number, takes two arguments a and b in float or any number, returns float or any number"""
    return a/b

@tool 
def get_date() ->str:
    """Get the current date"""
    return date.today()

@tool 
def get_weather(city: str)->str:
    """returns the weather of city in str, takes str arguments for city"""
    raise ConnectionError("couldnt connect to weather API")