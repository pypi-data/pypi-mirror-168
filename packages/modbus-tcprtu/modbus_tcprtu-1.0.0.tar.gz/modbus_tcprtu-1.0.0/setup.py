from setuptools import setup
import os, io
from modbus_tcprtu import __version__

here = os.path.abspath(os.path.dirname(__file__))
README = io.open(os.path.join(here, 'README.md'), encoding='UTF-8').read()
CHANGES = io.open(os.path.join(here, 'CHANGES.md'), encoding='UTF-8').read()
setup(name="modbus_tcprtu",
      version=__version__,
      keywords=('modbus', 'modbus_tk', 'modbus_tcp', 'modbus_rtu'),
      description="A ModbusRTU Over TCP/IP library, depends on modbus_tk.",
      long_description=README + '\n\n\n' + CHANGES,
      long_description_content_type="text/markdown",
      url='https://github.com/sintrb/modbus_tcprtu/',
      author="trb",
      author_email="sintrb@gmail.com",
      packages=['modbus_tcprtu'],
      install_requires=['modbus_tk'],
      zip_safe=False
      )
