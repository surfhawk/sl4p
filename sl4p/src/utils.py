# -*- coding: utf-8 -*-
import os
import glob
import time
import collections
import logging


def cdprint(prt=False, msg='', *args):
    if prt:
        print("{} {}".format(str(msg), ' '.join(map(str, args))))

def purge_old_logfiles(l4pConfig):
    for logdir in l4pConfig.to_purge_dirs:
        oldfiles = glob.glob(os.path.join(logdir, "{}*".format(l4pConfig.defaultConfig.logfile_name.replace('{}', ''))))
        #print(oldfiles)
        
        for _oldf in oldfiles:
            if os.path.getctime(_oldf) < (time.time() - (l4pConfig.defaultConfig.purge_window_hours * 3600)):
                try:
                    os.remove(_oldf)
                except:
                    print("old logfile '{}'' could not be deleted !".format(_oldf))

                    # TODO: 나중에 봐야함. 어떻게 해결하지?
                    '''logger = logging.getLogger(pplogger._root_logger_name)  # TODO: is that possible importing recursively?
                    logger.exception("old logfile '{}'' could not be deleted !".format(_oldf))'''

def make_foldertree_if_not_exists(folder_path):
    if not os.path.exists(folder_path):
        print('make_foldertree_if_not_exists', folder_path)
        os.makedirs(folder_path)

# https://stackoverflow.com/questions/3232943/update-value-of-a-nested-dictionary-of-varying-depth
# https://stackoverflow.com/questions/3387691/how-to-perfectly-override-a-dict

def override_dict(original_dict, override_dict):
    def update(mdict, u):
        for k, v in u.items():
            if isinstance(v, collections.Mapping):
                mdict[k] = update(mdict.get(k, {}), v)
            else:
                mdict[k] = v
        return mdict
    
    return update(original_dict, override_dict)
