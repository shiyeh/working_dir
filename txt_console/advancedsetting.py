#!/usr/bin/python
import socket
import sys
import urwid
import json
from uiwrap import TableView, ThingWithAPopUp, IpEdit, RangeEdit
from mainmenu import RootMenu, MenuButton, MenuNode


class AdvancedSerialPortSettingTbl(TableView):
    def __init__(self, model, title='', parent=None, focus_idx=1):
        self._model = model
        self.parent = parent
        self.focus_idx = focus_idx

        self._work_mode = self._model.com_work_mode
        self._trans_mode = self._model.com_trans_mode
        self._baud_rate = self._model.com_baud_rate
        self._parity = self._model.com_parity
        self._data_bits = self._model.com_data_bits
        self._stop_bits = self._model.com_stop_bits
        self._service_mode = self._model.com_service_mode
        self._ip_addr = self._model.com_ip_addr
        self._port = self._model.com_port

        self.show_ip_addr = True if str(self._service_mode) != '1' else False

        self._work_mode_dic = {
            'mccp': 'Console',
            'trans': 'Transparent',
        }
        self._trans_mode_dic = {
            '232': 'RS-232',
            '422': 'RS-422',
            '485': 'RS-485',
        }
        self._baud_rate_dic = {
            '1200': '1200',
            '2400': '2400',
            '4800': '4800',
            '9600': '9600',
            '19200': '19200',
            '38400': '38400',
            '57600': '57600',
            '115200': '115200',
            '230400': '230400',
        }
        self._parity_dic = {
            'none': 'None',
            'odd': 'Odd',
            'even': 'Even',
        }
        self._data_bits_dic = {
            '5': '5',
            '6': '6',
            '7': '7',
            '8': '8',
        }
        self._stop_bits_dic = {
            '1': '1',
            '1.5': '1.5',
            '2': '2',
        }
        self._service_mode_dic = {
            '0': 'TCP/Client',
            '1': 'TCP/Server',
            '2': 'UDP',
        }


        self.refresh = super(AdvancedSerialPortSettingTbl, self).__init__
        self.refresh(self.main_view())

    def _workmodechange(self, button, state, user_data):
        if state:
            self._work_mode = user_data

    def _transmodechange(self, button, state, user_data):
        if state:
            self._trans_mode = user_data

    def _baudratechange(self, button, state, user_data):
        if state:
            self._baud_rate = user_data

    def _paritychange(self, button, state, user_data):
        if state:
            self._parity = user_data

    def _databitschange(self, button, state, user_data):
        if state:
            self._data_bits = user_data

    def _stopbitschange(self, button, state, user_data):
        if state:
            self._stop_bits = user_data

    def _servicemodechange(self, button, state, user_data):
        if state:
            # self._service_mode = user_data
            self._service_mode = user_data
        if str(self._service_mode) == '1':
            if self.show_ip_addr:
                self.show_ip_addr = False
                self.focus_idx = 7
                self.refresh(self.main_view())
        else:
            if not self.show_ip_addr:
                self.show_ip_addr = True
                self.focus_idx = 7
                self.refresh(self.main_view())

    # Temporary solution,
    # TODO: using singal to replace the ugly self.parent relation.
    def _apply_cb(self, button):
        # submit to wrt db.
        self._model.com_work_mode = self._work_mode
        self._model.com_trans_mode = self._trans_mode
        self._model.com_baud_rate = self._baud_rate
        self._model.com_parity = self._parity
        self._model.com_data_bits = self._data_bits
        self._model.com_stop_bits = self._stop_bits
        self._model.com_service_mode = self._service_mode
        self._model.com_ip_addr = self.ip_addr_edt.get_edit_text()
        self._model.com_port = self.port_edt.get_edit_text()
        self._model.set_comsetting()

        self.parent.close_box()

    def main_view(self):
        blank = urwid.Divider()

        self.listbox_content = []
        self.listbox_content.append(blank)

        work_mode_grp = []
        urwid.RadioButton(work_mode_grp, 'Transparent',
            on_state_change=self._workmodechange, user_data='trans',
            state=str(self._work_mode)=='trans')
        urwid.RadioButton(work_mode_grp, 'Console',
            on_state_change=self._workmodechange, user_data='mccp',
            state=str(self._work_mode)=='mccp')
        work_mode_opt = []
        work_mode_opt.extend(work_mode_grp)

        work_mode_cap = urwid.Text('Working Mode'.ljust(28)+': ', 'center')
        btn_label = self._work_mode_dic[str(self._work_mode)]
        work_mode_btn = ThingWithAPopUp(btn_label, work_mode_opt)
        work_mode_row = urwid.Columns([
            ('fixed', 30, work_mode_cap),
            ('fixed', 30, work_mode_btn)],
            dividechars=0)

        trans_mode_grp = []
        urwid.RadioButton(trans_mode_grp, 'RS-232',
            on_state_change=self._transmodechange, user_data='232',
            state=str(self._trans_mode)=='232')
        urwid.RadioButton(trans_mode_grp, 'RS-422',
            on_state_change=self._transmodechange, user_data='422',
            state=str(self._trans_mode)=='422')
        urwid.RadioButton(trans_mode_grp, 'RS-485',
            on_state_change=self._transmodechange, user_data='485',
            state=str(self._trans_mode)=='485')
        trans_mode_opt = []
        trans_mode_opt.extend(trans_mode_grp)

        trans_mode_cap = urwid.Text('Serial Interface'.ljust(28)+': ', 'center')
        btn_label = self._trans_mode_dic[str(self._trans_mode)]
        trans_mode_btn = ThingWithAPopUp(btn_label, trans_mode_opt)
        urwid.WidgetDisable(trans_mode_btn)
        trans_mode_row = urwid.Columns([
            ('fixed', 30, trans_mode_cap),
            ('fixed', 30, trans_mode_btn)],
            dividechars=0)

        baud_rate_grp = []
        urwid.RadioButton(baud_rate_grp, '1200',
            on_state_change=self._baudratechange, user_data='1200',
            state=str(self._baud_rate)=='1200')
        urwid.RadioButton(baud_rate_grp, '2400',
            on_state_change=self._baudratechange, user_data='2400',
            state=str(self._baud_rate)=='2400')
        urwid.RadioButton(baud_rate_grp, '4800',
            on_state_change=self._baudratechange, user_data='4800',
            state=str(self._baud_rate)=='4800')
        urwid.RadioButton(baud_rate_grp, '9600',
            on_state_change=self._baudratechange, user_data='9600',
            state=str(self._baud_rate)=='9600')
        urwid.RadioButton(baud_rate_grp, '19200',
            on_state_change=self._baudratechange, user_data='19200',
            state=str(self._baud_rate)=='19200')
        urwid.RadioButton(baud_rate_grp, '38400',
            on_state_change=self._baudratechange, user_data='38400',
            state=str(self._baud_rate)=='38400')
        urwid.RadioButton(baud_rate_grp, '57600',
            on_state_change=self._baudratechange, user_data='57600',
            state=str(self._baud_rate)=='57600')
        urwid.RadioButton(baud_rate_grp, '115200',
            on_state_change=self._baudratechange, user_data='115200',
            state=str(self._baud_rate)=='115200')
        urwid.RadioButton(baud_rate_grp, '230400',
            on_state_change=self._baudratechange, user_data='230400',
            state=str(self._baud_rate)=='230400')
        baud_rate_opt = []
        baud_rate_opt.extend(baud_rate_grp)

        baud_rate_cap = urwid.Text('Baud-Rate'.ljust(28)+': ', 'center')
        btn_label = self._baud_rate_dic[str(self._baud_rate)]
        baud_rate_btn = ThingWithAPopUp(btn_label, baud_rate_opt)
        baud_rate_row = urwid.Columns([
            ('fixed', 30, baud_rate_cap),
            ('fixed', 30, baud_rate_btn)],
            dividechars=0)

        parity_grp = []
        urwid.RadioButton(parity_grp, 'None',
            on_state_change=self._paritychange, user_data='none',
            state=str(self._parity)=='none')
        urwid.RadioButton(parity_grp, 'Odd',
            on_state_change=self._paritychange, user_data='odd',
            state=str(self._parity)=='odd')
        urwid.RadioButton(parity_grp, 'Even',
            on_state_change=self._paritychange, user_data='even',
            state=str(self._parity)=='even')
        parity_opt = []
        parity_opt.extend(parity_grp)

        parity_cap = urwid.Text('Parity'.ljust(28)+': ', 'center')
        btn_label = self._parity_dic[str(self._parity)]
        parity_btn = ThingWithAPopUp(btn_label, parity_opt)
        parity_row = urwid.Columns([
            ('fixed', 30, parity_cap),
            ('fixed', 30, parity_btn)],
            dividechars=0)

        data_bits_grp = []
        urwid.RadioButton(data_bits_grp, '5',
            on_state_change=self._databitschange, user_data='5',
            state=str(self._data_bits)=='5')
        urwid.RadioButton(data_bits_grp, '6',
            on_state_change=self._databitschange, user_data='6',
            state=str(self._data_bits)=='6')
        urwid.RadioButton(data_bits_grp, '7',
            on_state_change=self._databitschange, user_data='7',
            state=str(self._data_bits)=='7')
        urwid.RadioButton(data_bits_grp, '8',
            on_state_change=self._databitschange, user_data='8',
            state=str(self._data_bits)=='8')
        data_bits_opt = []
        data_bits_opt.extend(data_bits_grp)

        data_bits_cap = urwid.Text('Data Bits'.ljust(28)+': ', 'center')
        btn_label = self._data_bits_dic[str(self._data_bits)]
        data_bits_btn = ThingWithAPopUp(btn_label, data_bits_opt)
        data_bits_row = urwid.Columns([
            ('fixed', 30, data_bits_cap),
            ('fixed', 30, data_bits_btn)],
            dividechars=0)

        stop_bits_grp = []
        urwid.RadioButton(stop_bits_grp, '1',
            on_state_change=self._stopbitschange, user_data='1',
            state=str(self._stop_bits)=='1')
        urwid.RadioButton(stop_bits_grp, '1.5',
            on_state_change=self._stopbitschange, user_data='1.5',
            state=str(self._stop_bits)=='1.5')
        urwid.RadioButton(stop_bits_grp, '2',
            on_state_change=self._stopbitschange, user_data='2',
            state=str(self._stop_bits)=='2')
        stop_bits_opt = []
        stop_bits_opt.extend(stop_bits_grp)

        stop_bits_cap = urwid.Text('Stop Bits'.ljust(28)+': ', 'center')
        btn_label = self._stop_bits_dic[str(self._stop_bits)]
        stop_bits_btn = ThingWithAPopUp(btn_label, stop_bits_opt)
        stop_bits_row = urwid.Columns([
            ('fixed', 30, stop_bits_cap),
            ('fixed', 30, stop_bits_btn)],
            dividechars=0)

        service_mode_grp = []
        urwid.RadioButton(service_mode_grp, 'TCP/Client',
            on_state_change=self._servicemodechange, user_data='0',
            state=str(self._service_mode)=='0')
        urwid.RadioButton(service_mode_grp, 'TCP/Server',
            on_state_change=self._servicemodechange, user_data='1',
            state=str(self._service_mode)=='1')
        urwid.RadioButton(service_mode_grp, 'UDP',
            on_state_change=self._servicemodechange, user_data='2',
            state=str(self._service_mode)=='2')
        service_mode_opt = []
        service_mode_opt.extend(service_mode_grp)

        service_mode_cap = urwid.Text('Operation Mode'.ljust(28)+': ', 'center')
        btn_label = self._service_mode_dic[str(self._service_mode)]
        service_mode_btn = ThingWithAPopUp(btn_label, service_mode_opt)
        service_mode_row = urwid.Columns([
            ('fixed', 30, service_mode_cap),
            ('fixed', 30, service_mode_btn)],
            dividechars=0)

        ip_addr_edtcap = ('editcap', 'IP Address'.ljust(28)+': ')
        ip_addr_edttxt = str(self._ip_addr)
        ip_addr_edt = IpEdit(ip_addr_edtcap, ip_addr_edttxt)
        self.ip_addr_edt = ip_addr_edt
        ip_addr_row = urwid.Columns([
            ('fixed', 60, urwid.AttrWrap(ip_addr_edt, 'editbx', 'editfc'))])

        port_edtcap = ('editcap', 'Port'.ljust(28)+': ')
        port_edttxt = str(self._port)
        port_edt = RangeEdit(port_edtcap, port_edttxt, max=65535)
        self.port_edt = port_edt
        port_row = urwid.Columns([
            ('fixed', 60, urwid.AttrWrap(port_edt, 'editbx', 'editfc'))])

        self.listbox_content.extend([
            work_mode_row, trans_mode_row, baud_rate_row, parity_row,
            data_bits_row, stop_bits_row, service_mode_row, ip_addr_row,
            port_row])
        if not self.show_ip_addr: self.listbox_content.remove(ip_addr_row)

        self.listbox_content.append(blank)
        self._apply = MenuButton("> Apply", self._apply_cb)
        self.listbox_content.append(self._apply)

        text_header = u"Comport Settings"
        txt = urwid.Text(['\n', text_header, '\n'], align='center')
        header = urwid.AttrWrap(txt, 'focus heading')
        listbox = urwid.ListBox(urwid.SimpleListWalker(self.listbox_content))
        listbox.set_focus(self.focus_idx)
        _frame = urwid.Frame(urwid.AttrWrap(listbox, 'body'), header=header)
        return _frame
