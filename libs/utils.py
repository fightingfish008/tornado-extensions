# -*- coding:utf-8 -*-

from tornado.options import define, options

def parse_config_file(path):
    """Rewrite tornado default parse_config_file.
    
    Parses and loads the Python config file at the given path.
    
    This version allow customize new options which are not defined before
    from a configuration file.
    """
    config = {}
    with open(path,'r') as f:
        exec(f.read(), config, config)
    
    for name in config:
        if name in options:
            setattr(options,name,config[name])
        else:
            define(name, config[name])

