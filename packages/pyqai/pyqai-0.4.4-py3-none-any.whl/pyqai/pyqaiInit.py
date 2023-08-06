import os
import json

def saveApitoken():
    homeDir = os.path.expanduser( '~' )
    print(homeDir)

    print("Please copy and paste the JSON you find at https://dev.pyqai.com/profile.\n And then hit Enter twice")

    lines = []
    while True:
        line = input()
        if line and line != '':
            lines.append(line)
        else:
            break

    apiToken = '\n'.join(lines)

    filename = homeDir+ "/pyqai.config"

    with open(filename, 'w') as f:
        f.write(apiToken)

    print(f"Successfully created {filename}.  You're all set to go with pyq!")

    return

def main():
    saveApitoken()