# -*- coding:utf-8 -*-

from libs.handler import ErrorHandler
from libs.decorators import route
from handlers import extensionCheck, systemInfo, celerySendSms

handlers = []

# add xxxx handlers
handlers.extend(extensionCheck.handlers)  # app 版本相关功能
handlers.extend(systemInfo.handlers)     # 调用 注册中心的接口
handlers.extend(celerySendSms.handlers)  # celery 短信功能

#
# # add @route handlers
handlers.extend(route.get_routes())
#
# # Append default 404 handler, and make sure it is the last one.
# handlers.append((r".*", ErrorHandler))
