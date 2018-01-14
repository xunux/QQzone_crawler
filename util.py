
from urllib import parse
import os
# import cookielib
# import http.cookiejar
 
def get_cookie():
    '''Get cookie from cookie_file'''
    with open('cookie_file') as f:
        cookie = f.read()
    cookie = cookie.replace('\n', '')

    return cookie

cookie = get_cookie()

# 创建MozillaCookieJar实例对象
# cookies = http.cookiejar.MozillaCookieJar()
# 从文件中读取cookie内容到变量
# cookies.load('cookie_file', ignore_discard=True, ignore_expires=True)
# print(cookies)

headers = {'host': 'h5.qzone.qq.com',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'zh,zh-CN;q=0.8,en-US;q=0.5,en;q=0.3',
            'Accept-Encoding': 'gzip, deflate, br',
            'Cookie': cookie,
            'connection': 'keep-alive'}

# 参考 https://qzonestyle.gtimg.cn/qzone/photo/v7/js/lib/photo.js 的 token() 方法
def get_g_tk():
    ''' make g_tk value'''
    pskey_start = cookie.find('skey=')
    pskey_end = cookie.find(';', pskey_start)
    if pskey_end == -1:
        p_skey = cookie[pskey_start+5]
    else:
        p_skey = cookie[pskey_start+5: pskey_end]
    print("p_skey: %s" % p_skey)
    h = 5381

    for s in p_skey:
        h += (h << 5) + ord(s)

    return h & 2147483647

g_tk = get_g_tk()

def parse_moods_url(qqnum):
    '''This method use to get every friend's mood cgi url
       So it needs the friend's qqnumber to get their url
    '''

    params = {"cgi_host": "http://taotao.qq.com/cgi-bin/emotion_cgi_msglist_v6",
              "code_version": 1,
              "format": "jsonp",
              "g_tk": g_tk,
              "hostUin": qqnum,
              "inCharset": "utf-8",
              "need_private_comment": 1,
              "notice": 0,
              "num": 20,
              "outCharset": "utf-8",
              "sort": 0,
              "uin": qqnum}
    host = "https://h5.qzone.qq.com/proxy/domain/taotao.qq.com/cgi-bin/emotion_cgi_msglist_v6?"

    url = host + parse.urlencode(params)
    return url

def parse_friends_url():
    '''This method only generate the friends of the owner
       So do not need to get qq number, just get it from
       self cookie
    '''

    cookie = headers['Cookie']
    qq_start = cookie.find('uin=o')
    qq_end = cookie.find(';', qq_start)
    qqnumber = cookie[qq_start+5 : qq_end]
    if qqnumber[0] == 0:
        qqnumber = qqnumber[1:]
    params = {"uin": qqnumber,
              "fupdate": 1,
              "do": 1,
              "g_tk": g_tk}

    # host = "https://h5.qzone.qq.com/proxy/domain/base.qzone.qq.com/cgi-bin/right/get_entryuinlist.cgi?"
    # host = "https://h5.qzone.qq.com/proxy/domain/r.qzone.qq.com/cgi-bin/tfriend/get_recent_contact.cgi?"
    host = "https://user.qzone.qq.com/proxy/domain/r.qzone.qq.com/cgi-bin/tfriend/friend_ship_manager.cgi?"
    #https://h5.qzone.qq.com/proxy/domain/base.qzone.qq.com/cgi-bin/right/get_entryuinlist.cgi?uin=284182470&fupdate=1&action=1&offset=200&g_tk=1350570173&qzonetoken=8114052f3d145601114b9b3f8caad4ad2853b418b9c345f42af296d6d3e2c980b592a1b7c52273aaa0
    
    # https://user.qzone.qq.com/proxy/domain/r.qzone.qq.com/cgi-bin/tfriend/friend_ship_manager.cgi?uin=1732149464&do=1&rd=0.2861801351564769&fupdate=1&clean=1&g_tk=1361273803&qzonetoken=2188ddd709008e0470e8d34bcbb9878902a462482f4a05bba172d34638be1bb511431c494533e64acace
    
    url = host + parse.urlencode(params)

    return url

def check_path(path):
    '''This method use to check if the path is exists.
       If not, create that
    '''

    if not os.path.exists(path):
        os.mkdir(path)
