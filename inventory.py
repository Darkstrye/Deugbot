import json
import os
from datetime import datetime
from typing import Dict
from dotenv import load_dotenv

load_dotenv()

INVENTORY_FILE = "inventory.json"
DEFAULT_CRATES = int(os.getenv("DEFAULT_CRATES", 50))
# Standard crate size - typically 24 beers per crate
BEERS_PER_CRATE = 24


def load_inventory() -> Dict:
    """Load inventory from JSON file. Creates file with default value if it doesn't exist."""
    if not os.path.exists(INVENTORY_FILE):
        # Initialize with default value
        initial_inventory = {
            "crates": DEFAULT_CRATES,
            "last_updated": datetime.now().isoformat()
        }
        save_inventory(initial_inventory)
        return initial_inventory
    
    try:
        with open(INVENTORY_FILE, 'r') as f:
            inventory = json.load(f)
        # Remove partial_beers if it exists (backwards compatibility)
        if "partial_beers" in inventory:
            del inventory["partial_beers"]
            save_inventory(inventory)
        return inventory
    except (json.JSONDecodeError, IOError) as e:
        # If file is corrupted, reinitialize
        initial_inventory = {
            "crates": DEFAULT_CRATES,
            "last_updated": datetime.now().isoformat()
        }
        save_inventory(initial_inventory)
        return initial_inventory


def save_inventory(inventory: Dict) -> None:
    """Save inventory to JSON file."""
    inventory["last_updated"] = datetime.now().isoformat()
    with open(INVENTORY_FILE, 'w') as f:
        json.dump(inventory, f, indent=2)


def get_inventory() -> int:
    """Get current crate count."""
    inventory = load_inventory()
    return inventory.get("crates", DEFAULT_CRATES)


def add_crates(crates: int) -> Dict[str, any]:
    """
    Add crates directly to inventory.
    
    Args:
        crates: Number of crates to add
        
    Returns:
        Dictionary with success status, new crate count, and message
    """
    inventory = load_inventory()
    current_crates = inventory.get("crates", DEFAULT_CRATES)
    
    new_crates = current_crates + crates
    
    inventory["crates"] = new_crates
    save_inventory(inventory)
    
    # Format message nicely
    message = f"Added {crates} crate{'s' if crates != 1 else ''} to inventory. Total: {new_crates} crate{'s' if new_crates != 1 else ''}."
    
    return {
        "success": True,
        "crates": new_crates,
        "crates_added": crates,
        "message": message
    }


def subtract_crates(crates: int) -> Dict[str, any]:
    """
    Subtract crates directly from inventory.
    
    Args:
        crates: Number of crates to subtract
        
    Returns:
        Dictionary with success status, new crate count, and message
    """
    inventory = load_inventory()
    current_crates = inventory.get("crates", DEFAULT_CRATES)
    
    new_crates = max(0, current_crates - crates)  # Don't go below 0
    
    inventory["crates"] = new_crates
    save_inventory(inventory)
    
    # Format message nicely
    if new_crates > 0:
        message = f"Removed {crates} crate{'s' if crates != 1 else ''} from inventory. {new_crates} crate{'s' if new_crates != 1 else ''} remaining."
    else:
        message = f"Removed {crates} crate{'s' if crates != 1 else ''} from inventory. Inventory is now empty."
    
    return {
        "success": True,
        "crates": new_crates,
        "crates_subtracted": crates,
        "message": message
    }


