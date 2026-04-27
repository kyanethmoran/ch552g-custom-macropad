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

