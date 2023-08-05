import glob
import os.path
import subprocess


def get_all_blockdevs():
    result = set()
    for blockdev in glob.glob('/sys/class/block/*'):
        # Skip block devices that are partitions
        if os.path.isfile(os.path.join(blockdev, 'partition')):
            continue

        # Skip devicemapper devices
        if os.path.isdir(os.path.join(blockdev, "dm")):
            continue

        # Skip empty
        sizefile = os.path.join(blockdev, 'size')
        if os.path.isfile(sizefile):
            with open(sizefile, 'r') as handle:
                sizeraw = handle.read()
            size = int(sizeraw.strip())
            if size == 0:
                continue

        result.add(blockdev.replace('/sys/class/block', '/dev'))
    return result


def check_boot_part_enabled(blockdev):
    block, bootpart = blockdev.split('boot')
    cmd = ['mmc', 'extcsd', 'read', block]
    try:
        process = subprocess.check_output(cmd)
    except subprocess.CalledProcessError:
        # mmc-utils missing or no permissions
        return None
    result = process.decode()
    return f'Boot Partition {bootpart} enabled' in result


if __name__ == '__main__':
    print(get_all_blockdevs())
