## 项目概述
　　基于Python，利用PyQt框架开发一个类似于DBMS软件的GUI程序，用于模拟建立、使用和维护数据库。 通过正则表达式实现该系统中的语法和语义检查模块
 为数据库表的主属性建立索引，分主属性有序、主属性无序两种情况，为数据库表的非主属性建立索引，分非主属性有序、非主属性无序两种情况，实现数据增删改时索引的维护功能，实现创建数据库用户并完成权限管理功能，对数据各种操作通过操作保存在本地文件系统中的文件实现的。<br>
　　开发环境：Python3.5, Sublime Text3, PyQt5, Designer
## 项目目录结构
.<br>
├─code<br>
│  ├─rcc---------资源文件<br>
│  ├─table<br>
│  │  ├─dict---------存储数据字典<br>
│  │  ├─index---------存储索引关系<br>
│  │  ├─tables---------存储表数据<br>
│  │  └─users---------存储用户信息<br>
│  ├─__pycache__---------程序编译得到的字节码文件<br>
│  ├─apprcc_rc.py----------资源文件转换<br>
│  ├─apprcc2_rc.py---------资源文件转换<br>
│  ├─bptree.py---------B+树设计<br>
│  ├─databaseframe.py---------界面和逻辑业务交互<br>
│  ├─filemanage.py---------将操作结果写入文件<br>
│  ├─loginfr.py---------登录界面设计<br>
│  ├─MainWindow.py---------主界面设计<br>
│  └─regex.py---------负责处理/检验SQL语句<br>
└─elements---------GitHub资源文件<br>
## 项目展示
　　　　　　　　　　　![](https://github.com/AlenaRuicheng/DBMS/blob/master/elements/执行SQL.png)
　　　　　　　　　　　　　　　　　　　　　　　　图1  执行SQL<br>
　　　　　　　　　　　![](https://github.com/AlenaRuicheng/DBMS/blob/master/elements/权限管理.png)
　　　　　　　　　　　　　　　　　　　　　　　　图2  权限管理<br>
　　　　　　　　![](https://github.com/AlenaRuicheng/DBMS/blob/master/elements/数据索引.png)
　　　　　　　　　　　　　　　　　　　　　　　　图3  数据索引<br>
 
