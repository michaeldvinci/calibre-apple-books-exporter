#!/usr/bin/env python
# -*- coding: utf-8 -*-

from qt.core import QToolButton, QInputDialog
from calibre.gui2.actions import InterfaceAction
import platform
import tempfile
import os
import subprocess


class AppleBooksGuiAction(InterfaceAction):

    name = 'Send to Apple Books'
    description = 'Send selected books to Apple Books on Mac'
    action_spec = ('Send to Apple Books', 'book.png', 'Send selected books to Apple Books', None)
    action_type = 'current'
    all_locations = frozenset({
        'context-menu',
        'context-menu-split',
        'toolbar',
        'menubar',
    })

    def genesis(self):
        self.qaction.triggered.connect(self.send_books)
        try:
            self.gui.send_to_menu.addAction(self.qaction)
        except Exception:
            pass
        try:
            self.gui.toolBar().addAction(self.qaction)
        except Exception:
            pass

    def location_selected(self, loc):
        enabled = loc == 'library'
        self.qaction.setEnabled(enabled)
        if hasattr(self, 'menuless_qaction'):
            self.menuless_qaction.setEnabled(enabled)

    def send_books(self):
        gui = self.gui

        mac_ver = platform.mac_ver()[0]
        if mac_ver:
            major = int(mac_ver.split('.')[0])
            if major < 11:
                gui.status_bar.show_message('Send to Apple Books requires macOS 11 or later', 5000)
                return

        try:
            book_ids = gui.library_view.get_selected_ids()
        except Exception:
            rows = gui.library_view.selectionModel().selectedRows()
            book_ids = [gui.library_view.model().id(r) for r in rows]

        book_ids = [bid for bid in book_ids if bid is not None]
        if not book_ids:
            gui.status_bar.show_message('No books selected', 3000)
            return

        db = gui.current_db

        def _format_path(book_id, fmt):
            try:
                return db.format_path(book_id, fmt, index_is_id=True)
            except TypeError:
                return db.format_path(book_id, fmt)

        def _formats(book_id):
            try:
                return db.formats(book_id, index_is_id=True)
            except TypeError:
                return db.formats(book_id)

        for book_id in book_ids:
            mi = db.get_metadata(book_id, index_is_id=True, get_cover=False)
            formats = _formats(book_id) or ''
            format_list = [f.strip().upper() for f in formats.split(',') if f.strip()]
            possible_formats = [f for f in format_list if f in ['EPUB', 'PDF', 'MOBI', 'AZW3', 'TXT', 'HTML', 'RTF']]
            if not possible_formats:
                gui.status_bar.show_message(f'No suitable format for {mi.title}', 5000)
                continue

            if 'EPUB' in possible_formats:
                choices = ['EPUB'] + [f for f in possible_formats if f != 'EPUB']
            else:
                choices = possible_formats

            chosen_format = choices[0]
            if len(choices) > 1:
                chosen_format, ok = QInputDialog.getItem(
                    gui,
                    'Select format',
                    f'Select the format to send for "{mi.title}":',
                    choices,
                    0,
                    False
                )
                if not ok:
                    continue

            temp_file = None
            converted = False

            if chosen_format in ['EPUB', 'PDF']:
                temp_file = _format_path(book_id, chosen_format)
            else:
                from calibre.ebooks.conversion.plumber import Plumber
                plumber = Plumber(mi.title, mi.authors, mi, db)
                plumber.input_path = _format_path(book_id, chosen_format)
                plumber.output_format = 'epub'
                with tempfile.NamedTemporaryFile(suffix='.epub', delete=False) as f:
                    temp_file = f.name
                plumber.output_path = temp_file
                try:
                    plumber.run()
                    converted = True
                except Exception as e:
                    gui.status_bar.show_message(f'Failed to convert {mi.title}: {e}', 5000)
                    os.unlink(temp_file)
                    continue

            if temp_file:
                applescript = f'tell application "Books"\n'
                applescript += f'    activate\n'
                applescript += f'    open (POSIX file "{temp_file}" as alias)\n'
                applescript += 'end tell\n'
                script_path = None
                try:
                    with tempfile.NamedTemporaryFile(suffix='.applescript', delete=False, mode='w', encoding='utf-8') as script:
                        script.write(applescript)
                        script_path = script.name
                    result = subprocess.run(
                        ['osascript', script_path],
                        capture_output=True,
                        text=True,
                        timeout=30
                    )
                    if result.returncode == 0:
                        gui.status_bar.show_message(f'Sent {mi.title} to Apple Books', 3000)
                    else:
                        gui.status_bar.show_message(f'Failed to send {mi.title} to Apple Books: {result.stderr}', 5000)
                except subprocess.TimeoutExpired:
                    gui.status_bar.show_message(f'Timeout sending {mi.title} to Apple Books', 5000)
                except Exception as e:
                    gui.status_bar.show_message(f'Error sending {mi.title} to Apple Books: {e}', 5000)
                finally:
                    if script_path and os.path.exists(script_path):
                        os.unlink(script_path)

                if converted:
                    os.unlink(temp_file)
