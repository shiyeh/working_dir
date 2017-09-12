from __future__ import unicode_literals
import os
import sys
import urwid

def test(button, data):
    print(data[1].get_edit_text())

_list = "button1 button2 button3 button4 button5 button6".split()
grid_list = []
for i in range(len(_list)):
    _list[i] = urwid.Button(_list[i])
    _list[i].user_data = 'this is ' + str(i)
    grid_list.append(_list[i])
    #grid_list.append(urwid.SelectableIcon(urwid.Text(_list[i].user_data), 0))
    grid_list.append(urwid.AttrWrap(urwid.Edit('', _list[i].user_data),'editbx', 'editfc'))

grid_list += [urwid.Divider(), urwid.Divider()]
# grid_list.append(urwid.Button('ok', test, user_data=grid_list))
# ok_button = urwid.Button('ok', test, user_data=grid_list)
ok_button = urwid.Button('ok')
ok_button._w = urwid.AttrMap(urwid.SelectableIcon('ok', 1), None, focus_map='selected')
# ok_button = urwid.AttrMap(urwid.Button('ok'), None, focus_map='selected')
grid_list.append(ok_button)

# urwid.connect_signal(ok_button, 'click', test)

def callback(button):
    print(grid_list[1])
    grid_list[1].set_text('ok')
grid = urwid.GridFlow(grid_list, 40, 2 , 0, 'left')
fill = urwid.Filler(grid, 'top', top=1)
pad = urwid.Padding(fill, left=1)
main = pad
palette = [
    ('none', '', '', ''),
    ('focus heading', 'black', 'light blue'),
    ('line', 'black', 'dark red'),
    ('options', '', ''),
    ('reversed', 'standout', ''),
    ('selected', 'bold, black', 'light gray'),
    ('editfc','white', 'dark blue', 'bold'),
    ('editbx','light gray', 'dark blue'),
    ]

urwid.MainLoop(main,  palette).run()
