import os
from threading import Thread
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
import xml.etree.ElementTree as ET

driver = webdriver.Chrome(executable_path=r"C:\Users\joshu\Desktop\projects\youtoob\bin\drivers\chromedriver.exe")
F = os.path.join(os.path.dirname(__file__), "YOUTOOBsaves.xml")
savesXML_Root = ET.parse(F).getroot()
s = "default"

def BOOKMARK(name):
    global s
    s = name

def LOADER(video):
    if savesXML_Root.find(".//video[@name='{}']".format(video)) != None:
        driver.get('https://www.youtube.com/watch?v={}&t={}'.format(savesXML_Root.find(".//video[@name='{}']/VIDID".format(video)).text, savesXML_Root.find(".//video[@name='{}']/TIME".format(video)).text))
        BOOKMARK(video)
    else:
        driver.get(('https://www.youtube.com/watch?v={}&t={}'.format(savesXML_Root.find(".//video[@name='default']/VIDID").text, savesXML_Root.find(".//video[@name='default']/TIME").text)))
        BOOKMARK("default")

def SAVER(save):
    video = {"VIDID": str(driver.current_url).split('https://www.youtube.com/watch?v=')[-1].split("&")[0], "TIME": int(driver.execute_script('return document.getElementsByTagName("video")[0].currentTime'))}
    driver.execute_script('document.getElementsByTagName("video")[0].pause()')
    for element in savesXML_Root.findall("video"):
        if element.attrib['name'] == save:
            savesXML_Root.remove(element)
    video_element = ET.Element('video', name="{}".format(save))
    for key, val in video.items():
        video_child = ET.SubElement(video_element, key)
        video_child.text = str(val)
    savesXML_Root.append(video_element)
    data = str(ET.tostring(savesXML_Root, encoding='unicode', method='xml'))
    saveto = open(F, "w")
    saveto.write(data)
    BOOKMARK(save)
            
def TIMER(time):
    ID = str(driver.current_url).split('https://www.youtube.com/watch?v=')[-1].split("&")[0]
    driver.get("https://www.youtube.com/watch?v={}".format(ID) + "&t={}".format(time))

def DELETE(file):
    if savesXML_Root.find(".//video[@name='{}']".format(file)) != None:
        savesXML_Root.remove(savesXML_Root.find(".//video[@name='{}']".format(file)))
        data = str(ET.tostring(savesXML_Root, encoding='unicode', method='xml'))
        saveto = open(F, "w")
        saveto.write(data)
        BOOKMARK("default")

def PROMPT(CMD):
    if CMD.lower() == "load":
        for files in savesXML_Root.findall(".//video"):
            print(files.attrib)
        load = input("LOAD: ")
        LOADER(load)
    elif CMD.lower() == "save":
        if "/watch?v=" in str(driver.current_url):
            if "ad-showing" in driver.execute_script('return document.getElementById("movie_player").classList'):
                print("cannot save")
            else:
                SAVER(s)
    elif CMD.lower() == "new":
        new = input("NEW: ")
        if "/watch?v=" in str(driver.current_url):
            if "ad-showing" in driver.execute_script('return document.getElementById("movie_player").classList'):
                print("cannot create")
            else:
                SAVER(new)
    elif CMD.lower() == "time":
        if "/watch?v=" in str(driver.current_url):
            T = input("TIME: ")
            if T.isdigit():
                TIMER(T)
    elif CMD.lower() == "delete":
        for files in savesXML_Root.findall(".//video"):
            print(files.attrib)
        remove = input("DELETE: ")
        if remove.lower() != 'default':
            DELETE(remove)
        else:
            print("cannot remove default!")
    elif CMD.lower() == "quit":
        driver.quit()

def APP():
    while True:
        try:
            PROMPT(input("CMD: "))
        except Exception as E:
            print(E)

def CHECK_DRIVER():
    while True:
        try:
           _ = driver.title
        except WebDriverException:
            break
        
if __name__ == '__main__':
    T1 = Thread(target=CHECK_DRIVER)
    T1.start()

    T2 = Thread(target=APP)
    T2.daemon = True
    T2.start()

