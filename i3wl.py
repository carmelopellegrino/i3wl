#!/usr/bin/python2
#-*- encoding:UTF-8 -*-

import pygtk
pygtk.require('2.0')
import gtk
import i3ipc

def populate(widget, connection):
    tree = connection.get_tree()
    for workspace in tree.workspaces():
        workspace_menu = gtk.MenuItem(workspace.name, True)
        submenu = gtk.Menu()

        for window in workspace.leaves():
            print " -", window.name
            submenu.append(gtk.MenuItem(window.name if len(window.name) < 30 else window.name[:27]+"..." ))

        workspace_menu.set_submenu(submenu)
        widget.append(workspace_menu)

class Gui:
  def __init__(self):
    self.i3 = i3ipc.Connection()
    self.statusIcon = gtk.StatusIcon()
    self.statusIcon.set_from_stock(gtk.STOCK_ABOUT)
    self.statusIcon.set_visible(True)
    self.statusIcon.set_tooltip("Windows list")
    self.statusIcon.connect('popup-menu', self.popup_menu_cb, None)
    self.statusIcon.set_visible(True)

  def popup_menu_cb(self, widget, button, time, data = None):
    if button == 3:
      menu = gtk.Menu()
      quit_item = gtk.ImageMenuItem(gtk.STOCK_QUIT)
      quit_item.connect('activate', gtk.main_quit, self.statusIcon)
      menu.append(quit_item)
      populate(menu)
      menu.show_all()
      menu.popup(None, None, gtk.status_icon_position_menu, 3, time, self.statusIcon)

if __name__=='__main__':
  gui=Gui()
  gtk.main()
