#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# Copyright (C) 2020 Brandon M. Pace
#
# This file is part of Quick Route Checker
#
# Quick Route Checker is free software: you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# Quick Route Checker is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with Quick Route Checker.
# If not, see <https://www.gnu.org/licenses/>.

"""
This module implements another layer of GUI functionality beyond the base.
"""

import logging
import os
import routeparser
import wx
import wx.adv

from collections import defaultdict
from typing import Callable, Dict, List, Optional

if __name__ == "__main__":
    # allow running this file directly to inspect GUI changes
    from RouteCheckerGUIbase import BaseMainFrame, PasteDialogBase, RoutePanelBase, HIGHLIGHT_MODE, MAX_FILE_SIZE
    from resources import RouteChecker128, RouteCheckerIcon
else:
    from .RouteCheckerGUIbase import BaseMainFrame, PasteDialogBase, RoutePanelBase, HIGHLIGHT_MODE, MAX_FILE_SIZE
    from .resources import RouteChecker128, RouteCheckerIcon


logger = logging.getLogger(__name__)


class MainFrame(BaseMainFrame):
    def __init__(self, *args, **kwds):
        BaseMainFrame.__init__(self, *args, **kwds)
        self.SetIcon(RouteCheckerIcon.GetIcon())
        self.__add_bindings()
        self.Center()

    def __add_bindings(self):
        """Add extra event handler bindings"""
        self.Bind(wx.EVT_BUTTON, self.on_button_file_submit, self.notebook_main.button_file_submit)
        self.Bind(wx.EVT_BUTTON, self.on_button_paste_text, self.notebook_main.button_paste_text)
        self.Bind(wx.EVT_NOTEBOOK_PAGE_CHANGED, self.on_notebook_page_changed, self.notebook_main)

    def generate_tab_name(self, prefix: str = "") -> str:
        """Generate a tab name that is not currently used"""
        counter = 0
        while True:
            name = f"{prefix}{counter}"
            if self.notebook_main.GetPageByText(name) is None:
                return name
            else:
                counter += 1

    def handle_new_input_source(self, tab_name: str, lines: List[str]) -> bool:
        """Parse input lines into route objects and populate a new tab on success."""
        matches = routeparser.identify_input(lines)
        if not matches:
            show_error("Unable to identify type of route command output")
            return False

        if len(matches) == 1:
            selection = matches[0]
        else:
            logger.info(f"Multiple matches: '{matches}'")
            question = wx.SingleChoiceDialog(
                self, "Could not identify input type. Please choose one:", "Error", matches
            )
            response = question.ShowModal()
            if response == wx.ID_OK:
                selection = question.GetStringSelection()
                print(selection)
            elif response == wx.ID_CANCEL:
                logger.warning(f"User aborted parsing from multiple match dialog")
                return False
            else:
                logger.error(f"Dialog returned unexpected value: '{response}'")
                return False

        try:
            routes = routeparser.function_for_content_type(selection)(lines)
        except Exception as E:
            logger.exception(f"Exception while parsing routes")
            show_error(str(E))
            return False

        new_panel = RoutePanel(self.notebook_main)
        new_panel.set_routes(routes)
        self.notebook_main.AddPage(new_panel, tab_name, select=True)
        return True

    def on_button_file_submit(self, event):
        filepath = self.notebook_main.filepicker_source_input.GetPath()
        if not filepath:
            return show_error("No file was specified")
        elif not os.path.isfile(filepath):
            return show_error(f"Path does not appear to be a file: {filepath}")
        elif os.path.getsize(filepath) > MAX_FILE_SIZE:
            return show_error(f"File is greater than 1MB (unlikely to contain valid command output)")

        with open(filepath, 'r', errors='replace') as file_handle:
            lines = file_handle.readlines()

        filename = os.path.split(filepath)[1]
        if not filename:
            return show_error("Could not extract filename from provided path")
        if self.notebook_main.GetPageByText(filename) is None:
            tab_name = filename
        else:
            for number in range(1, 10):
                temp_name = f"{filename} ({number})"
                if self.notebook_main.GetPageByText(temp_name) is None:
                    tab_name = temp_name
                    break
            else:
                return show_error("Maximum number of tabs with same filename reached")

        self.handle_new_input_source(tab_name, lines)

    def on_button_paste_text(self, event):
        """Display dialog box that allows pasting route command output"""
        dialog = PasteDialog(self)
        dialog.ShowWindowModal()

    def on_menu_about(self, event):
        event.Skip()
        program_description = \
            """Quick Route Checker allows importing text-format routing tables and checking route determination for a given IP or subnet.\n\n"""
        program_description += f"Supported command outputs: {routeparser.input_types}" "\n"
        program_license = \
            "LGPL-3.0-or-later (GNU Lesser General Public License 3.0 or later)\n" \
            "See the files COPYING and COPYING.LESSER distributed with this program\n" \
            "or https://www.gnu.org/licenses/ if you did not receive them with your copy."
        info = wx.adv.AboutDialogInfo()
        info.SetIcon(RouteChecker128.GetIcon())
        info.SetName("Quick Route Checker")
        info.SetVersion("0.2")
        info.SetDescription(program_description)
        info.SetCopyright('(C) 2020 Brandon M. Pace <brandonmpace@gmail.com>')
        info.SetWebSite("https://github.com/brandonmpace/Quick-Route-Checker")
        info.SetLicense(program_license)
        # info.AddDeveloper('Brandon M. Pace <brandonmpace@gmail.com>')

        wx.adv.AboutBox(info, parent=self)

    def on_menu_close_all_tabs(self, event):
        page_count = self.notebook_main.GetPageCount()
        if page_count > 1:
            for page_number in range(1, page_count):
                self.notebook_main.DeletePage(1)
            self.frame_main_menubar.menu_item_close_all_tabs.Enable(False)
        else:
            logger.debug(f"no action as page count is {page_count}")

    def on_menu_close_tab(self, event):
        self.notebook_main.DeleteCurrentPage()

    def on_menu_exit(self, event):
        self.Close()

    def on_notebook_page_changed(self, event: wx.BookCtrlEvent):
        destination = event.GetSelection()
        if destination == 0:
            # Prevent closing the default/initial tab
            self.frame_main_menubar.menu_item_close_tab.Enable(False)
        else:
            self.frame_main_menubar.menu_item_close_tab.Enable()

        page_count = self.notebook_main.GetPageCount()
        if page_count == 0:
            logger.error("the default tab seems to have gone missing!")
        elif page_count == 1:
            self.frame_main_menubar.menu_item_close_all_tabs.Enable(False)
        elif page_count > 1:
            self.frame_main_menubar.menu_item_close_all_tabs.Enable(True)


