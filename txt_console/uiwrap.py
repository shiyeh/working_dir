#!/usr/bin/python
import os
import sys
import string
import urwid

class CascadingBoxes(urwid.WidgetPlaceholder):
    max_box_levels = 4

    def __init__(self, box):
        _fill = urwid.SolidFill(u'\N{MEDIUM SHADE}')
        super(CascadingBoxes, self).__init__(_fill)
        self.box_level = 0
        self.open_box(box)

    def open_box(self, box):
        self.original_widget = urwid.Overlay(urwid.LineBox(box),
                                             self.original_widget,
                                             align='center',
                                             width=('relative', 80),
                                             valign='middle',
                                             height=('relative', 80),
                                             min_width=60,
                                             min_height=8)
        self.box_level += 1

    def close_box(self):
        if self.box_level > 1:
            self.original_widget = self.original_widget[0]
            self.box_level -= 1

    def keypress(self, size, key):
        if key == 'esc' and self.box_level > 1:
            self.original_widget = self.original_widget[0]
            self.box_level -= 1
        else:
            return super(CascadingBoxes, self).keypress(size, key)

'''
    MenuButton: MenuButton is the terminal node of menu tree,
                that contain a caption and action function.

    MenuNode: In usage, MenuButton is shown in list of MenuNode,
              and via add_choice to append item on tue current ListBox.
              New an instance of MenuNode requires a BoxHolder as a container.
              In current implemnetation, we used CascadingBoxes as container
              to provide some functions of MenuNode, like enter menu, leave menu.
'''

class MenuButton(urwid.Button):
    def __init__(self, caption, callback=None):
        super(MenuButton, self).__init__(caption)
        self.user_data = {}
        if callback:
            urwid.connect_signal(self, 'click', callback)
        self._w = urwid.AttrMap(urwid.SelectableIcon(caption, 1),
                                None, focus_map='selected')


class MenuNode(urwid.WidgetWrap):
    # MenuNode = BoxHolder  (urwid.Overlay) -- display screen
    #            Button     (urwid.Button)  -- current menu
    #            ListWidget (urwid.ListBox)
    def __init__(self, boxholder=None, caption='no title'):
        self._menubtn = MenuButton(' + ' + caption, self._open_menu)
        super(MenuNode, self).__init__(self._menubtn)
        self._boxholder = boxholder

        _Text = urwid.Text(['\n', caption, '\n'], align='center')
        _TitleAttr = urwid.AttrMap(_Text, 'focus heading')

        self._cplst = []
        self.add_choice(_TitleAttr)
        self.add_choice(urwid.Divider())

    def add_choice(self, item):
        self._cplst += [item]

    def _open_menu(self, button):
        # ListWalker body
        _listwalker = urwid.SimpleFocusListWalker(self._cplst)
        _listbox = urwid.ListBox(_listwalker)
        self.menu = urwid.AttrMap(_listbox, 'none')

        self._boxholder.open_box(self.menu)

# class CascadingBoxes(urwid.WidgetPlaceholder):
#     max_box_levels = 4

#     def __init__(self, box):
#         _fill = urwid.SolidFill(u'\N{MEDIUM SHADE}')
#         super(CascadingBoxes, self).__init__(_fill)
#         self.box_level = 0
#         self.open_box(box)

#     def open_box(self, box):
#         self.original_widget = urwid.Overlay(urwid.LineBox(box),
#                                              self.original_widget,
#                                              align='center',
#                                              width=('relative', 80),
#                                              valign='middle',
#                                              height=('relative', 80),
#                                              min_width=60,
#                                              min_height=8)
#         '''
#          left=self.box_level * 3,
#          right=(self.max_box_levels -
#                 self.box_level - 1) * 3,
#          top=self.box_level * 2,
#          bottom=(self.max_box_levels - self.box_level - 1) * 2)
#         '''
#         self.box_level += 1

#     def keypress(self, size, key):
#         if key == 'esc' and self.box_level > 1:
#             self.original_widget = self.original_widget[0]
#             self.box_level -= 1
#         else:
#             return super(CascadingBoxes, self).keypress(size, key)


# class menu_button(urwid.Button):
#     def __init__(self, caption, callback=None):
#         super(menu_button, self).__init__(caption)
#         self.user_data = {}
#         if callback:
#             urwid.connect_signal(self, 'click', callback)
#         self._w = urwid.AttrMap(urwid.SelectableIcon(caption, 1),
#                                 None, focus_map='selected')


# class choice(urwid.WidgetWrap):
#     def __init__(self, caption, callback=None):
#         super(choice, self).__init__(
#             menu_button(' - ' + caption, self.choice_cb))
#         self.caption = caption
#         self.callback = callback

#     def choice_cb(self, botton):
#         if self.callback:
#             self.callback(self.caption)

