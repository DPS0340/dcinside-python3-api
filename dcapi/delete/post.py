import requests
from bs4 import BeautifulSoup

# 갤러리 영문이름, 글번호, 닉네임, 비밀번호를 받습니다.
# 해당글을 삭제할수있습니다.

#gall_namme : 갤러리 영문 이름
#post_num : 삭제할 글의 번호 
#password : 비밀번호


def getCSRFtoken(gall_name,post_num):
    _hd ={
        "User-Agent" : "Mozilla/5.0 (Linux; Android 4.4.2; Nexus 4 Build/KOT49H) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.114 Mobile Safari/537.36"
    }
    url = "https://m.dcinside.com/confirmpw/"+gall_name+"/"+post_num+"?mode=del"
    req = requests.get(url=url,headers=_hd)
    html = req.text
    soup = BeautifulSoup(html, 'lxml')
    csrf = soup.find_all("meta",{"name" : "csrf-token"}) # get csrf token
    return csrf[0].get("content")

def getBlockKey(gall_name,post_num,csrf):
    _hd = {
        "User-Agent" : "Mozilla/5.0 (Linux; Android 4.4.2; Nexus 4 Build/KOT49H) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.114 Mobile Safari/537.36",
        "Referer" : "https://m.dcinside.com/confirmpw/"+gall_name+"/"+post_num+"?mode=del",
        "X-Requested-With" : "XMLHttpRequest",
        "X-CSRF-TOKEN" : csrf
    }
    _payload = {
        "token_verify" : "board_Del"
    }

    url = "https://m.dcinside.com/ajax/access"
    req = requests.post(url=url,headers=_hd,data=_payload)
    pars_key =  (req.text).split('"')
    return pars_key[5]

def deletePost(gall_name,post_num,password,csrf,block_key):
    _hd = {
        "User-Agent" : "Mozilla/5.0 (Linux; Android 4.4.2; Nexus 4 Build/KOT49H) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.114 Mobile Safari/537.36",
        "Referer" : "https://m.dcinside.com/confirmpw/"+gall_name+"/"+post_num+"?mode=del",
        "X-Requested-With" : "XMLHttpRequest",
        "Cookie" : "m_dcinisde_"+gall_name+"="+gall_name+";m_dcinside_lately="+gall_name,
        "X-CSRF-TOKEN" : csrf
    }
    _payload = {
        "_token" : "",
        "board_pw" : password,
        "id" : gall_name,
        "no" : post_num,
        "mode" : "del",
        "con_key" : block_key
    }

    url = "https://m.dcinside.com/del/board"
    req = requests.post(url=url,headers=_hd,data=_payload)
    res = (req.text).split('"')
    res = res[2].split(':')
    res = res[1].split(",")
    return res[0]

def main(gall_name,post_num,password):
    csrf = getCSRFtoken(gall_name,post_num)
    block_key = getBlockKey(gall_name,post_num,csrf)
    res = deletePost(gall_name,post_num,password,csrf,block_key)
    return res

#### dcapi.delete.post(gall_name,post_num,password)
#```python
#비로그인(유동) 글을 삭제할수있습니다.
#result = dcapi.delete.post("programming","99999","1234a")
#print(result)
# -> true
#글삭제를 성공할시 true값이 리턴됩니다.