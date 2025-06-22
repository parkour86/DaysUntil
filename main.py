from src.backend.PluginManager.PluginBase import PluginBase
from src.backend.PluginManager.ActionHolder import ActionHolder
from src.backend.PluginManager.ActionBase import ActionBase
from src.backend.DeckManagement.InputIdentifier import Input
from src.backend.PluginManager.ActionInputSupport import ActionInputSupport
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
        self.date_entry_row = None

    def get_config_rows(self):
        log.debug("get_config_rows called")
        lm = self.plugin_base.locale_manager
        settings = self.get_settings()
        target_date_str = settings.get("target_date", "")
        self.date_entry_row = Adw.EntryRow(
            title=lm.get("actions.daysuntil.date.title")
        )
        self.date_entry_row.set_text(target_date_str)
        self.date_entry_row.connect("notify::text", self.on_date_changed)

        return [self.date_entry_row]

    def on_date_changed(self, entry_row, *args):
        settings = self.get_settings()
        new_date = entry_row.get_text()
        settings["target_date"] = new_date
        self.set_settings(settings)
        log.info(f"User set target_date to: {new_date}")
        self.update_labels()

    def on_ready(self):
        log.debug("on_ready called")
        self.update_labels()

    def update_labels(self):
        settings = self.get_settings()
        date_str = settings.get("target_date", "").strip()
        log.debug(f"Updating labels with date_str: {date_str}")
        self.set_top_label(
            f"Days until\n{date_str if date_str else '____/__/__'}",
            font_size=15,
            color=[0, 180, 255],
            update=True
        )
        if not date_str:
            self.set_bottom_label(
                "—",
                font_size=16,
                color=[180, 180, 180],
                update=True
            )
        else:
            days = self.calculate_days_until(date_str)
            if days is not None:
                self.set_bottom_label(
                    f"{days} days",
                    font_size=16,
                    color=[0, 200, 100],
                    update=True
                )
            else:
                self.set_bottom_label(
                    "—",
                    font_size=22,
                    color=[180, 180, 180],
                    update=True
                )

    def calculate_days_until(self, date_str):
        try:
            date_str = date_str.replace("-", "/")
            target_date = datetime.datetime.strptime(date_str, "%Y/%m/%d").date()
            today = datetime.date.today()
            delta = (target_date - today).days
            log.debug(f"target_date={target_date}, today={today}, delta={delta}")
            log.debug(f"Calculated days until {date_str}: {delta}")
            return max(delta, 0)
        except Exception as e:
            log.warning(f"Failed to parse date '{date_str}': {e}")
            return None

class DaysUntilPlugin(PluginBase):
    def __init__(self):
        super().__init__()
        lm = self.locale_manager
        self.days_until_holder = ActionHolder(
            plugin_base=self,
            action_base=DaysUntilAction,
            action_id_suffix="DaysUntilAction",
            action_name=lm.get("actions.daysuntil.name"),
            action_support={
                Input.Key: ActionInputSupport.SUPPORTED,
                Input.Dial: ActionInputSupport.UNTESTED,
                Input.Touchscreen: ActionInputSupport.UNTESTED
            }
        )
        self.add_action_holder(self.days_until_holder)
        self.register(
            plugin_name=lm.get("plugin.name"),
            github_repo="https://github.com/StreamController/DaysUntilPlugin",
            plugin_version="1.0.0",
            app_version="1.1.1-alpha"
        )
