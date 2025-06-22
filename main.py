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
        self.date_format_switch = None

    def get_config_rows(self):
        lm = self.plugin_base.locale_manager
        settings = self.get_settings()
        target_date_str = settings.get("target_date", "")
        date_format_is_ymd = settings.get("date_format_ymd", True)

        self.date_entry_row = Adw.EntryRow(
            title=lm.get("actions.daysuntil.date.title")
        )
        self.date_entry_row.set_text(target_date_str)
        self.date_entry_row.connect("notify::text", self.on_date_changed)

        self.date_format_switch = Adw.SwitchRow(
            title=lm.get("actions.daysuntil.dateformat.title"),
            subtitle=lm.get("actions.daysuntil.dateformat.subtitle"),
        )
        self.date_format_switch.set_active(date_format_is_ymd)
        self.date_format_switch.connect("notify::active", self.on_date_format_toggled)

        return [self.date_entry_row, self.date_format_switch]

    def on_date_changed(self, entry_row, *args):
        settings = self.get_settings()
        new_date = entry_row.get_text()
        settings["target_date"] = new_date
        self.set_settings(settings)
        self.update_labels()

    def on_date_format_toggled(self, switch, *args):
        settings = self.get_settings()
        settings["date_format_ymd"] = switch.get_active()
        self.set_settings(settings)
        self.update_labels()

    def on_ready(self):
        self.update_labels()

    def update_labels(self):
        settings = self.get_settings()
        date_str = settings.get("target_date", "").strip()
        date_format_ymd = settings.get("date_format_ymd", True)

        # Format the date for display in the top label
        if date_str:
            try:
                # Accept both y/m/d and m/d/y input for display
                date_obj = None
                if date_format_ymd:
                    date_obj = datetime.datetime.strptime(date_str.replace("-", "/"), "%Y/%m/%d").date()
                    display_date = date_obj.strftime("%Y/%m/%d")
                else:
                    # Try parsing as m/d/y, fallback to y/m/d
                    try:
                        date_obj = datetime.datetime.strptime(date_str.replace("-", "/"), "%m/%d/%Y").date()
                    except Exception:
                        date_obj = datetime.datetime.strptime(date_str.replace("-", "/"), "%Y/%m/%d").date()
                    display_date = date_obj.strftime("%m/%d/%Y")
            except Exception:
                display_date = date_str
        else:
            display_date = "____/__/__" if date_format_ymd else "__/__/____"

        lm = self.plugin_base.locale_manager
        # Always show the placeholder if date_str is empty or cleared
        self.set_top_label(
            f"{lm.get('actions.daysuntil.name')}\n{display_date}",
            font_size=int(lm.get("actions.daysuntil.toplabel.font", 14)),
            color=[172, 244, 188],  # #ACF4BC
            font_family="Umpush:style=Bold",
            update=True
        )
        color = [253, 195, 123]  # #FDC37B

        days = self.calculate_days_until(date_str) if date_str else None

        if date_str and days is not None:
            label = f"\n{days} {lm.get('actions.daysuntil.days_label', 'days')}"
            font_size = 15
        else:
            label = "\n--"
            font_size = 22

        self.set_center_label(label, font_size=font_size, font_family="Umpush:style=Bold", color=color, update=True)

    def calculate_days_until(self, date_str):
        try:
            date_str = date_str.replace("-", "/")
            target_date = datetime.datetime.strptime(date_str, "%Y/%m/%d").date()
            today = datetime.date.today()
            delta = (target_date - today).days
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
