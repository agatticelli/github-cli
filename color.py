HEADER = '\033[95m'
OKBLUE = '\033[94m'
OKGREEN = '\033[92m'
WARNING = '\033[93m'
FAIL = '\033[91m'
ENDC = '\033[0m'
BOLD = '\033[1m'
UNDERLINE = '\033[4m'

def pRed(msg, **kwargs):
    print(FAIL + msg + ENDC, **kwargs)

def pGreen(msg, **kwargs):
    print(OKGREEN + msg + ENDC, **kwargs)

def pBlue(msg, **kwargs):
    print(OKBLUE + msg + ENDC, **kwargs)

