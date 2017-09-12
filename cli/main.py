from __future__ import unicode_literals
import os
import urwid
from database import database, db_index

db = database()


class popup_dialog(urwid.WidgetWrap):
    """A dialog that appears with nothing but a close button """
    signals = ['close']
    def __init__(self, _list):
        self._list = _list
        button_label = "ok"
        pop_message = ["* Need to click ",('important', 'Save'), 
                       " button after you set ready."
                       "    All settings will be applied.\n"]
        close_button = urwid.Button(button_label)
        close_button.user_data = self._list
        urwid.connect_signal(close_button, 'click', self.close)
        pile = urwid.Pile([urwid.Text(pop_message), close_button])
        fill = urwid.Filler(pile)
        self.__super.__init__(urwid.AttrWrap(fill, 'popbg'))
    
    def close(self, button):
        apply_config(button, self._list)
        self._emit("close")


class button_with_popup(urwid.PopUpLauncher):
    def __init__(self, _list):
        self._list = _list
        self.__super.__init__(urwid.Button("Apply"))
        urwid.connect_signal(self.original_widget, 'click',
            lambda button: self.open_pop_up())

    def create_pop_up(self):
        pop_up = popup_dialog(self._list)
        urwid.connect_signal(pop_up, 'close',
            lambda button: self.close_pop_up())
        return pop_up

    def get_pop_up_parameters(self):
        return {'left':3, 'top':1, 'overlay_width':49, 'overlay_height':6}


class menu_button(urwid.Button):
    def __init__(self, caption, callback=None):
        super(menu_button, self).__init__(caption)
        self.user_data = {}
        if callback:
            urwid.connect_signal(self, 'click', callback)
        self._w = urwid.AttrMap(urwid.SelectableIcon(caption, 1),
           None, focus_map='selected')


class t_menu(urwid.WidgetWrap):
    def __init__(self, caption, choices, _id=1):
        super(t_menu, self).__init__(menu_button(' + ' + caption, self.open_menu))
        self._list = []
        sub_index = db_index[caption] 
        sub_db = db.get_setting(caption)
        for i in range(len(choices)):
            choices[i].user_data['sub_menu'] = caption
            index = sub_index[choices[i].get_label()]
            choices[i].user_data['id'] = _id
            choices[i].user_data['value'] = sub_db[_id-1][index]

            self._list.append(choices[i])
            self._list.append(urwid.AttrWrap(urwid.Edit(
                        '', choices[i].user_data['value']),'editbx', 'editfc'))
        
        header = urwid.AttrMap(urwid.Text(['\n', caption, '\n'], align='center'), 'focus heading')
        grid = urwid.GridFlow(self._list + [
                        urwid.Divider(),
                        urwid.Divider(),
                        button_with_popup(self._list)], 35, 5, 0, 'left')
        fill = urwid.Filler(grid, 'top', top=1)
        pad = urwid.Padding(fill, left=3)
        main = urwid.Frame(pad, header=header)
        self.menu = urwid.AttrMap(main, 'none')

    def open_menu(self, button):
        top.open_box(self.menu)


class sub_menu(urwid.WidgetWrap):
    def __init__(self, caption, choices):
        super(sub_menu, self).__init__(menu_button(' + ' +  caption, self.open_menu))
        listbox = urwid.ListBox(urwid.SimpleFocusListWalker([
            urwid.AttrMap(urwid.Text(['\n', caption, '\n'], align='center'), 'focus heading'),
            urwid.Divider()] + choices + [urwid.Divider()]))
        self.menu = urwid.AttrMap(listbox, 'none')

    def open_menu(self, button):
        top.open_box(self.menu)

def menu(title, choices):
    txt = urwid.Text(['\n', title, '\n'], align='center')
    map = urwid.AttrMap(txt, 'focus heading')
    body = [map, urwid.Divider()]
    body.extend(choices)
    return urwid.ListBox(urwid.SimpleFocusListWalker(body))

