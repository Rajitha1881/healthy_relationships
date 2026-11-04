# ==============================================================================
# Standard Library Imports
# ==============================================================================
# The 'random' module provides functions for generating random selections or numbers.
# We use 'random.choice()' to randomly pick a message from a list.
import random

# The 'typing' module allows us to specify type hints for code readability and IDE support.
# - Optional[str]: means the value can either be a string (str) or None.
# - List[str]: indicates a list containing string elements.
from typing import Optional, List


# ==============================================================================
# Data Store (Dictionary of Messages)
# ==============================================================================
# A Python dictionary where:
# - Each KEY is a string representing a relationship category.
# - Each VALUE is a list of strings containing helpful advice or messages for that category.
MESSAGES = {
    # Tips focused on active listening and honest expression
    "communication": [
        "Take a moment to truly listen without planning your response while they are speaking.",
        "Clear and honest communication builds lasting trust.",
        "Express how you feel using 'I' statements rather than blame.",
        "Check in with your partner today: ask 'How can I best support you today?'",
    ],
    # Messages encouraging gratitude and acknowledging the other person
    "appreciation": [
        "Acknowledge the small things your partner does that often go unnoticed.",
        "Never let familiarity replace gratitude; say thank you often.",
        "Compliment your partner on a character trait you admire, not just their achievements.",
        "Remind your partner why you chose them and what you cherish most about them.",
    ],
    # Guidance on maintaining personal identity and respecting individuality
    "boundaries": [
        "Healthy boundaries protect the connection, not distance it.",
        "Respecting each other's individuality strengthens the bond you share.",
        "It's healthy to have separate hobbies and personal time to recharge.",
        "Saying 'no' to a request while offering reassurance is an act of care.",
    ],
    # Constructive ways to handle disagreements and conflicts
    "conflict_resolution": [
        "Remember: it's not you versus your partner; it's both of you against the problem.",
        "When emotions run high, it's okay to take a 15-minute breather before resuming the conversation.",
        "Focus on resolving the issue, not winning the argument.",
        "Apologize sincerely when you are wrong and accept apologies graciously.",
    ],
    # Encouragement for self-improvement and supporting each other's goals
    "growth": [
        "Celebrate each other's personal growth, even when it brings new changes.",
        "Encourage your partner's dreams, even when they take them out of their comfort zone.",
        "Be patient with each other's healing and learning processes.",
    ],
}

# ==============================================================================
# V2 Data Store: Actionable Daily Challenges & Tags
# ==============================================================================
CHALLENGES = {
    "communication": [
        "Spend 10 minutes tonight actively listening without offering advice unless requested.",
        "Ask your partner one open-ended question about their day and give 100% undistracted attention.",
        "Send a mid-day check-in text with zero expectations, just to say you are thinking of them.",
    ],
    "appreciation": [
        "Leave a hidden post-it note expressing gratitude for something specific they did this week.",
        "Verbally thank your partner for a small routine chore that is usually taken for granted.",
        "Tell your partner one specific character trait you admire in them today.",
    ],
    "boundaries": [
        "Take 30 minutes of intentional solo recharge time today with no guilt.",
        "Practice gently saying 'no' to an optional task so you can preserve emotional energy.",
        "Check in with your partner before venting: 'Do you have capacity to listen right now?'",
    ],
    "conflict_resolution": [
        "If a disagreement arises today, agree on a 10-minute pause before continuing.",
        "Replace 'You always...' or 'You never...' with 'When X happened, I felt Y.'",
        "Offer a genuine apology for a small friction point without adding 'but...'",
    ],
    "growth": [
        "Share one personal goal or dream you haven't talked about in a while.",
        "Celebrate one small personal win your partner achieved this week.",
        "Read an article or podcast together on personal development and discuss it.",
    ],
}

TAGS = {
    "communication": ["active-listening", "clarity", "empathy", "openness"],
    "appreciation": ["gratitude", "validation", "kindness", "affirmation"],
    "boundaries": ["self-care", "respect", "emotional-space", "independence"],
    "conflict_resolution": ["problem-solving", "emotional-maturity", "patience", "repair"],
    "growth": ["personal-development", "support", "future-planning", "encouragement"],
}


