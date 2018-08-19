import os,re,copy
import bptree

def get_all_files(rootdir):
    return os.listdir(rootdir)

def isExist(rootdir, file):
    return file in os.listdir(rootdir)

def write_dict_to_file(dirname, filename,content):
    f = open(dirname+'\\dict\\'+filename,'w',encoding='utf8')
    for cont in content:
        for row in cont:
            f.write(row + ' ')
        f.write('\n')
    f = open(dirname+'\\tables\\'+filename,'w', encoding='utf8')
    f.close()

def is_valid_arguments(file,arguments):
    f = open(file, 'r', encoding='utf8')
    lines = f.readlines()
    if len(arguments) != len(lines):
        f.close()
        return '参数太少或太多,请核对表属性.'
    types = {'int':'int', 'str':('char','varchar'), 'float':('float','double')} #设置三种数据类型
    for i in range(len(lines)): #not isinstance(arguments[i], types[lines[i] [:lines[i].index('(')].split()[-1] ] ):
        if ("'" in arguments[i] and lines[i][:lines[i].index('(')].split()[-1] in types['str']) \
        or ("." in arguments[i] and lines[i][:lines[i].index('(')].split()[-1] in types['float'])\
        or ("." not in arguments[i] and "'" not in arguments[i] and lines[i][:lines[i].index('(')].split()[-1] in types['int']):
            continue
        else:
            f.close()
            return '数据添加失败,参数类型不匹配.'
    f.close()
    return True

def write_data_to_file(file,content):       #向表中写入数据
    f = open(file,'a',encoding='utf8')
    for cont in content:
        if "'" in cont:
            f.write(cont.strip().strip("'").strip()+' ')
        else:
            f.write(cont.strip()+' ')
    f.write('\n')
    f.close()

def is_correct_type(arguments, table_dict):
    arg1 = arguments[0]
    for i in arg1:
        operator = re.sub("[a-zA-Z0-9\s'.]",'',i)
        value = i[i.index(operator)+1:].strip()
        mytype = table_dict[i[:i.index(operator)].strip()]
        if "'" in value and mytype in 'char|varchar'\
        or ("." in value and mytype in 'float|double')\
        or ("." not in value and "'" not in value and mytype in 'int'):
            continue
        else:
            return i[:i.index(operator)].strip()+'是'+mytype+'类型的值.'
    if len(arguments)>1:
        arg2 = arguments[1]
        for i in arg2:
            operator = re.sub("[a-zA-Z0-9\s'.]",'',i)
            if len(operator) == 1:
                value = i[i.index(operator)+1:].strip()
            else:
                value = i[i.index(operator)+2:].strip()
            mytype = table_dict[i[:i.index(operator)].strip()]
            if "'" in value and mytype in 'char|varchar'\
            or ("." in value and mytype in 'float|double')\
            or ("." not in value and "'" not in value and mytype in 'int'):
                continue
            else:
                return i[:i.index(operator)].strip()+'是'+mytype+'类型的值.'
    return True


def is_valid_data(file, arguments):
    f = open(file,'r',encoding='utf8')
    lines = f.readlines()
    f.close()
    strs = [line.split() for line in lines]     #列表解析
    table_dict = {k:v[:v.index('(')] for k,v in strs}   #字典生成器
    arg1 = arguments[0]
    for i in arg1:
        operator = re.sub("[a-zA-Z0-9\s'.]",'',i)
        ii = i[:i.index(operator)].strip()
        if ii not in table_dict:
            return "'"+ii+"'属性不存在,请核对后重新输入"
    if len(arguments) > 1:
        arg2 = arguments[1]
        for i in arg2:
            operator = re.sub("[a-zA-Z0-9\s'.]",'',i)
            ii = i[:i.index(operator)].strip()
            if ii not in table_dict:
                return "'"+ii+"'属性不存在,请核对后重新输入"
    is_correct = is_correct_type(arguments, table_dict)
    if is_correct != True:
        return is_correct
    return True

