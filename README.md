# DaysUntil Plugin for StreamController

**This plugin is designed for use with [StreamController](https://streamcontroller.core447.com/).**

## Overview

The **DaysUntil** plugin allows you to display the number of days remaining until a specified date directly on your StreamController device. It's perfect for countdowns to events, deadlines, holidays, or any important date you want to keep track of at a glance.

## Features

- **Custom Date Countdown:** Enter any target date and see the days remaining.
- **Flexible Date Format:** Switch between `yyyy/mm/dd` and `mm/dd/yyyy` display formats.
- **Live Updates:** The countdown updates automatically each day.
- **Localized Labels:** Supports multiple languages for plugin and action names.
- **Visual Feedback:** The plugin displays the target date and the countdown in a visually clear format.

## Usage

1. **Add the Plugin:**
   Install or add the DaysUntil plugin to your StreamController setup.

2. **Configure the Action:**
   - Open the configuration for the DaysUntil action.
   - Enter your target date in the provided field (e.g., `2025/12/31`).
   - Optionally, switch the date format to your preference.

3. **View the Countdown:**
   - The top label will show the action name and the target date.
   - The center label will display the number of days remaining.
   - If no date is set, a placeholder will be shown.

4. **Localization:**
   - The plugin supports multiple languages. You can add or edit locale files in the `locales/` directory.

## Technical Details

- Written in Python using GTK4 and Adwaita for UI components.
- Uses StreamController's plugin and action system.
- All configuration is persisted using StreamController's settings system.
- The plugin is fully open source and can be customized for your needs.

## License

MIT License. See [LICENSE](LICENSE) for details.

---

For more information about StreamController and available plugins, visit the [official documentation](https://streamcontroller.core447.com/).
