ACTION_UI_SCHEMA = {
    "open_app": {
        "fields": [
            {"name": "path", "label": "Path", "default": ""}
        ]
    },
    "open_url": {
        "fields": [
            {"name": "url", "label": "URL", "default": ""}
        ]
    },
    "open_folder": {
        "fields": [
            {"name": "path", "label": "Folder Path", "default": ""}
        ]
    },
    "close_app": {
        "fields": [
            {"name": "process_name", "label": "Process Name", "default": ""}
        ]
    },
    "send_hotkey": {
        "fields": [
            {"name": "keys", "label": "Keys", "default": ""}
        ]
    },
    "print_active_app": {
        "fields": []
    },
    "print_message": {
        "fields": [
            {"name": "message", "label": "Message", "default": ""}
        ]
    },
    "toggle_mute_active_app": {
        "fields": []
    },
    "volume_up_active_app": {
        "fields": [
            {"name": "step", "label": "Step", "default": 0.05}
        ]
    },
    "volume_down_active_app": {
        "fields": [
            {"name": "step", "label": "Step", "default": 0.05}
        ]
    },
}

ACTION_TYPES = list(ACTION_UI_SCHEMA.keys())