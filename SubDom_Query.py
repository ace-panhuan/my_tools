import socket,time
"""
调用 socket 模块的 gethostbyname 函数来判断该域名是否能够 解析 IP，
如果能说明该域名存在，不能则说明不存在。 
"""


def subdom_query(url):
    url = url.replace('www','')
    for dict in open('dice.txt'):
        dict = dict.replace('\n','')
        dict_url = dict + "." + url
        try:
            ip = socket.gethostbyname(dict_url)
            print(dict_url + "->" + ip)
            with open(r'scan_result.txt', 'a+') as f:
                f.write(dict_url + '\n')
            time.sleep(0.1)
        except Exception as e:
            time.sleep(0.1)


if __name__ == '__main__':
    url = input('输入地址')
    subdom_query(url)
