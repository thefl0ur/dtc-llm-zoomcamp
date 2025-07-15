import random

from fastmcp import FastMCP

mcp = FastMCP("0a Agents MCP Server")

known_weather_data = {
    'berlin': 20.0
}

@mcp.tool
def get_weather(city: str) -> float:
    """
    Get weather for location

    Parameters:
        city (str): Name of the city to get weather for

    Returns:
        float: Teamperature in city
    """
    city = city.strip().lower()

    if city in known_weather_data:
        return known_weather_data[city]

    return round(random.uniform(-5, 35), 1)

@mcp.tool
def set_weather(city: str, temp: float) -> None:
    """
    Set weather for location

    Parameters:
        city (str): Name of the city to set weather for
        temp (float): The temperature to associate with the city.
    Returns:
        str: A confirmation string 'OK' indicating successful update.
    """
    city = city.strip().lower()
    known_weather_data[city] = temp
    return 'OK'

if __name__ == "__main__":
    mcp.run()