class MainApp(wx.App):
    def OnInit(self):
        self.frame_main = MainFrame(None, wx.ID_ANY, "")
        self.SetTopWindow(self.frame_main)
        self.frame_main.Show()
        return True


class PasteDialog(PasteDialogBase):
    """Dialog where user can paste lines of output for processing"""
    def __init__(self, parent: MainFrame, *args, **kwds):
        PasteDialogBase.__init__(self, parent, *args, **kwds)
        self.SetIcon(RouteCheckerIcon.GetIcon())

    def on_button_paste_cancel(self, event):
        self.Close()
        self.Destroy()

    def on_button_paste_ok(self, event):
        parent: MainFrame = self.GetParent()
        tab_name = self.text_ctrl_tab_name_input.GetValue()

        if not tab_name:
            tab_name = parent.generate_tab_name(prefix="pasted_")
            self.text_ctrl_tab_name_input.SetValue(tab_name)

        if parent.notebook_main.GetPageByText(tab_name) is not None:
            return show_error(f"Tab with name '{tab_name}' already exists!")

        lines = self.text_ctrl_paste.GetValue()
        if not lines:
            return show_error("Please provide input or select Cancel")

        if parent.handle_new_input_source(tab_name, lines.split("\n")):
            self.Close()
            self.Destroy()


