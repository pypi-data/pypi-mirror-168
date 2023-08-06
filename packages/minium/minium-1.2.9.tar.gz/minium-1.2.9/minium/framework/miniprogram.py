class MiniProgram:
    class __MiniProgram(object):
        def __init__(self, appid, **kwargs) -> None:
            self.appid = appid
            self.update(**kwargs)

        def update(self, **kwargs):
            for k in kwargs:
                setattr(self, k, kwargs[k])

    instances = {}
    def __init__(self, appid, **kwargs):
        appid = appid or ""
        if not MiniProgram.instances.get(appid):
            MiniProgram.instances[appid] = MiniProgram.__MiniProgram(appid, **kwargs)
        else:
            MiniProgram.instances[appid].update(**kwargs)
        self.instance = MiniProgram.instances[appid]
        
    def __getattr__(self, name):
        return getattr(self.instance, name, None)

    @classmethod
    def get_instance(cls, appid):
        return MiniProgram.instances.get(appid or "")
    
