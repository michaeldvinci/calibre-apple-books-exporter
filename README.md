# Send to Apple Books Calibre Plugin

This plugin allows you to send ebooks from Calibre directly to Apple Books on macOS.

## Installation

1. Install the plugin from `apple_books_plugin_fixed.zip`.
2. In Calibre, go to Preferences > Plugins > Load plugin from file.
3. Select `apple_books_plugin_fixed.zip` and install.

## Usage

1. Select one or more books in Calibre.
2. Click the toolbar icon for "Send to Apple Books".
3. If the toolbar icon is not visible, add it from Calibre's toolbar customization.
4. You can also use the action from the "Send to" menu.

## Toolbar Icon

- The plugin includes a Calibre toolbar icon using `book.png`.
- This is the primary access point for sending books to Apple Books.
- If the icon is missing, look for "Send to Apple Books" in toolbar customization.

## Supported Formats

- EPUB (preferred)
- PDF
- Other formats will be offered for conversion to EPUB when selected

## Requirements

- Calibre 5.0 or later
- macOS 11 or later
- Apple Books app installed

## Notes

- The plugin uses AppleScript to interact with the Books application.
- Books will be added to your Apple Books library.
- Conversion may take some time for unsupported formats.
