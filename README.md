# Send to Apple Books Calibre Plugin

This plugin allows you to send ebooks from Calibre directly to Apple Books on macOS.

## Installation

1. Zip the `apple_books_plugin` directory into a `.zip` file.
2. In Calibre, go to Preferences > Plugins > Load plugin from file.
3. Select the zip file and install.

Alternatively, you can place the `apple_books_plugin` directory in:
`~/Library/Preferences/calibre/plugins/`

## Usage

1. Select one or more books in Calibre.
2. Go to the "Send to" menu (or right-click > Send to).
3. Choose "Apple Books".
4. The books will be imported into Apple Books.

## Supported Formats

- EPUB (preferred)
- PDF
- Other formats will be automatically converted to EPUB

## Requirements

- Calibre 5.0 or later
- macOS 11 or later
- Apple Books app installed

## Notes

- The plugin uses AppleScript to interact with the Books application.
- Books will be added to your Apple Books library.
- Conversion may take some time for unsupported formats.