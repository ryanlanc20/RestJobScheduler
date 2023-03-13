def getHandler(handler,data):
    return lambda: handler(data)