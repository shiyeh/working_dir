# import os
import sqlite3
import pdb

lan_setting = {
        'IP address': 'ip_addr',
        'Subnet mask': 'submask',
        'Primary DNS server': 'dns',
        'Secondary DNS server': 'sec_dns',
}
sim_config = {
        'APN': 'apn',
        'PIN': 'pin',
        'Authentication Protocal': 'auth',
        'Username': 'username',
        'Password': 'password',
}
 
db_index = {
    'table_index': {
        'Network Settings': 'lan_setting',
        'Cellular WAN Settings': 'wan_setting',
        'SIM1 Confiuration': 'wan_setting',
        'SIM2 Confiuration': 'wan_setting',
        'DHCP Server (AP only)': '',
    },
    'Network Settings': lan_setting,
    'SIM1 Confiuration': sim_config,
    'SIM2 Confiuration': sim_config,
}

# if os.path.exists('/tmp/app.db')
    
class database(object):
    def __init__(self):
        self.db = sqlite3.connect('/tmp/app.db')
        self.cur = self.db.cursor()

    def get_setting(self, index):
        table = db_index['table_index'][index]
        self.cur.execute("PRAGMA table_info({})".format(table))
        value = self.cur.fetchall()
        columns = [i[1] for i in value]

        self.cur.execute("SELECT * FROM {};".format(table))
        value = self.cur.fetchall()
        data = []
        for item in value:
            dic = {}
            for i in range(len(item)):
                dic[columns[i]] = item[i]
            data.append(dic)
        return data
        #while True:
        #    value = self.cur.fetchone()
        #    if not value:
        #        break
        #    for i in range(len(columns)):
        #        dic[columns[i]] = value[i]
        #print(dic)

        # for row in data:
        #     dic['ip_addr'] = row[1]
        #     dic['submask'] = row[2]
        #     dic['dns'] = row[3]
        #     dic['sec_dns'] = row[4]
        # return dic

    def set_setting(self, index, dic):
        table = db_index['table_index'][index]
        _id = dic.pop('id')
        for key in dic:
            self.db.execute("UPDATE {} set {} ='{}' where id={_id};".format(
                    table, key, dic.get(key), _id=_id))
        self.db.commit()
            

if __name__ == "__main__":
    db = database()
    lan = db.lan_setting()
    for keys in lan:
        print(keys)
    pdb.set_trace()
    print('last')
