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
def copy_line_to_variable(linenumber):
    if 0 < linenumber <= len(lines):
        content = lines[linenumber - 1].strip()  # 列表的索引从0开始，故减1
        return content
    else:
        return None


# 提取任务名
def find_task_name():
    goodnum = 0  # 完美任务计数
    for i in range(0, len(taskname)):  # 任务名中循环
        start = 0  # 初始化搜寻开始的位置
        # 此处循环是为了能在找到任务后，继续往下搜寻第二个同名任务
        while start < len(line_content):  # 搜寻开始的位置小于长度才继续做
            # 查找任务名在字符串中的位置 元组（任务名，位置）
            index = line_content.find(taskname[i], start)  # start控制起始搜寻处，未曾找到过时，应默认为0开始
            if index != -1:  # 如果找到
                if taskname[i] in goodtask:  # 判断是否为好任务，计数
                    goodnum += 1
                tasklist.append((taskname[i], index))  # 任务名及位置加入列表保存
                tasklistcn.append((tasknamecn[i], index))
                start = index + 1  # 找到后，索引+1的位置继续找有无同名任务
            else:  # 如果没找到
                break  # 跳出循环，while中止，到for的下一个任务名循环
    # 整理tasklist tasklistcn
    tasklist.sort(key=lambda x: x[1], reverse=False)
    tasklistcn.sort(key=lambda x: x[1], reverse=False)
    # 输出中文任务链
    for x in tasklistcn:
        print(f"\033[0;32;40m{x[0]}\033[0m")
    # 判断是否为完美任务
    if goodnum == len(tasklist):
        print(f"\033[0;32;40m恭喜找到完美任务链！\033[0m")
    else:
        print(f"\033[0;31;40m很遗憾，本次不是完美任务，祝下次好运！\033[0m")


def taskname_replace(content):
    # 待替换文本(希图斯：地下储藏箱；福尔图娜：摧毁无人机)
    oldtasklist = ['HiddenResourceCachesCave', 'DynamicExterminateDrones']
    # 替换后文本
    newtasklist = ['HiddenCaveResourceCaches', 'DynamicDronesExterminate']
    for i in range(0, len(oldtasklist)):  # 循环依次替换
        content = content.replace(oldtasklist[i], newtasklist[i])
    return content


