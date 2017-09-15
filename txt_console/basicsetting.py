#!/usr/bin/python
import socket
import sys
import urwid
import json
from uiwrap import TableView
from mainmenu import RootMenu, MenuButton, MenuNode


class CellSIM_X_ConfigTbl(TableView):
    def __init__(self, model, simindx=1, title='System Info', parent=None):
        self._model = model
        self.parent = parent
        self._simindx = simindx
        if simindx == 1:
            self._rbtn_auth = self._model.sim1_auth
        if simindx == 2:
            self._rbtn_auth = self._model.sim2_auth
        super(CellSIM_X_ConfigTbl, self).__init__(self.main_view())


#     self.sim1_apn = itm['apn']
#     self.sim1_auth = itm['auth']
#     self.sim1_passwd = itm['password']
#     self.sim1_pin = itm['pin']
#     self.sim1_username = itm['username']

#     self.sim2_apn = itm['apn']
#     self.sim2_auth = itm['auth']
#     self.sim2_passwd = itm['password']
#     self.sim2_pin = itm['pin']
#     self.sim2_username = itm['username']

    def _authchange(self, button, state, user_data):
        if state:
            self._rbtn_auth = user_data

    # Temporary solution,
    # TODO: using singal to replace the ugly self.parent relation.
    def _apply_cb(self, button):
        if self._simindx == 1:
            self._model.sim1_apn = self._edt_apn.get_edit_text()
            self._model.sim1_auth = self._rbtn_auth
            self._model.sim1_passwd = self._edt_passwd.get_edit_text()
            self._model.sim1_pin = self._edt_pin.get_edit_text()
            self._model.sim1_username = self._edt_username.get_edit_text()
        if self._simindx == 2:
            self._model.sim2_apn = self._edt_apn.get_edit_text()
            self._model.sim2_auth = self._rbtn_auth
            self._model.sim2_passwd = self._edt_passwd.get_edit_text()
            self._model.sim2_pin = self._edt_pin.get_edit_text()
            self._model.sim2_username = self._edt_username.get_edit_text()

        self._model.set_wansetting(id=self._simindx)
        self.parent.close_box()

    def main_view(self):
        blank = urwid.Divider()

        self.listbox_content = []
        self.listbox_content.append(blank)
        _txt = urwid.Text("SIM-{0} Configuration".format(self._simindx))
        self.listbox_content.append(urwid.AttrWrap(_txt, 'button select'))
        self.listbox_content.append(blank)

        _apn_edtcap = ('editcp', "APN".ljust(30) + " : ")
        if self._simindx == 1:
            _apn_edttxt = str(self._model.sim1_apn)
        if self._simindx == 2:
            _apn_edttxt = str(self._model.sim2_apn)

        self._edt_apn = urwid.Edit(_apn_edtcap, _apn_edttxt)
        self.listbox_content.append(
            urwid.Padding(
                urwid.AttrWrap(self._edt_apn, 'editbx', 'editfc'),
                width=60))

        _pin_edtcap = ('editcp', "PIN".ljust(30) + " : ")
        if self._simindx == 1:
            _pin_edttxt = str(self._model.sim1_pin)
        if self._simindx == 2:
            _pin_edttxt = str(self._model.sim2_pin)

        self._edt_pin = urwid.Edit(_pin_edtcap, _pin_edttxt)
        self.listbox_content.append(
            urwid.Padding(
                urwid.AttrWrap(self._edt_pin, 'editbx', 'editfc'),
                width=60))

        # radio button list
        _authmodelst = []
        rbtn_grp_authmodelst = []
        _cb = self._authchange
        _rbtn = urwid.RadioButton(rbtn_grp_authmodelst, "PAP",
                                  on_state_change=_cb, user_data="PAP")
        if self._rbtn_auth == "PAP":
            _rbtn.set_state(True, do_callback=False)
        _authmodelst.append(urwid.AttrWrap(_rbtn, 'buttn', 'buttnf'))

        _rbtn = urwid.RadioButton(rbtn_grp_authmodelst, "CHAP",
                                  on_state_change=_cb, user_data="CHAP")
        if self._rbtn_auth == "CHAP":
            _rbtn.set_state(True, do_callback=False)
        _authmodelst.append(urwid.AttrWrap(_rbtn, 'buttn', 'buttnf'))

        # attached radio button list with label
        _cellarray = []
        _txt = urwid.Text("Authentication Protocal".ljust(30) + " : ")
        _cellarray.append(urwid.AttrWrap(_txt, 'editcp'))
        _cellarray.append(urwid.Pile(_authmodelst))

        _cells = urwid.GridFlow(_cellarray, cell_width=32, h_sep=1, v_sep=0, align='left')
        _cells.focus_position = 1
        self.listbox_content.append(_cells)

        _username_edtcap = ('editcp', "Username".ljust(30) + " : ")
        if self._simindx == 1:
            _username_edttxt = str(self._model.sim1_username)
        if self._simindx == 2:
            _username_edttxt = str(self._model.sim2_username)
        self._edt_username = urwid.Edit(_username_edtcap, _username_edttxt)
        self.listbox_content.append(
            urwid.Padding(
                urwid.AttrWrap(self._edt_username, 'editbx', 'editfc'),
                width=60))

        _passwd_edtcap = ('editcp', "Password".ljust(30) + " : ")
        if self._simindx == 1:
            _passwd_edttxt = str(self._model.sim1_passwd)
        if self._simindx == 2:
            _passwd_edttxt = str(self._model.sim2_passwd)
        self._edt_passwd = urwid.Edit(_passwd_edtcap, _passwd_edttxt)
        self.listbox_content.append(
            urwid.Padding(
                urwid.AttrWrap(self._edt_passwd, 'editbx', 'editfc'),
                width=60))

        self.listbox_content.append(blank)

        self._apply = MenuButton("> Apply", self._apply_cb)
        self.listbox_content.append(self._apply)

        text_header = u"Cellular WAN Settings"
        txt = urwid.Text(['\n', text_header, '\n'], align='center')
        header = urwid.AttrWrap(txt, 'focus heading')
        listbox = urwid.ListBox(urwid.SimpleListWalker(self.listbox_content))
        frame = urwid.Frame(urwid.AttrWrap(listbox, 'body'), header=header)
        return frame


