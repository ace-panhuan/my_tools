import time
import requests
import json

class SqlScan(object):
    """
    sqlmapapi交互类
    """
    def __init__(self, server='', target_url='', data ='', referer ='', cookie =''):
        self.server = server
        if self.server[-1] != '/':
            self.server = self.server + '/'
        self.target_url = target_url
        self.taskid = ''
        self.status = ''
        self.data = data
        self.referer = referer
        self.cookie = cookie
        self.start_time = time.time()
        self.headers = {'Content-Type': 'application/json'}


    def task_new(self):
        self.taskid = json.loads(
            requests.get(self.server + 'task/new').text)['taskid']
        if len(self.taskid) > 0:
            return True
        return False


    def task_delete(self):
        kills = requests.get(self.server + 'task/' + self.taskid + '/delete').text
        if kills in 'success':
            print("任务删除")
            return True
        else:
            return False


    def get_payload(self):
        if self.data:
            payload = {'url': self.target_url,
                       'data': self.data}
            return payload
        if self.cookie:
            payload = {'url': self.target_url,
                       'cookie': self.cookie}
            return payload
        if self.referer :
            payload = {'url': self.target_url,
                       'referer': self.referer,
                       }
            return payload
        payload = {'url': self.target_url
                   }
        return payload

    def scan_start(self,payload):

        #payload = {'url': self.target}
        url = self.server + 'scan/' + self.taskid + '/start'
        t = json.loads(
            requests.post(url, data=json.dumps(payload), headers=self.headers).text)
        if t['success']:
            return True
        return False

    def scan_status(self):
        self.status = json.loads(
            requests.get(self.server + 'scan/' + self.taskid + '/status').text)['status']
        if self.status == 'running':
            return 'running'
        elif self.status == 'terminated':
            return 'terminated'
        else:
            return 'error'

    def scan_data(self):
        self.data = json.loads(
            requests.get(self.server + 'scan/' + self.taskid + '/data').text)['data']
        if len(self.data) == 0:
            pass
        else:
            with open(r'scan_result.txt', 'a+') as f:
                f.write(self.target_url + '\n')
                f.write(self.data + '\n')
                f.write('========================pyton sqlmapapi by ace ======================' + '\n')


    def option_set(self):
        headers = {'Content-Type': 'application/json'}
        option = {"options": {
                    "randomAgent": True,
                    "tech":"BT"
                    }
                 }
        url = self.server + 'option/' + self.taskid + '/set'
        t = json.loads(
            requests.post(url, data=json.dumps(option), headers=headers).text)


    def scan_stop(self):
        stop=requests.get(self.server + 'scan/' + self.taskid + '/stop').text


    def scan_kill(self):
        kill=requests.get(self.server + 'scan/' + self.taskid + '/kill').text


    def run(self):
        self.task_new()
        self.option_set()
        payload= self.get_payload()
        self.scan_start(payload)

        while True:
            if self.scan_status() == 'running':
                time.sleep(10)
            elif self.scan_status() == 'terminated':
                break
            else:
                break

            if time.time() - self.start_time > 500:
                error = True
                self.scan_stop()
                self.scan_kill()
                break
        self.scan_data()
        self.task_delete()



if __name__ == "__main__":
    server="http://127.0.0.1:8775/"
    for url in open('url.txt'):
        try:
            if "*" in url:
                urls = url.split('*', 1)
                url = urls[0]
                kwargs = urls[-1]
                kwarg = kwargs.replace('\n', '')
                if "cookie" in kwarg:
                    cookie = kwarg.split(':')[-1]
                    s = SqlScan(server=server, target_url=url, cookie=cookie)
                    s.run()
                elif 'referer' in kwarg:
                    referer = kwarg.split(':')[-1]
                    s = SqlScan(server=server, target_url=url, referer=referer)
                    s.run()
                else:
                    s = SqlScan(server=server, target_url=url, data=kwarg)
                    s.run()
            else:
                url = url.replace('/n', '')
                s = SqlScan(server=server, target_url=url)
                s.run()
        except:
            pass

