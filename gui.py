#! /usr/bin/python2

import wxversion
wxversion.select('2.8')
import wx
import wx.lib.mixins.inspection as wit

running = False

# Custom panel class with an image background
class ImagePanel(wx.Panel):
    def __init__(self, parent, image_file):
        wx.Panel.__init__(self, parent=parent)
        self.image_file = image_file
        self.SetBackgroundStyle(wx.BG_STYLE_CUSTOM)

        self.Bind(wx.EVT_ERASE_BACKGROUND, self.OnEraseBackground)

    def SetImage(self, image_file):
        self.image_file = image_file

    def OnEraseBackground(self, evt):
        if (self.image_file == None):
            return None

        dc = evt.GetDC()

        if not dc:
            dc = wx.ClientDC(self)
            rect = self.GetUpdateRegion().GetBox()
            dc.SetClippingRect(rect)
        dc.Clear()
        bmp = wx.Bitmap(self.image_file)
        dc.DrawBitmap(bmp, 0, 0)

# Custom listbox class which takes an ImagePanel and sets
# its background
class PlateListBox(wx.ListBox):
    def __init__(self, parent, image_panel):
        wx.ListBox.__init__(self, parent=parent)
        self.images = {}
        self.image_panel = image_panel

        self.Bind(wx.EVT_LISTBOX, self.OnSelect)

    def Add(self, plate_number, image_file):
        self.images[plate_number] = image_file
        self.InsertItems([plate_number],0)

    def OnSelect(self, evt):
        self.image_panel.SetImage(self.images[evt.GetString()])
        self.image_panel.Refresh()

class MainFrame(wx.Frame):

    def __init__(self,parent,title):
        wx.Frame.__init__(self, parent, title=title, size=(600,450))

        panel = wx.Panel(self,-1, style=wx.BORDER_SIMPLE)
        sizer = wx.GridBagSizer(4, 4)
        sizer.AddGrowableRow(0)
        sizer.AddGrowableCol(2)

        self.bitmap = ImagePanel(self, None)

        self.listbox = PlateListBox(panel, self.bitmap)
        sizer.Add(self.listbox, pos=(0,0), span=(4,1), flag=wx.EXPAND, border=5)

        bmsizer = wx.GridBagSizer(4, 4)
        bmsizer.AddGrowableRow(0)
        bmsizer.AddGrowableCol(2)
        bmsizer.SetEmptyCellSize((200,100))
        
        self.button = wx.Button(self.bitmap, label="Start", size=(80, 30))
        bmsizer.Add(self.button, pos=(3,3), span=(1,1),  flag=wx.ALL, border=5)
        self.bitmap.SetSizerAndFit(bmsizer)

        sizer.Add(self.bitmap, pos=(0,1), span=(4,3), flag=wx.EXPAND, border=5)

        self.Bind(wx.EVT_BUTTON, self.OnStartClick, self.button)
        self.Bind(wx.EVT_LISTBOX, self.OnListSelect, self.listbox)

        panel.SetSizerAndFit(sizer)

        mainSizer = wx.BoxSizer(wx.VERTICAL)
        mainSizer.Add(panel,1,wx.EXPAND,0)
        self.SetSizerAndFit(mainSizer)

        #--
        # test code
        self.listbox.Add("test", "test.jpg")
        #--

        self.Center()
        self.Show(True)

    def OnStartClick(self, event):
        global running
        running = not running
        if running:
            self.button.SetLabel("Stop")
        else:
            self.button.SetLabel("Start")

    def OnListSelect(self, event):
        pass

app = wx.App(False)
#app = wit.InspectableApp()
#wx.lib.inspection.InspectionTool().Show()
frame = MainFrame(None, "Plate Scanner GUI")
app.MainLoop()

