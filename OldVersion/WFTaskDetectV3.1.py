# import
import shutil
import os
import time


# 查找行数
def find_line_number(string):
    number = 0  # 初始化
    for i in range(len(lines) - 1, 0, -1):  # 倒序循环行
        if string in lines[i]:
            number = i + 1  # 定位用字符串所在行数
            # print(f"'{target_string}'出现在第{number}行")  # 调试用输出
            number += 2  # 加2以定位到任务链所在行
            break  # 找到就跳出寻找循环
    if number == 0:
        print(f"未在文件中找到'{target_string}'")
    return number


# 提取字符串
def copy_line_to_variable(line_number):
    if 0 < line_number <= len(lines):
        content = lines[line_number - 1].strip()  # 减去1是因为列表的索引从0开始，而人的计数习惯是从1开始
        return content
    else:
        return None


# 提取任务名
def find_task_name():
    goodnum = 0  # 完美任务计数
    for i in range(0, len(taskname)):  # 任务名中循环
        # 查找任务名在字符串中的位置 元组（任务名，位置）
        index = line_content.find(taskname[i])
        if index != -1:
            if taskname[i] in goodtask:
                goodnum += 1
            tasklist.append((taskname[i], index))
            tasklistcn.append((tasknamecn[i], index))
    # 整理tasklist tasklistcn
    tasklist.sort(key=lambda x: x[1], reverse=False)
    tasklistcn.sort(key=lambda x: x[1], reverse=False)
    # 输出中文任务链
    for x in tasklistcn:
        print(f"\033[0;32;40m{x[0]}\033[0m")
    # 判断是否为完美任务
    if goodnum == 5:
        print(f"\033[0;32;40m恭喜找到完美任务链！\033[0m")
    else:
        print(f"\033[0;31;40m很遗憾，本次不是完美任务，祝下次好运！\033[0m")


if __name__ == '__main__':
    # 获取用户名
    username = os.environ["USERNAME"]
    # 日志路径、副本路径
    log_path = rf'C:\Users\{username}\AppData\Local\Warframe\EE.log'
    copy_path = rf'C:\Users\{username}\Documents\WFTaskLog.txt'
    # 定位用字符串
    target_string = r'Script [Info]: EidolonJobBoard.lua: Selected job with jobInfo:'
    # 任务英文（'HiddenResourceCachesCave'替换为'HiddenCaveResourceCaches'以区分）
    taskname = ['DynamicResourceTheft', 'DynamicHijack',
                'HiddenCaveResourceCaches', 'HiddenResourceCaches',
                'DynamicAssassinate', 'DynamicDefend',
                'DynamicSabotage', 'DynamicExterminate',
                'DynamicCaveExterminate', 'DynamicCapture', 'DynamicRescue']
    # 任务中文
    tasknamecn = ['防御重甲金库', '护送无人机',
                  '寻找储藏舱(地下)', '寻找储藏舱',
                  '刺杀', '解放营地',
                  '破坏补给', '消灭一定数量的敌人',
                  '消灭一定数量的敌人(地下)', '捕获', '救援']
    # 完美任务英文（无人机、地上下储藏箱、刺杀、捕获、救援）
    goodtask = ['DynamicHijack', 'HiddenCaveResourceCaches',
                'HiddenResourceCaches', 'DynamicAssassinate',
                'DynamicCapture', 'DynamicRescue']
    # 选择运行方式
    while True:
        print('选择程序运行方式：（输入数字按下回车）')
        print('1 - 运行一次')
        print('2 - 自动运行')
        print('3 - 结束程序')
        choice = input()
        if choice == '1':
            t = 1
            break
        elif choice == '2':
            t = 1145141919  # 简单粗暴的大数字，就是有点臭
            break
        elif choice == '3':
            t = 0
            break
        else:
            print('输入有误，3秒后重启')
            time.sleep(3)
        print("\033c", end="")  # 清屏

    # 程序循环部分
    while t > 0:
        # 初始化
        print("\033c", end="")  # 清屏
        tasklist = []
        tasklistcn = []
        # 复制文件
        shutil.copy(log_path, copy_path)
        # 读取文件
        with open(copy_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()  # 按行读取，存入列表
        # 定位任务链行数
        line_number = find_line_number(target_string)
        if line_number == 0:
            break  # 若无法找到行数则终止程序
        # 任务链所在行内容赋值给变量
        line_content = copy_line_to_variable(line_number)
        if line_content is None:
            break  # 若无法找到任务链行内容则终止程序
        line_content = line_content.replace('HiddenResourceCachesCave', 'HiddenCaveResourceCaches')
        # 提取任务名,并判断任务链是否完美
        find_task_name()
        t -= 1
        time.sleep(1)
    input('按回车键退出')