def find_needed_lines(content,location_dict, lines_data):   #找到满足where条件的所有行
    lines_list = []
    for line_num in range(len(lines_data)):
        strs_list = lines_data[line_num].split()
        for j in content[-1]:
            operator = re.sub("[a-zA-Z0-9\s'.]",'',j)
            request_item = [j[:j.index(operator)].strip(),j[j.index(operator):].strip()]
            if operator == '=':
                request_item[-1] = '='+request_item[-1]         #两个等号才能做判断
            if isinstance(strs_list[location_dict[ request_item[0] ] ], int):
                strs_list[location_dict[ request_item[0] ] ] = int(strs_list[location_dict[ request_item[0] ] ])
            ev = eval("strs_list[location_dict[ request_item[0] ] ]" + request_item[-1])
            if not ev:
                break;     #若不满足where条件,则直接跳转到下一行
        if ev:      #最后一个条件也满足，那么where的所有条件都满足
            lines_list.append(line_num)
    return lines_list

def update_file(dirname, filename, content):   #修改文件中的某一行,把文件内容全部读入内存，在内存中修改之后再写回文件中。这个方法有缺陷
    f = open(dirname+'\\dict\\'+filename,'r')
    lines_dict = f.readlines()
    f.close()
    location_dict = {line.split()[0]:lines_dict.index(line) for line in lines_dict}   #字典生成器,用于记录每个表属性在数据文件中的列数

    f = open(dirname+'\\tables\\'+filename,'r')
    lines_data = f.readlines()
    f.close()
    if len(content) == 1:   #没有where语句
        lines_num = [i for i in range(len(lines_data))]
    else:
        lines_num = find_needed_lines(content,location_dict, lines_data)
        if not lines_num:
            return '数据库表数据更新失败,因为没有满足where条件的元组.'

    for i in lines_num:
        strs_list = lines_data[i].split()
        for j in content[0]:
            operator = re.sub("[a-zA-Z0-9\s'.]",'',j)
            update_item = [j[:j.index(operator)].strip(),j[j.index(operator)+1:].strip()]     #把变更属性等式分开
            strs_list[location_dict[ update_item[0] ] ] = update_item[-1].strip("'")
        lines_data[i] = ' '.join(strs_list)+'\n'

    f=open(dirname+'\\tables\\'+filename,'w')
    f.writelines(lines_data)
    f.close()
    lines_num = [i+1 for i in lines_num]
    return filename[:-4] + '表数据更新成功.其中第'+str(lines_num)+'行数据发生了变化.'

def delete_file_data(dirname, filename, content):
    if len(content) < 3:   #没有where语句
        f = open(dirname+'\\tables\\'+filename,'w')
        f.close()
        return filename[:-4] + '表数据已全部清除.'
    #有where语句
    content = content[2:]
    f = open(dirname+'\\dict\\'+filename,'r')
    lines_dict = f.readlines()
    f.close()
    f = open(dirname+'\\tables\\'+filename,'r')
    lines_data = f.readlines()
    f.close()
    location_dict = {line.split()[0]:lines_dict.index(line) for line in lines_dict}
    lines_num = find_needed_lines(content,location_dict, lines_data)
    if not lines_num:
        return '数据库表数据删除失败,因为没有满足where条件的元组.'
    tmp = [lines_data[i] for i in lines_num]
    for i in tmp:
        lines_data.remove(i)
    f=open(dirname+'\\tables\\'+filename,'w')
    f.writelines(lines_data)
    f.close()
    lines_num = [i+1 for i in lines_num]
    # for i in os.listdir(dirname+'\\index\\'):       #索引表里相应数据也要删除
    #     if filename[:-4] in i[:i.index('_')]:
    #         f = open(dirname+'\\index\\'+i,'r',encoding = 'utf8')
    #         lines = f.readlines()
    #         f.close()
    #         for line in lines:
    #             print('lines:',lines)
    #             if int(line.split()[-1])+1 in lines_num:
    #                 lines.remove(line)
    #         f = open(dirname+'\\index\\'+i,'w',encoding = 'utf8')
    #         f.writelines(lines)
    #         f.close()
    return filename[:-4] + '表数据更新成功.其中第'+str(lines_num)+'行数据被删除了.'

