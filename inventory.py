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
            return json.load(f)
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


def add_beers(amount: int) -> Dict[str, any]:
    """
    Add beers to inventory. Converts individual beers to crates.
    
    Args:
        amount: Number of individual beers to add
        
    Returns:
        Dictionary with success status, new crate count, and message
    """
    inventory = load_inventory()
    current_crates = inventory.get("crates", DEFAULT_CRATES)
    
    # Convert beers to crates (round up to account for partial crates)
    crates_to_add = (amount + BEERS_PER_CRATE - 1) // BEERS_PER_CRATE
    
    new_crates = current_crates + crates_to_add
    
    inventory["crates"] = new_crates
    save_inventory(inventory)
    
    return {
        "success": True,
        "crates": new_crates,
        "beers_added": amount,
        "crates_added": crates_to_add,
        "message": f"Added {amount} beers ({crates_to_add} crate(s)) to inventory. {new_crates} crate(s) total."
    }


def subtract_beers(amount: int) -> Dict[str, any]:
    """
    Subtract beers from inventory. Converts individual beers to crates.
    
    Args:
        amount: Number of individual beers to subtract
        
    Returns:
        Dictionary with success status, new crate count, and message
    """
    inventory = load_inventory()
    current_crates = inventory.get("crates", DEFAULT_CRATES)
    
    # Convert beers to crates (round up to account for partial crates)
    crates_to_subtract = (amount + BEERS_PER_CRATE - 1) // BEERS_PER_CRATE
    
    new_crates = max(0, current_crates - crates_to_subtract)  # Don't go below 0
    
    inventory["crates"] = new_crates
    save_inventory(inventory)
    
    return {
        "success": True,
        "crates": new_crates,
        "beers_subtracted": amount,
        "crates_subtracted": crates_to_subtract,
        "message": f"Removed {amount} beers ({crates_to_subtract} crate(s)) from inventory. {new_crates} crate(s) remaining."
    }


