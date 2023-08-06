from lxml import etree
from .list_processing import si

def url_Splicing(url_resp,href:str):
    """
    :param url_resp: #链接或响应对象
    :param href: 需要拼接的链接
    :return: 拼接完成的链接
    """
    start_url=url_resp

    if href.startswith('http'):
        return href

    if type(url_resp)!=str:
        start_url=url_resp.url

    if href.startswith('/'):
        href=href.lstrip('/')
        href_sp=href.split('/')[0]
        start_url_rsplit=start_url.rsplit('/'+href_sp,1)
        if len(start_url_rsplit)==2:
            start_url=start_url_rsplit[0]
        elif len(start_url_rsplit)==1:
            start_url = start_url.rsplit('/',1)[0]
    elif href.startswith('./'):
        href=href.lstrip('./')
        href_sp=href.split('/')[0]
        start_url_rsplit=start_url.rsplit('/'+href_sp,1)
        if len(start_url_rsplit)==2:
            start_url=start_url_rsplit[0]
        elif len(start_url_rsplit)==1:
            start_url = start_url.rsplit('/',1)[0]
    else:
        href_sp=href.split('/')[0]
        start_url_rsplit = start_url.rsplit('/' + href_sp,1)
        if len(start_url_rsplit) == 2:
            start_url = start_url_rsplit[0]
        elif len(start_url_rsplit) == 1:
            start_url = start_url.rsplit('/',1)[0]
    return start_url + '/' + href

def headers_dict(headers_raw):
    if headers_raw is None:
        return None
    if headers_raw.startswith(':'):
        print('requests请求头中键名前的冒号需要删除！！！')
    headers = headers_raw.splitlines()
    headers_tuples = [header.lstrip(':').split(":", 1) for header in headers]

    result_dict = {}
    for header_item in headers_tuples:
        if not len(header_item) == 2:
            continue

        item_key = header_item[0].strip()
        item_value = header_item[1].strip()
        result_dict[item_key] = item_value

    return result_dict

def param_dict(param_raw):
    if param_raw is None:
        return None
    params = param_raw.splitlines()
    param_tuples = [param.split(":", 1) for param in params]

    result_dict = {}
    for param_item in param_tuples:
        if not len(param_item) == 2:
            continue

        item_key = param_item[0].strip()
        item_value = param_item[1].strip()
        result_dict[item_key] = item_value

    return result_dict

def webptablesl(res,xpath):
    """
    :param res: url响应的html
    :param xpath: 表格xpath
    :return: 拆分后的表格数据，以列表返回
    """
    tree=etree.HTML(res)
    table = tree.xpath(xpath)[0]
    trs = table.xpath('//tr')

    #提取表格合并信息
    al=[]
    for tr in trs:
        l=[]
        tds=tr.xpath('./td|th')
        for td in tds:
            td_text=''.join(si(td.xpath('.//text()')))
            colspan=td.xpath('./@colspan')
            colspan =int(colspan[0]) if colspan else 1
            rowspan=td.xpath('./@rowspan')
            rowspan = int(rowspan[0]) if rowspan else 1
            l.append({td_text:(colspan,rowspan)})
        al.append(l)

    new_al=[]
    for n in range(len(al)):
        new_al.append([])

    #处理横向合并
    a=0
    for l in al:
        new_l=new_al[a]
        i=0
        for d in l:
            for key, value in d.items():
                for c in range(value[0]):
                    new_l.insert(i,key)
                    i+=1
            i+=1
        new_al.pop(a)
        new_al.insert(a,new_l)
        a+=1

    #处理纵向合并
    a=0
    for l in al:
        i=0
        for d in l:
            for key, value in d.items():
                if value[1]>1:
                    for r in range(1,value[1]):
                        new_l=new_al[a+r]
                        new_l.insert(i, key)
                        new_al.pop(a+r)
                        new_al.insert(a+r, new_l)
            i+=1
        a+=1
    return new_al