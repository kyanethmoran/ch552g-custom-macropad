import keyboard

for key in ["f13", "f14", "f15", "f16", "f17", "f18", "f19", "f20", "f21"]:
    keyboard.on_press_key(key, lambda e, k=key: print(f"Pressed: {k}"))

print("Listening... press ESC to quit")
keyboard.wait("esc")