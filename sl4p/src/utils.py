# -*- coding: utf-8 -*-
import sys
import os
import glob
import time
import collections
import logging
import copy


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


def get_os_userhome_dirpath():
    return os.path.expanduser('~')


# https://stackoverflow.com/questions/3232943/update-value-of-a-nested-dictionary-of-varying-depth
# https://stackoverflow.com/questions/3387691/how-to-perfectly-override-a-dict

def override_dict_lte_py38(original_dict, override_dict):
    def update(mdict, u):
        for k, v in u.items():
            if isinstance(v, collections.Mapping):
                mdict[k] = update(mdict.get(k, {}), v)
            else:
                mdict[k] = v
        return mdict

    return update(original_dict, override_dict)


def override_dict_gte_py39(original_dict, override_dict):
    for (key, val) in override_dict.items():
        a_vals = original_dict.get(key)
        if a_vals:
            original_dict[key] = a_vals | val
        else:
            original_dict[key] = val

    return original_dict


def override_dict(original_dict, override_dict):
    python_version = sys.version_info
    if (python_version.major >= 3) and (python_version.minor >= 9):
        return override_dict_gte_py39(original_dict, override_dict)
    else:
        return override_dict_lte_py38(original_dict, override_dict)


def replace_dict_key(dict_, old_key, new_key):
    if new_key not in dict_ and old_key in dict_:
        dict_[new_key] = copy.deepcopy(dict_[old_key])
    if old_key in dict_:
        del dict_[old_key]
    return dict_
