import re
from collections import namedtuple

class RegMatch(object):
    regs = []
    def __init__(self):
        reg1 = re.compile(r'''\s*select\s+(\w+\.\w+|\*)(?:\s*,\s*(\w+\.\w+))*\s+
                              from\s+(\w+)(?:\s*,\s*(\w+))*
                              (\s+where\s+(?P<where>(\w+\.\w+)\s*(?:<|>|=|>=|<=|!=)\s*(\w+\.\w+|'\w+'|\d+(?:\.\d+)?)
                              (?:\s+and\s+(\w+\.\w+)\s*(?:<|>|=|>=|<=|!=)\s*(\w+\.\w+|'\w+'|\d+(?:\.\d+)?))*))?\s*$''',re.I | re.X)

        reg2 = re.compile(r'''\s*insert\s+into\s+(\w+)\s+values\s*
                              \((?P<values>\s*('\w+'|\d+(?:\.\d+)?)(?:\s*,\s*('\w+'|\d+(?:\.\d+)?))*)\s*\)\s*$''',re.I | re.X)

        reg3 = re.compile(r'''\s*update\s+(\w+)\s+set\s+(?P<update>\w+\s*=\s*('\w+'|\d+(?:\.\d+)?)(?:\s*,\s*\w+\s*=\s*('\w+'|\d+(?:\.\d+)?))*)
                                (\s+where\s+(?P<where>(\w+)\s*(?:<|>|=|>=|<=|!=)\s*('\w+'|\d+(?:\.\d+)?)
                                (?:\s+and\s+(\w+)\s*(?:<|>|=|>=|<=|!=)\s*('\w+'|\d+(?:\.\d+)?))*))?\s*$''',re.I | re.X)

        reg4 = re.compile(r'''\s*delete\s+from\s+(\w+)(?:\s+
                               where\s+(?P<where>\w+\s*(?:<|>|=|>=|<=|!=)\s*('\w+'|\d+(?:\.\d+)?)
                               (?:\s+and\s+(\w+)\s*(?:<|>|=|>=|<=|!=)\s*('\w+'|\d+(?:\.\d+)?))*))?\s*$''',re.I | re.X)

        reg5 = re.compile(r'''\s*drop\s+table\s+(\w+)\s*$''')

        reg6 = re.compile(r'''\s*alter\s+table\s+(\w+)\s+drop\s+index\s+(?P<index>\w+)\s*$''', re.I | re.X)

        reg7 = re.compile(r'''\s*create\s+table\s+(\w+)\s*\((?P<properties>\s*\w+\s+\w+\s*\(\s*\d+\s*\)\s*(?P<key>primary\s+key)?
                            (\s+\w+\s+\w+\s*\(\s*\d+\s*\)\s*)*)\)\s*$''',re.I | re.X)

        reg8 = re.compile(r'''\s*create\s+index\s+(?P<index>\w+)\s+on\s+(?P<tablename>\w+)\s*\(\s*(?P<column>\w+)\s*\)\s*$''', re.I | re.X)

        reg9 = re.compile(r'''\s*alter\s+table\s+(\w+)\s+drop\s+column\s+(?P<column>\w+)\s*$''', re.I | re.X)

        reg10 = re.compile(r'''\s*alter\s+table\s+(\w+)\s+add\s+(?P<column>\w+)\s+(?P<properties>\w+\s*\(\s*\d+\s*\))\s*$''', re.I | re.X)

        reg11 = re.compile(r'''\s*grant\s+(?P<competence>select|insert|update|delete)\s+on\s+(?P<tablename>\w+)\s+to\s+(?P<username>\w+)\s*$''', re.I | re.X)

        reg12 = re.compile(r'''\s*revoke\s+(?P<competence>select|insert|update|delete)\s+on\s+(?P<tablename>\w+)\s+from\s+(?P<username>\w+)\s*$''', re.I | re.X)
        # alter table uu add age int(20)
        # alter table uu drop column birthday
        # update uu set name=1, age=1 where age=2

        self.regs = {'select':reg1, 'insert':reg2, 'update':reg3, 'delete':reg4,'drop':reg5, 'dropIndex':reg6, 'createTable':reg7,
                      'createIndex':reg8,'dropColumn':reg9,'addColumn':reg10, 'grant':reg11, 'revoke':reg12}

    def matchsql(self,sql):
        result = []
        #-----------------------------------------SELECT----------------------------------------
        if sql.split()[0].lower() == 'select':
            matched = self.regs['select'].match(sql)
            if matched:
                result.append(['select'])
                if matched.group(2):
                    properties = [i.strip() for i in sql[matched.start(1) : matched.end(2)].strip().split(',')]
                else:
                    properties = [matched.group(1)]
                if matched.group(4):
                    tables = [i.strip() for i in sql[matched.start(3) : matched.end(4)].strip().split(',')]
                else:
                    tables = [matched.group(3)]
                result.append(tables)
                result.append(properties)
                if matched.group('where'):
                    result.append(matched.group('where').strip().split('and'))
                return result
        #-----------------------------------------CREATE TABLE----------------------------------------
        if sql.lower().split()[:2] == ['create','table']:
            matched = self.regs['createTable'].match(sql)
            if matched:
                result.append(['create table'])
                result.append([matched.group(1)])
                pts = matched.group('properties').split()
                if matched.group('key'):
                    result.append(pts[:4])
                    for i in pts[4::2]:
                        index = pts.index(i)
                        result.append(pts[index:index+2])
                else:
                    for i in pts[::2]:
                        index = pts.index(i)
                        result.append(pts[index:index+2])
                return result
        #-----------------------------------------CREATE INDEX----------------------------------------
        if sql.lower().split()[:2] == ['create','index']:
            matched = self.regs['createIndex'].match(sql)
            if matched:
                result.append(['create index'])
                result.append([matched.group('tablename')])
                result.append([matched.group('column')])
                result.append([matched.group('index')])
                return result
        #-----------------------------------------INSERT----------------------------------------
        if sql.split()[0].lower() == 'insert':
            matched = self.regs['insert'].match(sql)
            if matched:
                result.append(['insert'])
                result.append([matched.group(1)])
                result.append(matched.group('values').split(','))
                return result
        #-----------------------------------------UPDATE----------------------------------------
        if sql.split()[0].lower() == 'update':
            matched = self.regs['update'].match(sql)
            if matched:
                result.append(['update'])
                result.append([matched.group(1)])
                result.append(matched.group('update').split(','))
                if matched.group('where'):
                    result.append(matched.group('where').split('and'))
                return result
        #-----------------------------------------DELETE----------------------------------------
        if sql.split()[0].lower() == 'delete':
            matched = self.regs['delete'].match(sql)
            if matched:
                result.append(['delete'])
                result.append([matched.group(1)])
                if matched.group('where'):
                    result.append(matched.group('where').split('and'))
                return result
        #-----------------------------------------DROP COLUMN----------------------------------------
        if re.match(r'\s*alter\s+table\s+\w+\s+drop\s+column\s+',sql.lower()):#删除表属性
            matched = self.regs['dropColumn'].match(sql)
            if matched:
                result.append(['drop column'])
                result.append([matched.group(1)])
                result.append([matched.group('column')])
                return result
        #-----------------------------------------DROP INDEX----------------------------------------
        if re.match(r'\s*alter\s+table\s+\w+\s+drop\s+index\s+',sql.lower()):#删除索引
            matched = self.regs['dropIndex'].match(sql)
            if matched:
                result.append(['drop index'])
                result.append([matched.group(1)])
                result.append([matched.group('index')])
                return result
        #-----------------------------------------TABLE ADD----------------------------------------
        if re.match(r'\s*alter\s+table\s+\w+\s+add\s+',sql.lower()):#增加表属性
            matched = self.regs['addColumn'].match(sql)
            if matched:
                result.append(['add column'])
                result.append([matched.group(1)])
                result.append([matched.group('column')])
                result.append([matched.group('properties').replace(' ','')])
                return result
        #-----------------------------------------DROP TABLE----------------------------------------
        if sql.lower().split()[:2] == ['drop', 'table']:#删表
            matched = self.regs['drop'].match(sql)
            if matched:
                result.append(['drop table'])
                result.append([matched.group(1)])
                return result

        #-----------------------------------------GRANT----------------------------------------
        if sql.lower().split()[0] == 'grant':#授权
            matched = self.regs['grant'].match(sql)
            if matched:
                result.append(['grant'])
                for i in matched.groups():
                    result.append([i])
                return result

        #----------------------------------------REVOKE----------------------------------------
        if sql.lower().split()[0] == 'revoke':#撤销权限
            matched = self.regs['revoke'].match(sql)
            if matched:
                result.append(['revoke'])
                for i in matched.groups():
                    result.append([i])
                return result

        return "不能识别的语句,请检查语法并重新输入."
