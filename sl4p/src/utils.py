# -*- coding: utf-8 -*-
import sys
import os
import glob
import time
import collections
import logging
import copy

python_version = sys.version_info
if (python_version.major >= 3) and (python_version.minor >= 10):
    from collections.abc import Mapping
else:
    from collections import Mapping


def cdprint(prt=False, msg='', *args):
    if prt:
        print("{} {}".format(str(msg), ' '.join(map(str, args))))


def purge_old_logfiles(l4pConfig):
    for logdir in l4pConfig.to_purge_dirs:
        oldfiles = glob.glob(os.path.join(logdir, "{}*".format(l4pConfig.defaultConfig.logfile_name.replace('{}', ''))))
        # print(oldfiles)

        for _oldf in oldfiles:
            if os.path.getctime(_oldf) < (time.time() - (l4pConfig.defaultConfig.purge_window_hours * 3600)):
                try:
                    os.remove(_oldf)
                except Exception as e:
                    print("old logfile '{}'' could not be deleted !\n  ---> {}".format(os.path.abspath(_oldf), e))

                    # TODO: is that possible importing recursively for writing purging log?
                    '''logger = logging.getLogger(pplogger._root_logger_name)
                    logger.exception("old logfile '{}'' could not be deleted !".format(_oldf))'''


def make_foldertree_if_not_exists(folder_path):
    if not os.path.exists(folder_path):
        print('make_foldertree_if_not_exists', folder_path)
        os.makedirs(folder_path)


def get_os_userhome_dirpath():
    return os.path.expanduser('~')


# https://stackoverflow.com/questions/3232943/update-value-of-a-nested-dictionary-of-varying-depth
# https://stackoverflow.com/questions/3387691/how-to-perfectly-override-a-dict

def override_dict(original_dict, to_override_dict):
    def update(mdict, u):
        for k, v in u.items():
            if isinstance(v, Mapping):
                mdict[k] = update(mdict.get(k, {}), v)
            else:
                mdict[k] = v
        return mdict

    return update(original_dict, to_override_dict)


def replace_dict_key(dict_, old_key, new_key):
    if new_key not in dict_ and old_key in dict_:
        dict_[new_key] = copy.deepcopy(dict_[old_key])
    if old_key in dict_:
        del dict_[old_key]
    return dict_
