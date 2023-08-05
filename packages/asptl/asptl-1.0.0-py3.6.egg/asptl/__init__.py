#由 AmirSong(pypi)独家开发

#封装了许多常用组件

#包括 文件读写 列表等
#--------------------------
#Exclusively developed by AmirSong (pypi)

#It encapsulates many common components

#Including file read-write list, etc
#--------------------------


'''
    use it!!!
    
    >>>from mypybag import lists
    >>>l=adellist(1,'a',True,None)
    >>>l.get():
    [1,'a',True,None]
    >>>l.elements(0,1)
    [1]
    >>>l.add('hello')
    [1,'a',True,None,'hello']
    >>>a.pop()
    >>>a.get()
    [1,'a',True,None]
    >>>a.clear()
    >>>a.get()
    []
    >>>a.addelems(1,'1')
    >>>a.get()
    [1,'1']
    >>>a.remove(1)
    >>>a.get()
    ['1']
    >>>b=a.copy()
    >>>b
    ['1']

'''

__all__={
    'list':['adellist','readerlist'],
    'file':'File',
    '……':'……'
    }
    
import mypybag.lists
import mypybag.file
import mypybag.windows
import mypybag.thread
