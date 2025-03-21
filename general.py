import pickle

class Banned:
    def __init__(self, filename='banned.pkl'):
        self.filename = filename
        self.banned_ips = self.load_banned_ips()

    def load_banned_ips(self):
        try:
            with open(self.filename, 'rb') as f:
                return pickle.load(f)
        except (FileNotFoundError, EOFError):
            return {}

    def save_banned_ips(self):
        with open(self.filename, 'wb') as f:
            pickle.dump(self.banned_ips, f)

    def add_banned_ip(self, ip):
        self.banned_ips[ip] = True
        self.save_banned_ips()

    def check_if_banned_ip(self, ip):
        return self.banned_ips.get(ip, False)


