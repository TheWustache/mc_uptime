import os.path
import os



def user_exists(username):
    """Checks whether user exists. Returns True if yes, False otherwise"""
    # users are implicitly listed in file names
    # TODO: make directory with users configurable
    files = os.listdir(os.path.join(os.curdir, 'data'))
    if files:
        for user in files:
            if (username + '.json') == user:
                return True
    return False

if __name__ == '__main__':
    import sys
    if len(sys.argv) >= 2:
        if user_exists(sys.argv[1]):
            print(sys.argv[1] + " exists!")
        else:
            print(sys.argv[1] + " does not exist!")
