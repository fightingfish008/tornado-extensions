import os
import sys
import logging
import getpass

def changetext(a,b):
    with open('config.py','r',encoding='utf-8') as f:
        lines=[] # 创建了一个空列表，里面没有元素
        for line in f.readlines():
            if line!='\n':
                lines.append(line)
            f.close()
    with open('config.py','w',encoding='utf-8') as f:
        for line in lines:
            if a in line:
                line = b
                f.write('%s\n' %line)
            else:
                f.write('%s' %line)


if __name__ =="__main__":
    logging.info("脚本名：{}".format(sys.argv[0]))
    for i in range(1, len(sys.argv)):
        print("参数", i, sys.argv[i])

    args = sys.argv
    mydict = {}
    for i in range(1, len(args)):
        # All things after the last option are command line arguments
        if not args[i].startswith("-"):
            remaining = args[i:]
            break
        if args[i] == "--":
            remaining = args[i + 1:]
            break
        arg = args[i].lstrip("-")
        name, equals, value = arg.partition("=")
        mydict[name] = value

    try:
        os.system("nohup celery -A doctor_tasks worker --config="+mydict["env"]+"_flag -l info &")
        os.system("nohup celery -A doctor_tasks beat --config="+mydict["env"]+"_flag -l info &")

    except Exception as e:
        logging.error("执行celery命令行错误")


