# Import StreamController modules
from src.backend.PluginManager.PluginBase import PluginBase
from src.backend.PluginManager.ActionHolder import ActionHolder
from src.backend.PluginManager.ActionBase import ActionBase

# Import GTK/Adw for UI
import gi
gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")
from gi.repository import Gtk, Adw

import datetime

class DaysUntilAction(ActionBase):
    """
    Action that allows the user to enter a date and shows the number of days until that date.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Do NOT access self.settings here!
        self.top_label = None
        self.center_label = None
        self.date_entry_row = None

    def get_config_rows(self):
        target_date_str = ""
        if hasattr(self, "settings") and self.settings is not None:
            target_date_str = self.settings.get("target_date", "")
        self.date_entry_row = Adw.EntryRow(
            title="Target Date",
            placeholder_text="yyyy/mm/dd",
            text=target_date_str
        )
        self.date_entry_row.connect("changed", self.on_date_changed)
        return [self.date_entry_row]

    def on_date_changed(self, entry_row, *args):
        if hasattr(self, "settings") and self.settings is not None:
            self.settings["target_date"] = entry_row.get_text()
        self.update_labels()

    def on_ready(self):
        self.update_labels()

    def update_labels(self):
        date_str = ""
        if hasattr(self, "settings") and self.settings is not None:
            date_str = self.settings.get("target_date", "").strip()
        if self.top_label:
            self.top_label.set_label(f"Days until {date_str if date_str else '____/__/__'}")
        if self.center_label:
            days = self.calculate_days_until(date_str)
            self.center_label.set_label(str(days) if days is not None else "—")

    def set_top_label(self, label_widget):
        self.top_label = label_widget
        self.update_labels()

    def set_center_label(self, label_widget):
        self.center_label = label_widget
        self.update_labels()

    def calculate_days_until(self, date_str):
        try:
            # Accept yyyy/mm/dd or yyyy-mm-dd
            date_str = date_str.replace("-", "/")
            target_date = datetime.datetime.strptime(date_str, "%Y/%m/%d").date()
            today = datetime.date.today()
            delta = (target_date - today).days
            return max(delta, 0)
        except Exception:
            return None

class DaysUntilPlugin(PluginBase):
    def __init__(self):
        super().__init__()
        self.days_until_holder = ActionHolder(
            plugin_base=self,
            action_base=DaysUntilAction,
            action_id="com_codeNinja_DaysUntil::DaysUntilAction",
            action_name="Days until"
        )
        self.add_action_holder(self.days_until_holder)
        self.register(
            plugin_name="Days until",
            github_repo="https://github.com/StreamController/DaysUntilPlugin",
            plugin_version="1.0.0",
            app_version="1.1.1-alpha"
        )
