#!/usr/bin/env python
# -*- coding: utf-8 -*-

from calibre.customize import InterfaceActionBase

class AppleBooksPlugin(InterfaceActionBase):

    name = 'Send to Apple Books'
    description = 'Send selected books to Apple Books on Mac'
    supported_platforms = ['osx']
    author = 'michaeldvinci'
    version = (1, 0, 0)
    minimum_calibre_version = (5, 0, 0)
    actual_plugin = 'calibre_plugins.book_bridge.ui:AppleBooksGuiAction'
