import json
import random
import asyncio
from pathlib import Path

DATA_FILE = Path("jokes.json")
NAMES_FILE = Path("names.json")


def _read_json_file(path: Path):
    """Blocking helper to read a JSON file (safe to run in thread)."""
    if not path.exists():
        path.write_text("[]")
    with open(path, "r") as f:
        return json.load(f)


async def get_data():
    """
    Async wrapper that returns a random joke text.
    Uses asyncio.to_thread to avoid blocking the event loop.
    """
    try:
        data = await asyncio.to_thread(_read_json_file, DATA_FILE)
        if not data:
            return []
        joke = random.choice(data)
        return joke.get("text", "") if isinstance(joke, dict) else str(joke)
    except Exception as e:
        # Return a serializable error structure similar to original behavior
        return {"error": str(e)}


async def get_search(name: str):
    """
    Async wrapper for searching names.json.
    Uses asyncio.to_thread to avoid blocking the event loop.
    """
    try:
        if not name:
            return {"found": False, "message": "No name provided."}

        names = await asyncio.to_thread(_read_json_file, NAMES_FILE)

        # Case-insensitive partial match
        matches = [n for n in names if name.lower() in n.lower()]

        if matches:
            return {
                "found": True,
                "message": f"Found {len(matches)} result(s): {', '.join(matches)}"
            }
        else:
            return {"found": False, "message": f"'{name}' was not found."}

    except Exception as e:
        return {"error": str(e)}


if __name__ == "__main__":
    import asyncio as _a
    print(_a.run(get_search("Trump")))
