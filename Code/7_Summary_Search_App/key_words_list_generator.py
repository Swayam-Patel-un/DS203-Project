import re

def extract_keywords(user_input):
    # Split at space, hyphen, or comma
    raw_keywords = re.split(r"[,\s\-]+", user_input.lower())
    # Strip spaces and remove empty strings
    keywords = [word.strip() for word in raw_keywords if word.strip()]
    return keywords
