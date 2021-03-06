#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#
# generated by wxGlade 0.9.5 on Wed May  6 20:41:18 2020
#

import wx

# begin wxGlade: dependencies
# end wxGlade

# begin wxGlade: extracode

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
This module implements the base layer of GUI functionality.
It should only address widget/frame layout and properties and not actual data handling.
The file is generated by wxGlade by using the wxg file.
"""


import enum
import os


# Corresponds to choices on RoutePanel
@enum.unique
class HIGHLIGHT_MODE(enum.IntEnum):
    NONE = 0
    BEST_MATCH = 1
    ALL_MATCHES = 2


MAX_FILE_SIZE = (1 << 20)
SHORT_LINE_LEN = 48
MAX_LINE_COUNT = MAX_FILE_SIZE // SHORT_LINE_LEN
MAX_TEXT_LEN = MAX_FILE_SIZE + MAX_LINE_COUNT


WIN32 = os.name == 'nt'


class ExtendedNotebook(wx.Notebook):
    def __init__(self, parent, *args, **kwds):
        wx.Notebook.__init__(self, parent, *args, **kwds)

    def DeleteCurrentPage(self):
        current_page_id = self.GetCurrentPageId()
        if current_page_id is None:
            return
        else:
            self.DeletePage(current_page_id)

    def GetCurrentPageId(self):
        """Get int page ID of current page, or None"""
        current_page = self.GetCurrentPage()
        if current_page:
            return self.FindPage(current_page)
        else:
            return None

    def GetPageByText(self, text: str):
        """Get int page ID by the page text. This assumes no two pages have the same text."""
        value = None
        for page_number in range(self.GetPageCount()):
            if self.GetPageText(page_number) == text:
                value = page_number
                break
        return value


import wx.lib.mixins.listctrl as listmix


class AutoWidthListCtrl(wx.ListCtrl, listmix.ListCtrlAutoWidthMixin):
    """ListCtrl that auto-extends last column to fill window width"""
    def __init__(self, parent, ID, pos=wx.DefaultPosition, size=wx.DefaultSize, style=0):
        wx.ListCtrl.__init__(self, parent, ID, pos, size, style)
        listmix.ListCtrlAutoWidthMixin.__init__(self)

    def Deselect(self, index):
        # self.SetItemState(index, 0, wx.LIST_STATE_SELECTED)
        self.Select(index, 0)

    def DeselectAll(self):
        for index in self.GetSelectedIndices():
            self.Deselect(index)

    def GetSelectedIndices(self, state=wx.LIST_STATE_SELECTED):
        indices = []
        last_found = -1
        while True:
            index = self.GetNextItem(
                last_found,
                wx.LIST_NEXT_ALL,
                state,
            )
            if index == -1:
                break
            else:
                last_found = index
                indices.append(index)
        return indices
# end wxGlade


class RouteNotebook(ExtendedNotebook):
    def __init__(self, *args, **kwds):
        # begin wxGlade: RouteNotebook.__init__
        kwds["style"] = kwds.get("style", 0) | wx.NB_TOP
        ExtendedNotebook.__init__(self, *args, **kwds)
        self.notebook_main_pane_start = wx.Panel(self, wx.ID_ANY)
        self.filepicker_source_input = wx.FilePickerCtrl(self.notebook_main_pane_start, wx.ID_ANY)
        self.button_file_submit = wx.Button(self.notebook_main_pane_start, wx.ID_ANY, "Submit")
        self.button_paste_text = wx.Button(self.notebook_main_pane_start, wx.ID_ANY, "Click to paste text")

        self.__set_properties()
        self.__do_layout()
        # end wxGlade

    def __set_properties(self):
        # begin wxGlade: RouteNotebook.__set_properties
        self.AddPage(self.notebook_main_pane_start, "New")
        self.SetBackgroundColour(wx.Colour(238, 238, 238))
        self.SetForegroundColour(wx.Colour(0, 0, 0))
        self.button_file_submit.SetToolTip("Parse the selected file")
        self.button_paste_text.SetToolTip("click for a popup to paste route command output into")
        self.notebook_main_pane_start.SetBackgroundColour(wx.Colour(238, 238, 238))
        self.notebook_main_pane_start.SetForegroundColour(wx.Colour(0, 0, 0))
        # end wxGlade

    def __do_layout(self):
        # begin wxGlade: RouteNotebook.__do_layout
        grid_sizer_start_outer = wx.GridBagSizer(0, 0)
        sizer_start_source = wx.StaticBoxSizer(wx.StaticBox(self.notebook_main_pane_start, wx.ID_ANY, "Source"), wx.VERTICAL)
        grid_sizer_start_source_inner = wx.GridBagSizer(0, 0)
        label_file_input = wx.StaticText(self.notebook_main_pane_start, wx.ID_ANY, "From file:", style=wx.ALIGN_CENTER)
        label_file_input.SetBackgroundColour(wx.Colour(238, 238, 238))
        label_file_input.SetForegroundColour(wx.Colour(0, 0, 0))
        grid_sizer_start_source_inner.Add(label_file_input, (0, 0), (1, 1), wx.ALIGN_CENTER | wx.ALL, 2)
        grid_sizer_start_source_inner.Add(self.filepicker_source_input, (0, 1), (1, 1), wx.ALIGN_CENTER_VERTICAL | wx.EXPAND | wx.RIGHT, 2)
        grid_sizer_start_source_inner.Add(self.button_file_submit, (0, 2), (1, 1), 0, 0)
        static_line_1 = wx.StaticLine(self.notebook_main_pane_start, wx.ID_ANY)
        grid_sizer_start_source_inner.Add(static_line_1, (1, 0), (1, 3), wx.ALL | wx.EXPAND, 10)
        label_from_pasted_input = wx.StaticText(self.notebook_main_pane_start, wx.ID_ANY, "From pasted text:", style=wx.ALIGN_CENTER)
        label_from_pasted_input.SetBackgroundColour(wx.Colour(238, 238, 238))
        label_from_pasted_input.SetForegroundColour(wx.Colour(0, 0, 0))
        grid_sizer_start_source_inner.Add(label_from_pasted_input, (2, 0), (1, 1), wx.ALIGN_CENTER | wx.ALL, 2)
        grid_sizer_start_source_inner.Add(self.button_paste_text, (2, 1), (1, 1), 0, 0)
        grid_sizer_start_source_inner.Add(20, 20, (3, 0), (1, 1), 0, 0)
        grid_sizer_start_source_inner.AddGrowableRow(3)
        grid_sizer_start_source_inner.AddGrowableCol(1)
        sizer_start_source.Add(grid_sizer_start_source_inner, 1, wx.EXPAND, 0)
        grid_sizer_start_outer.Add(sizer_start_source, (0, 0), (1, 1), wx.EXPAND, 0)
        self.notebook_main_pane_start.SetSizer(grid_sizer_start_outer)
        grid_sizer_start_outer.AddGrowableRow(0)
        grid_sizer_start_outer.AddGrowableCol(0)
        # end wxGlade

# end of class RouteNotebook

class BaseMainFrame(wx.Frame):
    def __init__(self, *args, **kwds):
        # begin wxGlade: BaseMainFrame.__init__
        kwds["style"] = kwds.get("style", 0) | wx.DEFAULT_FRAME_STYLE
        wx.Frame.__init__(self, *args, **kwds)
        self.SetSize((1100, 900))
        
        # Menu Bar
        self.frame_main_menubar = wx.MenuBar()
        wxglade_tmp_menu = wx.Menu()
        self.frame_main_menubar.menu_item_close_tab = wxglade_tmp_menu.Append(wx.ID_ANY, "Close Tab", "")
        self.Bind(wx.EVT_MENU, self.on_menu_close_tab, id=self.frame_main_menubar.menu_item_close_tab.GetId())
        self.frame_main_menubar.menu_item_close_all_tabs = wxglade_tmp_menu.Append(wx.ID_ANY, "Close All Tabs", "")
        self.Bind(wx.EVT_MENU, self.on_menu_close_all_tabs, id=self.frame_main_menubar.menu_item_close_all_tabs.GetId())
        item = wxglade_tmp_menu.Append(wx.ID_ANY, "Exit", "")
        self.Bind(wx.EVT_MENU, self.on_menu_exit, id=item.GetId())
        self.frame_main_menubar.Append(wxglade_tmp_menu, "File")
        wxglade_tmp_menu = wx.Menu()
        item = wxglade_tmp_menu.Append(wx.ID_ANY, "About", "")
        self.Bind(wx.EVT_MENU, self.on_menu_about, id=item.GetId())
        self.frame_main_menubar.Append(wxglade_tmp_menu, "Help")
        self.SetMenuBar(self.frame_main_menubar)
        # Menu Bar end
        self.frame_main_menubar.menu_item_close_tab.Enable(False)
        self.frame_main_menubar.menu_item_close_all_tabs.Enable(False)
        self.panel_main = wx.Panel(self, wx.ID_ANY, style=wx.CLIP_CHILDREN)
        self.notebook_main = RouteNotebook(self.panel_main, wx.ID_ANY)

        self.__set_properties()
        self.__do_layout()

        # end wxGlade

    def __set_properties(self):
        # begin wxGlade: BaseMainFrame.__set_properties
        self.SetTitle("Quick Route Checker")
        self.panel_main.SetBackgroundColour(wx.Colour(238, 238, 238))
        self.panel_main.SetForegroundColour(wx.Colour(0, 0, 0))
        # end wxGlade

    def __do_layout(self):
        # begin wxGlade: BaseMainFrame.__do_layout
        sizer_main_outer = wx.BoxSizer(wx.VERTICAL)
        grid_sizer_main = wx.GridBagSizer(0, 0)
        grid_sizer_main.Add(self.notebook_main, (0, 0), (1, 1), wx.EXPAND, 0)
        self.panel_main.SetSizer(grid_sizer_main)
        grid_sizer_main.AddGrowableRow(0)
        grid_sizer_main.AddGrowableCol(0)
        sizer_main_outer.Add(self.panel_main, 1, wx.EXPAND, 0)
        self.SetSizer(sizer_main_outer)
        self.Layout()
        # end wxGlade

    def on_menu_close_tab(self, event):  # wxGlade: BaseMainFrame.<event_handler>
        print("Event handler 'on_menu_close_tab' not implemented!")
        event.Skip()

    def on_menu_close_all_tabs(self, event):  # wxGlade: BaseMainFrame.<event_handler>
        print("Event handler 'on_menu_close_all_tabs' not implemented!")
        event.Skip()

    def on_menu_exit(self, event):  # wxGlade: BaseMainFrame.<event_handler>
        print("Event handler 'on_menu_exit' not implemented!")
        event.Skip()

    def on_menu_about(self, event):  # wxGlade: BaseMainFrame.<event_handler>
        print("Event handler 'on_menu_about' not implemented!")
        event.Skip()

# end of class BaseMainFrame

class RoutePanelBase(wx.Panel):
    def __init__(self, *args, **kwds):
        # begin wxGlade: RoutePanelBase.__init__
        kwds["style"] = kwds.get("style", 0) | wx.TAB_TRAVERSAL
        wx.Panel.__init__(self, *args, **kwds)
        self.list_ctrl_routes = AutoWidthListCtrl(self, wx.ID_ANY, style=wx.LC_HRULES | wx.LC_REPORT | wx.LC_VRULES)
        self.text_ctrl_address_input = wx.TextCtrl(self, wx.ID_ANY, "", style=wx.TE_RIGHT)
        self.radio_box_highlight_mode = wx.RadioBox(self, wx.ID_ANY, "Highlight Mode", choices=["None", "Best Match", "All Matches"], majorDimension=1, style=wx.RA_SPECIFY_ROWS)

        self.__set_properties()
        self.__do_layout()

        self.Bind(wx.EVT_LIST_ITEM_DESELECTED, self.on_list_item_deselected, self.list_ctrl_routes)
        self.Bind(wx.EVT_LIST_ITEM_SELECTED, self.on_list_item_selected, self.list_ctrl_routes)
        self.Bind(wx.EVT_TEXT, self.on_text_address_input, self.text_ctrl_address_input)
        self.Bind(wx.EVT_RADIOBOX, self.on_radiobox_highlight_mode, self.radio_box_highlight_mode)
        # end wxGlade

    def __set_properties(self):
        # begin wxGlade: RoutePanelBase.__set_properties
        self.text_ctrl_address_input.SetMinSize((200, -1))
        self.text_ctrl_address_input.SetBackgroundColour(wx.Colour(255, 255, 255))
        self.text_ctrl_address_input.SetForegroundColour(wx.Colour(0, 0, 0))
        self.text_ctrl_address_input.SetToolTip("IP address or network (e.g. 192.168.1.1 or 10.10.10.0/24)")
        self.radio_box_highlight_mode.SetSelection(0)
        # end wxGlade

    def __do_layout(self):
        # begin wxGlade: RoutePanelBase.__do_layout
        grid_sizer_routes = wx.GridBagSizer(0, 0)
        grid_sizer_address_input = wx.GridBagSizer(0, 0)
        grid_sizer_routes.Add(self.list_ctrl_routes, (0, 0), (1, 3), wx.EXPAND, 0)
        label_address_input = wx.StaticText(self, wx.ID_ANY, "IP or Network:", style=wx.ALIGN_CENTER)
        label_address_input.SetBackgroundColour(wx.Colour(238, 238, 238))
        label_address_input.SetForegroundColour(wx.Colour(0, 0, 0))
        grid_sizer_address_input.Add(label_address_input, (0, 0), (1, 1), wx.ALIGN_CENTER | wx.LEFT | wx.RIGHT, 2)
        grid_sizer_address_input.Add(self.text_ctrl_address_input, (0, 1), (1, 1), wx.EXPAND, 0)
        grid_sizer_routes.Add(grid_sizer_address_input, (1, 0), (1, 1), wx.EXPAND | wx.TOP, 12)
        grid_sizer_routes.Add(self.radio_box_highlight_mode, (1, 2), (1, 1), wx.BOTTOM | wx.RIGHT, 2)
        self.SetSizer(grid_sizer_routes)
        grid_sizer_routes.Fit(self)
        grid_sizer_routes.AddGrowableRow(0)
        grid_sizer_routes.AddGrowableCol(1)
        self.Layout()
        # end wxGlade

    def on_list_item_deselected(self, event):  # wxGlade: RoutePanelBase.<event_handler>
        print("Event handler 'on_list_item_deselected' not implemented!")
        event.Skip()

    def on_list_item_selected(self, event):  # wxGlade: RoutePanelBase.<event_handler>
        print("Event handler 'on_list_item_selected' not implemented!")
        event.Skip()

    def on_text_address_input(self, event):  # wxGlade: RoutePanelBase.<event_handler>
        print("Event handler 'on_text_address_input' not implemented!")
        event.Skip()

    def on_radiobox_highlight_mode(self, event):  # wxGlade: RoutePanelBase.<event_handler>
        print("Event handler 'on_radiobox_highlight_mode' not implemented!")
        event.Skip()

# end of class RoutePanelBase

class PasteDialogBase(wx.Dialog):
    def __init__(self, *args, **kwds):
        # begin wxGlade: PasteDialogBase.__init__
        kwds["style"] = kwds.get("style", 0) | wx.DEFAULT_DIALOG_STYLE | wx.MAXIMIZE_BOX | wx.RESIZE_BORDER
        wx.Dialog.__init__(self, *args, **kwds)
        self.panel_paste = wx.Panel(self, wx.ID_ANY)
        self.text_ctrl_tab_name_input = wx.TextCtrl(self.panel_paste, wx.ID_ANY, "", style=wx.TE_RIGHT)
        self.button_paste_cancel = wx.Button(self.panel_paste, wx.ID_ANY, "Cancel")
        self.button_paste_ok = wx.Button(self.panel_paste, wx.ID_ANY, "OK")
        self.text_ctrl_paste = wx.TextCtrl(self.panel_paste, wx.ID_ANY, "", style=wx.HSCROLL | wx.TE_MULTILINE)
        if WIN32:
            # work around issue that seems to match http://trac.wxwidgets.org/ticket/4646
            self.text_ctrl_paste.SetMaxLength(MAX_TEXT_LEN)

        self.__set_properties()
        self.__do_layout()

        self.Bind(wx.EVT_BUTTON, self.on_button_paste_cancel, self.button_paste_cancel)
        self.Bind(wx.EVT_BUTTON, self.on_button_paste_ok, self.button_paste_ok)
        # end wxGlade

    def __set_properties(self):
        # begin wxGlade: PasteDialogBase.__set_properties
        self.SetTitle("Paste Text")
        self.text_ctrl_tab_name_input.SetMinSize((150, -1))
        self.text_ctrl_tab_name_input.SetBackgroundColour(wx.Colour(255, 255, 255))
        self.text_ctrl_tab_name_input.SetForegroundColour(wx.Colour(0, 0, 0))
        self.text_ctrl_tab_name_input.SetToolTip("A short name to use for the tab text")
        self.text_ctrl_paste.SetMinSize((500, 500))
        self.text_ctrl_paste.SetBackgroundColour(wx.Colour(255, 255, 255))
        self.text_ctrl_paste.SetForegroundColour(wx.Colour(0, 0, 0))
        self.text_ctrl_paste.SetToolTip("Paste text output of a route command, such as 'netstat -rn'")
        self.panel_paste.SetBackgroundColour(wx.Colour(238, 238, 238))
        self.panel_paste.SetForegroundColour(wx.Colour(0, 0, 0))
        # end wxGlade

    def __do_layout(self):
        # begin wxGlade: PasteDialogBase.__do_layout
        sizer_paste_outer = wx.BoxSizer(wx.VERTICAL)
        grid_sizer_paste = wx.GridBagSizer(0, 0)
        label_tab_name_input = wx.StaticText(self.panel_paste, wx.ID_ANY, "New Tab Name:", style=wx.ALIGN_CENTER)
        label_tab_name_input.SetBackgroundColour(wx.Colour(238, 238, 238))
        label_tab_name_input.SetForegroundColour(wx.Colour(0, 0, 0))
        grid_sizer_paste.Add(label_tab_name_input, (0, 0), (1, 1), wx.ALIGN_CENTER | wx.LEFT | wx.RIGHT | wx.TOP, 2)
        grid_sizer_paste.Add(self.text_ctrl_tab_name_input, (0, 1), (1, 1), wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, 2)
        grid_sizer_paste.Add(self.button_paste_cancel, (0, 3), (1, 1), wx.LEFT | wx.RIGHT | wx.TOP, 2)
        grid_sizer_paste.Add(self.button_paste_ok, (0, 4), (1, 1), wx.LEFT | wx.RIGHT | wx.TOP, 2)
        grid_sizer_paste.Add(self.text_ctrl_paste, (1, 0), (1, 5), wx.ALL | wx.EXPAND, 2)
        self.panel_paste.SetSizer(grid_sizer_paste)
        grid_sizer_paste.AddGrowableRow(1)
        grid_sizer_paste.AddGrowableCol(2)
        sizer_paste_outer.Add(self.panel_paste, 1, wx.EXPAND, 0)
        self.SetSizer(sizer_paste_outer)
        sizer_paste_outer.Fit(self)
        self.Layout()
        # end wxGlade

    def on_button_paste_cancel(self, event):  # wxGlade: PasteDialogBase.<event_handler>
        print("Event handler 'on_button_paste_cancel' not implemented!")
        event.Skip()

    def on_button_paste_ok(self, event):  # wxGlade: PasteDialogBase.<event_handler>
        print("Event handler 'on_button_paste_ok' not implemented!")
        event.Skip()

# end of class PasteDialogBase

class MainAppBase(wx.App):
    def OnInit(self):
        self.frame_main = BaseMainFrame(None, wx.ID_ANY, "")
        self.SetTopWindow(self.frame_main)
        self.frame_main.Show()
        return True

# end of class MainAppBase

if __name__ == "__main__":
    app = MainAppBase(0)
    app.MainLoop()
