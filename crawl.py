from urllib import request
from urllib.parse import quote
from baike_spider.html_downloader import HtmlDownloader,driver

people19conf='../19大名单.txt'
downloader = HtmlDownloader()

with open(people19conf) as f:
    lines=f.readlines()

start=False
for li, line in enumerate(lines):
    place,list = line.replace('。','').strip().split('\t')
    pos=len(place)
    if place.find('第')!=-1: pos=place.find('第')
    if place.find("选举产生")!=-1: pos=min(place.find("选举产生"),pos)
    if place.find('省')!=-1: pos = min(place.find('省')+1,pos)
    if place.find('代表会议')!=-1: pos = min(place.find('代表会议'),pos)
    if place.find('各单位')!=-1: pos = min(place.find('各单位'),pos)
    place = place[:pos]
    place = place[place.find('、')+1:]
    place = place[place.find('，')+1:]
    if place.endswith('党'): place=place[:-1]
    if place.startswith('中国共产党'): place=place[place.find('中国共产党')+5:]
    for name in list.split('、'):
        if '（' in name:
            name=name[:name.find('（')]
        name=name.strip()

        # if name == '哈小琴':
        #     start = True
        #     continue
        # if not start:
        #     continue
        # find baike containing 19da in bing
        baike_url, mark, baike_page=None,'',''
        bing_url='%s %s'%(place,name)
        #bing_url = 'https://www.bing.com/search?q=%s+%s&form=EDGEAR&qs=AS&cvid=f3d99557745142eda87a63a803239fdf&cc=CN&setlang=zh-Hans-CN'%(quote(place),quote(name))
        page = downloader.download(url=bing_url)
        if 'baike.baidu.com' in page:
            lines=page.split('href=')
            for line in lines:
                keyword = "\"https://baike.baidu.com/item/"+name
                if keyword in line:
                    _url = line[line.find(keyword)+1:]
                    _url = _url[:_url.find("\"")]
                    if _url.endswith(name) or name+'/' in _url:
                        _url=_url.replace(name, quote(name))
                    else:
                        continue
                    baike_page = downloader.download(url=_url)
                    if "十九" in baike_page:
                        lemma_key='<dd class="lemmaWgt-lemmaTitle-title">'
                        title = baike_page[baike_page.find(lemma_key)+len(lemma_key):][:30].replace(' ','')
                        title = title[title.find('<h1>')+4:title.find('</h1>')]
                        if title==name:
                            baike_url=_url
                            mark+='含十九大'
                            break
        # if baike_url was not found, find it by url
        if not baike_url:
            _url='https://baike.baidu.com/item/%s' % quote(name)
            baike_page = downloader.download(url=_url)
            if baike_page and 'polysemantList-wrapper cmn-clearfix' not in baike_page:
                baike_url=_url
                mark+='单义词'

        # if baike_url is determined, print
        if baike_url:
            if "北京大学" in baike_page or "北大" in baike_page:
                mark+=',含北大'
            print('<p><a href="%s">'%baike_url, place, name, mark,'</a></p>')
        else:
            print('<p>', place, name, '</p>')

driver.quit()