if __name__ == '__main__':
    sql = input('sql:')
    regex = RegMatch()
    print(regex.matchsql(sql))
#insert into student values('hjk', 123, '10')
#update student set id = 1000 where birth >=1234 and birth <='1235'
#update uu set name=1, age=1 where age=2
#delete from student where name= 'a'
#create index aindex on student(id)
#select student.name from student where student.name = 1
#select * from student where student.name = 'Alice'
#alter table aa drop column birth
#delete from aa where name != 'Tim'
#
#{'student': [['name', 'char'], ['id', 'int'], ['birth', 'char']]}
# ['Alice 1000 1993\n', 'Mark 1002 2563\n', 'Mike 1003 8569\n', 'Tim 1100 8563\n', 'Jimmy 1005 9527\n', 'Roma 1006 5986\n', 'Tonnia 1007 2385\n', 'EWQ 1234 8523\n']
# [Finished in 0.3s]
# select * from student where student.name = 'Alice' and student.id = 1000
# select * from student, course where student.id = course.studentid
# select student.name from student, course where student.id = course.studentid
# select student.name, course.name from student,  course where student.id = 1000 and course.serialnumber > 8
# select student.name from student , course where student.id = course.studentid and student.id=1000
# select student.name,course.name, course.serialnumber from student , course where student.id=1000
# select student.name,course.name from student , course where student.id=1000   #笛卡尔积
# select student.id, student.name , course.name from student, course where student.id = course.studentid and student.id = 1000   #表连接
# grant update on course to abc
# revoke select on course from qwe
# select a.name,b.name,c.name from a,b,c
# select student.name, course.name from student, course where student.id = course.studentid