class CellPrioConfigTbl(TableView):
    def __init__(self, model, title='System Info', parent=None):
        self._model = model
        self.parent = parent
        self._proisim = self._model.priority
        self._redundant = self._model.redundant
        super(CellPrioConfigTbl, self).__init__(self.main_view())


# self.dsession_retry = itm['data_session_retry']
# self.priority = itm['priority']
# self.redundant = itm['redundant']
# self.reg_nw_tmout = itm['reg_nw_timeout']
# self.term_redundant = itm['term_redundant']

    def _actchange(self, button, state):
        if state:
            self._redundant = 1
        else:
            self._redundant = 0

    def _simsltchage(self, button, state, user_data):
        if state:
            self._proisim = user_data

    # Temporary solution,
    # TODO: using singal to replace the ugly self.parent relation.
    def _apply_cb(self, button):
        self._model.priority = int(self._proisim)
        self._model.redundant = int(self._redundant)
        self._model.reg_nw_tmout = int(self._edt_celltmout.get_edit_text())
        self._model.term_redundant = int(self._edt_termcnt.get_edit_text())
        self._model.dsession_retry = int(self._edt_retry.get_edit_text())
        self._model.set_priosetting()
        self.parent.close_box()

    def main_view(self):
        blank = urwid.Divider()

        self.listbox_content = []
        self.listbox_content.append(blank)
        _txt = urwid.Text("Priority Configuration")
        self.listbox_content.append(urwid.AttrWrap(_txt, 'button select'))
        self.listbox_content.append(blank)

        _redundant = []
        _cb = self._actchange
        _chkbox = urwid.CheckBox("Active", on_state_change=_cb)
        if int(self._redundant) == 1:
            _chkbox.set_state(True, do_callback=False)
        else:
            _chkbox.set_state(False, do_callback=False)

        _redundant.append(urwid.AttrWrap(urwid.Text("Redundant"), 'editcp'))
        _redundant.append(urwid.AttrWrap(_chkbox, 'buttn', 'buttnf'))
        _chkbox_wth_lbl = urwid.GridFlow(_redundant, cell_width=32, h_sep=1, v_sep=0, align='left')
        _chkbox_wth_lbl.focus_position = 1
        self.listbox_content.append(_chkbox_wth_lbl)

        # radio button list
        _simlst = []
        rbtn_grp_simlst = []
        _cb = self._simsltchage
        _rbtn = urwid.RadioButton(rbtn_grp_simlst, "SIM-1",
                                  on_state_change=_cb, user_data=1)
        if int(self._proisim) == 1:
            _rbtn.set_state(True, do_callback=False)
        _simlst.append(urwid.AttrWrap(_rbtn, 'buttn', 'buttnf'))
        _rbtn = urwid.RadioButton(rbtn_grp_simlst, "SIM-2",
                                  on_state_change=_cb, user_data=2)
        if int(self._proisim) == 2:
            _rbtn.set_state(True, do_callback=False)
        _simlst.append(urwid.AttrWrap(_rbtn, 'buttn', 'buttnf'))

        # attached radio button list with label
        _cellarray = []
        _txt = urwid.Text("Priority SIM".ljust(30) + " : ")
        _cellarray.append(urwid.AttrWrap(_txt, 'editcp'))
        _cellarray.append(urwid.Pile(_simlst))

        _cells = urwid.GridFlow(_cellarray, cell_width=32, h_sep=1, v_sep=0, align='left')
        _cells.focus_position = 1
        self.listbox_content.append(_cells)

        regtmout_edtcap = ('editcp', "Reg. Network Timeout(MIN)".ljust(30) + " : ")
        regtmout_edttxt = str(self._model.reg_nw_tmout)
        self._edt_celltmout = urwid.Edit(regtmout_edtcap, regtmout_edttxt)
        self.listbox_content.append(
            urwid.Padding(
                urwid.AttrWrap(self._edt_celltmout, 'editbx', 'editfc'),
                width=60))

        retrycnt_edtcap = ('editcp', "Data Session Retry".ljust(30) + " : ")
        retrycnt_edttxt = str(self._model.dsession_retry)
        self._edt_retry = urwid.Edit(retrycnt_edtcap, retrycnt_edttxt)
        self.listbox_content.append(
            urwid.Padding(
                urwid.AttrWrap(self._edt_retry, 'editbx', 'editfc'),
                width=60))

        termcnt_edtcap = ('editcp', "Terminated Redundant".ljust(30) + " : ")
        termcnt_edttxt = str(self._model.term_redundant)
        self._edt_termcnt = urwid.Edit(termcnt_edtcap, termcnt_edttxt)
        self.listbox_content.append(
            urwid.Padding(
                urwid.AttrWrap(self._edt_termcnt, 'editbx', 'editfc'),
                width=60))

        self.listbox_content.append(blank)

        self._apply = MenuButton("> Apply", self._apply_cb)
        self.listbox_content.append(self._apply)

        text_header = u"Cellular WAN Settings"
        txt = urwid.Text(['\n', text_header, '\n'], align='center')
        header = urwid.AttrWrap(txt, 'focus heading')
        listbox = urwid.ListBox(urwid.SimpleListWalker(self.listbox_content))
        frame = urwid.Frame(urwid.AttrWrap(listbox, 'body'), header=header)
        return frame


