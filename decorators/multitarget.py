
def multitarget(func):
    def wrapper(*args, **kwargs):   
        target = kwargs['target']
        if not target:
            return
        if isinstance(target, (list, tuple)):
            ret_val = []
            for st in target:
                kwargs['target'] = st
                ret = func(*args, **kwargs)
                if ret:
                    try:
                        ret_val.extend(ret)
                    except:
                        ret_val.append(ret)
            if ret_val:
                return ret_val if len(ret_val) > 1 else ret_val[0]
        else:
            return func(*args, **kwargs)

    return wrapper
