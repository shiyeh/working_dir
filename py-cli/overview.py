#!/usr/bin/python
import urwid
from uiwrap import TableView


class OverviewCellInfoTbl(TableView):
    def __init__(self, model, title='System Info'):
        self._model = model
        # for TEST
        # self._actsim = "TestSIM"
        # self._rssi = "TestRSSI"
        # self._wanip = "T10.194.65.26"
        # self._cellmode = "3G-HSUPA and HSDPA"
        # self._imei = "T357042060592632"
        # self._imsi = "T466011100713357"
        self._actsim = str(self._model.active_sim)
        self._rssi = str(self._model.rssi)
        self._wanip = str(self._model.wan_ipaddr)
        self._cellmode = str(self._model.cell_mode)
        self._imei = str(self._model.imei)
        self._imsi = str(self._model.imsi)
        super(OverviewCellInfoTbl, self).__init__(self.main_view())

    def main_view(self):
        blank = urwid.Divider()
        self.listbox_content = [blank,
            urwid.AttrWrap(urwid.Text("Cellular Info"), 'button select'),
            blank,
            urwid.AttrWrap(urwid.Text("Actived SIM".ljust(30) + " - " + self._actsim), 'button normal'),
            urwid.AttrWrap(urwid.Text("Cellular RSSI".ljust(30) + " - " + self._rssi), 'button normal'),
            urwid.AttrWrap(urwid.Text("WAN IP address".ljust(30) + " - " + self._wanip), 'button normal'),
            urwid.AttrWrap(urwid.Text("Cellular mode".ljust(30) + " - " + self._cellmode), 'button normal'),
            urwid.AttrWrap(urwid.Text("IMEI".ljust(30) + " - " + self._imei), 'button normal'),
            urwid.AttrWrap(urwid.Text("IMSI".ljust(30) + " - " + self._imsi), 'button normal'),
            blank, ]

        text_header = u"Overview"
        txt = urwid.Text(['\n', text_header, '\n'], align='center')
        header = urwid.AttrWrap(txt, 'focus heading')
        listbox = urwid.ListBox(urwid.SimpleListWalker(self.listbox_content))
        frame = urwid.Frame(urwid.AttrWrap(listbox, 'body'), header=header)
        return frame


class OverviewSysInfoTbl(TableView):
    def __init__(self, model, title='System Info'):
        self._model = model
        # self._sysname = "TestSystem"
        # self._devname = "TestDevice"
        # self._systime = "TestZone"
        # self._fwversion = "TestVer"
        # self._fwbuilt = "TestBuilt"
        self._sysname = str(self._model.model_name)
        self._devname = str(self._model.device_name)
        self._systime = str(self._model.up_time)
        self._fwversion = str(self._model.fw_ver)
        self._fwbuilt = str(self._model.fw_build_time)
        super(OverviewSysInfoTbl, self).__init__(self.main_view())

    def main_view(self):
        blank = urwid.Divider()
        self.listbox_content = [blank,
            urwid.AttrWrap(urwid.Text("System Info"), 'button select'),
            blank,
            urwid.AttrWrap(urwid.Text("Model name".ljust(30) + " - " + self._sysname), 'button normal'),
            urwid.AttrWrap(urwid.Text("Device name".ljust(30) + " - " + self._devname), 'button normal'),
            urwid.AttrWrap(urwid.Text("System time".ljust(30) + " - " + self._systime), 'button normal'),
            urwid.AttrWrap(urwid.Text("Firmware version".ljust(30) + " - " + self._fwversion), 'button normal'),
            urwid.AttrWrap(urwid.Text("Firmware built date".ljust(30) + " - " + self._fwbuilt), 'button normal'),
            blank, ]

        text_header = u"Overview"
        txt = urwid.Text(['\n', text_header, '\n'], align='center')
        header = urwid.AttrWrap(txt, 'focus heading')
        listbox = urwid.ListBox(urwid.SimpleListWalker(self.listbox_content))
        frame = urwid.Frame(urwid.AttrWrap(listbox, 'body'), header=header)
        return frame


class OverviewLanInfoTbl(TableView):
    def __init__(self, model, title='System Info'):
        self._model = model
        # self._macaddr = "AA:BB:CC:DD:EE:FF"
        # self._ipaddr = "111.222.333.044"
        # self._submask = "255.255.255.255"
        self._macaddr = str(self._model.mac_addr)
        self._ipaddr = str(self._model.lan_ipaddr)
        self._submask = str(self._model.submask)

        super(OverviewLanInfoTbl, self).__init__(self.main_view())

    def main_view(self):
        blank = urwid.Divider()
        self.listbox_content = [blank,
            urwid.AttrWrap(urwid.Text("LAN Info"), 'button select'),
            blank,
            urwid.AttrWrap(urwid.Text("Device MAC addr.".ljust(30) + " - " + self._macaddr), 'button normal'),
            urwid.AttrWrap(urwid.Text("Device IP addr.".ljust(30) + " - " + self._ipaddr), 'button normal'),
            urwid.AttrWrap(urwid.Text("Device Subnet mask".ljust(30) + " - " + self._submask), 'button normal'),
            blank, ]

        text_header = u"Overview"
        txt = urwid.Text(['\n', text_header, '\n'], align='center')
        header = urwid.AttrWrap(txt, 'focus heading')
        listbox = urwid.ListBox(urwid.SimpleListWalker(self.listbox_content))
        frame = urwid.Frame(urwid.AttrWrap(listbox, 'body'), header=header)
        return frame


class OverviewExampleTbl(TableView):
    """docstring for OverviewTbl"""
    def __init__(self, model, title='ExampleTable'):
        super(OverviewExampleTbl, self).__init__(self.main_view())
        self._model = model

    def main_view(self):
        blank = urwid.Divider()
        self.listbox_content = [blank,
            urwid.AttrWrap(urwid.Text("General"), 'button select'),
            blank,
            urwid.AttrWrap(urwid.Text("item1".ljust(12) + " - " + "1234"), 'button normal'),
            urwid.AttrWrap(urwid.Text("itemAA".ljust(12) + " - " + "ABCDEFGH"), 'button normal'),
            urwid.AttrWrap(urwid.Text("itemCC".ljust(12) + " - " + "#$%^&*"), 'button normal'),
            urwid.AttrWrap(urwid.Text("itemDDDD".ljust(12) + " - " + "000"), 'button normal'),
            blank, ]

        text_header = u"TableView tempalte"
        txt = urwid.Text(['\n', text_header, '\n'], align='center')
        header = urwid.AttrWrap(txt, 'focus heading')
        listbox = urwid.ListBox(urwid.SimpleListWalker(self.listbox_content))
        frame = urwid.Frame(urwid.AttrWrap(listbox, 'body'), header=header)
        return frame