def item_chosen(button):
    edit = urwid.Edit(('editcp', [button.label, ": "]), button.user_data['value'])
    response = urwid.AttrWrap(edit, 'editbx', 'editfc')

    button.user_data['edit'] = edit
    done = urwid.Button('Apply', save_config, user_data=button)
    top.open_box(urwid.Filler(urwid.Pile([response,urwid.Divider(), done])))

def apply_config(button, data):
    sub_index = data[0].user_data['sub_menu']
    sub_db_index = db_index[sub_index]
    dic = {}
    for i in range(len(data)):
        if i % 2 is 0:
            key = sub_db_index[data[i].get_label()]
        if i % 2 is 1:
            value = data[i].get_edit_text()
            dic[key] = value  
    dic['id'] = data[0].user_data['id']
    db.set_setting(sub_index, dic)    

def save_config(button):
        os.chdir('..')
        os.system('cp -f /tmp/app.db app/app.db')
        os.chdir('..')
        result = os.system('./web-update-all.sh')
        os.chdir('./web_console')
        if result is 0:
            os.system('./reboot.sh &')


def exit_program(button):
    raise urwid.ExitMainLoop()

sim_config = [
        menu_button('APN'),
        menu_button('PIN'),
        menu_button('Authentication Protocal'),
        menu_button('Username'),
        menu_button('Password'),
        ]

wan_setting = sub_menu('Cellular WAN Settings', [
    t_menu('SIM1 Confiuration', sim_config, _id=1),
    t_menu('SIM2 Confiuration', sim_config, _id=2)
])

menu_top = menu('Main Menu', [
    sub_menu('Basic Settings', [
        t_menu('Network Settings', [
            menu_button('IP address'),
            menu_button('Subnet mask'),
            menu_button('Primary DNS server'),
            menu_button('Secondary DNS server'),
        ]),
        wan_setting,
        wan_setting,
    ]),
    # sub_menu('test setting',
    #     t_menu('Network Settings', [
    #         menu_button('IP address'),
    #         menu_button('Subnet mask'),
    #         menu_button('Primary DNS server'),
    #         menu_button('Secondary DNS server'),
    #     ]),
    #     wan_setting,
    #     wan_setting,
    # ),
    menu_button('   SAVE', save_config),
])

class CascadingBoxes(urwid.WidgetPlaceholder):
    max_box_levels = 4

    def __init__(self, box):
        super(CascadingBoxes, self).__init__(urwid.SolidFill(' '))
        self.box_level = 0
        self.open_box(box)

    def open_box(self, box):
        self.original_widget = urwid.Overlay(urwid.LineBox(box),
            self.original_widget,
            align='center', width=('relative', 80),
            valign='middle', height=('relative', 80),
            min_width=60, min_height=8,
            left=self.box_level * 3,
            right=(self.max_box_levels - self.box_level - 1) * 3,
            top=self.box_level * 2,
            bottom=(self.max_box_levels - self.box_level - 1) * 2)
        self.box_level += 1

    def keypress(self, size, key):
        if key == 'esc' and self.box_level > 1:
            self.original_widget = self.original_widget[0]
            self.box_level -= 1
        else:
            return super(CascadingBoxes, self).keypress(size, key)


palette = [
    ('none', '', '', ''),
    ('focus heading', 'bold', 'dark blue'),
    ('line', 'black', 'dark red'),
    ('options', '', ''),
    ('reversed', 'standout', ''),
    ('selected', 'bold, black', 'light gray'),
    ('item', 'bold, white',''),
    ('editfc','white', 'dark blue', 'bold'),
    ('editbx','light gray', 'dark blue'),
    ('editcp','white','', 'standout'),
    ('popbg', 'white', 'dark blue'),
    ('important', 'bold, white', 'dark blue'),
    ]

top = CascadingBoxes(menu_top)
urwid.MainLoop(top,  palette, pop_ups=True).run()