class BasicPortForwardTbl(TableView):
    """docstring for BasicPortForwardTbl"""
    def __init__(self, model, title='System Info', parent=None):
        self._model = model
        self.parent = parent
        self._port_forward_active = self._model.port_forward_active
        super(BasicPortForwardTbl, self).__init__(self.main_view())

    def _portforwardactivechange(self, button, state):
        if state:
            self._port_forward_active = 1
        else:
            self._port_forward_active = 0

    def _apply_cb(self, button):
        for index in xrange(0, 5):
            self._model.port_forward_active[index] = int(self._port_forward_active_list[index].get_state())
            # self._model.dhcp_mapping_ip[index] = str(self._edt_mapping_ip_list[index].get_edit_text())
            # self._model.dhcp_mapping_mac[index] = str(self._edt_mapping_mac_list[index].get_edit_text())
            self._model.set_portforward()

        self.parent.close_box()

    def main_view(self):
        blank = urwid.Divider()

        self.listbox_content = []
        self.listbox_content.append(blank)
        self.listbox_content.append(
            urwid.AttrWrap(urwid.Text("Port Forwarding"), 'button select'))
        self.listbox_content.append(blank)

        self._spacecolumn = urwid.AttrWrap(urwid.Text(""), 'button normal')
        self.no = urwid.AttrWrap(urwid.Text("No."), 'button normal')
        self.act = urwid.AttrWrap(urwid.Text("Active"), 'button normal')
        self.protocal = urwid.AttrWrap(urwid.Text("Protocal"), 'button normal')
        self.pub_port = urwid.AttrWrap(urwid.Text("Public Port"), 'button normal')
        self.inter_ip = urwid.AttrWrap(urwid.Text("Internal IP"), 'button normal')
        self.inter_port = urwid.AttrWrap(urwid.Text("Internal Port"), 'button normal')
        self.listbox_content.append(
            # Create 6 columns
            urwid.Columns(
                [('fixed', 3, self.no),
                 ('fixed', 8, self.act),
                 ('fixed', 9, self.protocal),
                 ('fixed', 12, self.pub_port),
                 ('fixed', 16, self.inter_ip),
                 ('fixed', 16, self.inter_port),
                 ], dividechars=1)
        )

        # ipaddr_edtcap = ''
        # macaddr_edtcap = ''
        self._port_forward_active_list = []
        # self._edt_mapping_ip_list = []
        # self._edt_mapping_mac_list = []

        for index in xrange(0, 5):
            self._number = urwid.AttrWrap(urwid.Text("{}".format(index + 1)), 'button normal')

            _cb = self._portforwardactivechange
            _chkbox = urwid.CheckBox("", on_state_change=_cb)
            if int(self._port_forward_active[index]) == 1:
                _chkbox.set_state(True, do_callback=False)
            self._port_forward_act = urwid.AttrWrap(_chkbox, 'buttn', 'buttnf')
            self._port_forward_active_list.append(self._port_forward_act)
            # self._edt_mapping_ip = urwid.Edit(ipaddr_edtcap, self._mapping_ip[index])
            # self._edt_mapping_ip_list.append(self._edt_mapping_ip)
            # self._edt_mapping_mac = urwid.Edit(macaddr_edtcap, self._mapping_mac[index])
            # self._edt_mapping_mac_list.append(self._edt_mapping_mac)
            # self._wrap_mapping_ip = urwid.AttrWrap(self._edt_mapping_ip, 'editbx', 'editfc')
            # self._wrap_mapping_mac = urwid.AttrWrap(self._edt_mapping_mac, 'editbx', 'editfc')

            self.listbox_content.append(
                # Create 6 columns
                urwid.Columns(
                    [('fixed', 4, self._number),
                     ('fixed', 7, self._port_forward_act),
                     # ('fixed', 16, self._wrap_mapping_ip),
                     # ('fixed', 1, self._spacecolumn),
                     # ('fixed', 18, self._wrap_mapping_mac),
                     ], dividechars=1)
            )

        self.listbox_content.append(blank)
        self._apply = MenuButton("> Apply", self._apply_cb)
        self.listbox_content.append(self._apply)

        text_header = u"Basic Setting"
        txt = urwid.Text(['\n', text_header, '\n'], align='center')
        header = urwid.AttrWrap(txt, 'focus heading')
        listbox = urwid.ListBox(urwid.SimpleListWalker(self.listbox_content))
        frame = urwid.Frame(urwid.AttrWrap(listbox, 'body'), header=header)
        return frame