#         else:
#             # only for develop.
#             # response = urwid.Text([u'  You chose ', self.caption, u'\n'])
#             # done = menu_button(u'Ok', exit_program)
#             # response_box = urwid.Filler(urwid.Pile([response, done]))
#             # top.open_box(urwid.AttrMap(response_box, 'options'))
#             pass


# class sub_menu(urwid.WidgetWrap):
#     def __init__(self, caption, choices):
#         super(sub_menu, self).__init__(
#             menu_button(' + ' + caption, self.open_menu))
#         _Text = urwid.Text(['\n', caption, '\n'], align='center')
#         _TitleAttr = urwid.AttrMap(_Text, 'focus heading')

#         _cplst = [_TitleAttr, urwid.Divider()] + choices + [urwid.Divider()]
#         _listwalker = urwid.SimpleFocusListWalker(_cplst)  # ListWalker body

#         listbox = urwid.ListBox(_listwalker)
#         self.menu = urwid.AttrMap(listbox, 'none')

#     def open_menu(self, button):
#         top.open_box(self.menu)


# class MenuTreeView(urwid.WidgetWrap):
#     def menu(title, choices):
#         txt = urwid.Text(['\n', title, '\n'], align='center')
#         map = urwid.AttrMap(txt, 'focus heading')
#         body = [map, urwid.Divider()]
#         body.extend(choices)
#         return urwid.ListBox(urwid.SimpleFocusListWalker(body))

#     def item_chosen(button):
#         edit = urwid.Edit(
#             ('editcp', [button.label, ": "]), button.user_data['value'])
#         response = urwid.AttrWrap(edit, 'editbx', 'editfc')

#         button.user_data['edit'] = edit
#         done = urwid.Button('Apply', save_config, user_data=button)
#         top.open_box(urwid.Filler(urwid.Pile([response, urwid.Divider(), done])))


class TableView(urwid.WidgetWrap):
    """docstring for TableView(urwid.WidgetWrap)"""

    def __init__(self, controller):
        self.controller = controller
        super(TableView, self).__init__(self.main_view())

    def main_veiw():
        raise NotImplementedError("ust be overwrited.")


class PopUpDialog(urwid.WidgetWrap):
    signals = ['close']
    def __init__(self, option_list=[], title=""):
        close_button = urwid.Button("Close")
        close_button._label.align = 'center'
        urwid.connect_signal(close_button, 'click',
            # lambda button: self._emit('close', 'sdf'))
            lambda button: self.on_close())

        self.ol = option_list[:]
        self.ol.append(urwid.Divider())
        self.ol.append(close_button)
        listbox = urwid.ListBox(urwid.SimpleListWalker(self.ol))
        _type = self.ol[0].__class__.__name__
        if _type == 'RadioButton':
            ol = option_list[:]
            idx = [ol.index(x) for x in ol if x.get_state()][0]
            listbox.set_focus(idx)
        self.listbox = urwid.LineBox(listbox, title=title)
        self.__super.__init__(urwid.AttrWrap(self.listbox, 'popbg'))

    def keypress(self, size, key):
        _type = self.ol[0].__class__.__name__
        if key == 'enter' and _type != 'CheckBox':
            super(PopUpDialog, self).keypress(size, key)
            self.on_close()
        if key == 'esc':
            self.on_close()
        else:
            return super(PopUpDialog, self).keypress(size, key)

    def on_close(self):
        ol = self.ol[:-2]
        _type = ol[0].__class__.__name__
        if _type == 'Edit':
            _input = ol[0].get_edit_text()
            self._emit('close', _input)
        elif _type == 'RadioButton':
            _input = [opt.get_label() for opt in ol if opt.get_state()][0]
            self._emit('close', _input)
        elif _type == 'CheckBox':
            self._emit('close')
        else:
            self._emit('close')


class ThingWithAPopUp(urwid.PopUpLauncher):
    def __init__(self, btn_name="Change", option_list=[], title="",
                 left=0, top=1, width=30, height=None):
        self.option_list = option_list
        self.title = title
        self.left = left
        self.top = top
        self.width = width
        self.height = height
        self.btn = urwid.Button(btn_name)
        # p = u"\u25BC".encode('utf-8')
        self.btn._w = urwid.AttrMap(urwid.SelectableIcon(btn_name, 1),
                                None, focus_map='selected')
        self.__super.__init__(self.btn)
        urwid.connect_signal(self.original_widget, 'click',
            lambda button: self.open_pop_up())

    def create_pop_up(self):
        pop_up = PopUpDialog(self.option_list, self.title)
        urwid.connect_signal(pop_up, 'close',
            lambda button, label=None: self.on_close(label))
        return pop_up

    def get_pop_up_parameters(self):
        return {'left':self.left,
                'top':self.top,
                'overlay_width':self.width,
                'overlay_height':
                    self.height if self.height else len(self.option_list)+4}

    def on_close(self, label=None):
        if label != None:
            # self.btn.set_label(label)
            self.btn._w.original_widget.set_text(label)
        self.close_pop_up()


