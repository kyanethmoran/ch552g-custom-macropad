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