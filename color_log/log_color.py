from datetime import datetime


def log_info(string):
    print(Colors.GREEN + str(string) + " \t\tTime: " + str(datetime.now()) + Colors.END)


def log_verbose(string):
    print(Colors.BLUE + str(string) + " \t\tTime: " + str(datetime.now()) + Colors.END)


def log_error(string):
    print(Colors.FAIL + str(string) + " \t\tTime: " + str(datetime.now()) + Colors.END)


def log_start(string):
    print(Colors.HEADER + str(string) + " \t\tTime: " + str(datetime.now()) + Colors.END)


def log_warning(string):
    print(Colors.WARNING + str(string) + " \t\tTime: " + str(datetime.now()) + Colors.END)


class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    END = '\033[0m'

    def disable(self):
        self.HEADER = ''
        self.BLUE = ''
        self.GREEN = ''
        self.WARNING = ''
        self.FAIL = ''
        self.END = ''