class RoutePanel(RoutePanelBase):
    def __init__(self, *args, **kwds):
        RoutePanelBase.__init__(self, *args, **kwds)
        self.routes: Optional[routeparser.RoutingTable] = None
        self.list_id_to_route = {}
        self.route_to_list_id = {}
        self.init_route_columns()
        self.updating = False

    def init_route_columns(self):
        """Create the columns in the route ListCtrl"""
        self.list_ctrl_routes.DeleteAllColumns()
        self.list_ctrl_routes.AppendColumn('Network', format=wx.LIST_FORMAT_RIGHT, width=150)
        self.list_ctrl_routes.AppendColumn('Mask', width=150)
        self.list_ctrl_routes.AppendColumn('Gateway', width=210)
        self.list_ctrl_routes.AppendColumn('Interface', width=210)
        self.list_ctrl_routes.AppendColumn('Metric')

    def on_list_item_deselected(self, event):
        if self.updating:
            return
        else:
            self.updating = True
            self.radio_box_highlight_mode.SetSelection(HIGHLIGHT_MODE.NONE)
            self.updating = False

    def on_list_item_selected(self, event):
        if self.updating:
            return
        else:
            self.updating = True
            self.radio_box_highlight_mode.SetSelection(HIGHLIGHT_MODE.NONE)
            self.updating = False

    def on_radiobox_highlight_mode(self, event: wx.CommandEvent):
        if self.updating:
            logger.debug("returning early as internal update is happening")
            return
        else:
            self.updating = True
            self.refresh_highlighted_routes()
            self.updating = False

    def on_text_address_input(self, event):
        self.updating = True
        value = self.text_ctrl_address_input.GetValue()
        highlight_mode_selection = self.radio_box_highlight_mode.GetSelection()

        if value and self.routes:
            if highlight_mode_selection == HIGHLIGHT_MODE.NONE:
                self.radio_box_highlight_mode.SetSelection(HIGHLIGHT_MODE.BEST_MATCH)

        self.refresh_highlighted_routes()

        self.updating = False

    def refresh_displayed_routes(self):
        try:
            self.list_ctrl_routes.DeleteAllItems()
            self.list_id_to_route.clear()
            self.route_to_list_id.clear()
            for route in self.routes.routes:
                index = self.list_ctrl_routes.Append(
                    (
                        route.network.compressed,
                        route.netmask,
                        route.gateway.compressed if route.gateway else "",
                        route.interface,
                        route.metric
                    )
                )
                self.list_id_to_route[index] = route
                self.route_to_list_id[route] = index
        except Exception:
            logger.exception("Exception while refreshing routes")
            raise

    def refresh_highlighted_routes(self):
        highlight_mode_selection = self.radio_box_highlight_mode.GetSelection()
        if highlight_mode_selection == HIGHLIGHT_MODE.NONE:
            logger.debug("returning early due to highlight selection")
            return
        value = self.text_ctrl_address_input.GetValue()
        if value and self.routes:
            self.list_ctrl_routes.DeselectAll()
            try:
                if highlight_mode_selection == HIGHLIGHT_MODE.BEST_MATCH:
                    match = self.routes.match(value)
                    if match:
                        index = self.route_to_list_id[match]
                        self.list_ctrl_routes.Select(index)
                        self.list_ctrl_routes.EnsureVisible(index)
                    else:
                        logger.info(f"No match found for value: '{value}'")
                elif highlight_mode_selection == HIGHLIGHT_MODE.ALL_MATCHES:
                    matches = self.routes.matches(value)
                    for match in matches:
                        index = self.route_to_list_id[match]
                        self.list_ctrl_routes.Select(index)
                    narrowest_match_index = self.route_to_list_id[matches[-1]]
                    self.list_ctrl_routes.EnsureVisible(narrowest_match_index)
                else:
                    logger.error(f"Invalid highlight mode selection: '{highlight_mode_selection}'")
            except Exception as E:
                logger.info(E)

    def set_routes(self, routes: routeparser.RoutingTable):
        self.routes = routes
        self.refresh_displayed_routes()


def show_error(message: str) -> int:
    return wx.MessageBox(message, "Error", style=(wx.OK | wx.CENTER | wx.ICON_ERROR))


if __name__ == "__main__":
    app = MainApp(0)
    app.MainLoop()
