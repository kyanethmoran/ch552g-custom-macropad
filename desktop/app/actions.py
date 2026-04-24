"""
Holds the actual functions
- open app
- open URL
- close app
- print active app
- mute/unmute active app
- change active app volume
"""

import subprocess
import webbrowser
import psutil
import win32gui
import win32process
import pythoncom
from pycaw.pycaw import AudioUtilities

def get_foreground_process_name():

  hwnd = win32gui.GetForegroundWindow()
  _, pid = win32process.GetWindowThreadProcessId(hwnd)

  try:
    return psutil.Process(pid).name()
  
  except Exception as error:
    print(f"[ERROR] Could not get foreground process name: {error}")
    return None
  
def print_forground_app():
  app_name = get_foreground_process_name()
  print(f"[DEBUG] Active app: {app_name}")

def open_app(path_or_command: str):
  try: 
    subprocess.Popen([path_or_command], shell=False)

  except Exception as error:
    print(f"[ERROR] Failed to open app '{path_or_command}': {error}")

def open_url(url: str):
  try:
    webbrowser.open(url)
    print(f"[ACTION] Opened URL: {url}")

  except Exception as error:
    print(f"[ERROR] Failed to open URL '{url}': {error}")

def close_process_by_name(process_name: str):
  found_any = False
  try:

    for proc in psutil.process_iter(["name"]):
      name = proc.info.get("name")

      if name and name.lower() == process_name.lower():
        proc.kill()
        found_any = True
        print(f"[ACTION] Closed process: {process_name}")

    if not found_any:
      print(f"[INFO] No running process found with name: {process_name}")

  except Exception as error:
    print(f"[ERROR] Failed to close process '{process_name}': {error}")

def toggle_mute_active_app():
    pythoncom.CoInitialize()

    try:
        foreground_process = get_foreground_process_name()

        if not foreground_process:
            print("[INFO] No foreground process found.")
            return

        sessions = AudioUtilities.GetAllSessions()

        for session in sessions:
            if session.Process and session.Process.name().lower() == foreground_process.lower():
                volume = session.SimpleAudioVolume
                is_muted = volume.GetMute()
                new_state = 0 if is_muted else 1
                volume.SetMute(new_state, None)

                app_name = session.Process.name()
                print(f"[ACTION] Toggled mute for {app_name}. New mute state: {new_state}")
                return

        print(f"[INFO] No active audio session found for {foreground_process}")

    except Exception as error:
        print(f"[ERROR] Failed to toggle mute: {error}")

    finally:
        pythoncom.CoUninitialize()

def change_volume_active_app(delta: float):
    pythoncom.CoInitialize()

    try:
        foreground_process = get_foreground_process_name()

        if not foreground_process:
            print("[INFO] No foreground process found.")
            return

        sessions = AudioUtilities.GetAllSessions()

        for session in sessions:
            if session.Process and session.Process.name().lower() == foreground_process.lower():
                volume = session.SimpleAudioVolume
                current_volume = volume.GetMasterVolume()
                new_volume = max(0.0, min(1.0, current_volume + delta))
                volume.SetMasterVolume(new_volume, None)

                app_name = session.Process.name()
                print(
                    f"[ACTION] Changed {app_name} volume from "
                    f"{current_volume:.2f} to {new_volume:.2f}"
                )
                return

        print(f"[INFO] No active audio session found for {foreground_process}")

    except Exception as error:
        print(f"[ERROR] Failed to change volume: {error}")

    finally:
        pythoncom.CoUninitialize()