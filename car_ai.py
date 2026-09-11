import random
import os
from datetime import datetime

QUESTION_FILE = "bank.txt"
RECORD_FILE = "record.txt"
ERROR_FILE = "error.txt"

# 加载题库
def load_questions():
    if not os.path.exists(QUESTION_FILE):
        print(f"错误：找不到{QUESTION_FILE}，请确认和程序放在同一目录！")
        return []
    with open(QUESTION_FILE, "r", encoding="utf-8") as f:
        content = f.read()
    raw_list = content.split("====")
    q_list = []
    for item in raw_list:
        item = item.strip()
        if not item:
            continue
        lines = item.splitlines()
        q_data = {}
        q_data["topic"] = lines[0].replace("题目：", "").strip()
        q_data["A"] = lines[1].replace("A.", "").strip()
        q_data["B"] = lines[2].replace("B.", "").strip()
        q_data["C"] = lines[3].replace("C.", "").strip()
        q_data["D"] = lines[4].replace("D.", "").strip()
        q_data["ans"] = lines[5].replace("正确选项：", "").strip()
        q_data["explain"] = lines[6].replace("解析：", "").strip()

        # 简单自动分类（关键词匹配）
        text = q_data["topic"] + q_data["explain"]
        if "电池" in text or "BMS" in text or "SOC" in text or "SOH" in text:
            q_data["cate"] = "动力电池"
        elif "电机" in text or "MCU" in text or "旋变" in text:
            q_data["cate"] = "电机电控"
        elif "高压" in text or "绝缘" in text or "MSD" in text or "触电" in text:
            q_data["cate"] = "高压安全"
        elif "冷却" in text or "热管理" in text or "PTC" in text or "热泵" in text:
            q_data["cate"] = "热管理"
        else:
            q_data["cate"] = "CAN通讯&故障诊断"
        q_list.append(q_data)
    return q_list

# 加载错题本
def load_error_questions():
    if not os.path.exists(ERROR_FILE):
        return []
    with open(ERROR_FILE, "r", encoding="utf-8") as f:
        content = f.read()
    raw_list = content.split("====")
    err_list = []
    for item in raw_list:
        item = item.strip()
        if not item:
            continue
        lines = item.splitlines()
        q_data = {}
        q_data["topic"] = lines[0].replace("题目：", "").strip()
        q_data["A"] = lines[1].replace("A.", "").strip()
        q_data["B"] = lines[2].replace("B.", "").strip()
        q_data["C"] = lines[3].replace("C.", "").strip()
        q_data["D"] = lines[4].replace("D.", "").strip()
        q_data["ans"] = lines[5].replace("正确选项：", "").strip()
        q_data["explain"] = lines[6].replace("解析：", "").strip()
        err_list.append(q_data)
    return err_list

# 保存错题
def save_error(q):
    with open(ERROR_FILE, "a", encoding="utf-8") as f:
        f.write(f"题目：{q['topic']}\nA.{q['A']}\nB.{q['B']}\nC.{q['C']}\nD.{q['D']}\n正确选项：{q['ans']}\n解析：{q['explain']}\n====\n")

# 保存成绩记录
def save_record(total, right, wrong):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"\n【{now}】 总题数:{total} 答对:{right} 答错:{wrong} 得分:{int(right/total*100)}分"
    with open(RECORD_FILE, "a", encoding="utf-8") as f:
        f.write(line)
    print(line)