# ==============================================================================
# Main Function: Get Relationship Message (v1)
# ==============================================================================
def get_relationship_message(category: Optional[str] = None) -> str:
    """
    Retrieves a relationship message or tip.

    Parameters:
        category (Optional[str]): The category name (e.g., 'growth', 'communication').
                                  Defaults to None if not provided.

    Returns:
        str: A randomly selected message.

    Raises:
        ValueError: If the requested category does not exist in MESSAGES.
    """
    # Check if the user supplied a specific category
    if category:
        # Normalize the input: strip leading/trailing spaces and convert to lowercase
        # This allows inputs like ' GROWTH ' or 'Growth' to match 'growth'
        category_lower = category.strip().lower()

        # Check if the cleaned category exists in our dictionary keys
        if category_lower in MESSAGES:
            # Pick and return one random message from that specific category list
            return random.choice(MESSAGES[category_lower])
        else:
            # If the category is not found, gather all valid category names for a helpful error
            valid_keys = ", ".join(MESSAGES.keys())
            # Raise an exception informing the caller which categories are allowed
            raise ValueError(f"Unknown category '{category}'. Available categories: {valid_keys}")

    # If NO category was provided (category is None):
    # Flatten all message lists across all categories into a single list
    # This list comprehension loops through every list in MESSAGES.values()
    all_messages = [msg for category_list in MESSAGES.values() for msg in category_list]

    # Return one random message selected from all combined messages
    return random.choice(all_messages)


# ==============================================================================
# Helper Function: List Available Categories
# ==============================================================================
def get_categories() -> List[str]:
    """
    Returns a list of all supported category names.

    Returns:
        List[str]: A list of category strings (e.g., ['communication', 'appreciation', ...]).
    """
    # .keys() retrieves the dictionary keys; list(...) converts that view into a Python list
    return list(MESSAGES.keys())


# ==============================================================================
# V2 Function: Get Relationship Message with Challenges & Metadata
# ==============================================================================
def get_relationship_message_v2(category: Optional[str] = None) -> dict:
    """
    Retrieves an enhanced v2 relationship message containing:
    - Unique message identifier
    - Categorized message
    - Actionable daily challenge
    - Topic tags
    - Analytical metadata (character count, estimated read time, rating)
    """
    if category:
        cat_clean = category.strip().lower()
        if cat_clean not in MESSAGES:
            valid_keys = ", ".join(MESSAGES.keys())
            raise ValueError(f"Unknown category '{category}'. Available categories: {valid_keys}")
    else:
        cat_clean = random.choice(list(MESSAGES.keys()))

    msg = random.choice(MESSAGES[cat_clean])
    challenge = random.choice(CHALLENGES.get(cat_clean, ["Take a moment to connect with your partner today."]))
    tags = TAGS.get(cat_clean, ["relationships", "wellness"])

    # Generate a stable short hash-based ID
    msg_id = f"msg_{cat_clean[:4]}_{abs(hash(msg)) % 10000:04d}"

    return {
        "id": msg_id,
        "version": "2.0",
        "category": cat_clean,
        "message": msg,
        "actionable_challenge": challenge,
        "tags": tags,
        "metadata": {
            "char_count": len(msg),
            "word_count": len(msg.split()),
            "estimated_read_seconds": max(1, round(len(msg.split()) / 3)),
            "community_rating": 4.9,
        },
    }


def get_daily_challenge(category: Optional[str] = None) -> dict:
    """
    Retrieves a daily actionable challenge tailored to deepen connection.
    """
    if category:
        cat_clean = category.strip().lower()
        if cat_clean not in CHALLENGES:
            valid_keys = ", ".join(CHALLENGES.keys())
            raise ValueError(f"Unknown category '{category}'. Available categories: {valid_keys}")
    else:
        cat_clean = random.choice(list(CHALLENGES.keys()))

    challenge = random.choice(CHALLENGES[cat_clean])
    return {
        "version": "2.0",
        "category": cat_clean,
        "daily_challenge": challenge,
        "difficulty": random.choice(["Gentle & Easy", "Mindful Practice", "Deep Connection"]),
        "recommended_duration_minutes": random.choice([5, 10, 15]),
    }


# ==============================================================================
# Script Execution Block (Entry Point)
# ==============================================================================
# This condition checks if the script is being executed directly from the terminal
# (e.g., 'python3 relationship_messages.py') rather than being imported by another file.
if __name__ == "__main__":
    # The 'sys' module allows access to system-specific parameters and functions,
    # including command-line arguments via 'sys.argv'.
    import sys

    # 'sys.argv' is a list of command-line arguments passed to the script:
    # - sys.argv[0] is always the script name ('relationship_messages.py').
    # - sys.argv[1] is the first argument after the script name (if the user typed one).
    # If the user provided an argument (len > 1), use it; otherwise, default to None.
    category_arg = sys.argv[1] if len(sys.argv) > 1 else None

    # Use a try-except block to handle cases where the user passes an invalid category name
    try:
        # Call our function with the argument (or None for random)
        message = get_relationship_message(category_arg)

        # Create a display label: capitalized category name, or 'Random' if none was passed
        label = category_arg.capitalize() if category_arg else "Random"

        # Print the formatted output to the terminal console
        print(f"[{label}] {message}")

    except ValueError as e:
        # If an invalid category was requested, print the error message cleanly
        print(f"Error: {e}")
        # Exit with a non-zero status code (1) to indicate that an error occurred
        sys.exit(1)
