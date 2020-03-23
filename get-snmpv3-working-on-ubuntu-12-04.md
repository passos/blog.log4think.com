---
title: Get SNMP(v3) working on Ubuntu 12.04
date: '2013-11-04 10:44:25 +0800'
---

# 2013-11-04  Get SNMP\(v3\) working on Ubuntu 12.04

I am running an Ubuntu 12.04 as working environment on my local machine. Ubuntu 12.04 is latest LTS \(Long Term Support\) version so that it's a good choice for a server. I need to install SNMP on my machine recently and I install it by following command

```text
sudo apt-get install snmpd snmp
```

However it seems doesn't work. After checking the system log, I found the following errors in `/var/log/syslog`

```text
 snmpd[8461]: /etc/snmp/snmpd.conf: line 90: Error: Already have an entry for this process.
 snmpd[8461]: /etc/snmp/snmpd.conf: line 92: Error: Already have an entry for this process.
 snmpd[8461]: /etc/snmp/snmpd.conf: line 94: Error: Already have an entry for this process.
 snmpd[8461]: /etc/snmp/snmpd.conf: line 106: Error: includeAllDisks already specified.
 snmpd[8461]: /etc/snmp/snmpd.conf: line 106: Error: #011ignoring: includeAllDisks 10%
 snmpd[8461]: error on subcontainer '' insert (-1)
 snmpd[8461]: error on subcontainer '' insert (-1)
 snmpd[8461]: /etc/snmp/snmpd.conf: line 146: Error: duplicate trigger name
 snmpd[8461]: error on subcontainer '' insert (-1)
 snmpd[8461]: error on subcontainer '' insert (-1)
 snmpd[8461]: /etc/snmp/snmpd.conf: line 146: Error: duplicate trigger name
 snmpd[8461]: error on subcontainer '' insert (-1)
 snmpd[8461]: error on subcontainer '' insert (-1)
 snmpd[8461]: /etc/snmp/snmpd.conf: line 146: Error: duplicate trigger name
 snmpd[8461]: error on subcontainer '' insert (-1)
 snmpd[8461]: error on subcontainer '' insert (-1)
 snmpd[8461]: /etc/snmp/snmpd.conf: line 146: Error: duplicate trigger name
 snmpd[8461]: error on subcontainer '' insert (-1)
 snmpd[8461]: error on subcontainer '' insert (-1)
 snmpd[8461]: /etc/snmp/snmpd.conf: line 146: Error: duplicate trigger name
 snmpd[8461]: error on subcontainer '' insert (-1)
 snmpd[8461]: error on subcontainer '' insert (-1)
 snmpd[8461]: /etc/snmp/snmpd.conf: line 146: Error: duplicate trigger name
 snmpd[8461]: error on subcontainer '' insert (-1)
 snmpd[8461]: /etc/snmp/snmpd.conf: line 146: Error: duplicate trigger name
 snmpd[8461]: /etc/snmp/snmpd.conf: line 148: Error: duplicate trigger name
 snmpd[8461]: /etc/snmp/snmpd.conf: line 148: Error: duplicate trigger name
 snmpd[8461]: duplicate table data attempted to be entered. row exists
 snmpd[8461]: Failed to register extend entry 'test1' - possibly duplicate name.
 snmpd[8461]: duplicate table data attempted to be entered. row exists
 snmpd[8461]: Failed to register extend entry 'test2' - possibly duplicate name.
 snmpd[8461]: Turning on AgentX master support.
 snmpd[8461]: Error opening specified endpoint "udp:127.0.0.1:161"
 snmpd[8461]: Server Exiting with code 1
```

The content of `/etc/snmp/snmpd.conf` is like

```text
 89                                # At least one  'mountd' process
 90 proc  mountd
 91                                # No more than 4 'ntalkd' processes - 0 is OK
 92 proc  ntalkd    4
 93                                # At least one 'sendmail' process, but no more than 10
 94 proc  sendmail 10 1
 95
 96 #  Walk the UCD-SNMP-MIB::prTable to see the resulting output
 97 #  Note that this table will be empty if there are no "proc" entries in the snmpd.conf file
 98
 99
100 #
101 #  Disk Monitoring
102 #
103                                # 10MBs required on root disk, 5% free on /var, 10% free on all other disks
104 disk       /     10000
105 disk       /var  5%
106 includeAllDisks  10%

145                                    # generate traps on UCD error conditions
146 defaultMonitors          yes
147                                    # generate traps on linkUp/Down
148 linkUpDownNotifications  yes
149
150
```

So let's fix the problem. I comment the snmpd.conf configurations appeared in syslog, then use command `cat /etc/snmp/snmpd.conf | grep -v '#' | grep -v '^\s*$'` to get a clean version.

```text
view   systemonly  included   .1.3.6.1.2.1.1
view   systemonly  included   .1.3.6.1.2.1.25.1
rocommunity public  default    -V systemonly
rouser   authOnlyUser
sysLocation    Sitting on the Dock of the Bay
sysContact     Me <me@example.org>
sysServices    72
disk       /     10000
disk       /var  5%
load   12 10 5
trapsink     localhost public
iquerySecName   internalUser
rouser          internalUser
master          agentx
createUser testuser MD5 "testpasswd"
rouser testuser auth
```

After updated `/etc/snmpd/snmpd.conf` and `/etc/init.d/snmpd restart`, now it's working.

```text
$ snmpwalk -v 3 -l authNoPriv -a MD5 -u testuser -A testpasswd 127.0.0.1:161 sysDescr
SNMPv2-MIB::sysDescr.0 = STRING: Linux simon-desktop 3.9.3-generic #19-Ubuntu SMP Wed Oct 9 16:20:46 UTC 2013 x86_64
```

BTW, The [i3](http://i3wm.org) is the best tiling window manager I have ever used.