def create_index_bytree(dirname, filename, content):
    #当前只能建立一个索引
    if isExist(dirname+'\\index\\', filename+'_'+content[1][0]+'.txt'):
        return '当前索引已经存在,无需重复建立'
    #检查输入属性是否存在
    f = open(dirname + '\\dict\\' + filename+'.txt','r',encoding='utf8')
    lines_dict = f.readlines()
    f.close()
    columns = [line.split()[0] for line in lines_dict]
    if content[1][0] not in columns:
        return "'"+content[1][0]+"'属性不存在,请核对后重新输入"

    f = open(dirname + '\\tables\\' + filename+'.txt', 'r', encoding='utf8')
    lines_data = f.readlines()
    f.close()
    index_value = {index.split()[columns.index(content[1][0])]:value for value,index in enumerate(lines_data)}

    index_tree = bptree.BPtree(4, 4)    #构造一个4阶B+树,叶结点和内部结点保存的数据个数
    kv_list = []
    for index in index_value:
        kv_list.append(bptree.KeyValue(index, index_value[index]))
    #插入数据
    for i in kv_list:
        index_tree.insert(i)

    index_dict = index_tree.show()
    items = [str(index_dict[i])[1:-1] + '\n' for i in index_dict]
    f = open(dirname + '\\index\\' + filename+'_'+content[1][0]+'.txt', 'w', encoding='utf8')
    f.writelines(items)
    f.close()
    return "成功为"+content[0][0]+"表的"+content[1][0]+"属性建立了名为'"+content[2][0]+"'的索引"


