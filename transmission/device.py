class Device:
    '''Description for each encountered device'''
    _name = ''
    _mac = '00:00:00:00:00:00'
    _ips = set()
    _tss = []
    _max_tss = 42
    _priority = 0

    def __init__(self, name='', mac=''):
        self._name = name
        self._mac = mac
        self._ips = set()
        self._tss = []
        self._max_tss = 42
        self._priority = 0

    def set_name(self, name):
        self._name = name

    def set_mac(self, mac):
        self._mac = mac

    def set_priority(self, p):
        self._priority = p

    def add_ip(self, ip):
        self._ips.add(str(ip))

    def add_ts(self,time_stamp):
        self._tss.append(str(time_stamp))
        if len(self._tss) > self._max_tss:
            # avoid storing an endless amount of time stamps to stop that status/log file from growing
            self._tss = self._tss[1:]

    def is_mac(self,mac):
        return (mac == self._mac)

    def had_ip(self,ip):
        return (ip in self._ips)

    def occurance_count(self):
        return len(self._tss)

    def to_string(self):
        main_string = self._name + ";" + self._mac + ";" + str(self._priority) + ";"
        ip_string = ",".join(self._ips)
        ts_string = ",".join(self._tss)
        main_string += ip_string + ";" + ts_string
        return main_string

    def from_string(self, s):
        main_components = s.rstrip('\n').split(';')
        if len(main_components) != 5:
            print("Could not load device info",s)
            return

        index = 0

        self.set_name(main_components[index])
        index += 1
        self.set_mac(main_components[index])
        index += 1
        self.set_priority(int(main_components[index]))
        index += 1
        ips = main_components[index].split(',')
        for ip in ips:
            self.add_ip(ip)
        index += 1
        tss = main_components[index].split(',')
        for ts in tss:
            self.add_ts(ts)

    def last_seen(self):
        return self._tss[-1]

    def time_since_last_occurance(self):
        import datetime
        cur_time = datetime.datetime.now()
        last_log = self.last_seen()
        last_log_time = datetime.datetime.strptime(last_log,"%Y-%m-%d %H:%M:%S.%f") #2016-02-05 11:22:35.848370

        diff_time = cur_time - last_log_time
        return diff_time
