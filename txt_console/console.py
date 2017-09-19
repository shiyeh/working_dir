#!/usr/bin/python
import socket
import os
import sys
import time
import urwid
import json
# import subprocess
# from uiwrap import TableView
from mainmenu import RootMenu, MenuButton, MenuNode

from overview import OverviewCellInfoTbl
from overview import OverviewExampleTbl
from overview import OverviewLanInfoTbl
from overview import OverviewSysInfoTbl

from basicsetting import CellSIM_X_ConfigTbl
from basicsetting import CellPrioConfigTbl
from basicsetting import BasicLanSettingTbl
from basicsetting import BasicDeviceSettingTbl
from basicsetting import BasicDhcpSettingTbl
from basicsetting import BasicDhcpMappingTbl
from basicsetting import BasicPortForwardTbl

from advancedsetting import AdvancedSerialPortSettingTbl

class MlisConsoleModel(object):
    """docstring for MlisConsoleModel"""
    def __init__(self, arg):
        super(MlisConsoleModel, self).__init__()
        self.arg = arg

    def update_act(self, act):
        s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        s.connect("/tmp/db.sock")
        send_data = "{{\"method\": \"update\", \"values\": \"{}\"}}".format(act)
        s.send(send_data)
        # print(send_data)

        data = s.recv(10240)
        data = json.loads(data)
        s.close()
        return data

    def _getdb(self, tbl):
        s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        s.connect("/tmp/db.sock")
        send_data = "{{\"method\": \"get\", \"table\": \"{}\"}}".format(tbl)
        s.send(send_data)
        # print(send_data)

        data = s.recv(10240)
        data = json.loads(data)
        s.close()
        return data

    def _setdb(self, tbl, id=1, values=None):
        send_data = dict()
        send_data["method"] = "set"
        send_data["table"] = tbl
        send_data["id"] = int(id)
        send_data["values"] = values

        s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        s.connect("/tmp/db.sock")

        # print send_data
        send_data = json.dumps(send_data)
        # print send_data
        s.send(send_data)
        # print(send_data)

        data = s.recv(10240)
        data = json.loads(data)
        s.close()
        return data

    def get_sysinfo(self):
        # {"method": "get", "table": "system_info"}
        # {u'result': u'success',
        #  u'system_info': [{u'device_name': None,
        #                    u'fw_build_time': u'20170627',
        #                    u'fw_ver': u'v1.3.1_20170627_RC1_R0',
        #                    u'id': 1,
        #                    u'kernel_ver': None,
        #                    u'model_name': u'ISON IS-C Series',
        #                    u'serial_no': None,
        #                    u'timezone': u'UTC',
        #                    u'up_time': 1500524721.98,
        #                    u'utc_offset': u'+00:00'}]}
        data = self._getdb("system_info")
        # print data
        for itm in data["system_info"]:
            self.device_name = itm['device_name']
            self.fw_build_time = itm['fw_build_time']
            self.fw_ver = itm['fw_ver']
            self.id = itm['id']
            self.kernel_ver = itm['kernel_ver']
            self.model_name = itm['model_name']
            self.serial_no = itm['serial_no']
            self.timezone = itm['timezone']
            self.up_time = itm['up_time']
            self.utc_offset = itm['utc_offset']

    def set_devicesetting(self):
        _values = dict()
        # for Test.

        # _values['device_name'] = "TEST"
        # _values['up_time'] = 1500524721.98
        # self.utc_offset = "-13:00"

        _values['device_name'] = str(self.device_name)
        _values['utc_offset'] = str(self.utc_offset)
        self._setdb(tbl="system_info", values=_values)

    def get_cellinfo(self):
        # {"method": "get", "table": "cellular_info"}
        # {u'cellular_info': [{u'id': 1,
        #                      u'imei': u'357042060592632',
        #                      u'imsi': u'466011100713357'}],
        #  u'result': u'success'}
        data = self._getdb("cellular_info")
        for itm in data["cellular_info"]:
            self.imei = itm['imei']
            self.imsi = itm['imsi']

        # {"method": "get", "table": "cellular"}
        # {u'cellular': [{u'active_sim': u'SIM1',
        #                 u'id': 1,
        #                 u'ip_addr': u'192.168.0.1',
        #                 u'mode': u'3G-UTRAN',
        #                 u'rssi': u'13'}],
        #  u'result': u'success'}
        data = self._getdb("cellular")
        for itm in data["cellular"]:
            self.active_sim = itm['active_sim']
            self.wan_ipaddr = itm['ip_addr']
            self.cell_mode = itm['mode']
            self.rssi = itm['rssi']

    def get_laninfo(self):
        # {"method": "get", "table": "lan_info"}
        # {u'lan_info': [{u'id': 1,
        #                 u'ip_addr': u'10.0.10.1',
        #                 u'mac_addr': None,
        #                 u'submask': u'255.255.255.0'}],
        #  u'result': u'success'}
        data = self._getdb("lan_info")
        for itm in data["lan_info"]:
            self.lan_ipaddr = itm['ip_addr']
            self.mac_addr = itm['mac_addr']
            self.submask = itm['submask']

    def get_lansetting(self):
        # {"method": "get", "table": "lan_setting"}
        # {u'lan_setting': [{u'allow_ping': 0,
        #                    u'dns': u'8.8.8.8',
        #                    u'id': 1,
        #                    u'ip_addr': u'10.0.10.1',
        #                    u'sec_dns': u'8.8.4.4',
        #                    u'submask': u'255.255.255.0'}],
        #  u'result': u'success'}
        data = self._getdb("lan_setting")
        for itm in data["lan_setting"]:
            self.allow_ping = itm['allow_ping']
            self.pridns = itm['dns']
            self.secdns = itm['sec_dns']
            self.lanset_ipddr = itm['ip_addr']
            self.lanset_submsk = itm['submask']

    def set_lansetting(self):
        _values = dict()
        _values['allow_ping'] = int(self.allow_ping)
        _values['dns'] = str(self.pridns)
        _values['sec_dns'] = str(self.secdns)
        _values['ip_addr'] = str(self.lan_ipaddr)
        _values['submask'] = str(self.lanset_submsk)

        self._setdb(tbl="lan_setting", values=_values)

    def get_wansetting(self):
        # {"method": "get", "table": "wan_setting"}
        # {u'result': u'success',
        #  u'wan_setting': [{u'apn': u'internet',
        #                    u'auth': u'',
        #                    u'id': 1,
        #                    u'password': u'',
        #                    u'pin': u'',
        #                    u'username': u''},
        #                   {u'apn': u'internet',
        #                    u'auth': u'',
        #                    u'id': 2,
        #                    u'password': u'',
        #                    u'pin': u'',
        #                    u'username': u''}]}
        data = self._getdb("wan_setting")
        for itm in data["wan_setting"]:
            if itm['id'] == 1:
                self.sim1_apn = itm['apn']
                self.sim1_auth = itm['auth']
                self.sim1_passwd = itm['password']
                self.sim1_pin = itm['pin']
                self.sim1_username = itm['username']
            if itm['id'] == 2:
                self.sim2_apn = itm['apn']
                self.sim2_auth = itm['auth']
                self.sim2_passwd = itm['password']
                self.sim2_pin = itm['pin']
                self.sim2_username = itm['username']

    def set_wansetting(self, id=1):
        _values = dict()
        if id == 1:
            _values['apn'] = str(self.sim1_apn)
            _values['auth'] = str(self.sim1_auth)
            _values['password'] = str(self.sim1_passwd)
            _values['pin'] = str(self.sim1_pin)
            _values['username'] = str(self.sim1_username)
        if id == 2:
            _values['apn'] = str(self.sim2_apn)
            _values['auth'] = str(self.sim2_auth)
            _values['password'] = str(self.sim2_passwd)
            _values['pin'] = str(self.sim2_pin)
            _values['username'] = str(self.sim2_username)

        self._setdb(tbl="wan_setting", values=_values, id=id)

    def get_priosetting(self):
        # {"method": "get", "table": "wan_priority_setting"}
        # {u'result': u'success',
        #  u'wan_priority_setting': [{u'data_session_retry': 2,
        #                             u'id': 1,
        #                             u'priority': 1,
        #                             u'redundant': 0,
        #                             u'reg_nw_timeout': 5,
        #                             u'term_redundant': 10}]}
        data = self._getdb("wan_priority_setting")
        for itm in data["wan_priority_setting"]:
            self.dsession_retry = itm['data_session_retry']
            self.priority = itm['priority']
            self.redundant = itm['redundant']
            self.reg_nw_tmout = itm['reg_nw_timeout']
            self.term_redundant = itm['term_redundant']

    def set_priosetting(self):
        _values = dict()
        _values['data_session_retry'] = int(self.dsession_retry)
        _values['priority'] = int(self.priority)
        _values['redundant'] = int(self.redundant)
        _values['reg_nw_timeout'] = int(self.reg_nw_tmout)
        _values['term_redundant'] = int(self.term_redundant)

        self._setdb(tbl="wan_priority_setting", values=_values)

    def get_comsetting(self):
        # {"method": "get", "table": "com_setting"}
        # {u'com_setting': [{u'baud_rate': 115200,
        #            u'data_bits': 8,
        #            u'id': 1,
        #            u'ip_addr': u'0.0.0.0',
        #            u'parity': u'none',
        #            u'port': u'',
        #            u'service_mode': 0,
        #            u'stop_bits': 1,
        #            u'trans_mode': u'232',
        #            u'work_mode': u'trans'}],
        #            u'result': u'success'}
        data = self._getdb("com_setting")
        for itm in data["com_setting"]:
            self.com_work_mode = itm['work_mode']
            self.com_trans_mode = itm['trans_mode']
            self.com_baud_rate = itm['baud_rate']
            self.com_parity = itm['parity']
            self.com_data_bits = itm['data_bits']
            self.com_stop_bits = itm['stop_bits']
            self.com_service_mode = itm['service_mode']
            self.com_ip_addr = itm['ip_addr']
            self.com_port = itm['port']

    def set_comsetting(self):
        _values = dict()
        _values['work_mode'] = str(self.com_work_mode)
        _values['trans_mode'] = str(self.com_trans_mode)
        _values['baud_rate'] = str(self.com_baud_rate)
        _values['parity'] = str(self.com_parity)
        _values['data_bits'] = int(self.com_data_bits)
        _values['stop_bits'] = int(self.com_stop_bits)
        _values['service_mode'] = int(self.com_service_mode)
        _values['ip_addr'] = str(self.com_ip_addr)
        _values['port'] = str(self.com_port)

        self._setdb(tbl="com_setting", values=_values)

    def get_dhcpserver(self):
        data = self._getdb("dhcp_server")
        for itm in data["dhcp_server"]:
            self.dhcp_enable = itm['dhcp_server']
            self.gateway = itm['gateway']
            self.submask = itm['submask']
            self.pridns = itm['dns']
            self.secdns = itm['sec_dns']
            self.startip = itm['start_ip']
            self.maxusers = itm['max_users']
            self.clienttime = itm['client_time']

    def set_dhcpserver(self):
        _values = dict()
        _values['dhcp_server'] = str(self.dhcp_enable)
        _values['start_ip'] = str(self.startip)
        _values['max_users'] = str(self.maxusers)
        _values['client_time'] = str(self.clienttime)

        self._setdb(tbl="dhcp_server", values=_values)

    def get_dhcpmapping(self):
        data = self._getdb("dhcp_mapping")
        self.dhcp_active = []
        self.dhcp_mapping_ip = []
        self.dhcp_mapping_mac = []
        for itm in data["dhcp_mapping"]:
            # self.dhcp_act = itm['active']
            self.dhcp_active.append(str(itm['active']))
            self.dhcp_mapping_ip.append(str(itm['ip']))
            self.dhcp_mapping_mac.append(str(itm['mac']))
            # self.dhcp_mapping_id = itm['id']

    def set_dhcpmapping(self):
        _values = dict()
        # _values['active'] = str(self.dhcp_mapping_act)
        # _values['ip'] = str(self.dhcp_mapping_ip)
        # _values['mac'] = str(self.dhcp_mapping_mac)
        # _values['id'] = str(self.dhcp_mapping_id)

        for index in xrange(0, 16):
            _values['active'] = str(self.dhcp_active[index])
            _values['ip'] = str(self.dhcp_mapping_ip[index])
            _values['mac'] = str(self.dhcp_mapping_mac[index])
            self._setdb(tbl="dhcp_mapping", values=_values, id=index + 1)

    def get_portforward(self):
        data = self._getdb("port_forwarding")
        self.port_forward_active = []
        self.protocol = []
        self.public_port = []
        self.inter_ip = []
        self.inter_port = []
        for itm in data["port_forwarding"]:
            self.port_forward_active.append(str(itm['active']))
            self.protocol.append(str(itm['protocol']))
            self.public_port.append(str(itm['public_port']))
            self.inter_ip.append(str(itm['ip']))
            self.inter_port.append(str(itm['internal_port']))

    def set_portforward(self):
        _values = dict()

        for index in xrange(0, 5):
            _values['active'] = str(self.port_forward_active[index])
            _values['protocol'] = str(self.protocol[index])
            _values['public_port'] = str(self.public_port[index])
            _values['ip'] = str(self.inter_ip[index])
            _values['internal_port'] = str(self.inter_port[index])
            self._setdb(tbl="port_forwarding", values=_values, id=index + 1)