# 故障诊断案例
def fault_case():
    print("\n======== 新能源汽车故障案例库 ========")
    cases = [
        {"title":"预充失败，车辆无法READY",
         "reason":"预充回路故障、接触器损坏、MCU电容异常；上电前无法完成电容预充，整车禁止闭合高压主回路",
         "solve":"读取故障码，检查预充继电器、预充电阻，测量MCU电容状态"},
        {"title":"行驶动力限制，报电池高温故障",
         "reason":"冷却回路堵塞、电子水泵故障、NTC温度传感器失效，电池热量堆积触发保护",
         "solve":"检查冷却液液位、水泵工作状态，校验温度传感器数据流"},
        {"title":"高压绝缘故障，整车下高压",
         "reason":"高压线束破皮、电池包进水、部件绝缘老化，对地绝缘电阻低于阈值",
         "solve":"下高压等待放电，分段测量各高压部件绝缘，找到漏电位置"},
        {"title":"慢充无法充电，枪已插好无响应",
         "reason":"CC/CP信号异常、OBC故障、充电口电子锁损坏、12V低压供电异常",
         "solve":"检查充电枪CC确认信号，读取OBC故障码，检查12V电瓶电压"},
        {"title":"12V电瓶频繁亏电",
         "reason":"DC-DC转换器损坏，行车时无法给低压电瓶补电；车辆静态漏电过大",
         "solve":"检测DC-DC输出电压，整车静态电流排查漏电部件"}
    ]
    for c in cases:
        print(f"\n故障现象：{c['title']}")
        print(f"故障分析：{c['reason']}")
        print(f"维修方案：{c['solve']}")
    input("\n按回车返回主菜单")

# 答题主函数
def start_quiz(q_list):
    if len(q_list) == 0:
        print("当前题库为空！")
        return
    random.shuffle(q_list)
    right = 0
    wrong = 0
    total = len(q_list)
    for q in q_list:
        print("\n----------------------------------------")
        print(f"【{q['cate']}】{q['topic']}")
        print(f"A.{q['A']}")
        print(f"B.{q['B']}")
        print(f"C.{q['C']}")
        print(f"D.{q['D']}")
        user_in = input("请输入你的答案(A/B/C/D)，输入Q退出本次答题：").strip().upper()
        if user_in == "Q":
            break
        if user_in == q['ans']:
            print("✅回答正确！")
            right += 1
        else:
            print(f"❌答错，正确答案是：{q['ans']}")
            save_error(q)
            wrong +=1
        print(f"解析：{q['explain']}")
    if total>0:
        save_record(right+wrong, right, wrong)
    input("\n本次答题结束，回车返回菜单")

# 分类刷题菜单
def cate_quiz(all_q):
    cate_list = ["动力电池","电机电控","高压安全","热管理","CAN通讯&故障诊断"]
    print("\n===== 分类刷题 =====")
    for i,c in enumerate(cate_list):
        print(f"{i+1}. {c}")
    sel = input("请选择分类序号：").strip()
    try:
        idx = int(sel)-1
        target_cate = cate_list[idx]
        filter_q = [x for x in all_q if x["cate"] == target_cate]
        print(f"\n选中【{target_cate}】，共有{len(filter_q)}道题目")
        start_quiz(filter_q)
    except:
        print("输入错误，返回主菜单")

# 错题本刷题
def error_quiz():
    err_q = load_error_questions()
    print(f"\n===== 错题本，共{len(err_q)}道错题 =====")
    start_quiz(err_q)

def main():
    all_questions = load_questions()
    print(f"\n✅题库加载完成，共有 {len(all_questions)} 道新能源题目")
    while True:
        print("\n===== 新能智诊 - 新能源汽车智能测评与故障辅助诊断系统 =====")
        print("1. 新能源故障案例查询")
        print("2. 随机全套题库刷题")
        print("3. 按专业分类刷题")
        print("4. 错题本（练习做错题目）")
        print("0. 退出程序")
        choice = input("\n请输入功能序号：").strip()
        if choice == "1":
            fault_case()
        elif choice == "2":
            start_quiz(all_questions)
        elif choice == "3":
            cate_quiz(all_questions)
        elif choice == "4":
            error_quiz()
        elif choice == "0":
            print("程序退出，答题记录已保存")
            break
        else:
            print("输入无效，请重新选择")

if __name__ == "__main__":
    main()
