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


def add_beers(amount: int) -> Dict[str, any]:
    """
    Add beers to inventory. Only adds full crates (24 beers = 1 crate).
    
    Args:
        amount: Number of individual beers to add
        
    Returns:
        Dictionary with success status, new crate count, and message
    """
    inventory = load_inventory()
    current_crates = inventory.get("crates", DEFAULT_CRATES)
    
    # Only add full crates (floor division)
    crates_to_add = amount // BEERS_PER_CRATE
    remaining_beers = amount % BEERS_PER_CRATE
    
    new_crates = current_crates + crates_to_add
    
    inventory["crates"] = new_crates
    save_inventory(inventory)
    
    # Format message nicely
    if crates_to_add > 0 and remaining_beers > 0:
        message = f"Added {amount} beers. Only {crates_to_add} full crate{'s' if crates_to_add > 1 else ''} added to inventory. {remaining_beers} beer{'s' if remaining_beers > 1 else ''} not added. Total: {new_crates} crate{'s' if new_crates != 1 else ''}."
    elif crates_to_add > 0:
        message = f"Added {crates_to_add} crate{'s' if crates_to_add > 1 else ''} to inventory. Total: {new_crates} crate{'s' if new_crates != 1 else ''}."
    else:
        message = f"Added {amount} beers. No full crates to add. Total: {new_crates} crate{'s' if new_crates != 1 else ''}."
    
    return {
        "success": True,
        "crates": new_crates,
        "beers_added": amount,
        "crates_added": crates_to_add,
        "message": message
    }


def subtract_beers(amount: int) -> Dict[str, any]:
    """
    Subtract beers from inventory. Breaks crates if needed.
    
    Args:
        amount: Number of individual beers to subtract
        
    Returns:
        Dictionary with success status, new crate count, and message
    """
    inventory = load_inventory()
    current_crates = inventory.get("crates", DEFAULT_CRATES)
    
    # Calculate total beers available
    total_beers = current_crates * BEERS_PER_CRATE
    
    # Subtract requested amount
    new_total_beers = max(0, total_beers - amount)
    
    # Convert back to crates (floor division - only full crates remain)
    new_crates = new_total_beers // BEERS_PER_CRATE
    
    inventory["crates"] = new_crates
    save_inventory(inventory)
    
    # Calculate how many crates were broken
    crates_broken = current_crates - new_crates
    
    # Format message nicely
    if new_crates > 0:
        if crates_broken > 0:
            message = f"Removed {amount} beers from {crates_broken} crate{'s' if crates_broken > 1 else ''}. {new_crates} crate{'s' if new_crates != 1 else ''} remaining."
        else:
            message = f"Removed {amount} beers. {new_crates} crate{'s' if new_crates != 1 else ''} remaining."
    else:
        message = f"Removed {amount} beers. Inventory is now empty."
    
    return {
        "success": True,
        "crates": new_crates,
        "beers_subtracted": amount,
        "message": message
    }


