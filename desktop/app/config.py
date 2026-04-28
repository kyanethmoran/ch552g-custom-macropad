import json
from pathlib import Path

def load_profile(profile_path: str):
  path = Path(profile_path)

  if not path.exists():
    raise FileNotFoundError(f"Profile not found: {profile_path}")
  
  with path.open("r", encoding="utf=8") as file:
    return json.load(file)
  
def save_profile(profile_path: str, profile_data: dict):
  path = Path(profile_path)

  with path.open("w", encoding = "utf-8") as file:
    json.dump(profile_data, file, indent=2)