class MacEdit(urwid.IntEdit):
    def keypress(self, size, key):
        p = self.edit_pos
        t = self.get_edit_text()
        if key in string.hexdigits+':':
            rt, rp = self.insert_text_result(key)
            splitText = rt.split(':')
            if key == ':':
                if len(rt) == 1:
                    return
                if rt[-2] != ':' and len(rt.split(':')) < 7:
                    self.insert_text(u':')
            else:
                if any(len(num) > 2 for num in splitText):
                    if len(splitText) < 6:
                        self.edit_pos = len(t)
                        self.insert_text(u':')
                        self.insert_text(key)
                else:
                    self.insert_text(key)
                t = self.get_edit_text()
                self.set_edit_text(t.upper())
        elif key in ['backspace', 'delete']:
            if key == 'delete' and p not in [0, len(t)-1, len(t)]:
                if t != '' and t[p] == ':' and len(t) != 1: p += 1
                self.set_edit_text(t[:p]+t[p+1:])
            elif key == 'backspace' and p not in [0, 1, len(t)]:
                if p > 1 and t[p-1] == ':': p -= 1
                self.set_edit_text(t[:p-1]+t[p:])
                self.edit_pos -= 1 if p != len(self.get_edit_text())+1 else 0
            else:
                (maxcol,) = size
                unhandled = urwid.Edit.keypress(self,(maxcol,),key)
                return unhandled
        else:
            (maxcol,) = size
            unhandled = urwid.Edit.keypress(self,(maxcol,),key)
            return unhandled


class IpEdit(urwid.IntEdit):
    def keypress(self, size, key):
        p = self.edit_pos
        t = self.get_edit_text()
        if key in string.digits+'.':
            rt, rp = self.insert_text_result(key)
            splitText = rt.split('.')
            if key == '.':
                if len(rt) == 1:
                    return
                if rt[-2] != '.' and len(rt.split('.')) < 5:
                    self.insert_text(u'.')
            else:
                if any(len(num) > 3 for num in splitText):
                    if len(splitText) < 4:
                        self.edit_pos = len(t)
                        self.insert_text(u'.')
                        self.insert_text(key)
                else:
                    self.insert_text(key)
                    t = self.get_edit_text()
                    st = t.split('.')
                    for i, n in enumerate(st):
                        if not n:
                            st[i] = '0'
                        else:
                            st[i] = str(int(n))
                    self.set_edit_text('.'.join(st))
        elif key in ['backspace', 'delete']:
            if key == 'delete' and p not in [0, len(t)-1, len(t)]:
                if t != '' and t[p] == '.' and len(t) != 1: p += 1
                self.set_edit_text(t[:p]+t[p+1:])
            elif key == 'backspace' and p not in [0, 1, len(t)]:
                if p > 1 and t[p-1] == '.': p -= 1
                self.set_edit_text(t[:p-1]+t[p:])
                self.edit_pos -= 1 if p != len(self.get_edit_text())+1 else 0
            else:
                (maxcol,) = size
                unhandled = urwid.Edit.keypress(self,(maxcol,),key)
                return unhandled
        else:
            (maxcol,) = size
            unhandled = urwid.Edit.keypress(self,(maxcol,),key)
            return unhandled


class RangeEdit(urwid.IntEdit):
    def __init__(self,caption="",default=None, max=float('inf'), min=0):
        super(RangeEdit, self).__init__(caption, default)
        self.max = max
        self.min = min

    def keypress(self, size, key):
        text, p = self.insert_text_result(key)
        if key in string.digits:
            text = int(text)
            self.set_edit_text(str(min(self.max, max(self.min, text))))
            self.set_edit_pos(p)
        else:
            (maxcol,) = size
            unhandled = urwid.Edit.keypress(self,(maxcol,),key)
            return unhandled


class RestrictEdit(urwid.IntEdit):
    def __init__(self,caption="",default=None,
                 rule=string.letters+string.digits, maxlength=float('inf'),
                 mask=None):
        super(RestrictEdit, self).__init__(caption, default)
        self.maxlength = maxlength
        self.rule = rule
        self.set_mask(mask)

    def keypress(self, size, key):
        text, p = self.insert_text_result(key)
        if key in self.rule:
            if len(text) <= self.maxlength:
                self.insert_text(key)
        elif key in string.digits:
            pass
        else:
            (maxcol,) = size
            unhandled = urwid.Edit.keypress(self,(maxcol,),key)
            return unhandled


def main(argv=None):
    argv = sys.argv[1:]
    print "User input args: " + str(argv)


if __name__ == '__main__':
    main()
