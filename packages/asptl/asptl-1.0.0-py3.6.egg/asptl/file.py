class File():
    def __init__(self,name,way='.'):
        self.name=way+'\\'+name
    def write(self,text=''):
        f=open(self.name,'w')
        f.write(text)
        f.close()
    def create(self):
        f=open(self.name,'w')
        f.close()
    def addtext(self,text=''):
        f=open(self.name,'a')
        f.write(text)
        f.close()
    def remove(self,value='',times=1):
        f=open(self.name,'r+')
        text=f.read()
        f.close()
        for i in text:
            times-=1
            if i==value:
                text.replace(i,'')
            if times==0:
                break
        f=open(self.name,'w')
        f.write(text)
        f.close()
    def read(self):
        f=open(self.name,'r')
        txt=f.read()
        f.close()
        return txt
    def __pop(self,times=1):
        f=open(self.name,'r+')
        txt=f.read()
        lst=list(txt)
        for i in range(0,times+1):
            lst.pop()
        txt=str(lst)
        f.write(txt)
        f.close()
def write(file,text='',way='.'):
    f=open(way+'\\'+file,'w')
    f.write(text)
    f.close()
def addtext(self,text=''):
    f=open(self.name,'a')
    f.write(text)
    f.close()
def remove(self,value='',times=1):
    f=open(self.name,'r+')
    text=f.read()
    for i in text:
        times-=1
        if i==value:
            text.replace(i,'')
        if times==0:
            break
def read(self):
    f=open(self.name,'r')
    txt=f.read()
    f.close()
    return txt
