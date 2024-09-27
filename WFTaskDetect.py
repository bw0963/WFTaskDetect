# import
import shutil
import os


# 查找行数
def find_line_number(filename, target):
    with open(filename, 'r', encoding='utf-8') as file:
        lines = file.readlines()
    for i in range(len(lines) - 1, -1, -1):
        if target in lines[i]:
            return i + 1  # 返回行数，从1开始
    return None  # 如果未找到，返回None


# 提取字符串
def copy_line_to_variable(filename, line_number):
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            lines = file.readlines()
        if line_number > 0 and line_number <= len(lines):
            line_content = lines[line_number - 1].strip()  # 减去1是因为列表的索引从0开始，而人的计数习惯是从1开始
            return line_content
        else:
            return None
    except FileNotFoundError:
        return None


# 获取用户名
username = os.environ["USERNAME"]
# 复制文件
shutil.copy(rf'C:\Users\{username}\AppData\Local\Warframe\EE.log', rf'C:\Users\{username}\Desktop\WFTask.txt')
# 定位内容，输出行数
filename = rf'C:\Users\{username}\Desktop\WFTask.txt'
target = r'Script [Info]: EidolonJobBoard.lua: Selected job with jobInfo:'
line_number = find_line_number(filename, target)
if line_number is not None:
    print(f"'{target}'出现在第{line_number}行")
    line_number += 2
else:
    print(f"未在文件中找到'{target}'")
# 定位任务链所在行，内容赋值给变量
line_content = copy_line_to_variable(filename, line_number)
if line_content is not None:
    print(f"第{line_number}行的内容是: {line_content}")
else:
    print(f"无法找到第{line_number}行")

# 任务英文
taskname = ['DynamicResourceTheft', 'DynamicHijack',
            'HiddenResourceCachesCave', 'HiddenResourceCaches',
            'DynamicAssassinate', 'DynamicDefend',
            'DynamicSabotage', 'DynamicExterminate',
            'DynamicCaveExterminate', 'DynamicCapture', 'DynamicRescue']
# 任务中文
tasknamecn = ['防御重甲金库', '护送无人机',
              '寻找储藏舱(地下)', '寻找储藏舱',
              '刺杀', '解放营地',
              '破坏补给', '消灭一定数量的敌人',
              '消灭一定数量的敌人(地下)', '捕获', '救援']
# 完美任务英文
goodtask = ['DynamicHijack', 'HiddenResourceCachesCave',
            'HiddenResourceCaches', 'DynamicAssassinate',
            'DynamicCapture', 'DynamicRescue']

# 初始化
foundmark = 0
goodnum = 0
tasklist = []
tasklistcn = []
# 在任务链所在行提取出任务链，存给变量
for i in range(0, len(taskname)):
    index = line_content.find(taskname[i])
    if index != -1:
        if i == 2:
            foundmark = 1
        if i == 3 and foundmark == 1:
            continue
        if taskname[i] in goodtask:
            goodnum += 1
        tasklist.append((taskname[i], index))
        tasklistcn.append((tasknamecn[i], index))
# 整理tasklist tasklistcn
tasklist.sort(key=lambda x: x[1], reverse=False)
tasklistcn.sort(key=lambda x: x[1], reverse=False)
print(tasklist)

# 输出中文任务链
print("----任务链----")
for x in tasklistcn:
    print(x[0])
print("----任务链----")

# 判断是否为完美任务
if goodnum == 5:
    print(f"恭喜找到完美任务链！")
else:
    print(f"很遗憾，本次不是完美任务，祝下次好运！")

# 防止运行后自动退出
input("按回车键退出")
