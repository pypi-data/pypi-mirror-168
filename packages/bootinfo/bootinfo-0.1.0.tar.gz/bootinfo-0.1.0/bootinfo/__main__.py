import argparse
import sys
from bootinfo.signature import signatures
from bootinfo.block import get_all_blockdevs, check_boot_part_enabled


def wipeboot():
    parser = argparse.ArgumentParser(description="Bootloader detection and clean tool")
    parser.add_argument('blockdev', help='Block device to check/clean')
    parser.add_argument('--all', '-a', action='store_true',
                        help='Clean all found signatures')
    parser.add_argument('--invert', '-i', action='store_true', help='Invert the found signatures (reversable)')
    args = parser.parse_args()

    found = 0
    for sig in signatures:
        if sig.check(args.blockdev):
            found += 1
            inv = ''
            if sig.found_inv:
                inv = ' (inverted)'
            print("Found '{}' on {} offset {}B{}".format(sig.label, args.blockdev, sig.offset, inv))

    if found == 0:
        print("No known signature found on {}".format(args.blockdev))
    if args.all and found > 0:
        op = 'invert' if args.invert else 'wipe'
        print("Do you want to {} the {} sectors "
              "containing boot signatures?".format(op, found))
        print("Enter to continue, ctrl+c to abort")
        input()

        for sig in signatures:
            if sig.check(args.blockdev):
                if args.invert:
                    sig.wipe_reversable(args.blockdev)
                    print('Inverted {} ({})'.format(sig.offset, sig.label))
                else:
                    sig.wipe(args.blockdev)
                    print('Wiped {} ({})'.format(sig.offset, sig.label))


def bootinfo():
    parser = argparse.ArgumentParser(description="Bootloader information tool")
    parser.add_argument('--verbose', '-v', help='Show verbose info', action='store_true')
    parser.add_argument('--any', help="Check if there's any bootloader and exit 0", action='store_true')
    args = parser.parse_args()

    found = 0
    for blockdev in sorted(get_all_blockdevs()):
        devtype = 'mmc'
        if 'boot' in blockdev:
            devtype = 'mmcboot'
        elif 'mtd' in blockdev:
            devtype = 'spi'

        if args.verbose:
            sys.stderr.write(f"checking {blockdev} ({devtype})\n")

        for sig in signatures:
            if sig.check(blockdev, devtype=devtype):
                found += 1
                inv = ''
                if sig.found_inv:
                    inv = ' (inverted)'
                print("Found '{}' on {} offset {}B{}".format(sig.label, blockdev, sig.offset, inv))
                if sig.checkboot:
                    bootable = check_boot_part_enabled(blockdev)
                    if bootable is None:
                        print("    cannot check mmcboot status without mmc-utils")
                    elif bootable:
                        print(f"    {blockdev} is marked bootable")
                    else:
                        print(f"    {blockdev} is not marked bootable!")

    if found == 0:
        print("No valid bootloaders found")

    if args.any:
        if found > 0:
            exit(0)
        else:
            exit(1)


if __name__ == '__main__':
    bootinfo()
