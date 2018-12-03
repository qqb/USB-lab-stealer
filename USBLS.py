import time
from pathlib import Path
import shutil

import psutil


def file_search(path):
    p = Path(path)
    types = ('*.docx', '*.docx', '*.pptx', '*.ppt', '*.xmcd')
    files_grabbed = []
    for file_type in types:
        files_grabbed.extend(list(p.rglob(file_type)))
    return files_grabbed


def copy_files(files):
    p = Path('lab')
    for file in files:
        shutil.copy2(str(file), p / file.name)


def enumerate_serial_devices():
    return set([item.device for item in psutil.disk_partitions() if 'removable' in item.opts])


def check_new_devices(old_devices):
    devices = enumerate_serial_devices()
    added = devices.difference(old_devices)
    removed = old_devices.difference(devices)
    if added:
        print('added: {}'.format(added))
        for path in added:
            files = file_search(path)
            copy_files(files)
    if removed:
        print('removed: {}'.format(removed))
    return devices


if __name__ == '__main__':
    old_devices = enumerate_serial_devices()
    while True:
        old_devices = check_new_devices(old_devices)
        time.sleep(0.5)
