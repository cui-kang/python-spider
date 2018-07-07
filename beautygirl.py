import urllib.request
import re
import os

#爬取地址http://www.mmonly.cc/tag/cs/2.html，第二页开始爬取
#简单的妹子图片爬取并进行下载，会在当前文件夹下创建文件夹并进行保存

class girls():
    def __init__(self):
        self.url = 'http://www.mmonly.cc/tag/cs/'

    #获取索引页面内容
    def getPage(self,page):
        url = self.url+str(page)+'.html'
        request1 = urllib.request.Request(url)
        response = urllib.request.urlopen(request1)
        return response.read().decode('gbk')
    #提取主页页面妹子内容，保存她的地址和个人描述
    def getcontent(self,page):
        page = self.getPage(page)
        pattern = re.compile('<div.*?class="item masonry_brick.*?<div.*?class="item_t.*?<a.*?href="(.*?)">.*?<img.*?alt="(.*?)" ',re.S)
        items = re.findall(pattern,page)
        contents = {}
        for item in items:
            contents[item[0]] = item[1]
        return contents
    #最后总的查询
    def finalsave(self,num):
        contents = []
        num1=0
        #此循环主要是为了统计某页面个数
        for i in range(2,num+1):
            qwe = self.getcontent(i)
            contents.append(qwe)
            num1+=len(qwe)
        print("总共发现"+str(num1)+"个美女")
    #item表示当前页数，item1表示当前页面某个妹子
        for item in range(0,num-1):
            for item1 in contents[item]:

                self.mkdir(contents[item][item1])
                pages = self.getgirlsnum(item1)
                print('此美女有' + list(pages.values())[0] + '张照片')
                if not pages:continue
                else:
                    self.saveimg(list(pages.keys())[0],'beadty/'+contents[item][item1]+'/1.jpg')
                number = int(pages[list(pages.keys())[0]])
                for i in range(2,number+1):
                    html = self.pipei(item1,i)
                    pa = self.getgirlsnum(html)
                    if not pages:
                        continue
                    else:
                        self.saveimg(list(pa.keys())[0], 'beadty/' + contents[item][item1] + '/'+str(i)+'.jpg')
    #主要是改变每个妹子的翻页照片url
    def pipei(self,url,num):
        pattern = re.compile('(.*?).html',re.S)
        items = re.findall(pattern,url)
        return items[0]+'_'+str(num)+'.html'


    # 获取女孩照片数量以及相应的url getgirlsnum
    def getgirlsnum(self,url):

        response = urllib.request.urlopen(url)
        html = response.read().decode('gbk')
        pattern = re.compile(
            '<div class="photo.*?<div class="wrapper clearfix.*?<div class="big-pic.*?<a href.*?<img .*?src="(.*?)jpg.*?<div class="pages.*?<a>(.*?)</a>',
            re.S)
        items = re.findall(pattern, html)
        pages = {}
        for item in items:
            pages[item[0] + 'jpg'] = re.findall(r'\d+', item[1])[0]
        return pages

    #将图片保存
    def saveimg(self,Imageurl,filename):
        u = urllib.request.urlopen(Imageurl)
        data = u.read()
        with open(filename,'wb') as f:
            f.write(data)
        print("正在保存"+filename+"的照片")
        f.close()
    # 创建文件夹，每个妹子为一个文件夹
    def mkdir(self,path):
        path = 'beadty/'+path.strip()
        isExists = os.path.exists(path)
        if not isExists:
            print("悄悄创建了"+path+"文件夹")
            os.makedirs(path)
            return True
        else:
            print(path+"目录存在准备下载")
            return False




if __name__=="__main__":
    #c从第二页开始爬取到number页
    number = input("输入要爬取的页面个数")
    girls = girls()
    girls.finalsave(int(number))

