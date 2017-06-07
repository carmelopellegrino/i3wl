# i3wl
A simple applet for navigating through windows in [i3wm](https://i3wm.org/).

When you start nesting tabbed, stacked and tiling layouts on several
workspaces, remembering the position of a window can be difficult if not
impossible.

This applet shows an icon in the tray. Clicking on it shows a menu listing
the workspaces, each of them containing the list of windows in that
workspace. By clicking on a item the focus is raised on the corresponding
window.

# Requirements
* [Python](https://www.python.org) 2 (should work also in Python 3, but it's still untested)
* [PyGTK](www.pygtk.org)
* [i3ipc-python](https://github.com/acrisci/i3ipc-python)
