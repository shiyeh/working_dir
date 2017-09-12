#!/usr/bin/python
import urwid
from uiwrap import MenuButton, MenuNode, CascadingBoxes


# def menu(title, choices):
#     _txt = urwid.Text(['\n', title, '\n'], align='center')
#     _map = urwid.Attr_Map(_txt, 'focus heading')
#     body = [_map, urwid.Divider()]
#     body.extend(choices)
#     return urwid.ListBox(urwid.SimpleFocusListWalker(body))

# _submenu_overview = SubMenu('Overview',
#              [choice('System Info'),
#               choice('LAN Info', ov_laninfo),
#               choice('Cellular Info'),
#               choice('Monitor'), ])

# wan_setting = SubMenu('Cellular WAN Settings', [
#     t_menu('SIM1 Confiuration', sim_config, _id=1),
# ])

# _submenu_basicsetting = SubMenu('Basic Settings',
#              [ wan_setting,
#                wan_setting, ])              

# _choices = [ _submenu_overview, 
#              _submenu_basicsetting,
#              choice('SAVE', save_config),
#              choice('EXIT')
# ]

# menu_top = menu('Main Menu', _choices)
# RootMenu is not a kind of MenuNode.
# It does not contain MENUBUTTON, so it's not inherited from urwid.WidgetWrap. 
# RootMenu creates ListBox and BoxHolder to setup screen to display.
class RootMenu(object):
    def __init__(self, palette, title):
        super(RootMenu, self).__init__()

        _txt = urwid.Text(['\n', title, '\n'], align='center')
        _map = urwid.AttrMap(_txt, 'focus heading')

        self._listbody = [_map, urwid.Divider()]
        # _listbody.extend(choices)
        self._box = urwid.ListBox(urwid.SimpleFocusListWalker(self._listbody))
        self._boxholder = CascadingBoxes(self._box)

        self._palette = palette
        self._loop = urwid.MainLoop(self._boxholder, self._palette, pop_ups=True)

    def get_boxholder(self):
        return self._boxholder

    def add_submenu(self, choice):
        # self._listbody.extend(choices)
        self._listbody.append(choice)

    def run(self):
        self._box.body = urwid.SimpleFocusListWalker(self._listbody)
        self._loop.run()

    def stop(self):
        raise urwid.ExitMainLoop()


def main():
    palette = [
        ('none', '', '', ''),
        ('focus heading', 'bold', 'dark blue'),
        ('line', 'black', 'dark red'),
        ('options', '', ''),
        ('reversed', 'standout', ''),
        ('selected', 'bold, black', 'light gray'),
        ('item', 'bold, white', ''),
        ('editfc', 'white', 'dark blue', 'bold'),
        ('editbx', 'light gray', 'dark blue'),
        ('editcp', 'white', '', 'standout'),
        ('popbg', 'white', 'dark blue'),
        ('important', 'bold, white', 'dark blue'),
    ]

    mainmenu = RootMenu(palette, 'Main Menu')
    _top = mainmenu.get_boxholder()

    # _submenu_overview = MenuNode(_top, 'Overview')
    # _submenu_overview.add_choice(MenuButton('System Info'))
    # _submenu_overview.add_choice(MenuButton('LAN Info'))
    # _submenu_overview.add_choice(MenuButton('Cellular Info'))
    # _submenu_overview.add_choice(MenuButton('Monitor'))

    # mainmenu.add_submenu(_submenu_overview)

    # _submenu_net_setting = MenuNode(_top, 'Network Settings')
    # _submenu_net_setting.add_choice(MenuButton('Device Setting'))
    # _submenu_net_setting.add_choice(MenuButton('LAN Settings'))

    # _submenu_wan_setting = MenuNode(_top, 'Cellular WAN Settings')
    # _submenu_wan_setting.add_choice(MenuButton('Priority Configuration'))
    # _submenu_wan_setting.add_choice(MenuButton('SIM1 Confiuration'))
    # _submenu_wan_setting.add_choice(MenuButton('SIM2 Confiuration'))

    # _submenu_basicsetting = MenuNode(_top, 'Basic Settings')
    # _submenu_basicsetting.add_choice(_submenu_net_setting)
    # _submenu_basicsetting.add_choice(_submenu_wan_setting)

    mainmenu.add_submenu(_submenu_basicsetting)
    mainmenu.run()


if __name__ == '__main__':
    main()
