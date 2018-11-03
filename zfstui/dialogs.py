import curses
import curses.panel
from . import zfs
import os
import sys
from .widgets import *
from . import helptext

GLOBAL = {
    'stdscr': None,
    'focuswidget': None,
    'mainmenu': None,
    'overlay': None
}


def on_mainmenu_entry_changed(index):
    GLOBAL['overlay'] = None
    if index == MAINMENU_POOLS:
        set_contents_pools(GLOBAL['mainwidget'])
    elif index == MAINMENU_VOLS:
        set_contents_volumes(GLOBAL['mainwidget'])
    elif index == MAINMENU_FSYS:
        set_contents_filesystems(GLOBAL['mainwidget'])
    elif index == MAINMENU_SNAP:
        set_contents_snapshots(GLOBAL['mainwidget'])
        

def on_mainmenu_entry_selected(index):
    if index == MAINMENU_QUIT:
        sys.exit()
    else:
        set_keyboard_focus(GLOBAL['mainwidget'])


def on_poollist_key_press(entry, key):
    if key == ord('\n') or key == curses.KEY_ENTER:
        pass
    elif key == ord('h'):
        show_pool_history(entry.split()[0])
    elif key == ord('i'):
        show_pool_iostat(entry.split()[0])


def on_filesystemlist_key_press(entry, key):
    if key == ord('s'):
        show_dataset_snapshots(entry.split()[0])


def create_overlay(caption, header, contents):
    h, w = GLOBAL['stdscr'].getmaxyx()
    win = curses.newwin(h-3, w-1, 3, 1)
    widget = Widget(win, caption)
    widget.set_header_line(header)
    widget.set_text_list(contents)
    widget.set_close_callback(on_overlay_wants_close, None)
    GLOBAL['overlay'] = curses.panel.new_panel(win)
    GLOBAL['overlay'].set_userptr(widget)
 

def show_help():
    lines = helptext.fulltext
    create_overlay("Help", None, lines)


def show_pool_history(poolname):
    lines = zfs.zfsPoolHistory(poolname)
    caption = [("History of pool: ", curses.A_NORMAL), (poolname, curses.A_BOLD)]
    create_overlay(caption, None, lines)
    

def show_pool_iostat(poolname):
    lines = zfs.zfsPoolIostat(poolname)
    caption = [("Iostat of pool: ", curses.A_NORMAL), (poolname, curses.A_BOLD)]
    create_overlay(caption, None, lines)
    

def show_dataset_snapshots(dataset):
    lines = zfs.zfsListSnapshotsOf(dataset)
    caption = [("Snapshots of: ", curses.A_NORMAL), (dataset, curses.A_BOLD)]
    create_overlay(caption, None, lines)


def on_pool_selected(index, data):
    poolline = data.lines[index]
    caption = [("Properties: ", curses.A_NORMAL), (poolline.split()[0], curses.A_BOLD)]
    lines = zfs.zfsPoolProperties(poolline.split()[0])
    create_overlay(caption, lines[0], lines[1:])
    

def on_dataset_selected(index, data):
    datasetline = data.lines[index]
    caption = [("Properties: ", curses.A_NORMAL), (datasetline.split()[0], curses.A_BOLD)]
    lines = zfs.zfsDatasetProperties(datasetline.split()[0])
    create_overlay(caption, lines[0], lines[1:])


def on_snapshot_selected(index, data):
    snapline = data.lines[index]
    caption = [("Properties: ", curses.A_NORMAL), (snapline.split()[0], curses.A_BOLD)]
    lines = zfs.zfsSnapshotProperties(snapline.split()[0])
    create_overlay(caption, lines[0], lines[1:])


def on_overlay_wants_close(data):
    GLOBAL['overlay'] = None


def set_contents_pools(widget):
    lines = zfs.zfsListPools()
    widget.set_header_line(lines[0])
    widget.set_text_list(lines[1:])
    widget.footer = "[Ret] Properties────[H] History───[I] Iostat"
    widget.set_caption("Pools")
    widget.set_rowselected_callback(on_pool_selected, widget)
    widget.key_callback = on_poollist_key_press


def set_contents_volumes(widget):
    lines = zfs.zfsListVolumes()
    widget.set_header_line(lines[0])
    widget.set_text_list(lines[1:])
    widget.footer = "[Ret] Properties"
    widget.set_caption("Volumes")    
    widget.set_rowselected_callback(on_dataset_selected, widget)


