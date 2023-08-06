import re
import sys

try:
    from api.command import command
except Exception as e:
    from src.api.command import command

def main():
    '''
    call command
    '''
    sys.argv[0] = re.sub(r"(-script\.pyw?|\.exe)?$", "", sys.argv[0])
    sys.exit(command())

if __name__ == "__main__":
    main()