class BasicDhcpMappingTbl(TableView):
    """docstring for BasicDhcpMappingTbl"""
    def __init__(self, model, title='System Info', parent=None):
        self._model = model
        self.parent = parent
        self._dhcp_active = self._model.dhcp_active
        self._mapping_ip = self._model.dhcp_mapping_ip
        self._mapping_mac = self._model.dhcp_mapping_mac
        super(BasicDhcpMappingTbl, self).__init__(self.main_view())

    def _dhcpactivechange(self, button, state):
        if state:
            self._dhcp_active = 1
        else:
            self._dhcp_active = 0

    def _apply_cb(self, button):
        for index in xrange(0, 5):
            self._model.dhcp_active[index] = int(self._dhcp_active_list[index].get_state())
            self._model.dhcp_mapping_ip[index] = str(self._edt_mapping_ip_list[index].get_edit_text())
            self._model.dhcp_mapping_mac[index] = str(self._edt_mapping_mac_list[index].get_edit_text())
            self._model.set_dhcpmapping()

        self.parent.close_box()

    def main_view(self):
        blank = urwid.Divider()

        self.listbox_content = []
        self.listbox_content.append(blank)
        self.listbox_content.append(
            urwid.AttrWrap(urwid.Text("Static DHCP Mapping"), 'button select'))
        self.listbox_content.append(blank)

        self._spacecolumn = urwid.AttrWrap(urwid.Text(""), 'button normal')
        self.no = urwid.AttrWrap(urwid.Text("No."), 'button normal')
        self.act = urwid.AttrWrap(urwid.Text("Active"), 'button normal')
        self.ipaddr = urwid.AttrWrap(urwid.Text("IP Address"), 'button normal')
        self.macaddr = urwid.AttrWrap(urwid.Text("MAC Address"), 'button normal')
        self.listbox_content.append(
            # Create 4 columns
            urwid.Columns(
                [('fixed', 3, self.no),
                 ('fixed', 8, self.act),
                 ('fixed', 16, self.ipaddr),
                 ('fixed', 1, self._spacecolumn),
                 ('fixed', 16, self.macaddr),
                 ], dividechars=1)
        )

        ipaddr_edtcap = ''
        macaddr_edtcap = ''
        self._dhcp_active_list = []
        self._edt_mapping_ip_list = []
        self._edt_mapping_mac_list = []

        for index in xrange(0, 5):
            self._number = urwid.AttrWrap(urwid.Text("{}".format(index + 1)), 'button normal')

            _cb = self._dhcpactivechange
            _chkbox = urwid.CheckBox("", on_state_change=_cb)
            if int(self._dhcp_active[index]) == 1:
                _chkbox.set_state(True, do_callback=False)
            self._mapping_act = urwid.AttrWrap(_chkbox, 'buttn', 'buttnf')
            self._dhcp_active_list.append(self._mapping_act)
            self._edt_mapping_ip = urwid.Edit(ipaddr_edtcap, self._mapping_ip[index])
            self._edt_mapping_ip_list.append(self._edt_mapping_ip)
            self._edt_mapping_mac = urwid.Edit(macaddr_edtcap, self._mapping_mac[index])
            self._edt_mapping_mac_list.append(self._edt_mapping_mac)
            self._wrap_mapping_ip = urwid.AttrWrap(self._edt_mapping_ip, 'editbx', 'editfc')
            self._wrap_mapping_mac = urwid.AttrWrap(self._edt_mapping_mac, 'editbx', 'editfc')

            self.listbox_content.append(
                # Create 4 columns
                urwid.Columns(
                    [('fixed', 4, self._number),
                     ('fixed', 7, self._mapping_act),
                     ('fixed', 16, self._wrap_mapping_ip),
                     ('fixed', 1, self._spacecolumn),
                     ('fixed', 18, self._wrap_mapping_mac),
                     ], dividechars=1)
            )

        self.listbox_content.append(blank)
        self._apply = MenuButton("> Apply", self._apply_cb)
        self.listbox_content.append(self._apply)

        text_header = u"Basic Setting"
        txt = urwid.Text(['\n', text_header, '\n'], align='center')
        header = urwid.AttrWrap(txt, 'focus heading')
        listbox = urwid.ListBox(urwid.SimpleListWalker(self.listbox_content))
        frame = urwid.Frame(urwid.AttrWrap(listbox, 'body'), header=header)
        return frame


