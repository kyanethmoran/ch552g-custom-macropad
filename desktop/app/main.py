import keyboard

from config import load_profile
from actions import (
  open_app,
  open_url,
  close_process_by_name,
  print_forground_app,
  toggle_mute_active_app,
  change_volume_active_app,
)

"""
Action wrapper functions
"""
def action_open_app(action_config: dict):
  open_app(action_config["path"])

def action_open_url(action_config: dict):
  open_url(action_config["url"])

def action_close_app(action_config: dict):
  close_process_by_name(action_config["process_name"])

# testing
def action_print_active_app(action_config: dict):
  print_forground_app()

def action_print_message(action_config: dict):
  print(f"[ACTION] {action_config['message']}")

def action_toggle_mute_active_app(action_config: dict):
    toggle_mute_active_app()


def action_volume_up_active_app(action_config: dict):
    step = action_config.get("step", 0.05)
    change_volume_active_app(step)


def action_volume_down_active_app(action_config: dict):
    step = action_config.get("step", 0.05)
    change_volume_active_app(-step)

"""
Action map
"""
ACTION_MAP = {
   "open_app": action_open_app,
   "open_url": action_open_url,
   "close_app": action_close_app,
   "print_active_app": action_print_active_app,
   "print_message": action_print_message,
   "toggle_mute_active_app": action_toggle_mute_active_app,
   "volume_up_active_app": action_volume_up_active_app,
   "volume_down_active_app": action_volume_down_active_app,
}

"""
Action execution
"""
def execute_action(action_config: dict):
   action_type = action_config.get("type")
   handler = ACTION_MAP.get(action_type)

   if handler is None:
      print(f"[WARNING] Unknown action type: {action_type}")
      return
   
   handler(action_config)

#testing to see if keys are registering
def debug_key_event(event):
   if event.event_type == "down":
      print(f"[DEBUG] key name={event.name}, scan_code={event.scan_code}")

"""
Global profile storage
"""
PROFILE = {}

"""
Key event handler
"""
def handle_key_event(event):
   if event.event_type != "down":
      return
   
   key_name = str(event.name).lower()

   print(f"[DEBUG] Key name={key_name}, scan_code={event.scan_code}")

   if key_name not in PROFILE:
      return
   
   action_config = PROFILE[key_name]

   print(f"[INFO] Triggering {key_name} -> {action_config.get('type')}")
   execute_action(action_config)

"""
Main
"""
def main():
    global PROFILE

    profile_path = "../profiles/default.json"

    print("=" * 60)
    print("CH552G JSON Macro Listener")
    print("=" * 60)
    print(f"Loading profile: {profile_path}")

    PROFILE = load_profile(profile_path)

    #test and see if the keys are even registering to my scripts
    keyboard.hook(debug_key_event)

    for hotkey, action_config in PROFILE.items():
       print(f"[INFO] Loaded {hotkey} -> {action_config.get('type')}")

    print("Listening for keypad input...")
    print("Press ESC on your main keyboard to quit.")
    print("=" * 60)

    keyboard.hook(handle_key_event)

    keyboard.wait("esc")

    print("[INFO] Macro listener stopped.")


if __name__ == "__main__":
    main()