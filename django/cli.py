# -*- coding: UTF-8 -*-

import sys, os
from os.path import dirname, abspath

from django.core.management import setup_environ

def setup_env(callerpath, settings_module='settings'):
    '''Setup nessesary django environment needed by a command line script
    
    return django settings module
    
    '''
    callerpath = abspath(callerpath)
    _path = dirname(callerpath)
    while True:
        ls = os.listdir(_path)
        
        if '__init__.py' in ls and \
            'manage.py' in ls and \
            'settings.py' in ls:
            
            PROJ_PATH = _path
            break
        
        elif '/' == _path or dirname(_path) == _path:
            raise Exception('Could not find django project path in `{}`'.\
                            format(callerpath))
            
        _path = dirname(_path)
    
    PROJ_CONTAINER = dirname(PROJ_PATH)
    PROJ_NAME = PROJ_PATH.split('/')[-1]
    
    # make possible to import project.settings
    sys.path.append(PROJ_CONTAINER)
    os.environ['DJANGO_SETTINGS_MODULE'] = PROJ_NAME + '.' + settings_module
    __import__(os.environ['DJANGO_SETTINGS_MODULE'])
    # nolonger needed after importing project.settings
    # so make the python search path cleaner
    sys.path.remove(PROJ_CONTAINER)
    
    settings = sys.modules[os.environ['DJANGO_SETTINGS_MODULE']]
    setup_environ(settings)
    # make ur appz inside project able to import by relative path
    sys.path.append(PROJ_PATH)
    
    return settings