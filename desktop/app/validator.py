"""
Catch problems such as:
- missing "type"
- unknown action type
- open_app missing "path"
- open_url missing "url"
- close_app missing "process_name"
- send_hotkey missing "keys"
- volume actions having a bad "step" value
print warnings and skip broken action, avoid crashing
"""

REQUIRED_FIELDS = {
  "open_app": ["path"],
  "open_url": ["url"],
  "open_folder": ["path"],
  "close_app": ["process_name"],
  "send_hotkey": ["keys"],
  "print_active_app": [],
  "print_message": ["message"],
  "toggle_mute_active_app": [],
  "volume_up_active_app": [],
  "volume_down_active_app": [],
}

def validate_action(action_key: str, action_config: dict) -> tuple[bool, str | None]:
  if not isinstance(action_config, dict):
    return False, f"{action_key}: action must be an object/dictionary"
  
  action_type = action_config.get("type")
  if not isinstance(action_type, str):
    return False, f"{action_key}: missing or invalid 'type'"
  
  if action_type not in REQUIRED_FIELDS:
    return False, f"{action_key}: unknown action type '{action_type}'"
  
  for field in REQUIRED_FIELDS[action_type]:
    if field not in action_config:
      return False, f"{action_key}: action type '{action_type}' is missing required field '{field}'"
    
  if action_type in ("volume_up_active_app", "volume_down_active_app"):
    if "step" in action_config and not isinstance(action_config["step"], (int,float)):
      return False, f"{action_key}: 'step' must be a number"
    
  return True, None

def validate_profile(profile: dict) -> tuple[dict, list[str]]:
  valid_profile = {}
  errors = []

  if not isinstance(profile, dict):
    return {}, ["Profile root must be a JSON object/dictionary"]
  
  for action_key, action_config in profile.items():
    is_valid, error = validate_action(action_key, action_config)

    if is_valid:
      valid_profile[action_key] = action_config
    else:
      errors.append(error)

  return valid_profile, errors