import json
from datetime import datetime
import os

# 1. 添加消费记录
def add_consumption(matter, money, document):   # matter 是做的事情, money 是钱(给字典加一个判断 > 0是收入，<0 是支出), document 是操作文件

    # a. 判断有该文件且文件中有内容(此时文件中本来就是正确的 json 格式)
    if os.path.exists(document) and os.path.getsize(document) > 0:
        with open(document, 'r', encoding = 'utf-8') as in_file:
            old_file = json.load(in_file)
    else:
        old_file = []   # 该存储方式是 json 数组

    # 处理只有一个字典的情况
    if isinstance(old_file, dict):
        old_file = [old_file]

    # b. 将新字典加入列表中
    new_dict = dict()  # 将该字典加入 json 
    new_dict['名称'] = matter
    new_dict['金额'] = money
    new_dict['时间'] = datetime.now().strftime("%Y-%m-%d %H-%M-%S")
    old_file.append(new_dict)

    # c. 将新 json 传回文件
    with open(document, 'w', encoding = 'utf-8') as infile:
        json.dump(old_file, infile, ensure_ascii = False)
    return True

# 2. 查看所有消费记录(把负数绝对值化，结果你一直在给正数绝对值化你也真是疯了)
def view_consumption(document):

    # a. 文件不存在或者文件中无内容
    if not os.path.exists(document) or os.path.getsize(document) == 0:
        return 0

    # b. 打开文件并读出消费记录
    with open(document, 'r', encoding = 'utf-8') as outfile:
        open_file = json.load(outfile)
    result_list = []
    for cur_dict in open_file:   # cur_dict 是列表中的字典
        name = cur_dict['名称']
        money = cur_dict['金额']
        cur_time = cur_dict['时间']
        result_list.append(f"在 {cur_time}  花费 {money} 元做了 {name} 这件事")
    return result_list

# 3. 按类别查询
def search_category(document, category):

    # a. 文件不存在或者文件中无内容
    if not os.path.exists(document) or os.path.getsize(document) == 0:
        return 0

    # b. 文件存在
    result_list = []    # 返回的文件
    num = 0 # 保存的有无类别的次数

    with open(document, 'r', encoding = 'utf-8') as outfile:
        open_file = json.load(outfile)
    for cur_dict in open_file:   # cur_dict 是列表中的字典
        name = cur_dict['名称']

        # 当前的消费类别与查询的消费类别一致
        if name == category:
            num += 1
            money = cur_dict['金额']
            cur_time = cur_dict['时间']
            result_list.append(f"在 {cur_time}  花费 {money} 元做了 {name} 这件事")

    # c.文件存在，但是并没有这个类别的消费
    if num == 0:
        return 1
    return result_list

# 4. 查看统计, 即总消费记录
def view_statistics(document):

    # a.文件不存在或者文件中无内容
    if not os.path.exists(document) or os.path.getsize(document) == 0:
        return 0

    # b. 打开文件, 开始操作
    with open(document, 'r', encoding = 'utf-8') as outfile:
        open_file = json.load(outfile)  # 拿出来的东西是一个列表
    sum = 0 # 总消费金额
    for cur_file in open_file:
        sum += cur_file["金额"]
    return sum

# 5. 删除记录
def delete_record(document, delete_time):

    # a. 如果文件不存在或者无内容
    if not os.path.exists(document) or os.path.getsize(document) == 0:
        return 0

    # b. 打开文件，开始操作
    found = False
    with open(document, 'r', encoding = 'utf-8') as infile:
        operation_file = json.load(infile, )
    for cur_dict in operation_file:
        if cur_dict["时间"] == delete_time:
            operation_file.remove(cur_dict)
            found = True
            break

    # 已经结束遍历，都没有找到这个时间段
    if not found:
        return 11

    # c. 写回文件
    with open(document, 'w', encoding = 'utf-8') as file:
        json.dump(operation_file, file, ensure_ascii = False)
    return 1

def menu(document):
    
    print("================个人记账======================")
    print("\t1.添加消费记录")
    print("\t2.查看记录")
    print("\t3.按类别查询")
    print("\t4.查看统计")
    print("\t5.删除记录")
    print("\t0.退出")
    print("=============================================")

    while True:
        choose = int(input("||请输入选择类型"))
        # 选择类型
        if choose == 1:
            print("您选择了添加消费记录")
            matter = input("请添加消费名称:\t")
            money = float(input("请添加消费金额:\t"))
            add_con_result = add_consumption(matter, money, document)
            if add_con_result:
                print(f"添加消费类别{matter}, 消费金额{money}的记录成功")
            else:
                print("添加失败")

        elif choose == 2:
            view_con_result = view_consumption(document)
            if view_con_result == 0:
                print("没有消费记录")
            elif isinstance(view_con_result, list):
                for i in view_con_result:
                    print(i)
            else:
                print("查询失败")

        elif choose == 3:
            category = input("请输入您要查询的消费类别:\t")
            search_cate_result = search_category(document, category)
            if search_cate_result == 0:
                print("没有消费记录")
            elif search_cate_result == 1:
                print("不存在此消费类别")
            else:
                for i in search_cate_result:
                    print(i)

        elif choose == 4:
            view_stat_retult = view_statistics(document)
            if view_stat_retult == 0:
                print("未添加过消费记录")
            else:
                print(f"消费记录为{view_stat_retult}")

        elif choose == 5:
            delete_time = input("请输入你要删除该时间的消费")
            delete_time_result = delete_record(document, delete_time)
            if delete_time_result == 0:
                print("无消费记录")
            elif delete_time_result == 11:
                print(f"未找到该{delete_time}时间的消费")
            else:
                print("删除成功")

        elif choose == 0:
            print("退出成功")
            break

        else:
            print("不存在此选项")

menu("e:/workspace/internship/python/accountBook/data.txt")