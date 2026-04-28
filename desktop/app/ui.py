import customtkinter as ctk
from tkinter import messagebox

from action_schema import ACTION_TYPES, ACTION_UI_SCHEMA
from config import load_profile, save_profile
from validator import validate_profile

class MacroApp(ctk.CTk):
  def __init__(self, profile_path: str, listener):
        super().__init__()

        self.profile_path = profile_path
        self.listener = listener

        # Example shape:
        # self.row_widgets["f13"] = {
        #     "type_var": ...,
        #     "field1_label": ...,
        #     "field1_entry": ...,
        #     "field2_label": ...,
        #     "field2_entry": ...
        # }
        self.row_widgets = {}

        self.title("CH552G Macro Pad")
        self.geometry("980x680")

        # Configure the main window layout
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self._build_header()
        self._build_editor_area()
        self._build_footer()

        # Load the current default profile into the UI on startup
        self.load_profile_into_ui()

    # UI BUILD
  def _build_header(self):
      """
      Build the top header section of the window.
      """
      header = ctk.CTkFrame(self)
      header.grid(row=0, column=0, sticky="ew", padx=12, pady=(12, 6))
      header.grid_columnconfigure(0, weight=1)

      title = ctk.CTkLabel(
          header,
          text="CH552G Default Profile Editor",
          font=ctk.CTkFont(size=22, weight="bold"),
      )
      title.grid(row=0, column=0, sticky="w", padx=12, pady=(10, 2))

      subtitle = ctk.CTkLabel(
          header,
          text="Edit default.json, save changes, and control the listener.",
          font=ctk.CTkFont(size=13),
      )
      subtitle.grid(row=1, column=0, sticky="w", padx=12, pady=(0, 10))

  def _build_editor_area(self):
      """
      Build the scrollable area where the hotkey rows will appear.
      """
      self.editor = ctk.CTkScrollableFrame(self)
      self.editor.grid(row=1, column=0, sticky="nsew", padx=12, pady=6)

      # Column layout:
      # 0 = hotkey label
      # 1 = action type dropdown
      # 2 = field1 label
      # 3 = field1 entry
      # 4 = field2 label
      # 5 = field2 entry
      self.editor.grid_columnconfigure(0, weight=0)
      self.editor.grid_columnconfigure(1, weight=0)
      self.editor.grid_columnconfigure(2, weight=0)
      self.editor.grid_columnconfigure(3, weight=1)
      self.editor.grid_columnconfigure(4, weight=0)
      self.editor.grid_columnconfigure(5, weight=1)

  def _build_footer(self):
      """
      Build the bottom control buttons and status label.
      """
      footer = ctk.CTkFrame(self)
      footer.grid(row=2, column=0, sticky="ew", padx=12, pady=(6, 12))
      footer.grid_columnconfigure(0, weight=1)

      button_row = ctk.CTkFrame(footer, fg_color="transparent")
      button_row.grid(row=0, column=0, sticky="ew", padx=10, pady=(10, 4))

      ctk.CTkButton(
          button_row,
          text="Load Profile",
          command=self.load_profile_into_ui,
      ).pack(side="left", padx=6)

      ctk.CTkButton(
          button_row,
          text="Save Profile",
          command=self.save_profile_from_ui,
      ).pack(side="left", padx=6)

      ctk.CTkButton(
          button_row,
          text="Start Listener",
          command=self.start_listener,
      ).pack(side="left", padx=6)

      ctk.CTkButton(
          button_row,
          text="Stop Listener",
          command=self.stop_listener,
      ).pack(side="left", padx=6)

      ctk.CTkButton(
          button_row,
          text="Reload Listener",
          command=self.reload_listener,
      ).pack(side="left", padx=6)

      self.status_label = ctk.CTkLabel(
          footer,
          text="Status: Ready",
          anchor="w",
      )
      self.status_label.grid(row=1, column=0, sticky="ew", padx=12, pady=(4, 10))

  # PROFILE -> UI
  def load_profile_into_ui(self):
      """
      Load the JSON profile from disk and rebuild all hotkey rows.
      """
      try:
          profile = load_profile(self.profile_path)
      except Exception as error:
          messagebox.showerror("Load Error", f"Failed to load profile:\n{error}")
          return

      # Remove old rows before rebuilding
      for child in self.editor.winfo_children():
          child.destroy()

      self.row_widgets.clear()

      # Build rows in sorted order for predictable layout
      for row_index, hotkey in enumerate(sorted(profile.keys())):
          action_config = profile[hotkey]
          self._build_hotkey_row(row_index, hotkey, action_config)

      self.set_status("Status: Profile loaded.")

  def _build_hotkey_row(self, row_index: int, hotkey: str, action_config: dict):
      """
      Build one editable row for one hotkey.
      """
      hotkey_label = ctk.CTkLabel(
          self.editor,
          text=hotkey.upper(),
          font=ctk.CTkFont(weight="bold"),
          width=70,
      )
      hotkey_label.grid(row=row_index, column=0, padx=8, pady=8, sticky="w")

      action_type = action_config.get("type", "print_message")

      type_var = ctk.StringVar(value=action_type)
      type_menu = ctk.CTkOptionMenu(
          self.editor,
          values=ACTION_TYPES,
          variable=type_var,
          command=lambda _value, hk=hotkey: self.refresh_row_fields(hk),
          width=190,
      )
      type_menu.grid(row=row_index, column=1, padx=8, pady=8, sticky="ew")

      field1_label = ctk.CTkLabel(self.editor, text="Field 1")
      field1_label.grid(row=row_index, column=2, padx=8, pady=8, sticky="e")

      field1_entry = ctk.CTkEntry(self.editor)
      field1_entry.grid(row=row_index, column=3, padx=8, pady=8, sticky="ew")

      field2_label = ctk.CTkLabel(self.editor, text="Field 2")
      field2_label.grid(row=row_index, column=4, padx=8, pady=8, sticky="e")

      field2_entry = ctk.CTkEntry(self.editor)
      field2_entry.grid(row=row_index, column=5, padx=8, pady=8, sticky="ew")

      self.row_widgets[hotkey] = {
          "type_var": type_var,
          "field1_label": field1_label,
          "field1_entry": field1_entry,
          "field2_label": field2_label,
          "field2_entry": field2_entry,
      }

      self.populate_row_fields(hotkey, action_config)

  def populate_row_fields(self, hotkey: str, action_config: dict):
      """
      Read the selected action type's schema and configure the
      row fields automatically.
      """
      widgets = self.row_widgets[hotkey]
      action_type = widgets["type_var"].get()

      field1_label = widgets["field1_label"]
      field1_entry = widgets["field1_entry"]
      field2_label = widgets["field2_label"]
      field2_entry = widgets["field2_entry"]

      # Clear old values before repopulating
      field1_entry.delete(0, "end")
      field2_entry.delete(0, "end")

      # Show everything first, then hide what is not needed
      field1_label.grid()
      field1_entry.grid()
      field2_label.grid()
      field2_entry.grid()

      schema = ACTION_UI_SCHEMA.get(action_type, {"fields": []})
      fields = schema.get("fields", [])

      # If the action needs no fields, hide both input areas
      if len(fields) == 0:
          field1_label.grid_remove()
          field1_entry.grid_remove()
          field2_label.grid_remove()
          field2_entry.grid_remove()
          return

      # Configure the first field
      field1 = fields[0]
      field1_label.configure(text=field1["label"])
      field1_value = action_config.get(field1["name"], field1.get("default", ""))
      field1_entry.insert(0, str(field1_value))

      # Configure the second field if present
      if len(fields) >= 2:
          field2 = fields[1]
          field2_label.configure(text=field2["label"])
          field2_value = action_config.get(field2["name"], field2.get("default", ""))
          field2_entry.insert(0, str(field2_value))
      else:
          field2_label.grid_remove()
          field2_entry.grid_remove()

  def refresh_row_fields(self, hotkey: str):
      """
      Refresh the visible row fields when the action type dropdown changes.
      """
      action_type = self.row_widgets[hotkey]["type_var"].get()
      self.populate_row_fields(hotkey, {"type": action_type})

  # UI -> PROFILE
  def collect_profile_from_ui(self):
      """
      Read all UI rows and convert them into a profile dictionary.
      This is schema-driven, so it reads field definitions from
      ACTION_UI_SCHEMA instead of hardcoded if/elif logic.
      """
      profile = {}

      for hotkey, widgets in self.row_widgets.items():
          action_type = widgets["type_var"].get()
          field1 = widgets["field1_entry"].get().strip()
          field2 = widgets["field2_entry"].get().strip()

          action_config = {"type": action_type}

          schema = ACTION_UI_SCHEMA.get(action_type, {"fields": []})
          fields = schema.get("fields", [])

          # Save first field if this action type uses one
          if len(fields) >= 1:
              field_name = fields[0]["name"]
              action_config[field_name] = self._coerce_field_value(field_name, field1)

          # Save second field if this action type uses one
          if len(fields) >= 2:
              field_name = fields[1]["name"]
              action_config[field_name] = self._coerce_field_value(field_name, field2)

          profile[hotkey] = action_config

      return profile

  def _coerce_field_value(self, field_name: str, value: str):
      """
      Convert text input into better Python values where needed.

      For now:
      - 'step' should become a float if possible
      - everything else stays as a string
      """
      if field_name == "step":
          if value == "":
              return 0.05

          try:
              return float(value)
          except ValueError:
              # Keep the bad value so validation can reject it clearly
              return value

      return value

   
  # SAVE / LISTENER CONTROLS
    
  def save_profile_from_ui(self):
      """
      Collect the current UI state, validate it, and save it to disk.
      """
      profile = self.collect_profile_from_ui()
      valid_profile, errors = validate_profile(profile)

      if errors:
          messagebox.showwarning(
              "Validation Error",
              "The profile has invalid entries:\n\n" + "\n".join(f"- {e}" for e in errors),
          )
          self.set_status("Status: Save failed due to validation errors.")
          return

      try:
          save_profile(self.profile_path, valid_profile)
          self.set_status("Status: Profile saved successfully.")
          messagebox.showinfo("Saved", "Default profile saved successfully.")
      except Exception as error:
          messagebox.showerror("Save Error", f"Failed to save profile:\n{error}")
          self.set_status("Status: Save failed.")

  def start_listener(self):
      """
      Start the macro listener using the current saved profile.
      """
      errors = self.listener.start()

      if errors:
          messagebox.showwarning(
              "Listener Validation Warnings",
              "Some profile entries were invalid and skipped:\n\n" +
              "\n".join(f"- {e}" for e in errors)
          )

      self.set_status("Status: Listener started.")

  def stop_listener(self):
      """
      Stop the macro listener.
      """
      self.listener.stop()
      self.set_status("Status: Listener stopped.")

  def reload_listener(self):
      """
      Reload the saved profile into the active listener.
      """
      errors = self.listener.reload()

      if errors:
          messagebox.showwarning(
              "Reload Validation Warnings",
              "Some profile entries were invalid and skipped:\n\n" +
              "\n".join(f"- {e}" for e in errors)
          )

      self.set_status("Status: Listener reloaded.")

  # STATUS HELPER
  def set_status(self, text: str):
      """
      Update the footer status message.
      """
      self.status_label.configure(text=text)