from bs4 import BeautifulSoup
from .MatchAttributes import find_the_elements_by_event,xpath_soupreq
from selenium_pro.webdriver.support.global_vars import get_global_driver,get_browser_name
from selenium_pro.webdriver.support.get_elements.ReportError import *
from .FindXpath import *
import requests
import json
import sys
def get_the_analysis(bot_id,multiple_element):
    found=False
    message=""
    send_bot_id=bot_id
    if(multiple_element==True):
        send_bot_id=send_bot_id+"_repeat"
    response=requests.post("https://jpzu5bjwzg.execute-api.us-east-2.amazonaws.com/default/read_bot_analysis",data=json.dumps({"bot_id":send_bot_id}),headers={"content-type":"application/json"}).json()
    found=response["status"]
    analysis=response["analysis"]
    if(found==False):
        try:
            message=response["message"]
        except:
            message="Not Found"
    return analysis,found,message
def change_analysis(analysis,multiple_element):
    new_analysis={}
    for event_number in analysis:
        event_name=list(analysis[event_number].keys())[0]
        new_analysis=analysis[event_number][event_name]
        break
    try:
        new_analysis["Event"]["xlength"]=int(new_analysis["Event"]["xlength"])
    except:
        pass
    try:
        new_analysis["Parent"]["xlength"]=int(new_analysis["Parent"]["xlength"])
    except:
        pass
    if(multiple_element==False):
        new_analysis["isrepeat"]=False
    return new_analysis
def get_the_front_xpath(element):
    global_driver=get_global_driver()
    front_xpath=JavaScriptXpath(global_driver,element)
    return front_xpath
def send_the_log(bot_id,multiple_element,browser):
    log="find_element_by_pro called"
    if(multiple_element==True):
        log="find_elements_by_pro called"
    log=log+" for bot:-"+str(bot_id)
    report_log(browser,browser,sys.platform,log,"Log")
def get_the_elements_by_bot_id(page_source,bot_id,driver,multiple_element):
    try:
        browser=get_browser_name()
        send_the_log(bot_id,multiple_element,browser)
        typee="driver"
        front_xpath=""
        if("webdriver.remote.webelement.WebElement" in str(type(driver))):
            typee="element"
            front_xpath=get_the_front_xpath(driver)
        analysis,found,message=get_the_analysis(bot_id,multiple_element)
        if(found==False):
            print(message)
            report_log(browser,browser,sys.platform,message+":-"+str(bot_id),"Log")
            return None
        reqsoup=BeautifulSoup(page_source,'html.parser')
        analysis=change_analysis(analysis,multiple_element)
        elements=find_the_elements_by_event(reqsoup,page_source,analysis)
        if(multiple_element==False):
            element=driver.find_element_by_xpath(front_xpath+xpath_soupreq(elements[0]))
        else:
            element=[]
            for el in elements:
                element.append(driver.find_element_by_xpath(front_xpath+xpath_soupreq(el)))
    except Exception as e:
        report_log("","",sys.platform,str(e),"Log")
        raise RuntimeError(str(e))
    return element