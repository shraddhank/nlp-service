def singleton(cls):
    instance_container = []
    def getinstance(**kwargs):
        if not len(instance_container):
            instance_container.append(cls(**kwargs))
        return instance_container[0]
    return getinstance