def select_data_from_file(dirname, filenames, content):     #dirname = r'D:\PySubjects\database3\table'
    #如果有索引，则优先按索引查找
    files_dict = {}
    data_dict = {}
    for file in filenames:
        if isExist(dirname+'\\dict\\',file +'.txt'):
            f = open(dirname+'\\dict\\'+ file +'.txt', 'r', encoding = 'utf8')
            lines = f.readlines()
            f.close()
            lines = [i[:i.index('(')].split() for i in lines]
            files_dict.setdefault(file,lines)
        else:
            return file + '表不存在'
    for i in content[0]:    #处理select属性
        if '*' in i:
            break
        if i[:i.index('.')] not in files_dict:
            return i[:i.index('.')] + '表不存在'
        former_type_list = [i[0] for i in files_dict[i[:i.index('.')]]]
        if i[i.index('.')+1:] not in former_type_list:
            return i[:i.index('.')] + "表中没有'" + i[i.index('.')+1:] + "'的属性"
    for file in filenames:  #读入文件数据
        f = open(dirname+'\\tables\\'+ file +'.txt', 'r', encoding = 'utf8')
        lines = f.readlines()
        f.close()
        data_dict.setdefault(file,lines)

    index_dict = {}
    for indexfile in os.listdir(dirname+'\\index\\'):   #如果有索引把索引表打开并保存
        f = open(dirname+'\\index\\'+ indexfile, 'r', encoding = 'utf8')
        index_str = f.readlines()[-1]
        f.close()
        indexfile = indexfile[:indexfile.index('.txt')]
        index_dict.setdefault(indexfile,{})
        for index in re.findall(r"'[a-zA-Z0-9]+', \d+",index_str):
            index = index.replace("'", '').split(', ')
            if index[0] in index_dict[indexfile]:
                index_dict[indexfile][index[0]].append(index[-1])
            else:
                index_dict[indexfile].setdefault(index[0], [index[-1]])

    result = files_dict.fromkeys(files_dict,'')
    for i in result:
        result[i] = []
    linked = False    #设置一个标记，标识是否有表连接
    if len(content) > 1:    #先做选择
        tmp_dict = copy.deepcopy(data_dict)
        for cont in content[-1]:   #检查where条件
            cont = cont.strip()
            if cont[:cont.index('.')] not in files_dict:
                return cont[:cont.index('.')] + '表不存在'

            operator = re.sub("[a-zA-Z0-9\s'.]",'',cont)
            former = cont[:cont.index(operator)].strip()        #former表示运算符之前的属性
            if len(operator) == 1:
                latter = cont[cont.index(operator)+1:].strip()  #latter表示运算符之后的属性
            else:
                latter = cont[cont.index(operator)+2:].strip()  #运算符长度为2，比如>=,!=等等

            former_type_list = [i[0] for i in files_dict[former[:former.index('.')]]]
            if former[former.index('.')+1:] not in former_type_list:
                return former[:former.index('.')] + "表中没有'" + former[former.index('.')+1:] + "'的属性"

            if re.match('[a-zA-Z]+\.[a-zA-Z]+', latter):    #有表连接先处理表连接
                linked = True  #表示有表连接
                latter_type_list = [i[0] for i in files_dict[latter[:latter.index('.')]]]
                if latter[:latter.index('.')] not in files_dict:
                    return latter[:latter.index('.')] + '表不存在'
                if latter[latter.index('.')+1:] not in latter_type_list:
                    return latter[:latter.index('.')] + "表中没有'" + latter[latter.index('.')+1:] + "'的属性"
                former_table = data_dict[former[:former.index('.')]]
                latter_table = data_dict[latter[:latter.index('.')]]
                greater, less = (former_table, latter_table) if len(former_table) > len(latter_table) else (latter_table, former_table)
                #取出表属性对应的列号
                for former_column in range(len(files_dict[former[:former.index('.')]])):
                    if files_dict[former[:former.index('.')]][former_column][0] == former[former.index('.')+1:]:
                        break
                for latter_column in range(len(files_dict[latter[:latter.index('.')]])):
                    if files_dict[latter[:latter.index('.')]][latter_column][0] == latter[latter.index('.')+1:]:
                        break
                #表查询优化
                for ls in less:
                    for gt in greater:
                        if less == former_table:
                            if ls.split()[former_column] == gt.split()[latter_column]:
                                result[former[:former.index('.')]].append(ls)
                                result[latter[:latter.index('.')]].append(gt)
                        else:
                            if ls.split()[latter_column] == gt.split()[former_column]:
                                result[latter[:latter.index('.')]].append(ls)
                                result[former[:former.index('.')]].append(gt)


            else:
                for ii in files_dict[former[:former.index('.')]]:
                    if ii[0] == former[former.index('.')+1:]:
                        mytype = ii[-1]
                        break
                if "'" in latter and mytype in 'char|varchar'\
                or ("." in latter and mytype in 'float|double')\
                or ("." not in latter and "'" not in latter and mytype in 'int'):
                    for former_column in range(len(files_dict[former[:former.index('.')]])):
                        if files_dict[former[:former.index('.')]][former_column][0] == former[former.index('.')+1:]:
                            break
                    if operator == '=':
                        operator = '=' + operator         #两个等号才能做判断
                    if (linked == True and not result[former[:former.index('.')]]) or not data_dict[former[:former.index('.')]]:
                        return '没有满足where条件的数据'

                    if former.replace('.', '_') in index_dict: #如果有索引就直接取出索引进行比较,省去了检索每一行的大循环
                        idx_dict = index_dict[former.replace('.', '_')]
                        if operator == '==' and latter.replace("'",'') not in idx_dict:
                            return '没有满足where条件的数据'
                    if linked:
                        for item in copy.copy(result[former[:former.index('.')]]):
                            formervalue = item.split()[former_column]
                            if files_dict[former[:former.index('.')]][former_column][-1] == 'int':
                                formervalue = int(formervalue)
                            if not eval("formervalue" + operator + latter):
                                location = result[former[:former.index('.')]].index(item)
                                for ii in result:
                                    if result[ii]:
                                        del result[ii][location]
                    else:
                        for index in range(len(tmp_dict[former[:former.index('.')]])):
                            formervalue = tmp_dict[former[:former.index('.')]][index].split()[former_column]
                            if files_dict[former[:former.index('.')]][former_column][-1] == 'int':
                                formervalue = int(formervalue)
                            if not eval("formervalue" + operator + latter):
                                if tmp_dict[former[:former.index('.')]][index] in data_dict[former[:former.index('.')]]:
                                    data_dict[former[:former.index('.')]].remove(tmp_dict[former[:former.index('.')]][index])
                else:
                    return cont[:cont.index(operator)].strip()+'是'+mytype+'类型的值.'
    #处理select投影的属性
    keys = list(result.keys())
    for i in keys:
        if not result[i]:
            result.pop(i)
    if (linked and not result) or not data_dict:
        return '没有满足where条件的数据'

    finalresult = []
    if '*' in content[0]:
        if linked:
            for key in result.keys():   #取出字典的第一个键
                break
            for i in range(len(result[key])):
                res = ''
                for j in result.values():
                    res = res + j[i].strip() + ' '
                finalresult.append(res)
        else:       #没有表连接就将所有表作笛卡尔积
            finalresult.append('')
            for i in data_dict.keys():
                r = [j+k.strip() + ' ' for j in finalresult for k in data_dict[i]]
                del finalresult[:]
                finalresult.extend(r)
    else:
        tmp_dict = {i:[] for i in data_dict}
        for cont in content[0]:
            col = [i[0] for i in files_dict[cont[:cont.index('.')]]].index(cont[cont.index('.')+1:])
            if linked:
                tmp = [i.split()[col] for i in result[cont[:cont.index('.')]]]
                if not finalresult:
                    finalresult.extend(tmp)
                else:
                    for j in range(len(finalresult)):
                        finalresult[j] += ' ' + tmp[j]
            else:
                tmp_list = [i.split()[col] for i in data_dict[cont[:cont.index('.')]]]  #取出投影的属性
                if not tmp_dict[cont[:cont.index('.')]]:
                    tmp_dict[cont[:cont.index('.')]].extend(tmp_list)
                else:
                    for j in range(len(tmp_dict[cont[:cont.index('.')]])):
                        tmp_dict[cont[:cont.index('.')]][j] += ' ' + tmp_list[j]
                for i in tmp_dict:
                    if not tmp_dict[i]:     #该表没有投影操作
                        tmp_dict[i] = ['']*len(tmp_dict[i])
        if len(tmp_dict) > 1:
            finalresult.append('')
            for i in tmp_dict:
                if not tmp_dict[i]:
                    continue
                r = [j+k.strip() + ' ' for j in finalresult for k in tmp_dict[i]]
                del finalresult[:]
                finalresult.extend(r)
        else:
            finalresult.extend(tmp_dict[cont[:cont.index('.')]])
    return finalresult


