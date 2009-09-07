import os
from string import Template
import subprocess

import config


def substitute(data_dict):
    fd = open(os.path.join(config.path.data, 'Makefile.tpl'))
    data = fd.read()
    tpl = Template(data)
    fd.close()
    return tpl.safe_substitute(data_dict)

def makefile(pde_file):
    target_name, ext = os.path.basename(pde_file).rsplit('.', 1)
    if ext != 'pde':
        raise Exception, 'no es un archivo valido'
    target_path = os.path.dirname(pde_file)
    data_dict = {'target_name': target_name,
                 'target_path': target_path,
                 'install_dir': config.path.APP_PATH,
                 'port': config.main.port,
                 'upload_rate': config.main.upload_rate,
                 'avrdude_programmer': config.main.avrdude_programmer,
                 'avr_tools_path': config.path.avr_tools_path,
                 'mcu': config.main.mcu,
                 'f_cpu': config.main.f_cpu,
                 'debug': config.main.debug,
                 'lib_path': config.path.lib,
                 }
    return substitute(data_dict)

def make(makefile, *args):
    subargs = ['make', '-f', makefile]
    subargs.extend(args)
    print subargs
    try:
        subprocess.check_call(subargs)
    except subprocess.CalledProcessError, error:
        print error
        return
    return True

compile = lambda makefile: make(makefile)
upload = lambda makefile: make(makefile, 'upload')
clean = lambda makefile: make(makefile, 'clean')
