from urllib import request
from urllib.parse import quote

class HtmlDownloader(object):
    def download(self, url):
        response = request.urlopen(url)
        if response.getcode() != 200:
            return None
        return response.read().decode('utf-8')
downloader = HtmlDownloader()

xuebuweiyuan_url='http://cass.cssn.cn/xuebuweiyuan/xuebuweiyuan/index.html'
for i in range(6):
    if i==0:
        xbwy_url=xuebuweiyuan_url
    else:
        xbwy_url=xuebuweiyuan_url[:-4]+'_'+str(i)+'.html'
    page=downloader.download(xbwy_url)
    keyword='<a style="color:#FFFFFF;font-family:" href="./wwg/" target="_blank" 微软雅黑\';font-size:20px;line-height:35px;\'="">'
    if keyword in page:
        page=page[page.find(keyword)+len(keyword):]
        print(page[3:])
        print()