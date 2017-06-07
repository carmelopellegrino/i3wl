#!/usr/bin/python2
#-*- encoding:UTF-8 -*-

import pygtk
pygtk.require('2.0')
import gtk
import i3ipc

class Focuser(object):
    def __init__(self, connection, wid):
        self.id = wid
        self.connection = connection

    def focus(self, data):
        self.connection.command('[con_id=%s] focus' % self.id)

class WorkspaceSwitcher(object):
    def __init__(self, connection, workspace):
        self.workspace = workspace
        self.connection = connection

    def switch(self, data):
        self.connection.command("workspace %s" % self.workspace)

def populate(widget, connection):
    tree = connection.get_tree()
    for workspace in tree.workspaces():
        workspace_menu = gtk.MenuItem(workspace.name, True)
        submenu = gtk.Menu()
        switch = gtk.ImageMenuItem(gtk.STOCK_GO_FORWARD)
        switch.get_child().set_text("go to")
        switch.connect('activate', WorkspaceSwitcher(connection, workspace.name).switch)
        submenu.append(switch)
        submenu.append(gtk.SeparatorMenuItem())

        for window in workspace.leaves():
            text = window.name if len(window.name) < 30 else window.name[:27] + "..."
            elem = gtk.MenuItem(text)
            if window.urgent:
                elem.get_children()[0].set_markup("<b><i>%s</i></b>" % text)
            elem.connect('activate', Focuser(connection, window.id).focus)
            submenu.append(elem)

        workspace_menu.set_submenu(submenu)
        widget.append(workspace_menu)

class Gui:
  def __init__(self):
    self.i3 = i3ipc.Connection()
    self.statusIcon = gtk.StatusIcon()
    self.statusIcon.set_from_stock(gtk.STOCK_INDEX)
    self.statusIcon.set_visible(True)
    self.statusIcon.set_tooltip("Windows list")
    self.statusIcon.connect('button-press-event', self.on_click)
    self.statusIcon.set_visible(True)

  def generate_menu(self):
    menu = gtk.Menu()
    quit_item = gtk.ImageMenuItem(gtk.STOCK_QUIT)
    quit_item.connect('activate', gtk.main_quit, self.statusIcon)
    menu.append(quit_item)
    menu.append(gtk.SeparatorMenuItem())
    populate(menu, self.i3)
    menu.show_all()
    return menu

  def on_click(self, widget, event):
      menu = self.generate_menu()
      menu.popup(None, None, gtk.status_icon_position_menu, 3, event.time, widget)

if __name__=='__main__':
    try:
        gui=Gui()
        gtk.main()
    except:
        print 'Exception thrown... bye!'
