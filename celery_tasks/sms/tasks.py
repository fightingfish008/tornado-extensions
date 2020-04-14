import json
import logging
import uuid
from celery_tasks.main import celery_app
from celery_tasks.sms.dysms_python.demo_sms_send import send_sms

# 获取日志器
logger = logging.getLogger('myapp')


# 阿里云发送短信验证码
@celery_app.task(name='send_sms_code')
def send_sms_code(mobile, sms_code):
    logger.info(sms_code)
    __business_id = uuid.uuid1()
    params = {'code': sms_code}
    params = json.dumps(params)
    try:
        smsResponse = send_sms(__business_id, mobile, "啄鸟云医", "SMS_148862221", template_param=params)

    except Exception as e:
        logger.error('发送短信异常: mobile: %s sms_code: %s', mobile, sms_code)
    else:
        jn = json.loads(smsResponse.decode())
        logger.error(jn)
        if jn.get("Code") != "OK":
            logger.error('发送短信失败: mobile: %s sms_code: %s' % (mobile, sms_code))





