# -*- coding: utf-8 -*-
# @Filename : utils
# @Date : 2022-07-27-11-40
# @Project: content-script-slack-block-builder

def obj2dict(obj):
    if not hasattr(obj, "__dict__"):
        return obj
    result = {}
    for key, val in obj.__dict__.items():
        if key.startswith("_"):
            continue
        element = []
        if isinstance(val, list):
            for item in val:
                element.append(obj2dict(item))
        else:
            element = obj2dict(val)
        result[key] = element
    return result
