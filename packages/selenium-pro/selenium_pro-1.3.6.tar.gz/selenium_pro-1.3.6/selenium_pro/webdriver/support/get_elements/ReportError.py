import requests
import json
from threading import Thread
def hit_report_log_api(incoming_browser,browser,platform,log,typee):
    try:
        requests.post("https://3ouwk7rvskgijv6tapptkhum3i0fuyke.lambda-url.us-east-2.on.aws/",data=json.dumps({"log":str(log),"os":platform,"incoming_browser":incoming_browser,"browser":browser,"type":typee}),headers={"content-type":"Application/json"},timeout=3)
    except Exception as e:
        print("Exception",e)
def report_log(incoming_browser,browser,platform,log,typee):
    Thread(target = hit_report_log_api,args=(incoming_browser,browser,platform,log,typee,)).start()