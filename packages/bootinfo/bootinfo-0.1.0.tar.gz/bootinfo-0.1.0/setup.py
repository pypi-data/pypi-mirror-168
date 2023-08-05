from setuptools import setup

setup(
    name='bootinfo',
    version='0.1.0',
    packages=['bootinfo'],
    url='https://git.sr.ht/~martijnbraam/bootinfo',
    license='GPL3',
    author='Martijn Braam',
    author_email='martijn@brixit.nl',
    description='Detect ARM boot signatures on storage devices',
    long_description=open("README.md").read(),
    long_description_content_type='text/markdown',
    entry_points={
        'console_scripts': [
            'bootinfo = bootinfo.__main__:bootinfo',
            'wipeboot = bootinfo.__main__:wipeboot',
        ],
    },
)
