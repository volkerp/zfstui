import curses
import curses.panel


MAINMENU = ['[F2]Pools', '[F3]Volumes', '[F4]Filesysts', '[F5]Snapshots', '[F10]Quit']
MAINMENU_POOLS = 0
MAINMENU_VOLS  = 1
MAINMENU_FSYS  = 2
MAINMENU_SNAP  = 3
MAINMENU_QUIT  = 4

def pprint(window, text):
    if isinstance(text, list):
        for txt, style in text:
            window.addstr(txt, style)
    else:
        window.addstr(text)


class MainMenu:
    def __init__(self, window):
        self.window = window
        self.keyboard_focus = False
        self.window.keypad(1)
        self.highlight_idx = 0
        self.change_callback = None
        self.select_callback = None
        

    def set_keyboard_focus(self, hasfocus):
        self.keyboard_focus = hasfocus
        self.draw()


    def set_highlight_idx(self, idx):
        self.highlight_idx = idx
        self.draw()


    def draw(self):
        self.window.clear()
        self.window.move(0, 1)
        for i, entry in enumerate(MAINMENU):
            if i == self.highlight_idx and self.keyboard_focus == True:
                self.window.addstr(entry, curses.A_REVERSE)
            else:
                self.window.addstr(entry, curses.A_NORMAL)
            if i != len(MAINMENU) - 1:
                self.window.addstr('    ', curses.A_NORMAL)
        self.window.refresh()


    def handle_key(self, key):
        if key == curses.KEY_LEFT:
            self.set_highlight_idx(max(0, self.highlight_idx - 1))
            if self.select_callback:
                self.change_callback(self.highlight_idx) 
        elif key == curses.KEY_RIGHT:
            self.set_highlight_idx(min(len(MAINMENU) - 1, self.highlight_idx + 1))
            if self.select_callback:
                self.change_callback(self.highlight_idx) 
        elif key == ord('\n') or key == curses.KEY_ENTER:   # callback select on ENTER
            if self.select_callback:
                self.select_callback(self.highlight_idx)
    


class Widget:
    def __init__(self, window, caption = None):
        self.window = window
        self.caption = caption
        self.footer = None
        self.window.keypad(1)
        self.selline = 0   # highlighted line
        self.y_ofs = 0       # first displayed line
        self.x_ofs = 0       # first displayed column
        self.rowselect_callback = None
        self.close_callback = None
        self.key_callback = None
        self.headerline = None  # first line is header
        self.keyboard_focus = False


    def set_caption(self, caption):
        self.caption = caption
        self.draw()

   
    def set_header_line(self, headerline):
        """
        Set a stationary, non selectable first line
        """
        self.headerline = headerline


    def set_text_list(self, listofstr):
        self.lines = []
        self.selline = 0
        self.y_ofs = self.x_ofs = 0
        self.maxlinelen = 0
        self.footer = None
        for line in listofstr:
            self.maxlinelen = max(self.maxlinelen, len(line))
            self.lines.append(line)
        self.draw()


    def set_keyboard_focus(self, hasfocus):
        self.keyboard_focus = hasfocus
        self.draw()


    def draw(self):
        self.window.clear()
        self.window.box()

        h, w = self.window.getmaxyx()
        if self.caption:
            #self.window.addstr(0, 4, self.caption, curses.A_NORMAL)
            self.window.move(0, 4)
            pprint(self.window, self.caption)

        h_ofs = 0
        if self.headerline:
            self.window.addnstr(1, 1, self.headerline, w-2, curses.A_NORMAL)
            h_ofs = 1

        for i, line in enumerate(self.lines[self.y_ofs:]):
            if i + h_ofs == h-2:
                break
            line = line.ljust(w-2)
            if i + self.y_ofs == self.selline and self.keyboard_focus:
                self.window.addnstr(i+1 + h_ofs, 1, line[self.x_ofs:], w-2, curses.A_REVERSE)
            else:
                self.window.addnstr(i+1 + h_ofs, 1, line[self.x_ofs:], w-2,curses.A_NORMAL)
                
        if self.footer and self.keyboard_focus:
            self.window.move(h-1, 4)
            self.window.addstr(self.footer)


    def handle_key(self, key):
        h, w = self.window.getmaxyx()
        vis_h, vis_w = h - 2 - (1 if self.headerline else 0), w - 2    # visible lines/cols
        
        self.key_callback(self.lines[self.selline], key) if self.key_callback else None
        if key == 27:  # ESC or ALT
            self.window.nodelay(True)
            n = self.window.getch()
            if n == -1:  # ESC
                self.window.nodelay(False)
                self._call_close_callback()
        elif key == curses.KEY_UP:
            if self.selline > 0:
                self.selline -= 1
            if self.selline < self.y_ofs:
                self.y_ofs = self.selline     # scroll up by one line
        elif key == curses.KEY_DOWN:
            if self.selline < len(self.lines) - 1:
                self.selline += 1
            if self.selline > self.y_ofs + vis_h -1:
                self.y_ofs += 1
        elif key == curses.KEY_LEFT:
            self.x_ofs = max(0, self.x_ofs - 1)
        elif key == curses.KEY_RIGHT:
            self.x_ofs = max(0, min(self.x_ofs + 1, self.maxlinelen - vis_w))
        elif key == curses.KEY_PPAGE:
            self.y_ofs = max(0, self.y_ofs - vis_h)
            self.selline = self.y_ofs
        elif key == curses.KEY_NPAGE:
            self.y_ofs = min(self.y_ofs + vis_h, len(self.lines)-vis_h)
            self.selline = self.y_ofs
        elif key == curses.KEY_HOME:
            self.y_ofs = 0
            self.selline = self.y_ofs
        elif key == curses.KEY_END:
            self.y_ofs = len(self.lines)-vis_h
            self.selline = len(self.lines) - 1             # place cursor on last line
        elif key == ord('\n') or key == curses.KEY_ENTER:
            if self.selline is not None and self.rowselect_callback is not None:
                callback, data = self.rowselect_callback
                callback(self.selline, data)
        elif key == ord('q'):
            self._call_close_callback()
       
        self.draw()

 
    def set_rowselected_callback(self, callback, data):
        self.rowselect_callback = callback, data

    
    def set_close_callback(self, callback, data):
        """
        set callback when widget wants to be closed
        """
        self.close_callback = callback, data


    def _call_close_callback(self):
        if self.close_callback:
            callback, data = self.close_callback
            callback(data)
        

    


