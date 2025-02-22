from datetime import datetime
from typing import List, Tuple

def get_current_meal_time():
    """Determine the meal time based on current hour"""
    hour = datetime.now().hour
    if 5 <= hour < 11:
        return "breakfast"
    elif 11 <= hour < 16:
        return "lunch"
    elif 16 <= hour < 22:
        return "dinner"
    else:
        return "late night"

def create_recommendation_prompt(menu_items: str, previous_orders: str, meal_time: str) -> str:
    """Create the prompt for Gemini recommendation"""
    return f"""
    Act as a restaurant menu expert. Based on the following information, suggest 3 menu items.

    Current time: {meal_time} time
    
    Available menu items:
    {menu_items}

    {previous_orders}

    Please recommend 3 specific items from the menu that would be good for {meal_time} time.
    Consider previous orders in your recommendations if available.
    Format your response like this:
    1. [Item Name]: [Brief reason for recommendation]
    2. [Item Name]: [Brief reason for recommendation]
    3. [Item Name]: [Brief reason for recommendation]

    Then add a brief summary of why these items work well together.
    """

def parse_recommendations(response_text: str) -> Tuple[List[str], str]:
    """Parse Gemini response to extract recommended items and reasoning"""
    lines = response_text.strip().split('\n')
    recommended_items = []
    reasoning_parts = []
    
    for line in lines:
        line = line.strip()
        if line.startswith(('1.', '2.', '3.')):
            # Extract item name (text before the colon)
            item_parts = line.split(':', 1)
            if len(item_parts) > 0:
                item_name = item_parts[0].lstrip('123. ').strip()
                recommended_items.append(item_name)
                if len(item_parts) > 1:
                    reasoning_parts.append(line)
    
    # Get the summary (any text after the numbered list)
    summary = ""
    for line in lines:
        if not line.startswith(('1.', '2.', '3.')) and line.strip():
            summary += line + "\n"
    
    # Combine reasoning parts and summary
    full_reasoning = "\n".join(reasoning_parts)
    if summary.strip():
        full_reasoning += "\n\n" + summary.strip()
    
    return recommended_items, full_reasoning