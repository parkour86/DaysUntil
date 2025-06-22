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
        self.calendar = None

    def get_config_rows(self):
        log.debug("get_config_rows called")

        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        box.set_margin_top(6)
        box.set_margin_bottom(6)
        box.set_margin_start(12)
        box.set_margin_end(12)

        label = Gtk.Label(label="Target Date", halign=Gtk.Align.START)
        box.append(label)

        self.calendar = Gtk.Calendar()
        box.append(self.calendar)

        settings = self.get_settings()
        target_date_str = settings.get("target_date", "")
        if target_date_str:
            try:
                dt = datetime.datetime.strptime(target_date_str, "%Y/%m/%d")
                self.calendar.select_month(dt.month - 1, dt.year)  # month 0-based
                self.calendar.select_day(dt.day)
            except Exception as e:
                log.warning(f"Failed to parse stored target_date: {e}")

        self.calendar.connect("day-selected-double-click", self.on_calendar_date_selected)
        self.calendar.connect("day-selected", self.on_calendar_date_selected)

        return [box]

    def on_calendar_date_selected(self, calendar, *args):
        year, month, day = calendar.get_date()  # month is zero-based
        date_str = f"{year}/{month+1:02d}/{day:02d}"

        settings = self.get_settings()
        settings["target_date"] = date_str
        self.set_settings(settings)

        log.info(f"User selected date: {date_str}")
        self.update_labels()

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

        self.days_until_holder = ActionHolder(
            plugin_base=self,
            action_base=DaysUntilAction,
            action_id_suffix="DaysUntilAction",
            action_name="Days Until"
        )
        self.add_action_holder(self.days_until_holder)

        self.register(
            plugin_name="Days Until",
            github_repo="https://github.com/StreamController/DaysUntilPlugin",
            plugin_version="1.0.0",
            app_version="1.1.1-alpha"
        )