class BasicDhcpSettingTbl(TableView):
    """docstring for BasicDhcp"""
    def __init__(self, model, title='System Info', parent=None):
        self._model = model
        self.parent = parent
        self._dhcp_enable = self._model.dhcp_enable
        super(BasicDhcpSettingTbl, self).__init__(self.main_view())

    def _dhcpenablechange(self, button, state):
        if state:
            self._dhcp_enable = 1
        else:
            self._dhcp_enable = 0

    # Temporary solution,
    # TODO: using singal to replace the ugly self.parent relation.
    def _apply_cb(self, button):
        self._model.dhcp_enable = int(self._dhcp_enable)
        self._model.startip = str(self._edt_startip.get_edit_text())
        self._model.maxusers = str(self._edt_maxusers.get_edit_text())
        self._model.clienttime = str(self._edt_clienttime.get_edit_text())
        self._model.set_dhcpserver()

        self.parent.close_box()

    def main_view(self):
        blank = urwid.Divider()

        self.listbox_content = []
        self.listbox_content.append(blank)
        self.listbox_content.append(
            urwid.AttrWrap(urwid.Text("DHCP Server Setting"), 'button select'))
        self.listbox_content.append(blank)

        _dhcpenable = []
        _cb = self._dhcpenablechange
        _chkbox = urwid.CheckBox("Enable", on_state_change=_cb)
        if int(self._dhcp_enable) == 1:
            _chkbox.set_state(True, do_callback=False)
        _dhcpenable.append(urwid.AttrWrap(urwid.Text("DHCP Server"), 'editcp'))
        _dhcpenable.append(urwid.AttrWrap(_chkbox, 'buttn', 'buttnf'))
        _chkbox_wth_lbl = urwid.GridFlow(_dhcpenable, cell_width=32, h_sep=1, v_sep=0, align='left')
        _chkbox_wth_lbl.focus_position = 1

        self.listbox_content.append(_chkbox_wth_lbl)
        self.listbox_content.append(blank)

        self.listbox_content.append(
            urwid.AttrWrap(urwid.Text("Default Gateway".ljust(30) + " : " + self._model.lanset_ipddr), 'button normal'))
        self.listbox_content.append(
            urwid.AttrWrap(urwid.Text("Subnet Mask".ljust(30) + " : " + self._model.lanset_submsk), 'button normal'))
        self.listbox_content.append(
            urwid.AttrWrap(urwid.Text("Primary DNS".ljust(30) + " : " + self._model.pridns), 'button normal'))
        self.listbox_content.append(
            urwid.AttrWrap(urwid.Text("Second DNS".ljust(30) + " : " + self._model.secdns), 'button normal'))

        startip_edtcap = ('editcp', "Start IP Address".ljust(30) + " : ")
        startip_edttxt = str(self._model.startip)
        self._edt_startip = urwid.Edit(startip_edtcap, startip_edttxt)
        self.listbox_content.append(
            urwid.Padding(
                urwid.AttrWrap(self._edt_startip, 'editbx', 'editfc'),
                width=60))

        maxusers_edtcap = ('editcp', "Maximum Number of Users".ljust(30) + " : ")
        maxusers_edttxt = str(self._model.maxusers)
        self._edt_maxusers = urwid.Edit(maxusers_edtcap, maxusers_edttxt)
        self.listbox_content.append(
            urwid.Padding(
                urwid.AttrWrap(self._edt_maxusers, 'editbx', 'editfc'),
                width=60))

        clienttime_edtcap = ('editcp', "Client Lease Time (secs)".ljust(30) + " : ")
        clienttime_edttxt = str(self._model.clienttime)
        self._edt_clienttime = urwid.Edit(clienttime_edtcap, clienttime_edttxt)
        self.listbox_content.append(
            urwid.Padding(
                urwid.AttrWrap(self._edt_clienttime, 'editbx', 'editfc'),
                width=60))

        self.listbox_content.append(blank)

        self._apply = MenuButton("> Apply", self._apply_cb)
        self.listbox_content.append(self._apply)

        text_header = u"Basic Setting"
        txt = urwid.Text(['\n', text_header, '\n'], align='center')
        header = urwid.AttrWrap(txt, 'focus heading')
        listbox = urwid.ListBox(urwid.SimpleListWalker(self.listbox_content))
        frame = urwid.Frame(urwid.AttrWrap(listbox, 'body'), header=header)
        return frame