def drop_table(dirname, file):
    if isExist(dirname+'\\dict\\',file+'.txt'):
        os.remove(dirname+'\\tables\\'+file+'.txt')
        for i in os.listdir(dirname+'\\index\\'):
            if file in i[:i.index('_')]:
                os.remove(dirname+'\\index\\'+i)
        if file+'.txt' in [i for i in os.listdir(dirname+'\\dict\\')]:
            os.remove(dirname+'\\dict\\'+file+'.txt')
        f = open(dirname+'\\users\\'+'users'+'.txt','r',encoding = 'utf8')
        lines = f.readlines()
        f.close()
        for i in lines:
            if i.split()[-1] == file:
                lines.remove(i)
        f = open(dirname+'\\users\\'+'users'+'.txt','w',encoding = 'utf8')
        f.writelines(lines)
        f.close()
        return '删除了' + file + '表'
    else:
        return file + '表不存在'

def drop_column(dirname, file, column):
    if isExist(dirname+'\\dict\\',file+'.txt'):
        f = open(dirname+'\\dict\\'+file+'.txt', 'r', encoding = 'utf8')
        lines = f.readlines()
        f.close()
        columns = [i.split()[0] for i in lines]
        if column not in columns:
            return file+ "表中没有'" + column + "'属性"

        for column_order in range(len(columns)):
            if column == columns[column_order]:
                del lines[column_order]
                f = open(dirname+'\\dict\\'+file+'.txt', 'w', encoding = 'utf8')
                f.writelines(lines)
                f.close()
                break
        f = open(dirname+'\\tables\\'+file+'.txt', 'r', encoding = 'utf8')
        data_lines = f.readlines()
        f.close()
        tmp = []
        for i in data_lines:
            i = i.split()
            del i[column_order]
            a = ' '.join(i)
            tmp.append(a+'\n')
        data_lines = tmp
        f = open(dirname+'\\tables\\'+file+'.txt', 'w', encoding = 'utf8')
        f.writelines(data_lines)
        f.close()

        for i in os.listdir(dirname+'\\index\\'):
            if file== i[:i.index('_')] and column in i[i.index('_')+1:i.index('.')]:
                os.remove(dirname+'\\index\\'+i)

        return '删除了' + file+ "表的'" + column +"'属性"
    else:
        return file + '表不存在'

