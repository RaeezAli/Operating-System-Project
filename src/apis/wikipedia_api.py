import wikipedia

def get_wiki_summary(query, sentences=2):
    """Fetches a summary from Wikipedia."""
    try:
        summary = wikipedia.summary(query, sentences=sentences)
        return summary
    except wikipedia.exceptions.DisambiguationError as e:
        return f"There are multiple results for {query}. Could you be more specific?"
    except wikipedia.exceptions.PageError:
        return f"I couldn't find any Wikipedia page for {query}."
    except Exception as e:
        print(f"[ERROR] Wikipedia lookup failed: {e}")
        return "I encountered an error while searching Wikipedia."