# 循环输出任务链的主体
def main_cycle_task_detect():
    print("\033c", end="")  # 清屏
    # 声明全局变量
    global t, taskarea, lines, taskname, tasknamecn, goodtask, \
        tasklist, tasklistcn, line_number, line_content
    # 初始化
    taskarea = ''
    tasklist = []
    tasklistcn = []
    # 复制文件
    try:
        shutil.copy(log_path, copy_path)
    except:
        if choice == '1':  # 单次执行模式手动返回重试
            print('复制日志文件失败，请重试')
        elif choice == '2':  # 给自动执行模式的失败调整提示语，并加上重试间隔
            print('复制日志文件失败，1秒后重试')
            time.sleep(1)
        return  # 出错就退出循环
    # 读取文件
    with open(copy_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()  # 按行读取，存入列表
    # 定位任务链行数
    line_number = find_line_number(target_string)
    if line_number == 0:
        return  # 若无法找到行数则终止循环
    # 任务链所在行内容赋值给变量
    line_content = copy_line_to_variable(line_number)
    if line_content is None:
        return  # 若无法找到任务链行内容则终止循环
    # 任务名替换以区分
    line_content = taskname_replace(line_content)
    # 判断赏金所属地
    for area in ['Eidolon', 'Venus', 'InfestedMicroplanet']:
        if line_content.find(area) != -1:  # 若找到地名关键词
            taskarea = area
            exec(f'taskname = taskname_{area}', globals())  # 对应地名的数据赋值待用
            exec(f'tasknamecn = tasknamecn_{area}', globals())
            exec(f'goodtask = goodtask_{area}', globals())
            break  # 找到则退出判断属地循环
    if taskname == []:  # 为空则说明判断属地失败
        print('无法判断赏金所在属地（希图斯、福尔图娜、殁世幽都）')
        return  # 中止循环
    # 提取任务名,并判断任务链是否完美
    find_task_name()
    t -= 1  # 剩余运行次数-1
    time.sleep(JianGe)  # 等待JianGe秒


# 主程序
if __name__ == '__main__':
    # 获取用户名
    username = os.environ["USERNAME"]
    # 日志路径、副本路径
    log_path = rf'C:\Users\{username}\AppData\Local\Warframe\EE.log'
    copy_path = rf'C:\Users\{username}\Documents\WFTaskLog.txt'
    # 定位用字符串
    target_string = r'Script [Info]: EidolonJobBoard.lua: Selected job with jobInfo:'
    # 任务英文、任务中文、完美任务英文 初始化
    taskname = []
    tasknamecn = []
    goodtask = []
    # 希图斯任务英文（'HiddenResourceCachesCave'替换为'HiddenCaveResourceCaches'以区分）
    taskname_Eidolon = ['DynamicResourceTheft', 'DynamicHijack',
                        'HiddenCaveResourceCaches', 'HiddenResourceCaches',
                        'DynamicAssassinate', 'DynamicDefend',
                        'DynamicSabotage', 'DynamicExterminate',
                        'DynamicCaveExterminate', 'DynamicCapture', 'DynamicRescue']
    # 希图斯任务中文
    tasknamecn_Eidolon = ['防御重甲金库', '护送无人机',
                          '寻找储藏舱(地下)', '寻找储藏舱',
                          '刺杀', '解放营地',
                          '破坏补给', '消灭一定数量的敌人',
                          '消灭一定数量的敌人(地下)', '捕获', '救援']
    # 希图斯完美任务英文（无人机、地下储藏箱、地上储藏箱、刺杀、捕获、救援）
    goodtask_Eidolon = ['DynamicHijack', 'HiddenCaveResourceCaches',
                        'HiddenResourceCaches', 'DynamicAssassinate',
                        'DynamicCapture', 'DynamicRescue']
    # 福尔图娜任务英文（'DynamicExterminateDrones'替换为'DynamicDronesExterminate'以区分）
    taskname_Venus = ['DynamicBaseSpy', 'DynamicAssassinate',
                      'DynamicDronesExterminate', 'DynamicExterminate',
                      'DynamicResourceCapture', 'DynamicExcavation',
                      'DynamicRecovery', 'DynamicAmbush',
                      'DynamicDroneDefense', 'DynamicCachesAirDrop']
    # 福尔图娜任务中文
    tasknamecn_Venus = ['间谍', '刺杀',
                        '摧毁无人机', '消灭一定数量的敌人',
                        '占领储藏箱', '挖掘',
                        '调查索拉里斯营地', '伏击线圈滚轮',
                        '停用无人机', '寻找储藏箱']
    # 福尔图娜完美任务英文（间谍、刺杀、摧毁无人机、寻找储藏箱、消灭一定数量的敌人）
    goodtask_Venus = ['DynamicBaseSpy', 'DynamicAssassinate',
                      'DynamicDronesExterminate', 'DynamicCachesAirDrop',
                      'DynamicExterminate']
    # 殁世幽都任务英文
    taskname_InfestedMicroplanet = ['DynamicAssassinate', 'DynamicExterminate',
                                    'DynamicAreaDefense', 'DynamicPurify',
                                    'DynamicCorpusSurvivors', 'DynamicGrineerSurvivors',
                                    'DynamicExcavation', 'DynamicKeyPieces']
    # 殁世幽都任务中文
    tasknamecn_InfestedMicroplanet = ['刺杀', '消灭巢囊',
                                      '防御区域', '萃取样本',
                                      '帮助Corpus研究员', '和Grineer小队比赛',
                                      '挖掘', '找到并消灭肿瘤']
    # 殁世幽都完美任务英文
    goodtask_InfestedMicroplanet = ['DynamicKeyPieces', 'DynamicCorpusSurvivors',
                                    'DynamicPurify', 'DynamicAssassinate']

    # 菜单循环
    while True:
        print("\033c", end="")  # 清屏
        print('选择程序运行方式：（输入数字按下回车）')
        print('1 - 运行一次')
        print('2 - 自动运行')
        print('3 - 结束程序')
        JianGe = 0  # 间隔默认为0，除自动执行外，不需要停顿
        t = 1  # 次数默认为1(意义不大，就是定义一下)
        choice = input()
        if choice == '1':
            main_cycle_task_detect()
            input('按回车键回到菜单')
        elif choice == '2':
            t = 1145141919  # 简单粗暴的大数字，就是有点臭
            try:
                JianGe = input('运行间隔时间（单位：秒）直接回车默认2秒\n'
                               '(过快可能导致读取和wf写入冲突而使脚本崩溃)\n')  # 询问运行间隔
                if JianGe == '':
                    JianGe = 2  # 默认间隔
                else:
                    JianGe = int(JianGe)  # 不为空就转为数字
            except ValueError:  # 转换出错时，走这里
                print('输入错误！3秒后重启')
                time.sleep(3)  # 3秒后重启
                continue
            while t > 0:
                main_cycle_task_detect()
        elif choice == '3':
            break
        else:
            print('输入有误！3秒后重启')
            time.sleep(3)