def add_column(dirname, file, content):
    if isExist(dirname+'\\dict\\',file+'.txt'):
        f = open(dirname+'\\dict\\'+file+'.txt', 'r', encoding = 'utf8')
        lines = [i.split()[0] for i in f.readlines()]
        f.close()
        if content[0][0] in lines:
            return "'"+ content[0][0] + "'属性已经存在，不能重复添加"

        f = open(dirname+'\\dict\\'+file+'.txt', 'a', encoding = 'utf8')
        f.write(content[0][0]+' '+content[1][0]+'\n')
        f.close()
        f = open(dirname+'\\tables\\'+file+'.txt', 'r', encoding = 'utf8')
        lines = f.readlines()
        f.close()
        lines = [line.strip()+' NULL'+'\n' for line in lines]
        f = open(dirname+'\\tables\\'+file+'.txt', 'w', encoding = 'utf8')
        f.writelines(lines)
        f.close()
        return file + "表增加了'" + content[0][0] + "'属性"
    else:
        return file + '表不存在'

def drop_index(dirname, file, indexname):
    if isExist(dirname+'\\dict\\',file+'.txt'):
        if isExist(dirname+'\\index\\',file+'_'+indexname+'.txt'):
            os.remove(dirname+'\\index\\'+file+'_'+indexname+'.txt')
            return '删除了' + file + "表的'" + indexname + "'索引"
        return file + "表没有名为'" + indexname + "'的索引"
    else:
        return file + '表不存在'

def grant(dirname, file, content):
    f = open(dirname+file,'r', encoding = 'utf8')
    lines = f.readlines()
    f.close()
    with open(dirname+r'\users\usernames.txt','r', encoding = 'utf8') as ff:
        if content[-1][0] not in [i.split()[0] for i in ff.readlines()]:
            return "用户'"+content[-1][0]+"'不存在"
    if not isExist(dirname+'\\dict\\',content[1][0]+'.txt'):
        return "'"+content[1][0]+"'表不存在"
    result = ''
    tables = [i.split()[-1] for i in lines if i.split()[0] == content[-1][0]]
    if content[1][0] not in tables:
        result = content[-1][0]+' '+content[0][0]+' '+content[1][0]+'\n'
        lines.append(result)
    else:
        for i in lines:
            splited = i.split()
            if splited[0] == content[-1][0] and splited[-1] == content[1][0]:
                if content[0][0] not in splited[1]:
                    splited[1] = splited[1]+','+content[0][0]
                    for j in splited:
                        result += ' ' + j
                    result += '\n'
                    lines[lines.index(i)] = result
                break
    f = open(dirname+file,'w', encoding = 'utf8')
    f.writelines(lines)
    f.close()
    return "为用户'"+content[-1][0]+"'在'"+content[1][0]+"'表上授予了'"+content[0][0]+"'权限\n重新登录帐号以生效"

def revoke(dirname, file, content):
    f = open(dirname+file,'r', encoding = 'utf8')
    lines = f.readlines()
    f.close()
    with open(dirname+r'\users\usernames.txt','r', encoding = 'utf8') as ff:
        if content[-1][0] not in [i.split()[0] for i in ff.readlines()]:
            return "用户'"+content[-1][0]+"'不存在"
    if not isExist(dirname+'\\dict\\',content[1][0]+'.txt'):
        return "'"+content[1][0]+"'表不存在"
    for i in lines:
        splited = i.split()
        if splited[0] == content[-1][0] and splited[-1] == content[1][0]:
            if splited[1] == content[0][0]:    #只有一个权限
                splited[1] = ''
            elif content[0][0]+',' in splited[1]:  #要撤销的权限不是最后一个权限
                splited[1] = splited[1].replace(content[0][0]+',','')
            else:           #要撤销的权限是最后一个权限
                splited[1] = splited[1].replace(','+content[0][0], '')

            if not splited[1]:  #如果所有权限都被撤销，则删除这一行
                lines.remove(i)
            else:
                lines[lines.index(i)] = splited[0]+' '+splited[1]+' '+splited[-1]+'\n'

            f = open(dirname+file,'w', encoding = 'utf8')
            f.writelines(lines)
            f.close()
            break
    return "用户'"+content[-1][0]+"'在'"+content[1][0]+"'表上的'"+content[0][0]+"'权限已被撤销\n重新登录帐号以生效"