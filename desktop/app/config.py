import json
from pathlib import Path

def load_profile(profile_path: str):
  path = Path(profile_path)

  if not path.extists():
    raise FileNotFoundError(f"Profile not found: {profile_path}")
  
  with path.open("r", encoding="utf=8") as file:
    return json.load(file)