def set_contents_snapshots(widget):
    lines = zfs.zfsListSnapshots()
    widget.set_header_line(lines[0])
    widget.set_text_list(lines[1:]) 
    widget.footer = "[Ret] Properties"
    widget.set_caption("Snapshots")
    widget.set_rowselected_callback(on_snapshot_selected, widget)


def set_contents_filesystems(widget):
    lines = zfs.zfsListFilesystems()
    widget.set_header_line(lines[0])
    widget.set_text_list(lines[1:])
    widget.footer = "[Ret] Properties───[S] Snapshots"
    widget.set_caption("Filesystems")
    widget.set_rowselected_callback(on_snapshot_selected, widget)
    widget.key_callback = on_filesystemlist_key_press

def set_keyboard_focus(widget):
    print(type(widget))
    GLOBAL['focuswidget'].set_keyboard_focus(False)
    GLOBAL['focuswidget'] = widget
    GLOBAL['focuswidget'].set_keyboard_focus(True)


def mainloop(stdscr):
    GLOBAL['stdscr'] = stdscr
    h, w = GLOBAL['stdscr'].getmaxyx()

    if h < 24 or w < 80:
        sys.exit('Terminal size must be at least 80x24')
   
    zfs.check_zfs_executables()

    curses.curs_set(0)
    stdscr.clear()

    subwin = stdscr.subwin(1, w, 0, 0)
    mainmenu = MainMenu(subwin)
    mainmenu.change_callback = on_mainmenu_entry_changed
    mainmenu.select_callback = on_mainmenu_entry_selected
    GLOBAL['mainmenu'] = mainmenu

    subwin = stdscr.subwin(2, 0)
    widget = Widget(subwin, "Pools")
    GLOBAL['mainwidget'] = widget
    widgetpanel = curses.panel.new_panel(subwin)
    widgetpanel.set_userptr(widget)

    set_contents_pools(GLOBAL['mainwidget'])

    GLOBAL['mainmenu'].set_keyboard_focus(True)
    GLOBAL['focuswidget'] = GLOBAL['mainmenu']

    curses.panel.update_panels()
    curses.doupdate()

    while True:
        key = stdscr.getch()
        
        if key == curses.KEY_F10:
            return
        elif key == ord('q'):
            if not GLOBAL['overlay']:
                return
            else:
                curses.panel.top_panel().userptr().handle_key(key)
        elif key == curses.KEY_F1:
            show_help()
        elif key == curses.KEY_F2:
            GLOBAL['mainmenu'].set_highlight_idx(0)
            GLOBAL['overlay'] = None
            set_keyboard_focus(GLOBAL['mainwidget'])
            set_contents_pools(GLOBAL['mainwidget'])
        elif key == curses.KEY_F3:
            GLOBAL['mainmenu'].set_highlight_idx(1)
            GLOBAL['overlay'] = None
            set_keyboard_focus(GLOBAL['mainwidget'])
            set_contents_volumes(GLOBAL['mainwidget'])
        elif key == curses.KEY_F4:
            GLOBAL['mainmenu'].set_highlight_idx(2)
            GLOBAL['overlay'] = None
            set_keyboard_focus(GLOBAL['mainwidget'])
            set_contents_filesystems(GLOBAL['mainwidget'])
        elif key == curses.KEY_F5:
            GLOBAL['mainmenu'].set_highlight_idx(3)
            GLOBAL['overlay'] = None
            set_keyboard_focus(GLOBAL['mainwidget'])
            set_contents_snapshots(GLOBAL['mainwidget'])
        elif key == ord('\t'):
            if GLOBAL['focuswidget'] == GLOBAL['mainmenu']:
                set_keyboard_focus(curses.panel.top_panel().userptr())
                #set_keyboard_focus(GLOBAL['mainwidget'])
            else:
                set_keyboard_focus(GLOBAL['mainmenu'])
        else:
            if GLOBAL['focuswidget'] == GLOBAL['mainmenu']:
                GLOBAL['mainmenu'].handle_key(key)
            else:
                curses.panel.top_panel().userptr().handle_key(key)

        curses.panel.update_panels()
        curses.doupdate()
