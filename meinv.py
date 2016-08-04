import sys
import os
import requests
from bs4 import BeautifulSoup
from datetime import datetime

cid=0
pager_offset=1
localStoreImagePath='./image'
headers={'user-agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.82 Safari/537.36'}
baseUrl='http://www.dbmeinv.com/dbgroup/show.htm?cid={cid}&pager_offset={pager_offset}'
baseUrlAll='http://www.dbmeinv.com/dbgroup/show.htm?pager_offset={pager_offset}'

def initLocalStoreImageDir(cid,pager_offset):
	if os.path.exists(localStoreImagePath):
		print("main dir exists")
		addSubDir(cid,pager_offset)
	else:
		print("main dir not exists,will create")
		os.mkdir(localStoreImagePath)
		addSubDir(cid,pager_offset)

def addSubDir(cid,pager_offset):
	sub_dir=os.path.join(localStoreImagePath,str(cid),str(pager_offset))
	if os.path.exists(sub_dir):
		print('sub dir exists')
	else:
		print('sub dir not exists will create')
		os.makedirs(sub_dir)

def getHtmlStr(cid=cid, pager_offset=pager_offset):
	initLocalStoreImageDir(cid,pager_offset)
	targetUrl=""
	if cid == 0:
		targetUrl=baseUrlAll.format(pager_offset=pager_offset)
	else:
		targetUrl=baseUrl.format(cid=cid,pager_offset=pager_offset)
	print(targetUrl)
	r=requests.get(targetUrl,headers)
	print(r.status_code)
	soup=BeautifulSoup(r.text,'html.parser')
	for item in soup.find_all('img'):
		print(item)
		image_url=item.get('src')
		timestamp=datetime.today()
		image_title=str(timestamp)+item.get('title')
		print(image_url)
		print(image_title)
		target_path=os.path.join(localStoreImagePath,str(cid),str(pager_offset),image_title+'.jpg')
		downloadAndSave(image_url,target_path)

def downloadAndSave(image_url,image_save_path):
	print(image_save_path)
	print('start downloading ',image_save_path)
	r = requests.get(image_url,headers ,stream=True)
	if r.status_code == 200:
		with open(image_save_path, 'wb') as f:
			for chunk in r.iter_content(1024):
				f.write(chunk)
	print('save success')
	

params = sys.argv
print(params)
if len(params) == 2 :
	getHtmlStr(0,int(params[1]))
elif len(params) == 3 :
	getHtmlStr(int(params[1]),int(params[2]))
else:
	getHtmlStr()

