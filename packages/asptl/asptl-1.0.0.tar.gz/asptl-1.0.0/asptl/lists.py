class adellist(list):
    
    def __init__(self,*arg):
        super().__init__(arg)
    def get(self):#get the values in adellist
        return self
    def elements(self,up=0,down=1):#get list[int:int]
        return self[up:down]
    def add(self,text=None):#add one value into the list
        self.append(text)
        return self
    def addelems(self,*arg):#add values into the list
        for i in arg:
            self.append(i)
    def sort(self,error=False,reverse=False,error_text=True):#sort the list(int list)
        try:
            super().sort(reverse=reverse)
        except TypeError as e:
            if error:
                if not error_text:
                    raise TypeError(e)
                else:
                    print(e)
    #def pop(self,index=-1):#remove one value from the list
    #    super().pop(index)
    #def clear(self):#clear th list
    #    super().clear()
    #def remove(self,value,error=True):
    #    try:
    #        super().remove(value)
    #    except ValueError as v:
    #        if error:
    #            raise ValueError(v)
    #def copy(self):
    #    return self.copy()


class readerlist(list):
    def __init__(self,*arg):
        super().__init__(arg)
    def get(self):
        return self
    def add(self,text=None):
        self.append(text)
        return self
    #def pop(self,index=-1):
    #    self.pop(index)
    #def clear(self):
    #    self.clear()
    def __find(self,value,times=1):
        lst=[]
        list2=self.copy()
        for i in list2:
            times-=1
            if i==value:
                lst.append(self.index(i))
                list2[list2.index(i)]=str(value)+'iscoded'
            if times==0:break
        return lst
    def count(self,value):
        n=0
        for i in self:
            if i==value:
                n+=1
        return n
    #def copy(self):
    #    return self.copy()

class queue():
    def __init__(self):
        self.__text=[]
    def push(self,s):
        self.__text.append(s)
    def size(self):
        return len(self.__text)
    def front(self):
        class qError(Exception):
            def __init__(self,e):
                super().__init__(e)
    
        if self.size()>0:
            return self.__text[0]
        else:
            raise qError('QueueIsEmptyError:Queue is empty.Please use push before using front()')
    def pop(self):
        if self.size()>0:
            self.__text.pop(0)
        else:
            class qError(Exception):
                def __init__(self,e):
                    super().__init__(e)
            raise qError('QueueIsEmptyError:Queue is empty.Please use push before using pop()')

class stack():
    def __init__(self):
        self.__text=[]
    def push(self,s):
        self.__text.append(s)
    def size(self):
        return len(self.__text)
    def top(self):
        class sError(Exception):
            def __init__(self,e):
                super().__init__(e)
    
        if self.size()>0:
            return self.__text[len(self.__text)-1]
        else:
            raise sError('StackIsEmptyError:Stack is empty.Please use push before using top()')
    def pop(self):
        if self.size()>0:
            self.__text.pop(len(self.__text)-1)
        else:
            class sError(Exception):
                def __init__(self,e):
                    super().__init__(e)
            raise sError('StackIsEmptyError:Stack is empty.Please use push before using pop()')

        
