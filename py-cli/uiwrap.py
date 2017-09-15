#!/usr/bin/python
import os
import sys
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


def main(argv=None):
    argv = sys.argv[1:]
    print "User input args: " + str(argv)


if __name__ == '__main__':
    main()
