import inspect

KIKYOPP_SOURCE = '__kikyopp_source__'

KIKYOPP_SINK = '__kikyopp_sink__'


def source(name: str):
    """
    标识数据源

    :param name: 数据源名称
    """

    def wrapper(func):
        setattr(func, KIKYOPP_SOURCE, name)
        return func

    return wrapper


def sink(name: str):
    """
    标识数据处理器

    :param name: 数据处理器名称
    """

    def wrapper(func):
        setattr(func, KIKYOPP_SINK, name)
        return func

    if inspect.isfunction(name):
        f = name
        name = None
        return wrapper(f)
    return wrapper
