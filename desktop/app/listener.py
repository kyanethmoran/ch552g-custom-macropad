import threading 
import keyboard
from actions import (
  open_app,
  open_url,
  open_folder,
  close_process_by_name,
  send_hotkey,
  print_forground_app,
  toggle_mute_active_app,
  change_volume_active_app,
)
from config import load_profile
from validator import validate_profile

#ACTION WRAPPER FUNCTIONS

def action_open_app(action_config: dict):
    open_app(action_config["path"])


def action_open_url(action_config: dict):
    open_url(action_config["url"])


def action_open_folder(action_config: dict):
    open_folder(action_config["path"])


def action_close_app(action_config: dict):
    close_process_by_name(action_config["process_name"])


def action_send_hotkey(action_config: dict):
    send_hotkey(action_config["keys"])


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

# ACTION DISPATCH MAP
ACTION_MAP = {
    "open_app": action_open_app,
    "open_url": action_open_url,
    "open_folder": action_open_folder,
    "close_app": action_close_app,
    "send_hotkey": action_send_hotkey,
    "print_active_app": action_print_active_app,
    "print_message": action_print_message,
    "toggle_mute_active_app": action_toggle_mute_active_app,
    "volume_up_active_app": action_volume_up_active_app,
    "volume_down_active_app": action_volume_down_active_app,
}

# LISTENER CLASS
class MacroListener:
  def __init__(self, profile_path: str):
      self.profile_path = profile_path
      self.profile = {}
      self.validation_errors = []
      self.running = False

      self._hook = None

  # PROFILE LOADING
  def load_profile(self):
      raw_profile = load_profile(self.profile_path)
      valid_profile, errors = validate_profile(raw_profile)

      self.profile = valid_profile
      self.validation_errors = errors

      return valid_profile, errors

  # ACTION EXECUTION
  def execute_action(self, action_config: dict):
      action_type = action_config.get("type")

      if not isinstance(action_type, str):
          print(f"[WARNING] Invalid action config, missing type: {action_config}")
          return
      
      handler = ACTION_MAP.get(action_type)

      if handler is None:
          print (f"[WARNING] Unknown action type: {action_type}")
          return
      
      handler(action_config)

  # KEY EVENT HANDLER
  def handle_key_event(self, event):
      if event.event_type != "down":
          return
      
      key_name = str(event.name).lower()

      if key_name not in self.profile:
          return
      
      action_config = self.profile[key_name]

      print(f"[INFO] Triggering {key_name} -> {action_config.get('type')}")
      self.execute_action(action_config)
  
  # START
  def start(self):
      if self.running:
          print("[INFO] Listener is already running.")
          return self.validation_errors
      
      _, errors = self.load_profile()

      self._hook = keyboard.hook(self.handle_key_event)
      self.running = True

      print("[INFO] Listener started.")
      return errors
  
  # STOP
  def stop(self):
      if not self.running:
          print("[INFO] Listener is not running")

      if self._hook is not None:
          keyboard.unhook(self._hook)
          self._hook = None

      self.running = False
      print ("[INFO] Listener stopped")

  # RELOAD
  def reload(self):
      _, errors = self.load_profile()
      print("[INFO] Listener profile reloaded.")
      return errors