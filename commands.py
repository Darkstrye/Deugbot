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
    if message_lower in ["commands", "help", "list commands", "what can you do", "commando's", "hulp"]:
        return """📋 Beschikbare Commando's:

1️⃣ VOORRAAD CONTROLEREN / STATUS
   • "status"
   • "voorraad"
   • "hoeveel"
   • "check voorraad"

2️⃣ KRATEN TOEVOEGEN
   • "voeg X kratten toe" (bijv. "voeg 2 kratten toe")
   • "toegevoegd X kratten"
   • "voorraad X kratten"

3️⃣ KRATEN VERWIJDEREN
   • "verwijder X kratten"
   • "weggehaald X kratten"
   • "haal X kratten weg"

💡 Alle bewerkingen werken met volledige kratten!"""
    
    # Check inventory commands
    if any(keyword in message_lower for keyword in ["check inventory", "how many", "inventory", "beers left", "beer count", "status", "voorraad", "hoeveel", "check voorraad"]):
        crates = get_inventory()
        if crates > 0:
            return f"🍺 Huidige voorraad: {crates} krat{'ten' if crates != 1 else ''}"
        else:
            return f"🍺 Huidige voorraad: Leeg"
    
    # Add crates to inventory commands
    add_crate_patterns = [
        r"add\s+(\d+)\s+crates?",
        r"added\s+(\d+)\s+crates?",
        r"add\s+(\d+)\s+crates?\s+to\s+inventory",
        r"added\s+(\d+)\s+crates?\s+to\s+inventory",
        r"stock\s+(\d+)\s+crates?",
        r"restock\s+(\d+)\s+crates?",
        r"received\s+(\d+)\s+crates?",
        r"voeg\s+(\d+)\s+kratten?\s+toe",
        r"toegevoegd\s+(\d+)\s+kratten?",
        r"voorraad\s+(\d+)\s+kratten?",
        r"ontvangen\s+(\d+)\s+kratten?",
    ]
    
    for pattern in add_crate_patterns:
        match = re.search(pattern, message_lower)
        if match:
            crates = int(match.group(1))
            if crates <= 0:
                return "❌ Geef een positief aantal kratten op."
            
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
        r"verwijder\s+(\d+)\s+kratten?",
        r"weggehaald\s+(\d+)\s+kratten?",
        r"haal\s+(\d+)\s+kratten?\s+weg",
        r"eruit\s+(\d+)\s+kratten?",
    ]
    
    for pattern in subtract_patterns:
        match = re.search(pattern, message_lower)
        if match:
            crates = int(match.group(1))
            if crates <= 0:
                return "❌ Geef een positief aantal kratten op."
            
            result = subtract_crates(crates)
            return result["message"]
    
    # Unknown command
    return "🤔 Ik begrijp dat commando niet. Probeer:\n• 'commando's' - Zie alle beschikbare commando's\n• 'status' - Controleer huidige voorraad\n• 'voeg X kratten toe' - Voeg kratten toe aan voorraad\n• 'verwijder X kratten' - Verwijder kratten uit voorraad"


def handle_message(message: str) -> str:
    """
    Main handler for incoming messages.
    
    Args:
        message: The incoming message text
        
    Returns:
        Response message string
    """
    response = parse_command(message)
    return response if response else "Sorry, ik begrijp dat commando niet."