class BasicLanSettingTbl(TableView):
    def __init__(self, model, title='System Info', parent=None):
        self._model = model
        self.parent = parent
        self._allow_ping = self._model.allow_ping
        super(BasicLanSettingTbl, self).__init__(self.main_view())

# self.allow_ping = itm['allow_ping']
# self.pridns = itm['dns']
# self.secdns = itm['sec_dns']
# self.lanset_ipddr = itm['ip_addr']
# self.lanset_submsk = itm['submask']

    def _allowpingchange(self, button, state):
        if state:
            self._allow_ping = 1
        else:
            self._allow_ping = 0

    # Temporary solution,
    # TODO: using singal to replace the ugly self.parent relation.
    def _apply_cb(self, button):
        self._model.allow_ping = int(self._allow_ping)
        self._model.lanset_ipddr = str(self._edt_lanip.get_edit_text())
        self._model.lanset_submsk = str(self._edt_lanmsk.get_edit_text())
        self._model.pridns = str(self._edt_pridns.get_edit_text())
        self._model.secdns = str(self._edt_secdns.get_edit_text())
        self._model.set_lansetting()

        self.parent.close_box()

    def main_view(self):
        blank = urwid.Divider()

        self.listbox_content = []
        self.listbox_content.append(blank)
        self.listbox_content.append(
            urwid.AttrWrap(urwid.Text("LAN Setting"), 'button select'))
        self.listbox_content.append(blank)

        ipaddr_edtcap = ('editcp', "IP address".ljust(30) + " : ")
        ipaddr_edttxt = str(self._model.lanset_ipddr)
        self._edt_lanip = urwid.Edit(ipaddr_edtcap, ipaddr_edttxt)
        self.listbox_content.append(
            urwid.Padding(
                urwid.AttrWrap(self._edt_lanip, 'editbx', 'editfc'),
                width=60))

        submask_edtcap = ('editcp', "Subnet mask".ljust(30) + " : ")
        submask_edttxt = str(self._model.lanset_submsk)
        self._edt_lanmsk = urwid.Edit(submask_edtcap, submask_edttxt)
        self.listbox_content.append(
            urwid.Padding(
                urwid.AttrWrap(self._edt_lanmsk, 'editbx', 'editfc'),
                width=60))

        primdns_edtcap = ('editcp', "Primary DNS".ljust(30) + " : ")
        primdns_edttxt = str(self._model.pridns)
        self._edt_pridns = urwid.Edit(primdns_edtcap, primdns_edttxt)
        self.listbox_content.append(
            urwid.Padding(
                urwid.AttrWrap(self._edt_pridns, 'editbx', 'editfc'),
                width=60))

        secndns_edtcap = ('editcp', "Secondary DNS".ljust(30) + " : ")
        secndns_edttxt = str(self._model.secdns)
        self._edt_secdns = urwid.Edit(secndns_edtcap, secndns_edttxt)
        self.listbox_content.append(
            urwid.Padding(
                urwid.AttrWrap(self._edt_secdns, 'editbx', 'editfc'),
                width=60))

        self.listbox_content.append(blank)
        _allowping = []
        _cb = self._allowpingchange
        _chkbox = urwid.CheckBox("Accept", on_state_change=_cb)
        if int(self._allow_ping) == 1:
            _chkbox.set_state(True, do_callback=False)
        _allowping.append(urwid.AttrWrap(urwid.Text("Allow Ping"), 'editcp'))
        _allowping.append(urwid.AttrWrap(_chkbox, 'buttn', 'buttnf'))
        _chkbox_wth_lbl = urwid.GridFlow(_allowping, cell_width=32, h_sep=1, v_sep=0, align='left')
        _chkbox_wth_lbl.focus_position = 1

        self.listbox_content.append(_chkbox_wth_lbl)
        self.listbox_content.append(blank)

        self._apply = MenuButton("> Apply", self._apply_cb)
        self.listbox_content.append(self._apply)

        text_header = u"Basic Setting"
        txt = urwid.Text(['\n', text_header, '\n'], align='center')
        header = urwid.AttrWrap(txt, 'focus heading')
        listbox = urwid.ListBox(urwid.SimpleListWalker(self.listbox_content))
        frame = urwid.Frame(urwid.AttrWrap(listbox, 'body'), header=header)
        return frame


