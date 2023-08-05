import pathlib

import bootinfo.signature as signature

testset = [
    ['allwinner/mmc.a64.img', ['Sunxi/Allwinner eGON header']],
    ['allwinner/mmcboot.a64.img', ['Sunxi/Allwinner eGON header mmcboot']],
    ['allwinner/mmcfar.a64.img', ['Sunxi/Allwinner eGON header far']],
    ['rockchip/mmc.rk3399.img', ['RK3399 boot header']],
    ['rockchip/spi.rk3399.img', ['RK3399 boot header SPI']],
]


def test_check():
    basedir = pathlib.Path(__file__).parent.resolve()

    for case in testset:
        path = basedir / 'fixtures' / case[0]
        results = []
        for sig in signature.signatures:
            if sig.check(str(path)):
                results.append(sig.label)
        assert results == case[1]


def test_wipe_reverseable(tmp_path):
    basedir = pathlib.Path(__file__).parent.resolve()
    for case in testset:
        testfile = basedir / 'fixtures' / case[0]

        with open(testfile, 'rb') as handle:
            original = handle.read()

        # Create working copy of the test file
        d = tmp_path
        d.mkdir(exist_ok=True)

        changefile = d / 'test.img'
        with open(changefile, 'wb') as handle:
            handle.write(original)

        # Find signature for the test file
        for sig in signature.signatures:
            if sig.check(changefile):
                break
        else:
            assert 0

        # Use the reversable wipe
        sig.wipe_reversable(changefile)

        # Find the signature again on the wiped file
        for sig in signature.signatures:
            if sig.check(changefile):
                break
        else:
            assert False

        # Check if the wiped signature was there
        assert sig.found_inv

        # Wipe again to place back the original signature
        sig.wipe_reversable(changefile)

        # Check if the file is identical to the original now
        with open(changefile, 'rb') as handle:
            roundtripped = handle.read()

        assert roundtripped == original
