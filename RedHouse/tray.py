import wx
import folders

TRAY_TOOLTIP = 'Red House'
TRAY_ICON = 'icon.png'


def create_menu_item(menu, label, func):
    item = wx.MenuItem(menu, -1, label)
    menu.Bind(wx.EVT_MENU, func, id=item.GetId())
    menu.AppendItem(item)
    return item


class TaskBarIcon(wx.TaskBarIcon):
    def __init__(self, fileDaemon):
        self.fileDaemon = fileDaemon
        super(TaskBarIcon, self).__init__()
        self.set_icon(TRAY_ICON)
        self.Bind(wx.EVT_TASKBAR_LEFT_DOWN, self.on_left_down)

    def CreatePopupMenu(self):
        menu = wx.Menu()
        create_menu_item(menu, 'Exit', self.on_exit)
        return menu

    def set_icon(self, path):
        icon = wx.IconFromBitmap(wx.Bitmap(path))
        self.SetIcon(icon, TRAY_TOOLTIP)

    def on_left_down(self, event):
        a,b,c,d,e = self.fileDaemon.GetStatistics()
        #balloonText = 'Total files: {}\nAdded local files: {}\nDelete local files: {}\nAdded remote files: {}\nDeleted remote files: {}'.format(self.fileDaemon.GetStatistics())
        balloonText = 'Total files: {}\nAdded local files: {}\nDelete local files: {}\nAdded remote files: {}\nDeleted remote files: {}'.format(a,b,c,d,e)
        self.ShowBalloon('RedHouse usage', balloonText)
        print 'Tray icon was left-clicked.'

    def on_hello(self, event):
        print 'Hello, world!'

    def on_exit(self, event):
        self.fileDaemon.stop()
        wx.CallAfter(self.Destroy)

def StartRedHouseTaskBar ():
    app = wx.PySimpleApp()
    TaskBarIcon()
    app.MainLoop()
   

def main():
    f = folders.folders ('C:\Users\dfugelso\Documents\Projects\RedHouse', 'Jacks URL')
    app = wx.PySimpleApp()
    TaskBarIcon(f)
    app.MainLoop()


if __name__ == '__main__':
    main()