class BasicDeviceSettingTbl(TableView):
    def __init__(self, model, title='System Info', parent=None):
        self._model = model
        self.parent = parent
        self.gmtmode = self._model.utc_offset[0]
        _lst = self._model.utc_offset[1:].split(':')
        self.gmthr = _lst[0]
        self.gmtmin = _lst[1]
        self.device_name = ""
        super(BasicDeviceSettingTbl, self).__init__(self.main_view())

    def _gmtchange(self, button, state, user_data):
        if state:
            self.gmtmode = user_data

    def _hrchange(self, button, state, user_data):
        if state:
            self.gmthr = user_data

    def _minchange(self, button, state, user_data):
        if state:
            self.gmtmin = user_data

    # Temporary solution,
    # TODO: using singal to replace the ugly self.parent relation.
    def _apply_cb(self, button):
        self._model.utc_offset = "{0}{1}:{2}".format(self.gmtmode,
                                                     self.gmthr,
                                                     self.gmtmin)
        self._model.device_name = self._edt_name.get_edit_text()

        # submit to wrt db.
        self._model.set_devicesetting()
        self.parent.close_box()

    def main_view(self):
        blank = urwid.Divider()
        devname_edtcap = ('editcp', "Device Name".ljust(30) + " : ")
        devname_edttxt = str(self._model.device_name)

        _gmtlst = []
        _gmtlst.append(urwid.AttrWrap(urwid.Text("   [GMT]"), 'button normal'))

        rbtn_gmt = []
        _cb = self._gmtchange
        _rbtn = urwid.RadioButton(rbtn_gmt, " +",
                                  on_state_change=_cb, user_data="+")
        if self.gmtmode == "+":
            _rbtn.set_state(True, do_callback=False)
        _gmtlst.append(urwid.AttrWrap(_rbtn, 'buttn', 'buttnf'))
        _rbtn = urwid.RadioButton(rbtn_gmt, " -",
                                  on_state_change=_cb, user_data="-")
        if self.gmtmode == "-":
            _rbtn.set_state(True, do_callback=False)
        _gmtlst.append(urwid.AttrWrap(_rbtn, 'buttn', 'buttnf'))

        _hourlst = []
        rbtn_grp_hr = []
        _hourlst.append(urwid.AttrWrap(urwid.Text("   [HOUR]"), 'button normal'))

        _hrtxt_lst = ["00", "01", "02", "03", "04", "05", "06", "07",
                      "08", "09", "10", "11", "12", "13", "14", ]
        _cb = self._hrchange
        for _txt in _hrtxt_lst:
            _rbtn = urwid.RadioButton(rbtn_grp_hr, _txt,
                                      on_state_change=_cb, user_data=_txt)
            if self.gmthr == _txt:
                _rbtn.set_state(True, do_callback=False)
            _hourlst.append(urwid.AttrWrap(_rbtn, 'buttn', 'buttnf'))

        _minlst = []
        _minlst.append(urwid.AttrWrap(urwid.Text("   [MIN]"), 'button normal'))
        rbtn_grp_min = []
        _cb = self._minchange
        _rbtn = urwid.RadioButton(rbtn_grp_min, " 00",
                                  on_state_change=_cb, user_data="00")
        if self.gmtmin == "00":
            _rbtn.set_state(True, do_callback=False)
        _minlst.append(urwid.AttrWrap(_rbtn, 'buttn', 'buttnf'))
        _rbtn = urwid.RadioButton(rbtn_grp_min, " 30",
                                  on_state_change=_cb, user_data="30")
        if self.gmtmin == "30":
            _rbtn.set_state(True, do_callback=False)
        _minlst.append(urwid.AttrWrap(_rbtn, 'buttn', 'buttnf'))
        _rbtn = urwid.RadioButton(rbtn_grp_min, " 45",
                                  on_state_change=_cb, user_data="45")
        if self.gmtmin == "45":
            _rbtn.set_state(True, do_callback=False)
        _minlst.append(urwid.AttrWrap(_rbtn, 'buttn', 'buttnf'))

        _tmzcells = []
        _tmzcells.append(urwid.Pile(_gmtlst))
        _tmzcells.append(urwid.Pile(_hourlst))
        _tmzcells.append(urwid.Pile(_minlst))

        _tmlstcell = urwid.GridFlow(_tmzcells, cell_width=10, h_sep=1, v_sep=0, align='left')

        cellarray = []
        _timezone = "Current Time Zone is " + str(self._model.utc_offset)
        cellarray.append(urwid.AttrWrap(urwid.Text(_timezone.ljust(30) + " : "), 'editcp'))
        cellarray.append(_tmlstcell)

        _cells = urwid.GridFlow(cellarray, cell_width=32, h_sep=1, v_sep=0, align='left')
        _cells.focus_position = 1

        self.listbox_content = []
        self.listbox_content.append(blank)
        self.listbox_content.append(
            urwid.AttrWrap(urwid.Text("Device Setting"), 'button select'))
        self.listbox_content.append(blank)
        self._edt_name = urwid.Edit(devname_edtcap, devname_edttxt)
        self.listbox_content.append(urwid.Padding(
                                    urwid.AttrWrap(self._edt_name, 'editbx', 'editfc'),
                                    width=60))
        self.listbox_content.append(_cells)
        self.listbox_content.append(blank)

        self._apply = MenuButton("> Apply", self._apply_cb)
        self.listbox_content.append(self._apply)

        text_header = u"Basic Setting"
        txt = urwid.Text(['\n', text_header, '\n'], align='center')
        header = urwid.AttrWrap(txt, 'focus heading')
        listbox = urwid.ListBox(urwid.SimpleListWalker(self.listbox_content))
        _frame = urwid.Frame(urwid.AttrWrap(listbox, 'body'), header=header)
        return _frame
