#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This module contains the OpenFileField class.
"""
import gi
import os
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from mosaicomponents.field import Field


class OpenFileField(Field):
    """
    This class contains methods related the OpenFileField class.
    """

    configuration = {"label": "", "value": "", "name": ""}

    # --------------------------------------------------------------------------
    def __init__(self, data, event):
        """
        This method is the constructor.
        """
        if not isinstance(data, dict):
            return
        Field.__init__(self, data, event)

        self.check_values()
        self.create_label()

        self.file = self.data["value"]
        self.parent_window = None
        self.field = Gtk.Entry()
        self.field.set_text(self.file)
        if event is not None:
            self.field.connect("changed", event)
        self.add(self.field)

        button = Gtk.Button.new_from_icon_name("gtk-file", Gtk.IconSize.BUTTON)
        button.connect("clicked", self.on_choose_file)
        self.add(button)
        self.show_all()

    # --------------------------------------------------------------------------
    def set_parent_window(self, widget):
        self.parent_window = widget

    # --------------------------------------------------------------------------
    def on_choose_file(self, widget):
        dialog = Gtk.FileChooserDialog("Open...",
                                       self.parent_window,
                                       Gtk.FileChooserAction.OPEN,
                                       (Gtk.STOCK_CANCEL,
                                        Gtk.ResponseType.CANCEL,
                                        Gtk.STOCK_OPEN,
                                        Gtk.ResponseType.OK)
                                       )
        current_dir = ""
        if os.path.isdir(self.field.get_text()):
            current_dir = self.field.get_text()
        else:
            current_dir = os.path.dirname(self.field.get_text())
        dialog.set_current_folder(current_dir)

        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            self.field.set_text(dialog.get_filename())
        elif response == Gtk.ResponseType.CANCEL:
            pass
        dialog.destroy()

    # --------------------------------------------------------------------------
    def get_value(self):
        return self.field.get_text()

    # --------------------------------------------------------------------------
    def set_value(self, value):
        self.field.set_text(value)

# --------------------------------------------------------------------------
