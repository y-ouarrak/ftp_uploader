import os
import ftplib
from os import path
from time import sleep
from datetime import datetime

# Check if directory exists (in current location)


def directory_exists(session, dir):
    filelist = []
    session.retrlines('LIST', filelist.append)
    for f in filelist:
        if f.split()[-1] == dir and f.upper().startswith('D'):
            return True
    return False


def file_exists(session, filename):
    filelist = session.nlst()
    print(filelist)
    print(filename)
    for file in filelist:
        if file == filename:
            return True
    return False


while True:
    try:
        _path = './data'
        files = os.listdir(_path)

        if len(files) == 0:
            sleep(10)
            print("passed")
            continue
        session = ftplib.FTP('34.136.86.238', 'camera', 'camera')
        prefix = datetime.now().strftime("%d_%m_%Y")
        if directory_exists(session, prefix) is False:
            session.mkd(prefix)
        session.cwd(prefix)
        for file in files:
            path_tmp = path.join(_path, file)
            tmp = open(path_tmp, 'rb')         # file to send
            # send the file
            session.storbinary(f'STOR {file}', tmp)
            tmp.close()                                    # close file and FTP
            if file_exists(session, file):
                os.remove(path_tmp)
        session.quit()
    except Exception as ex:
        print(ex)
    sleep(20)
