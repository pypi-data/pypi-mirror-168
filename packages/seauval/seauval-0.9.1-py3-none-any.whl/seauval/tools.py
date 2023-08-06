import io
import sys
import tarfile


def prompt(msg, options):
    """
    Send a message to the user and wait for him to choose among the given options
    """
    while True:
        print(msg)
        print(" ", end='')
        print("> ", end='')
        sys.stdout.flush()
        answer = sys.stdin.readline().strip().lower()
        if answer in options:
            return answer
        print("You should answer one of the following: {:}".format(options))


def question(text):
    """
    Ask a 'yes' or 'no' question to the user and returns true if answer was yes
    """
    return prompt(text, ['y', 'n']) == 'y'


def freeTextQuestion(msg):
    print(msg)
    print("> ", end='')
    sys.stdout.flush()
    return sys.stdin.readline().strip()


def askFloat(msg):
    print(msg)
    while True:
        print("> ", end='')
        sys.stdout.flush()
        try:
            return float(sys.stdin.readline().strip().lower())
        except ValueError as e:
            print("Not a valid number " + str(e))


def tarOpenUTF8Proof(path):
    """
    Open a utf8 file and returns the associated tarfile.TarFile while
    supporting utf8 encoding in paths
    """
    # from: https://issue.life/questions/57723988
    with open(path, 'rb') as f:
        return tarfile.open(fileobj=io.BytesIO(f.read()), mode='r')
