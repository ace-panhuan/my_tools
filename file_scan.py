import threading
import requests
import time

# 定义线程数为5
threads = 5
# 目标网址
target_url = "http://127.0.0.1:8888"
# 自己的字典文件
file_txt = "top.txt"
# 模拟浏览器的http头
user_agent = "Mozilla/5.0 (compatible; Baiduspider/2.0; +http://www.baidu.com/search/spider.html)"       # 模拟浏览器的http头
# 设置代理
proxies = None

STATU_CODE_200 = ["200", "201", "202", "203", "204", "205", "206"]
STATU_CODE_300 = ["300", "301", "302", "303", "304", "305", "307"]
STATU_CODE_400 = ["400", "403", "401"]
STATU_CODE_500 = ["500", "501", "502", "503", "504"]
dir_list = []


def get_dir(file_txt):
    with open(file_txt, 'r') as f:
        s = f.readlines()
        for i in s:
            dir_list.append(i)


def get_code(url):
    try:
        headers = {
            'User-Agent': user_agent
        }
        response = requests.get(url, headers=headers, proxies=proxies, verify=False, )
        res_code = response.status_code
        res_code = str(res_code)

        if res_code in STATU_CODE_200:
            print("[%s] => %s" % (res_code, url))
            with open('scan_ok200', 'a+') as file:
                file.write("[%s] => %s" % (res_code, url))
                file.close()

        elif res_code in STATU_CODE_300:
            print("[%s] => %s" % (res_code, url))
            with open('scan_ok300', 'a+') as file:
                file.write(url + res_code + "\n")
                file.close()

        elif res_code in STATU_CODE_400:
            print("[%s] => %s" % (res_code, url))
            with open('scan_ok400', 'a+') as file:
                file.write(url + res_code + "\n")
                file.close()

        elif res_code in STATU_CODE_500:
            print("[%s] => %s" % (res_code, url))
            with open('scan_ok500', 'a+') as file:
                file.write(url + res_code + "\n")
                file.close()

        else:
            print("[%s] => %s" % (response.status_code, url))
            time.sleep(0.01)
    except:
        pass


def dir_scan2(dir_list):
    try:
        for i in range(len(dir_list) + 1):
            s = dir_list.pop()
            url = target_url + s
            get_code(url)

    except IndexError:
        pass


if __name__ == '__main__':
    get_dir(file_txt)
    for i in range(threads):
        t = threading.Thread(target=dir_scan2(dir_list))
        t.start()
