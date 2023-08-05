import os


class Signature:
    def __init__(self, label, offset, magic, size=512, only=None, checkboot=False):
        self.label = label
        self.offset = offset
        self.size = size
        self.magic = magic
        self.only = only
        self.checkboot = checkboot
        self.found_offset = None
        self.found_length = None
        self.found_inv = False

        self.magic_inv = b''
        for b in magic:
            self.magic_inv += (b ^ 0xff).to_bytes(1, byteorder='little')

    def check(self, device, devtype=None):
        if devtype is not None and self.only is not None:
            if devtype != self.only:
                # Ignore a signature on the wrong storage medium to avoid false positive of badly flashed setups
                return False

        mmc = os.open(device, os.O_RDONLY)
        os.lseek(mmc, self.offset, os.SEEK_SET)
        data = os.read(mmc, self.size)
        os.close(mmc)
        found = data.find(self.magic)
        if found == -1:
            found = data.find(self.magic_inv)
            if found > -1:
                self.found_inv = True
        self.found_offset = found
        self.found_length = len(self.magic)
        return found > -1

    def wipe(self, device):
        # wipe the boot header by erasing the magic
        mmc = os.open(device, os.O_RDWR)
        os.lseek(mmc, self.offset, os.SEEK_SET)
        os.write(mmc, b'\0' * self.size)
        os.close(mmc)

    def wipe_reversable(self, device):
        # wipe the boot header by inverting the bits of the magic

        # Sanity check, and generate offsets
        if not self.check(device):
            raise RuntimeError("Cannot wipe signature that was not detected")

        # Replace magic with inverted magic
        mmc = os.open(device, os.O_RDWR)
        os.lseek(mmc, self.offset + self.found_offset, os.SEEK_SET)
        if self.found_inv:
            # The disk currently contains the wiped magic, fix the magic to enable
            os.write(mmc, self.magic)
        else:
            # Write the inverted magic to the correct spot
            os.write(mmc, self.magic_inv)
        os.close(mmc)


signatures = [
    Signature('Sunxi/Allwinner eGON header', 16 * 512, b'eGON.BT0', only='mmc'),
    Signature('Sunxi/Allwinner eGON header mmcboot', 0, b'eGON.BT0', only='mmcboot', checkboot=True),
    Signature('Sunxi/Allwinner eGON header far', 256 * 512, b'eGON.BT0', only='mmc'),
    Signature('RK3399 boot header', 64 * 512, b'\x3b\x8c\xdc\xfc', size=4),
    Signature('RK3399 boot header SPI', 0, b'\x3b\x8c\xdc\xfc', size=4),
    Signature('Amlogic boot header', 512, b'@AML', size=32, only='mmc'),
    Signature('Amlogic boot header SPI', 0, b'@AML', size=32, only='spi'),
]
