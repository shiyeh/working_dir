#!/usr/bin/env python
#import pdb

class db_confirm(object):
    def __init__(self):
        self.D = {
                   'cellular': self.cellular,
                   'system_info': self.systemInfo,
                   'lan_info': self.lanInfo,
                   'cellular_info': self.cellularInfo,
                   'io_status': self.ioStatus,
                   'user': self.user,
                   'lan_setting': self.lanSetting,
                   'wan_priority_setting': self.wanPrioritySetting,
                   'wan_setting': self.wanSetting,
                   'dhcp_server': self.dhcpServer,
                   'port_forwarding': self.portForwarding,
                   'vpn_active': self.vpnActive,
                   'vpn': self.vpn,
                   'ca_cert': self.caCert,
                   'ee_cert': self.eeCert,
                   'openvpn': self.openvpn,
                   'com_setting': self.comSetting,
                   'snmp_agent': self.snmpAgent,
                   'service_setting': self.serviceSetting,
                 }

    def isInIntList(self, target, _list):
        try:
            if not int(target) in _list:
                return False
            return True
        except:
            return False

    def isBool(self, _bool):
        try:
            if not 0 <= int(_bool) <= 1:
                return False
            return True
        except:
            return False

    def isInt(self, _int):
        try:
            if not isinstance(int(_int), int):
                return False
            return True
        except:
            return False

    def isInRange(self, _min, target, _max):
        try:
            if not _min <= int(target) <= _max:
                return False
            return True
        except:
            return False

    def isIP(self, address):
        try:
            if address == '':
                return True
            parts = address.split(".")
            if len(parts) != 4:
                return False
            for item in parts:
                if not 0 <= int(item) <= 255:
                    return False
            return True
        except:
            return False

    def isPort(self, port):
        try:
            if port == '':
                return True
            if not 1 <= int(port) <= 65535:
                return False
            return True
        except:
            return False

    def cellular(self):
        _bool = True
        for key, value in self.values.items():
            if key is 'ip_addr':
                _bool = _bool and self.isIP(value)
        return _bool

    def systemInfo(self):
        _bool = True
        for key, value in self.values.items():
            if key is '':
                _bool = _bool and self.isBool(value)
        return _bool

    def lanInfo(self):
        _bool = True
        ips = ['submask',
               'ip_addr']
        for key, value in self.values.items():
            if key in ips:
                _bool = _bool and self.isIP(value)
        return _bool

    def cellularInfo(self):
        _bool = True
        for key, value in self.values.items():
            if key is '':
                _bool = _bool and self.isBool(value)
        return _bool

    def ioStatus(self):
        _bool = True
        for key, value in self.values.items():
            if key is 'relay':
                _bool = _bool and self.isBool(value)
        return _bool

    def user(self):
        _bool = True
        for key, value in self.values.items():
            if key is '':
                _bool = _bool and self.isBool(value)
        return _bool

    def lanSetting(self):
        _bool = True
        ips = ['ip_addr',
               'dns',
               'sec_dns',
               'submask']
        for key, value in self.values.items():
            if key is 'dns' and value is '':
                self.values[key] = '8.8.8.8'
            elif key is 'sec_dns' and value is '':
                self.values[key] = '8.8.4.4'
            elif key is 'allow_ping':
                _bool = _bool and self.isBool(value)
            elif key is 'ping_intvl':
                _bool = _bool and self.isInt(value)
            elif key in ips:
                _bool = _bool and self.isIP(value)
        return _bool

    def wanPrioritySetting(self):
        _bool = True
        for key, value in self.values.items():
            if key is 'redundant':
                _bool = _bool and self.isBool(value)
            elif key is 'priority':
                _bool = _bool and self.isInRange(1, value, 2)
            elif key is 'reg_nw_timeout':
                _bool = _bool and self.isInt(value)
            elif key is 'term_redundant':
                _bool = _bool and self.isInt(value)
            elif key is 'data_session_retry':
                _bool = _bool and self.isInt(value)
        return _bool

    def wanSetting(self):
        auths = ['pap', 'chap']
        _bool = True
        for key, value in self.values.items():
            if key is 'auth' and value is not '':
                _bool = _bool and value in auths
            elif key is 'pin' and value is not '':
                _bool = _bool and self.isInt(value)
        return _bool

    def dhcpServer(self):
        _bool = True
        ips = ['start_ip',
               'dns',
               'gateway',
               'sec_dns',
               'submask']
        for key, value in self.values.items():
            if key is 'dhcp_server':
                _bool = _bool and self.isBool(value)
            elif key is 'client_time':
                _bool = _bool and self.isInRange(120, value, 864000)
            elif key is 'max_users':
                _bool = _bool and self.isInRange(1, value, 99)
            elif key in ips:
                _bool = _bool and self.isIP(value)
        return _bool

    def dhcpMapping(self):
        _bool = True
        for key, value in self.values.items():
            if key is 'active':
                _bool = _bool and self.isBool(value)
            elif key is 'ip':
                _bool = _bool and self.isIP(value)
        return _bool

    def portForwarding(self):
        _bool = True
        ports = ['internal_port',
                 'public_port']
        protocols = ['tcp',
                     'udp']
        for key, value in self.values.items():
            if key is 'active':
                _bool = _bool and self.isBool(value)
            elif key in ports:
                _bool = _bool and self.isPort(value)
            elif key is 'ip':
                _bool = _bool and self.isIP(value)
            elif key is 'protocol':
                _bool = _bool and value in protocols
        return _bool

    def vpnActive(self):
        _bool = True
        for key, value in self.values.items():
            if key is 'active':
                _bool = _bool and self.isBool(value)
        return _bool

    def vpn(self):
        _bool = True
        ips = ['_right',
               '_left']
        bools = ['startup_mode',
                 'ipsec']
        auth_modes = ['psk',
                      'pubkey']
        aggressives = ['no',
                       'yes']
        dpdactions = ['none',
                      'clear',
                      'hold',
                      'start']
        keyexchanges = ['ikev1',
                        'ikev2']
        rekeys = ['yes',
                  'no']
        for key, value in self.values.items():
            if key in bools:
                _bool = _bool and self.isBool(value)
            elif key is 'auth_mode':
                _bool = _bool and value in auth_modes
            elif key is 'aggressive':
                _bool = _bool and value in aggressives
            elif key is 'dpdaction':
                _bool = _bool and value in dpdactions
            elif key is 'keyexchange':
                _bool = _bool and value in keyexchanges
            elif key is 'rekey':
                _bool = _bool and value in rekeys
            elif key in ips:
                _bool = _bool and self.isIP(value)
        return _bool

    def caCert(self):
        _bool = True
        for key, value in self.values.items():
            if key is '':
                _bool = _bool and self.isBool(value)
            elif key is 'lifetime':
                _bool = _bool and self.isInt(value)
        return _bool

    def eeCert(self):
        _bool = True
        for key, value in self.values.items():
            if key is '':
                _bool = _bool and self.isBool(value)
            elif key is 'lifetime':
                _bool = _bool and self.isInt(value)
        return _bool

    def openvpn(self):
        _bool = True
        for key, value in self.values.items():
            if key is 'active':
                _bool = _bool and self.isBool(value)
        return _bool

    def comSetting(self):
        _bool = True
        baudRates = [ 1200,
                      2400,
                      4800,
                      9600,
                      19200,
                      38400,
                      57600,
                      115200,
                      230400 ]
        paritys = [ 'none', 'odd', 'even' ]
        stopBits = [ 1, 1.5, 2 ]
        transMode = [ 232, 422, 485 ]
        workMode = ['mccp', 'trans']

        for key, value in self.values.items():
            if key is 'baud_rate':
                _bool = _bool and self.isInIntList(value, baudRates)
            elif key is 'data_bits':
                _bool = _bool and self.isInRange(5, value, 8)
            elif key is 'ip_addr':
                _bool = _bool and self.isIP(value)
            elif key is 'parity':
                _bool = _bool and value in paritys
            elif key is 'port':
                _bool = _bool and self.isPort(value)
            elif key is 'stop_bits':
                _bool = _bool and self.isInIntList(value, stopBits)
            elif key is 'trans_mode':
                _bool = _bool and self.isInIntList(value, transMode)
            elif key is 'work_mode':
                _bool = _bool and value in workMode
            elif key is 'service_mode':
                _bool = _bool and self.isInRange(0, value, 2)
        return _bool

    def snmpAgent(self):
        _bool = True
        auth_protocols = [0, 1, 2]
        priv_protocols = [0, 1, 2]
        agent_vers = [1, 2, 3]
        for key, value in self.values.items():
            if key is 'active':
                _bool = _bool and self.isBool(value)
            elif key is 'auth_protocol':
                _bool = _bool and self.isInIntList(value, auth_protocols)
            elif key is 'priv_protocol':
                _bool = _bool and self.isInIntList(value, priv_protocols)
            elif key is 'agent_ver':
                _bool = _bool and self.isInIntList(value, agent_vers)
        return _bool

    def serviceSetting(self):
        _bool = True
        bools = ['lan_allow_http',
                 'lan_allow_https',
                 'lan_allow_ssh',
                 'wan_allow_http',
                 'wan_allow_https',
                 'wan_allow_ssh']
        for key, value in self.values.items():
            if key in bools:
                _bool = _bool and self.isBool(value)
        return _bool

    def confirm(self, payload):
        _bool = True
        self.values = payload.get('values')
        self.table = payload.get('table')

        for table, func in self.D.items():
            if self.table == table:
                _bool = func()

        payload['values'] = self.values
        return _bool, payload

if __name__ == '__main__':
    null = "";
    data = {"method": "set",
            "table": "com_setting",
            "id": 1,
            "values":  {
                   'baud_rate': 57600,
                   'data_bits': 7,
                   'parity': u'none',
                   'stop_bits': 1.5,
                   'work_mode': u'mccp'
               }
            }
    data2 = {"method": "set",
            "table": "lan_setting",
            "id": 1,
            "values":
                {
                  "sec_dns": "8.8.4.4",
                  "ip_addr": "10.0.10.1",
                  "ping_intvl": "50",
                  "dns": "8.8.8.8",
                  "submask": "255.255.255.0",
                  "allow_ping": 0,
                  "ping_addr": "8.8.8.88"
                }
            }

    db = db_confirm()
    import json
    print(json.dumps(db.confirm(data2), indent=2, sort_keys=True))
    del db

    #pdb.set_trace()
    #print('finish')
