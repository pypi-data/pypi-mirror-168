def si(ls:list,s:str=None):
    """
    :param ls: 需要处理的列表
    :param s: 移除字符串头尾指定的字符（默认为空格或换行符）或字符序列
    :return: 移除元素某些字符的列表
    """
    if s:
        return [l.strip(s) for l in ls]
    return [l.strip() for l in ls]

def rl(ls:list,s1:str,s2:str):
    """
        :param ls: 需要处理的列表
        :param s1: 需要被替换的字符串
        :param s2: 替换完成的字符串
        :return: 替换元素字符后的列表
        """
    return [l.replace(s1,s2) for l in ls]