import re
from typing import Optional
from inventory import get_inventory, subtract_beers, add_beers


def parse_command(message: str) -> Optional[str]:
    """
    Parse incoming WhatsApp message and return appropriate response.
    
    Args:
        message: The incoming message text
        
    Returns:
        Response message string or None if command not recognized
    """
    # Normalize message to lowercase for easier matching
    message_lower = message.lower().strip()
    
    # Check inventory commands
    if any(keyword in message_lower for keyword in ["check inventory", "how many", "inventory", "beers left", "beer count"]):
        crates = get_inventory()
        if crates > 0:
            return f"🍺 Current inventory: {crates} crate{'s' if crates != 1 else ''}"
        else:
            return f"🍺 Current inventory: Empty"
    
    # Add beers to inventory commands
    add_patterns = [
        r"add\s+(\d+)\s+beers?",
        r"add\s+(\d+)\s+beers?\s+to\s+inventory",
        r"added\s+(\d+)\s+beers?\s+to\s+inventory",
        r"stock\s+(\d+)\s+beers?",
        r"restock\s+(\d+)\s+beers?",
        r"received\s+(\d+)\s+beers?",
    ]
    
    for pattern in add_patterns:
        match = re.search(pattern, message_lower)
        if match:
            amount = int(match.group(1))
            if amount <= 0:
                return "❌ Please specify a positive number of beers."
            
            result = add_beers(amount)
            return result["message"]
    
    # Subtract beers from inventory commands (when added to fridge)
    subtract_patterns = [
        r"added\s+(\d+)\s+beers?",
        r"added\s+(\d+)\s+beers?\s+to\s+fridge",
        r"add\s+(\d+)\s+beers?\s+to\s+fridge",
        r"subtract\s+(\d+)\s+beers?",
        r"removed\s+(\d+)\s+beers?",
        r"take\s+(\d+)\s+beers?",
    ]
    
    for pattern in subtract_patterns:
        match = re.search(pattern, message_lower)
        if match:
            amount = int(match.group(1))
            if amount <= 0:
                return "❌ Please specify a positive number of beers."
            
            result = subtract_beers(amount)
            return result["message"]
    
    # Unknown command
    return "🤔 I didn't understand that command. Try:\n• 'check inventory' - See current stock\n• 'add X beers' - Add X beers to inventory\n• 'added X beers' - Remove X beers when added to fridge"


def handle_message(message: str) -> str:
    """
    Main handler for incoming messages.
    
    Args:
        message: The incoming message text
        
    Returns:
        Response message string
    """
    response = parse_command(message)
    return response if response else "Sorry, I didn't understand that command."


