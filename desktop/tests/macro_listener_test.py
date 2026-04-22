import subprocess
import psutil
import keyboard
import win32gui
import win32process

from pycaw.pycaw import AudioUtilities

# ============================================================
# This section holds values that are easy to change without
# digging through the rest of the code.
STEAM_PATH = r"G:\Steam\steam.exe"

SECOND_APP = "notepad.exe"

TEST_CLOSE_PROCESS = "notepad.exe"

VOLUME_STEP = 0.05
# ============================================================

def get_foreground_process_name():
    """
    Return the executable name of the currently focused window.

    Example outputs:
    - "chrome.exe"
    - "spotify.exe"
    - "notepad.exe"

    Returns None if the active window cannot be identified.
    """

    hwnd = win32gui.GetForegroundWindow()

    _, pid = win32process.GetWindowThreadProcessId(hwnd)

    try:
        process_name = psutil.Process(pid).name()
        return process_name
    except Exception as error:
        print(f"[ERROR] Could not get foreground process name: {error}")
        return None


def print_foreground_app():
    """
    Simple debug helper.

    This lets us test whether our code is correctly identifying
    the currently active app.
    """
    app_name = get_foreground_process_name()
    print(f"[DEBUG] Active app: {app_name}")


def get_audio_session_for_foreground():
    """
    Try to find the Windows audio session that matches the
    currently focused application.

    Returns:
    - a pycaw session object if found
    - None if the active app has no active audio session
    """

    foreground_process = get_foreground_process_name()

    if not foreground_process:
        print("[INFO] No foreground process found.")
        return None

    sessions = AudioUtilities.GetAllSessions()

    for session in sessions:
        if session.Process:
            session_name = session.Process.name()

            if session_name.lower() == foreground_process.lower():
                return session

    print(f"[INFO] No active audio session found for {foreground_process}")
    return None

def toggle_mute_active_app():
    """
    Toggle mute/unmute for the currently focused application's
    audio session.
    """

    session = get_audio_session_for_foreground()

    if session is None:
        print("[INFO] Could not toggle mute because no active audio session was found.")
        return

    try:
        volume = session.SimpleAudioVolume

        is_muted = volume.GetMute()

        new_state = 0 if is_muted else 1
        volume.SetMute(new_state, None)

        app_name = session.Process.name() if session.Process else "Unknown app"
        print(f"[ACTION] Toggled mute for {app_name}. New mute state: {new_state}")

    except Exception as error:
        print(f"[ERROR] Failed to toggle mute: {error}")


def change_volume_active_app(delta):
    """
    Raise or lower the volume of the currently focused app.

    Parameters:
    - delta: a float
        positive value  = volume up
        negative value  = volume down

    Example:
    - +0.05 raises volume by 5%
    - -0.05 lowers volume by 5%
    """

    session = get_audio_session_for_foreground()

    if session is None:
        print("[INFO] Could not change volume because no active audio session was found.")
        return

    try:
        volume = session.SimpleAudioVolume

        current_volume = volume.GetMasterVolume()

        new_volume = max(0.0, min(1.0, current_volume + delta))

        volume.SetMasterVolume(new_volume, None)

        app_name = session.Process.name() if session.Process else "Unknown app"
        print(
            f"[ACTION] Changed {app_name} volume from "
            f"{current_volume:.2f} to {new_volume:.2f}"
        )

    except Exception as error:
        print(f"[ERROR] Failed to change volume: {error}")

def open_app(path_or_command):
    """
    Open an application using either a full path or a simple command.

    Examples:
    - open_app(r"C:\Program Files (x86)\Steam\steam.exe")
    - open_app("notepad.exe")
    """

    try:
        subprocess.Popen(path_or_command, shell=True)
        print(f"[ACTION] Opened app: {path_or_command}")
    except Exception as error:
        print(f"[ERROR] Failed to open app '{path_or_command}': {error}")


def close_process_by_name(process_name):
    """
    Close all processes with the given executable name.

    Example:
    - close_process_by_name("notepad.exe")

    WARNING:
    This uses proc.kill(), which forcefully stops the process.
    That is fine for testing, but later you may want a safer
    or more graceful close for some applications.
    """

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

def register_hotkeys():
    """
    Register all keypad hotkeys and connect them to actions.
    """

    # F13 = Button 1
    keyboard.add_hotkey("f13", lambda: open_app(STEAM_PATH))

    # F14 = Button 2
    keyboard.add_hotkey("f14", lambda: open_app(SECOND_APP))

    # F15 = Button 3
    keyboard.add_hotkey("f15", lambda: close_process_by_name(TEST_CLOSE_PROCESS))

    # F16 = Button 4
    # Print the currently active app
    # This is mainly a debug tool right now
    keyboard.add_hotkey("f16", print_foreground_app)

    # F17 = Button 5
    keyboard.add_hotkey("f17", lambda: print("[ACTION] F17 pressed - placeholder action"))

    # F18 = Button 6
    keyboard.add_hotkey("f18", lambda: print("[ACTION] F18 pressed - placeholder action"))

    # F19 = Encoder press
    keyboard.add_hotkey("f19", toggle_mute_active_app)

    # F20 = Encoder clockwise
    keyboard.add_hotkey("f20", lambda: change_volume_active_app(VOLUME_STEP))

    # F21 = Encoder counterclockwise
    keyboard.add_hotkey("f21", lambda: change_volume_active_app(-VOLUME_STEP))

def main():
    """
    Start the macro listener test script.
    """

    print("=" * 60)
    print("CH552G Macro Listener Test")
    print("=" * 60)
    print("Listening for keypad input...")
    print("F13 -> Open Steam")
    print("F14 -> Open second app")
    print("F15 -> Close test process")
    print("F16 -> Print active app")
    print("F17 -> Placeholder")
    print("F18 -> Placeholder")
    print("F19 -> Toggle mute active app")
    print("F20 -> Volume up active app")
    print("F21 -> Volume down active app")
    print("Press ESC on your main keyboard to quit.")
    print("=" * 60)

    register_hotkeys()

    keyboard.wait("esc")

    print("[INFO] Macro listener stopped.")


if __name__ == "__main__":
    main()