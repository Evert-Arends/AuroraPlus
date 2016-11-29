import datetime

json_obj = {"RequestDetails": {"Connection": {"SSL": "Yes", "LAN IPAddress": "192.168.188.55"},
                               "Time": {"RequestSent": "2016-11-29 22:17:41.100349"}},
            "Server": {"Action": {"Register": "True"},
                       "ServerDetails": {"NetworkLoad": {"Received": 4628, "Sent": 4554}, "ServerName": "berm-pc",
                                         "CPU_Usage": 38.7, "ServerKey": "Lqdie4ARBhbJtawrmTBCkenmhb9rvqgRzWN"}}}, {
               "RequestDetails": {"Connection": {"SSL": "Yes", "LAN IPAddress": "192.168.188.55"},
                                  "Time": {"RequestSent": "2016-11-29 22:17:41.100349"}},
               "Server": {"Action": {"Register": "True"},
                          "ServerDetails": {"NetworkLoad": {"Received": 4628, "Sent": 4554}, "ServerName": "berm-pc",
                                            "CPU_Usage": 38.7, "ServerKey": "Lqdie4ARBhbJtawrmTBCkenmhb9rvqgRzWN"}}}, {
               "RequestDetails": {"Connection": {"SSL": "Yes", "LAN IPAddress": "192.168.188.55"},
                                  "Time": {"RequestSent": "2016-11-29 22:17:41.100349"}},
               "Server": {"Action": {"Register": "True"},
                          "ServerDetails": {"NetworkLoad": {"Received": 4628, "Sent": 4554}, "ServerName": "berm-pc",
                                            "CPU_Usage": 38.7, "ServerKey": "Lqdie4ARBhbJtawrmTBCkenmhb9rvqgRzWN"}}}, {
               "RequestDetails": {"Connection": {"SSL": "Yes", "LAN IPAddress": "192.168.188.55"},
                                  "Time": {"RequestSent": "2016-11-29 22:17:41.100349"}},
               "Server": {"Action": {"Register": "True"},
                          "ServerDetails": {"NetworkLoad": {"Received": 4628, "Sent": 4554}, "ServerName": "berm-pc",
                                            "CPU_Usage": 38.7, "ServerKey": "Lqdie4ARBhbJtawrmTBCkenmhb9rvqgRzWN"}}}, {
               "RequestDetails": {"Connection": {"SSL": "Yes", "LAN IPAddress": "192.168.188.55"},
                                  "Time": {"RequestSent": "2016-11-29 22:17:41.100349"}},
               "Server": {"Action": {"Register": "True"},
                          "ServerDetails": {"NetworkLoad": {"Received": 4628, "Sent": 4554}, "ServerName": "berm-pc",
                                            "CPU_Usage": 38.7, "ServerKey": "Lqdie4ARBhbJtawrmTBCkenmhb9rvqgRzWN"}}}

Range = 3000
for item in json_obj:
    test1 = item['RequestDetails']['Time']['RequestSent']


time = 60
date_now = datetime.datetime.now()
old_date = date_now - datetime.timedelta(seconds=time)
test = ('old_date: %s new_date: %s' % (old_date, date_now))
print(test)


