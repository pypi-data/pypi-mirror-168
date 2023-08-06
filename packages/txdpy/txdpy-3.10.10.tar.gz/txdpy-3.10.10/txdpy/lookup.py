import re

def get_chinese(s:str):
    """
    :param s: 提取的字符串
    :return: 返回提取结果列表
    """
    return re.findall('([\u4e00-\u9fa5]+)',s)

def get_letter(s:str):
    """
    :param s: 提取的字符串
    :return: 返回提取结果列表
    """
    return re.findall('([a-zA-Z]+)',s)

def get_Bletter(s:str):
    """
    :param s: 提取的字符串
    :return: 返回提取结果列表
    """
    return re.findall('([A-Z]+)',s)

def get_Sletter(s:str):
    """
    :param s: 提取的字符串
    :return: 返回提取结果列表
    """
    return re.findall('([a-z]+)',s)

def get_num(s:str):
    """
    :param s: 提取的字符串
    :return: 返回提取结果列表
    """
    return re.findall('([0-9]+)',s)

def get_middle(s:str,front:str,after:str,contain=True):
    """
    :param front: 开头字符串
    :param after: 结尾字符串
    :param s: 查找字符串
    :param contain: 是否包含开头和末尾的字符串
    :return: 返回提取结果列表
    """
    if contain:
        return re.findall(f'({front}.*?{after})',s)
    else:
        return re.findall(f'{front}(.*?){after}',s)