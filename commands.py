import re
from typing import Optional
from inventory import get_inventory, subtract_crates, add_crates


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
    
    # Commands list command
    if message_lower in ["commands", "help", "list commands", "what can you do"]:
        return """📋 Available Commands:

1️⃣ CHECK INVENTORY
   • "check inventory"
   • "how many"
   • "inventory"
   • "beers left"
   • "beer count"

2️⃣ ADD CRATES
   • "add X crates" (e.g., "add 2 crates")
   • "added X crates"
   • "stock X crates"
   • "restock X crates"

3️⃣ SUBTRACT CRATES
   • "subtract X crates"
   • "removed X crates"
   • "take X crates"
   • "remove X crates"

💡 All operations work with full crates!"""
    
    # Check inventory commands
    if any(keyword in message_lower for keyword in ["check inventory", "how many", "inventory", "beers left", "beer count"]):
        crates = get_inventory()
        if crates > 0:
            return f"🍺 Current inventory: {crates} crate{'s' if crates != 1 else ''}"
        else:
            return f"🍺 Current inventory: Empty"
    
    # Add crates to inventory commands
    add_crate_patterns = [
        r"add\s+(\d+)\s+crates?",
        r"added\s+(\d+)\s+crates?",
        r"add\s+(\d+)\s+crates?\s+to\s+inventory",
        r"added\s+(\d+)\s+crates?\s+to\s+inventory",
        r"stock\s+(\d+)\s+crates?",
        r"restock\s+(\d+)\s+crates?",
        r"received\s+(\d+)\s+crates?",
    ]
    
    for pattern in add_crate_patterns:
        match = re.search(pattern, message_lower)
        if match:
            crates = int(match.group(1))
            if crates <= 0:
                return "❌ Please specify a positive number of crates."
            
            result = add_crates(crates)
            return result["message"]
    
    # Subtract crates from inventory commands
    subtract_patterns = [
        r"subtract\s+(\d+)\s+crates?",
        r"removed\s+(\d+)\s+crates?",
        r"take\s+(\d+)\s+crates?",
        r"remove\s+(\d+)\s+crates?",
        r"subtract\s+(\d+)\s+crates?\s+from\s+inventory",
        r"removed\s+(\d+)\s+crates?\s+from\s+inventory",
    ]
    
    for pattern in subtract_patterns:
        match = re.search(pattern, message_lower)
        if match:
            crates = int(match.group(1))
            if crates <= 0:
                return "❌ Please specify a positive number of crates."
            
            result = subtract_crates(crates)
            return result["message"]
    
    # Unknown command
    return "🤔 I didn't understand that command. Try:\n• 'commands' - See all available commands\n• 'check inventory' - See current stock\n• 'add X crates' - Add X crates to inventory\n• 'subtract X crates' - Remove X crates from inventory"


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


