# python setup.py build
# you will need cx_Freeze installed before compiling
# pip install cx_Freeze
# https://anthony-tuininga.github.io/cx_Freeze/

from cx_Freeze import setup, Executable

build_exe_options = {"packages": ["socket", "threading", "sys"]}

setup(name='client',
      version="0.1",
      description="py chat client",
      options={"build_exe": build_exe_options},
      executables=[Executable("client.py")])

setup(name='server',
      version="0.1",
      description="py chat server",
      options={"build_exe": build_exe_options},
      executables=[Executable("server.py")])
