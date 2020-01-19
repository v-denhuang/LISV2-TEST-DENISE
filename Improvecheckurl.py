import requests
import pandas as pd
from bs4 import BeautifulSoup
import time
import requests.exceptions

from openpyxl import load_workbook

webs = 'C:\PythonRelatedProject\checkUrl\SupplierWebs.xlsx'

#check website is active and connective,return code
def check_urlStatus(url):
    try:
        headers = {'user-agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36'}
        re = requests.get(url, headers=headers, timeout=5)
        #print(url+"  "+str(re.status_code)+"   "+time.strftime("%Y-%m-%d-%H_%M_%S", time.localtime(time.time())))
        if re.status_code == 200:
            return True, re.status_code
        else:
            return False, re.status_code
    except Exception:
        print(url+" exception connection")
        return False, 999

def check_urlLang(url):
    try:
        headers = {'user-agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36'}
        re = requests.get(url, headers=headers, timeout=5)
        bsobj = BeautifulSoup(re.text, 'lxml')
        lang = bsobj.findAll('html',{"lang":True})[0]['lang']
        print(url + '\tlang: ' + lang)
        return lang
    except Exception as e:
        print(url+'\tError: ' + str(e))
        return ''

#####for each row of url, add one column about url's response code
def addnewcolumnStatus(file):
    urls = pd.read_excel(file, sheet_name='sheet1', header=0, usecols=[1])
    urls['active'] = urls.apply(lambda x: check_urlStatus(x.website), axis=1)
    urls['lang'] = urls.apply(lambda x: check_urlLang(x.website), axis=1)
    now = time.strftime("%m%d%H%M", time.localtime(time.time()))
    checkresultFile = 'C:\PythonRelatedProject\checkUrl\\checkresult_ '+now+' .xlsx'
    writer = pd.ExcelWriter(checkresultFile)
    urls.to_excel(writer, sheet_name='activewebs')
    writer.save()
    return checkresultFile

if __name__ == '__main__':
    addnewcolumnStatus(webs)