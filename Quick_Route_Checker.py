import GUI
import logcontrol
import logging
import sys
import wx


logger = logging.getLogger(__name__)


class MainApp(wx.App):
    def OnInit(self):
        self.frame_main = GUI.MainFrame(None, wx.ID_ANY, "", name="MainFrame")
        self.SetTopWindow(self.frame_main)
        self.frame_main.Show()
        return True


if __name__ == "__main__":
    logcontrol.set_log_file("Quick_Route_Checker_log.txt")
    if "-d" in sys.argv:
        logcontrol.set_level(logging.DEBUG)
        logger.debug("debug mode enabled")
    logger.info("program starting")
    app = MainApp(0)
    app.MainLoop()
