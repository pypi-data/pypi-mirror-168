# -*- coding: utf-8 -*-
""" Test for universal logger

"""
import sys, os, logging


##############################################################################
def test_all():

    test1()
    test2()
    test_logging()



def test1():
    """function test1.
    """
    os.environ['log_verbosity']='10'
    os.environ['log_type']='base'

    from util_log import log3, log2, log, logw, loge, logc, logr
    log3("debug2")
    log2("debug")
    log("info")
    logw("warning")
    logc("critical")

    try:
        a = 1 / 0
    except Exception as e:
        logr("error", e)
        loge("Exception"), e

    log("finish")

        


def test2():
    """function test2.
    """
    os.environ['log_verbosity']='10'
    os.environ['log_type']='loguru'

    import util_log
    from util_log import log3, log2, log, logw, loge, logc, logr

    ### Redefine new template
    util_log.logger_setup('config_loguru.yaml', 'default')

    log3("debug2")
    log2("debug")
    log("info")
    logw("warning")
    logc("critical")

    try:
        a = 1 / 0
    except Exception as e:
        logr("error", e)
        loge("Exception"), e

    log("finish")



def test_logging():
    os.environ['log_verbosity']='10'
    os.environ['log_type']='logging'

    from util_log import logger, log3, log2, log, logw, loge, logc, logr, logger_setup
    from util_log import FORMATTER_1,FORMATTER_2,FORMATTER_3,FORMATTER_4,FORMATTER_5
    
   

    s='test logger_name'
    print('\ntest logger_name')
    logger=logger_setup(logger_name= 'test_logging' )
    log2(s)

    # test log_fomatter
    print('\ntest log_fomatter ')
    log_formats=[FORMATTER_1, FORMATTER_2,FORMATTER_3,FORMATTER_4,FORMATTER_5]
    for format in log_formats:
        logger=logger_setup(formatter=format)
        log2(s)

    # test isrotate
    s='test isrotate'
    print('\ntest isrotate ')
    logger=logger_setup(isrotate=True)
    log2(s)

    # test isconsole_output
    s='test isconsole_output'
    print('\ntest isconsole_output ')
    logger=logger_setup(isconsole_output=False)
    log2(s)

    # test logging_level
    print('\ntest logging levels')
    log_levels=[logging.CRITICAL, logging.ERROR,logging.WARNING,logging.INFO,logging.DEBUG]

    for log in log_levels:
        logger=logger_setup(logging_level=log)
        if log==logging.CRITICAL:
            s='critical'
            logc(s)
        elif log==logging.ERROR:
            s='error'
            loge(s)
        elif log==logging.WARNING:
            s='warning'
            logw(s)
        elif log==logging.INFO:
            s='info'
            log2(s)
        elif log==logging.DEBUG:
            s='debug'
            log3(s)


    # test log_file
    s='test log_file'
    print('\ntest log_file test.log')
    logger=logger_setup(log_file='test.log')
    log2(s)
  


############################################################################
if __name__ == "__main__":
    # test_logging()
    import fire
    fire.Fire()


"""
03.07.21 00:06:55|DEBUG   |   __main__    |    mytest     |  5|debug
03.07.21 00:06:55|INFO    |   __main__    |    mytest     |  6|info
03.07.21 00:06:55|WARNING |   __main__    |    mytest     |  7|warning
03.07.21 00:06:55|ERROR   |   __main__    |    mytest     |  8|error
NoneType: None
03.07.21 00:06:55|CRITICAL|   __main__    |    mytest     |  9|critical
03.07.21 00:06:55|ERROR   |   __main__    |    mytest     | 14|error,division by zero
03.07.21 00:06:55|ERROR   |   __main__    |    mytest     | 15|Catcch
Traceback (most recent call last):

  File "D:/_devs/Python01/gitdev/arepo/zz936/logs\test.py", line 21, in <module>
    mytest()
    └ <function mytest at 0x000001835D132EA0>

> File "D:/_devs/Python01/gitdev/arepo/zz936/logs\test.py", line 12, in mytest
    a = 1 / 0

ZeroDivisionError: division by zero

Process finished with exit code 0


"""
