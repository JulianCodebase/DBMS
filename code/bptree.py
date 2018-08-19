#!/usr/bin/env python
from random import randint, choice
from bisect import bisect_right, bisect_left
from collections import deque


#生成键值对
class KeyValue(object):
    __slots__=('key', 'value')
    def __init__(self, key, value):
        self.key=key
        self.value=value

    def __str__(self):
        return str((self.key, self.value))

    def __lt__(self, other):
        if (type(self) == type(other)):
            return self.key < other.key;
        else:
            return (self.key) < (other)

    def __eq__(self, other):
        if (type(self) == type(other)):
            return self.key == other.key
        else:
            return (self.key) == (other)

class BPtree(object):
    class __InterNode(object):
        def __init__(self, M):      #M代表阶数
            if not isinstance(M, int):
                raise ValueError('M must be int')
            if M<=3:
                raise ValueError('M must be greater than 3')
            else:
                self.__M=M
                self.childlist=[] #存放区间
                self.indexlist=[] #存放索引/序号
                self.par=None
        def isleaf(self):
            return False
        def isfull(self):   #关键值的数量是否装满
            return len(self.indexlist)>=self.M-1
        def isempty(self):
            return len(self.indexlist)<=(self.M+1)/2-1
        @property
        def M(self):
            return self.__M

    #叶结点
    class __Leaf(object):
        def __init__(self,L):
            if not isinstance(L,int):
                raise InitError('L must be int')
            else:
                self.__L=L
                self.vlist=[]
                self.bro=None #兄弟结点
                self.par=None #父结点
        def isleaf(self):
            return True
        def isfull(self):
            return len(self.vlist)>self.L
        def isempty(self):
            return len(self.vlist)<=(self.L+1)/2
        @property
        def L(self):
            return self.__L

    #初始化
    def __init__(self,M,L):
        if L>M:
            raise InitError('L must be less or equal than M')
        else:
            self.__M=M
            self.__L=L
            self.__root=BPtree.__Leaf(L)  #刚开始时根结点就是叶子结点
            self.__leaf=self.__root
    @property
    def M(self):
        return self.__M
    @property
    def L(self):
        return self.__L

    @property
    def leaf(self):
        return self.__leaf

    #插入
    def insert(self, key_value):
        node=self.__root
        def insert_node(n):
            if n.isleaf():               #走到了叶结点,先插入再考虑是否分裂结点
                p=bisect_right(n.vlist,key_value)
                n.vlist.insert(p,key_value)
                if n.isfull():
                    split_leaf(n)
                else:
                    return

            else:      #不是叶结点
                if n.isfull():
                    insert_node(split_node(n))
                else:
                    p=bisect_right(n.indexlist,key_value)
                    insert_node(n.childlist[p])


        def split_node(n1):
            mid=self.M//2 #此处注意，可能出错
            newnode=BPtree.__InterNode(self.M)
            newnode.indexlist=n1.indexlist[mid:]
            newnode.childlist=n1.childlist[mid:]
            newnode.par=n1.par
            for c in newnode.childlist:
                c.par=newnode
            if n1.par is None:  #如果待分裂结点是根结点
                newroot=BPtree.__InterNode(self.M)
                newroot.indexlist=[n1.indexlist[mid-1]]
                newroot.childlist=[n1,newnode]
                n1.par=newnode.par=newroot
                self.__root=newroot
            else:
                i=n1.par.childlist.index(n1)
                n1.par.indexlist.insert(i,n1.indexlist[mid-1])
                n1.par.childlist.insert(i+1,newnode)    #把分裂出的新结点加到原来根结点的孩子列表中
            n1.indexlist=n1.indexlist[:mid-1]
            n1.childlist=n1.childlist[:mid]
            return n1.par
        def split_leaf(n2):
            mid=(self.L+1)//2   #保证左边的索引值比右边的多
            newleaf=BPtree.__Leaf(self.L)
            newleaf.vlist=n2.vlist[mid:]
            if n2.par==None:
                newroot=BPtree.__InterNode(self.M)
                newroot.indexlist=[n2.vlist[mid].key]
                newroot.childlist=[n2,newleaf]
                n2.par=newleaf.par=newroot
                self.__root=newroot
            else:
                i=n2.par.childlist.index(n2)
                n2.par.indexlist.insert(i,n2.vlist[mid].key)
                n2.par.childlist.insert(i+1,newleaf)
                newleaf.par=n2.par
                newleaf.bro=n2.bro    #我不能忘记这个错误！！！！！！
            n2.vlist=n2.vlist[:mid]
            n2.bro=newleaf
        insert_node(node)

    #搜索
    def search(self,start=None,end=None):
        result=[]
        node=self.__root
        leaf=self.__leaf
        # if start is None or end is None:
        #     raise ParaError('you need to setup searching range')
        if start and end and start > end:
            raise ParaError('upper bound must be greater or equal than lower bound')
        def search_key(n,k):
            if n.isleaf():          #在叶子结点中找到键值
                p=bisect_left(n.vlist,k)
                return (p,n)        #返回键值和相应的结点值
            else:
                p=bisect_right(n.indexlist,k)       #右子树的索引值大于等于父结点索引值
                return search_key(n.childlist[p],k)
        if not start and end:
            while True:
                for kv in leaf.vlist:       #若vlist为空则循环体不会执行
                    if kv<=end:
                        result.append(kv)
                    else:
                        return result
                if leaf.bro==None:
                    return result
                else:
                    leaf=leaf.bro
        elif start and not end:      #如果没有设置结束边界值就把索引值右侧的所有关键值返回
            index,leaf=search_key(node,start)
            result.extend(leaf.vlist[index:])
            while True:
                if leaf.bro==None:
                    return result
                else:
                    leaf=leaf.bro
                    result.extend(leaf.vlist)
        elif not start and not end:
            while True:
                result.extend(leaf.vlist)
                if leaf.bro == None:
                    return result
                else:
                    leaf = leaf.bro
        else:
            if start==end:
                i,l=search_key(node,start)
                try:
                    if l.vlist[i]==start:
                        result.append(l.vlist[i])
                        return result
                    else:           #未找到索引值
                        return result
                except IndexError:
                    return result
            else:
                i1,l1=search_key(node,start)
                i2,l2=search_key(node,end)
                if l1 is l2:        #如果查找的索引值在同一个叶子结点上
                    if i1==i2:      #未找到该索引值
                        return result
                    else:
                        result.extend(l2.vlist[i1:i2])
                        return result
                else:
                    result.extend(l1.vlist[i1:])
                    l=l1
                    while True:
                        if l.bro==l2:
                            result.extend(l2.vlist[:i2])
                            return result
                        elif l.bro != None:
                            result.extend(l.bro.vlist)
                            l=l.bro
                        else:
                            return result;
    def traversal(self):
        result=[]
        l=self.__leaf
        while True:
            result.extend(l.vlist)
            if l.bro==None:
                return result
            else:
                l=l.bro
    def show(self):
        q=deque()
        result = {}
        h=0         #根结点的高度设为0
        q.append([self.__root,h])
        while True:
            try:
                w,height=q.popleft()
                if height not in result:
                    if w.isleaf():
                        result.setdefault(height, [[(v.key,v.value) for v in w.vlist]])
                    else:
                        result.setdefault(height, [w.indexlist])
                else:
                    if w.isleaf():
                        result[height].append([(v.key,v.value) for v in w.vlist])
                    else:
                        result[height].append(w.indexlist)
            except IndexError:
                return  result
            else:
                if w.isleaf():
                    pass
                    # print([(v.key,v.value) for v in w.vlist],'the leaf is,',height)
                else:
                    # print(w.indexlist,'the height is',height)
                    if height==h:
                        h+=1
                    q.extend([[i,h] for i in w.childlist])

    #删除
    def delete(self,key_value):
        def del_node(n,kv):
            if n.isleaf():      #如果待删除的键值在叶子结点上,则直接删除
                p=bisect_left(n.vlist,kv)
                try:
                    pp=n.vlist[p]
                except IndexError:
                    return -1
                else:
                    if pp!=kv:      #未找到索引值
                        return -1
                    else:
                        n.vlist.remove(kv)
                        return 0
            else:
                p=bisect_right(n.indexlist,kv)   #注意这里是indexlist
                if p==len(n.indexlist):
                    if not n.childlist[p].isempty():
                        return del_node(n.childlist[p],kv)
                    elif not n.childlist[p-1].isempty():    #如果p结点不可再拆分
                        tran_l2r(n,p-1)
                        return del_node(n.childlist[p],kv)
                    else:                         #n.childlist[p] is empty and n.childlist[p-1] is empty
                        return del_node(merge(n,p-1),kv)
                else:
                    if not n.childlist[p].isempty():        #isempty: len(self.vlist)<=(self.L+1)/2
                        return del_node(n.childlist[p],kv)
                    elif not n.childlist[p+1].isempty():
                        tran_r2l(n,p)
                        return del_node(n.childlist[p],kv)
                    else:
                        return del_node(merge(n,p),kv)

        def modify_index(n,kv):
            if not n.isleaf():
                p=bisect_right(n.indexlist, kv)
                try:
                    pp=n.indexlist[p-1]
                except IndexError:
                    return -1
                else:
                    if pp!=kv:
                        modify_index(n.childlist[p],kv)
                    else:
                        if not n.childlist[p].isleaf():
                            n.indexlist[p-1] = n.childlist[p].indexlist[0]
                        else:
                            n.indexlist[p-1] = n.childlist[p].vlist[0].key
                        return 0


        def merge(n,i):
            if n.childlist[i].isleaf():
                n.childlist[i].vlist=n.childlist[i].vlist+n.childlist[i+1].vlist
                n.childlist[i].bro=n.childlist[i+1].bro
            else:
                n.childlist[i].indexlist=n.childlist[i].indexlist+[n.indexlist[i]]+n.childlist[i+1].indexlist   #[n.indexlist[i]]
                n.childlist[i].childlist=n.childlist[i].childlist+n.childlist[i+1].childlist
            n.childlist.remove(n.childlist[i+1])
            n.indexlist.remove(n.indexlist[i])
            if n.indexlist==[]:
                n.childlist[0].par=None
                self.__root=n.childlist[0]
                del n
                return self.__root
            else:
                return n
        def tran_l2r(n,i):
            if not n.childlist[i].isleaf():     #如果是叶子结点就直接向左边的叶子结点
                n.childlist[i+1].childlist.insert(0,n.childlist[i].childlist[-1])
                n.childlist[i].childlist[-1].par=n.childlist[i+1]
                n.childlist[i+1].indexlist.insert(0,n.indexlist[i])     #把父结点的索引拿下来
                n.indexlist[i]=n.childlist[i].indexlist[-1]
                n.childlist[i].childlist.pop()
                n.childlist[i].indexlist.pop()
            else:
                n.childlist[i+1].vlist.insert(0,n.childlist[i].vlist[-1])
                n.childlist[i].vlist.pop()
                n.indexlist[i]=n.childlist[i+1].vlist[0].key
        def tran_r2l(n,i):
            if not n.childlist[i].isleaf():
                n.childlist[i].childlist.append(n.childlist[i+1].childlist[0])
                n.childlist[i+1].childlist[0].par=n.childlist[i]
                n.childlist[i].indexlist.append(n.indexlist[i])
                n.indexlist[i]=n.childlist[i+1].indexlist[0]
                n.childlist[i+1].childlist.remove(n.childlist[i+1].childlist[0])
                n.childlist[i+1].indexlist.remove(n.childlist[i+1].indexlist[0])
            else:
                n.childlist[i].vlist.append(n.childlist[i+1].vlist[0])
                n.childlist[i+1].vlist.remove(n.childlist[i+1].vlist[0])
                n.indexlist[i]=n.childlist[i+1].vlist[0].key

        if del_node(self.__root,key_value) == 0:
            modify_index(self.__root,key_value)

def test():
    #初始化数据源
    mini=50
    maxi=200
    testlist=[]
    ll = []
    for i in range(20):
        key=i#randint(1,1000)
        #key=i
        value=choice(['Do', 'Re', 'Mi', 'Fa', 'So', 'La', 'Si'])
        testlist.append(KeyValue(key,value))
        ll.append(key)

    #初始化B树
    mybptree=BPtree(5, 5)

    #插入
    for x in testlist:
        mybptree.insert(x)

    result = mybptree.show()
    a = [str(result[i])[1:-1] + '\n' for i in result]
    print(a)
    #查找
    print([(v.key,v.value) for v in mybptree.search(18,18)])


    #删除
    # mybptree.delete(testlist[0])
    # print('\n删除 {0}后， the newtree is:\n'.format(testlist[0]));
    # mybptree.show()



    #深度遍历
    # print('\nkey of this b+tree is \n')
    # print([kv.key for kv in mybptree.traversal()])




if __name__ == '__main__':
    test();

#</span>