class MlisConsoleView(object):
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

    """docstring for MlisConsoleView"""
    def __init__(self, arg, model=None):
        super(MlisConsoleView, self).__init__()
        self.arg = arg
        self._model = model

        self.mainmenu = RootMenu(MlisConsoleView.palette, title='Main Menu')
        self._top = self.mainmenu.get_boxholder()

        self._submenu_overview = MenuNode(self._top, 'Overview')
        self._submenu_overview.add_choice(MenuButton('ExampleTable', self.ov_example_tbl))
        self._submenu_overview.add_choice(MenuButton('System Info', self.ov_sysinfo_tbl))
        self._submenu_overview.add_choice(MenuButton('LAN Info', self.ov_laninfo_tbl))
        self._submenu_overview.add_choice(MenuButton('Cellular Info', self.ov_cellinfo_tbl))
        self._submenu_overview.add_choice(MenuButton('Monitor', self.ov_monitor_tbl))
        self.mainmenu.add_submenu(self._submenu_overview)

        self._submenu_net_setting = MenuNode(self._top, 'Network Settings')
        self._submenu_net_setting.add_choice(MenuButton('Device Setting', self.basic_netsetting_tbl))
        self._submenu_net_setting.add_choice(MenuButton('LAN Settings', self.basic_lansetting_tbl))

        self._submenu_wan_setting = MenuNode(self._top, 'Cellular WAN Settings')
        self._submenu_wan_setting.add_choice(MenuButton('Priority Configuration', self.cell_prioconfig_tbl))
        self._submenu_wan_setting.add_choice(MenuButton('SIM1 Confiuration', self.cell_sim1cfg_tbl))
        self._submenu_wan_setting.add_choice(MenuButton('SIM2 Confiuration', self.cell_sim2cfg_tbl))

        self._submenu_dhcp_server = MenuNode(self._top, 'DHCP Server')
        self._submenu_dhcp_server.add_choice(MenuButton('DHCP Server', self.basic_dhcp_setting_tbl))
        self._submenu_dhcp_server.add_choice(MenuButton('Static DHCP Mapping', self.basic_dhcp_map_setting_tbl))

        self._submenu_port_forward = MenuButton(' + Port forwarding', self.basic_port_forward_setting_tbl)

        self._submenu_basicsetting = MenuNode(self._top, 'Basic Settings')
        self._submenu_basicsetting.add_choice(self._submenu_net_setting)
        self._submenu_basicsetting.add_choice(self._submenu_wan_setting)
        self._submenu_basicsetting.add_choice(self._submenu_dhcp_server)
        self._submenu_basicsetting.add_choice(self._submenu_port_forward)

        self._submenu_serial_setting = MenuNode(self._top, 'Serial Settings')
        self._submenu_serial_setting.add_choice(MenuButton('Comport Settings', self.advanced_comsetting_tbl))

        self._submenu_advancedsetting = MenuNode(self._top, 'Advanced Settings')
        self._submenu_advancedsetting.add_choice(self._submenu_serial_setting)

        self.mainmenu.add_submenu(self._submenu_basicsetting)
        self.mainmenu.add_submenu(self._submenu_advancedsetting)
        self.mainmenu.add_submenu(urwid.Divider())
        self.mainmenu.add_submenu(MenuButton(' > Reset to Default', self._reset_to_default))
        self.mainmenu.add_submenu(MenuButton(' > Save', self._save_to_reset))

    def run(self):
        self.mainmenu.run()
        self.mainmenu.stop()

    def _reset_to_default(self, button):
        self._model.update_act('reset_to_default')
        urwid.ExitMainLoop()

        # result = os.system('/opt/mlis/web_console/reset_to_default.sh &')
        # if result is 0:
        #     os.system('/opt/mlis/web_console/reboot.sh &')
        #     time.sleep(1)
        #     self.mainmenu.stop()
        #     return "success"
        # else:
        #     return "error"

    def _save_to_reset(self, button):
        self._model.update_act('save_to_reset')
        urwid.ExitMainLoop()
        # os.system('/bin/cp -f /tmp/app.db /opt/mlis/web_console/app/app.db &')
        # result = os.system('/opt/mlis/web-update-all.sh &')
        # if result is 0:
        #     os.system('/opt/mlis/web_console/reboot.sh &')
        #     time.sleep(1)
        #     self.mainmenu.stop()
        #     return "success"
        # else:
        #     return "error"

    def ov_example_tbl(self, button):
        self._extbl = OverviewExampleTbl(self._model)
        self._top.open_box(self._extbl)

    def ov_laninfo_tbl(self, button):
        self._laninfotbl = OverviewLanInfoTbl(self._model)
        self._top.open_box(self._laninfotbl)

    def ov_cellinfo_tbl(self, button):
        self._cellinfotbl = OverviewCellInfoTbl(self._model)
        self._top.open_box(self._cellinfotbl)

    def ov_sysinfo_tbl(self, button):
        self._sysinfotbl = OverviewSysInfoTbl(self._model)
        self._top.open_box(self._sysinfotbl)

    def ov_monitor_tbl(self, button):
        pass

    def basic_netsetting_tbl(self, button):
        self._devicesettingtbl = BasicDeviceSettingTbl(model=self._model,
                                                       parent=self._top)
        self._top.open_box(self._devicesettingtbl)

    def basic_lansetting_tbl(self, button):
        self._lansettingtbl = BasicLanSettingTbl(self._model,
                                                 parent=self._top)
        self._top.open_box(self._lansettingtbl)

    def basic_dhcp_setting_tbl(self, button):
        self._dhcpsettingtbl = BasicDhcpSettingTbl(self._model,
                                                   parent=self._top)
        self._top.open_box(self._dhcpsettingtbl)

    def basic_dhcp_map_setting_tbl(self, button):
        self._dhcpmappingtbl = BasicDhcpMappingTbl(self._model,
                                                   parent=self._top)
        self._top.open_box(self._dhcpmappingtbl)

    def basic_port_forward_setting_tbl(self, button):
        self._portforwardtbl = BasicPortForwardTbl(self._model,
                                                   parent=self._top)
        self._top.open_box(self._portforwardtbl)

    def cell_prioconfig_tbl(self, button):
        self._proiconfigtbl = CellPrioConfigTbl(self._model,
                                                parent=self._top)
        self._top.open_box(self._proiconfigtbl)

    def cell_sim1cfg_tbl(self, button):
        self._sim1cfg_tbl = CellSIM_X_ConfigTbl(self._model, simindx=1,
                                                parent=self._top)
        self._top.open_box(self._sim1cfg_tbl)

    def cell_sim2cfg_tbl(self, button):
        self._sim2cfg_tbl = CellSIM_X_ConfigTbl(self._model, simindx=2,
                                                parent=self._top)
        self._top.open_box(self._sim2cfg_tbl)

    def advanced_comsetting_tbl(self, button):
        self._comsetting_tbl = AdvancedSerialPortSettingTbl(self._model,
                                                parent=self._top)
        self._top.open_box(self._comsetting_tbl)


class MlisConsole(object):
    """docstring for MlisConsole"""
    def __init__(self, arg):
        super(MlisConsole, self).__init__()
        self.arg = arg

        self.model = MlisConsoleModel(arg)
        self.model.get_sysinfo()
        self.model.get_cellinfo()
        self.model.get_laninfo()
        self.model.get_lansetting()
        self.model.get_priosetting()
        self.model.get_wansetting()
        self.model.set_devicesetting()
        self.model.get_comsetting()
        self.model.get_dhcpserver()
        self.model.get_dhcpmapping()
        self.model.set_dhcpmapping()
        self.model.get_portforward()
        self.model.set_portforward()

        self.view = MlisConsoleView(arg, self.model)

    def run(self):
        self.view.run()


def main(argv=None):
    argv = sys.argv[1:]
    if argv is None:
        print "user input args: "
        print argv

    app = MlisConsole(argv)
    app.run()


if __name__ == '__main__':
    main()
