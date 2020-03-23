# -*- coding:utf-8 -*-


class Status(object):
    NEW = 0
    CHECKED = 1
    PAID = 2
    EXPRESS = 3
    CLOSED = 4


class MsgCode(object):
    """
    请求返回状态码
    """
    SUCCESS = 0
    FAILURE = -1
    FAILURE2 = -2


class CheckInCode(object):
    """
    登录状态
    """
    CHECKEIN = 0
    TIMEOUTTOKEN = -1
    MISSTOKEN = -2


class PageCode(object):
    PAGELIMIT = 10  # 每页数量
    MIDPAGELIMIT = 20
    BIGPAGELIMIT = 30  # 30每页数量
    SKIP =0


class CreateFlag(object):
    CREATE = 1
    UPDATE = 2
    DELETE = 3
