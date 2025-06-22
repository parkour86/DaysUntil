# Import StreamController modules
from src.backend.PluginManager.PluginBase import PluginBase
from src.backend.PluginManager.ActionHolder import ActionHolder
from src.backend.PluginManager.ActionBase import ActionBase
from loguru import logger as log

import gi
gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")
from gi.repository import Gtk, Adw

import datetime

class DaysUntilAction(ActionBase):
    HAS_CONFIGURATION = True  # Show config after adding

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.top_label = None
        self.center_label = None
        self.date_entry_row = None

    def get_config_rows(self):
        log.debug("get_config_rows called")

        # settings = self.get_settings()
        # target_date_str = settings.get("target_date", "")
        # log.debug(f"Loading config row with target_date: {target_date_str}")

        self.date_entry_row = Adw.EntryRow(
            title="Target Date",
            #placeholder_text="YYYY/MM/DD"
        )
        self.date_entry_row.connect("notify::text", self.on_date_changed)

        return [self.date_entry_row]

    def on_date_changed(self, entry_row, *args):
        settings = self.get_settings()
        new_date = entry_row.get_text()
        settings["target_date"] = new_date
        self.set_settings(settings)
        log.info(f"User set target_date to: {new_date}")
        #self.update_labels()

    def on_ready(self):
        log.debug("on_ready called")
        self.update_labels()

    def update_labels(self):
        settings = self.get_settings()
        date_str = settings.get("target_date", "").strip()
        log.debug(f"Updating labels with date_str: {date_str}")
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
            date_str = date_str.replace("-", "/")
            target_date = datetime.datetime.strptime(date_str, "%Y/%m/%d").date()
            today = datetime.date.today()
            delta = (target_date - today).days
            log.debug(f"Calculated days until {date_str}: {delta}")
            return max(delta, 0)
        except Exception as e:
            log.warning(f"Failed to parse date '{date_str}': {e}")
            return None

class DaysUntilPlugin(PluginBase):
    def __init__(self):
        super().__init__()
        # Use hardcoded action name instead of localization (for debugging)
        self.days_until_holder = ActionHolder(
            plugin_base=self,
            action_base=DaysUntilAction,
            action_id_suffix="DaysUntilAction",
            action_name="Days Until"
        )
        self.add_action_holder(self.days_until_holder)

        self.register(
            plugin_name="Days Until",  # ← Also hardcoded
            github_repo="https://github.com/StreamController/DaysUntilPlugin",
            plugin_version="1.0.0",
            app_version="1.1.1-alpha"
        )
