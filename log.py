import logging
def getloger(logname = "ddddddddddddefault.log",programeName = 'programeName'):
    logger = logging.getLogger(programeName)
    logger.setLevel(logging.INFO)
    # 建立一个filehandler来把日志记录在文件里，级别为debug以上
    fh = logging.FileHandler(logname)
    fh.setLevel(logging.INFO)
    # 建立一个streamhandler来把日志打在CMD窗口上，级别为error以上
    #ch = logging.StreamHandler()
    #ch.setLevel(logging.INFO)
    # 设置日志格式
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    #ch.setFormatter(formatter)
    fh.setFormatter(formatter)
    #将相应的handler添加在logger对象中
    #logger.addHandler(ch)
    logger.addHandler(fh)
    
    # 开始打日志
    return logger
    '''
    logger.debug("debug message")
    logger.info("info message")
    logger.warn("warn message")
    logger.error("error message")
    logger.critical("critical message")
    '''
