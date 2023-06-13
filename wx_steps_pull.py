# 同步微信步数
import sys
sys.path.append(r"D:\PycharmProjects\unittest_demo")
sys.path.append(r"D:\software\work\anaconda\envs\pytorch\Lib")
sys.path.append(r"D:\software\work\anaconda\envs\pytorch\Lib\site-packages")
sys.path.append(r"C:\Users\XDJ\AppData\Roaming\Python\Python36\site-packages")

import requests

def wxstep(steps):

    s = requests.session()

    url =r'http://118.195.237.33/'
    res = s.get(url)
    import re
    csrf_token = re.findall('name="csrf_token" type="hidden" value="(.+?)"',res.text)[0]


    url =r'http://118.195.237.33/changeXiaomiSteps'
    data = {
        "csrf_token": csrf_token,
        "phone": "18770917594",
        "password": "6382463qq",
        "steps": steps,
    }
    re =s.post(url,data=data)
    return re.json()["msg"]


import random
steps = random.randint(3000,6000)
print(wxstep(steps))
