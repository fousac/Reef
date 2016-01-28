#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys    
import sqlite3 as sqlite

sys.path.insert(0, '/usr/lib/python2.7/bridge/') 
from bridgeclient import BridgeClient as bridgeclient
                                                    
value = bridgeclient()                                                                                                          

con = sqlite.connect('/mnt/sd/arduino/db/reef.db')
cur = con.cursor()
cur.execute('INSERT INTO teplota_log (teplota) VALUES(?)', (value.get('teplota'),))
con.commit()
con.close()