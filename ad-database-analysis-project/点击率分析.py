from matplotlib import pyplot as plt
import pandas as pd


sample = pd.read_csv("D:/代码集合/数据分析/ad-database-analysis-project/原始数据/raw_sample.csv")
clk = sample[sample["clk"] == 1]
df = pd.DataFrame()
ts = sample["time_stamp"]
time_stamp = pd.to_datetime(ts, unit="s")


#05 周五 06 周六 07 周日 08 周一 09 周二 10 周三 11 周四 12 周五 13 周六
def max_and_min(n):
    print("最大值：",max(n),"\n",
          "最小值",min(n),"\n",
          "极差",max(n)-min(n),"\n")
def all_ctr_calculate():
    sample_number = len(sample)
    clk_number = len(clk)
    ctr = (clk_number / sample_number) * 100
    return "样本数：{0}\n点击数：{1}\n点击率：{2:2f}%\n".format(sample_number, clk_number, ctr)
def day_and_clk():
    day = time_stamp.dt.day
    hour = time_stamp.dt.hour
    day_clk = pd.DataFrame({"day": day, "hour": hour, "clk": sample["clk"]})
    return day_clk
day_clk = day_and_clk()
def ctr_calculate(dc):
    if len(dc) !=0:
        dcn = dc.query("clk == 1")
        return (len(dcn) / len(dc)) * 100
    else:return 0

def day_ctr_calculate():
    dc = day_and_clk().sort_values("day")
    day_labels = ["5","6","7","8","9","10","11","12","13"]
    day_clk = {}
    user_num = []
    for i in range(5, 14):
        dc0 = dc.query("day == {0:2f}".format(i))
        user_num.append(len(dc0))
        day_clk.update({"{}".format(i): ctr_calculate(dc0)})
    va = day_clk.values()
    day_clk = pd.DataFrame({"ctr": va}, index=list(day_clk.keys()))
    print(user_num)
    print(day_clk["ctr"])
    max_and_min(user_num)
    max_and_min(day_clk["ctr"])
    fig, ax1 = plt.subplots(figsize=(10, 6))
    color1 = 'tab:red'
    ax1.plot(day_labels, day_clk["ctr"], color=color1, marker='o', linewidth=2, label='ctr')
    ax1.grid(True, linestyle='--', alpha=0.6)
    ax1.set_xlabel('day')
    ax1.set_ylabel('ctr', color=color1)
    ax1.tick_params(axis='y', labelcolor=color1)

    ax2 = ax1.twinx()
    color2 = 'tab:blue'
    ax2.plot(user_num, color=color2, marker='s', linewidth=2, linestyle='--', label='user_num')
    ax2.grid(True, linestyle='--', alpha=0.6)
    ax2.set_ylabel('num', color=color2)
    ax2.tick_params(axis='y', labelcolor=color2)

    plt.xticks(range(len(day_labels)), day_clk.index, rotation=45)
    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()

    ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper left')
    plt.title('ctr and user_num by Day')
    plt.grid(True, linestyle='--', alpha=0.3)
    plt.tight_layout()
    plt.show()


    plt.show()


def time_ctr_calculate():
    time_label = ["morning","afternoon","night","down"]
    clk_morning = day_clk.query("6<hour<=12")
    clk_afternoon = day_clk.query("12<hour<=18")
    clk_night = day_clk.query("18<hour<=24")
    clk_dawn = day_clk.query("0<hour<=6")
    time_clk = [clk_morning,clk_afternoon,clk_night,clk_dawn]
    time_ctr = [ctr_calculate(tc) for tc in time_clk ]
    user_num = [len(n) for n in time_clk]
    print(user_num)
    print(time_ctr)
    max_and_min(user_num)
    max_and_min(time_ctr)
    fig, ax1 = plt.subplots(figsize=(10, 6))
    color1 = 'tab:red'
    ax1.plot(time_label,time_ctr, color=color1, marker='o', linewidth=2, label='ctr')
    ax1.grid(True, linestyle='--', alpha=0.6)
    ax1.set_xlabel('price')
    ax1.set_ylabel('ctr', color=color1)
    ax1.tick_params(axis='y', labelcolor=color1)

    ax2 = ax1.twinx()
    color2 = 'tab:blue'
    ax2.plot(user_num, color=color2, marker='s', linewidth=2, linestyle='--', label='user_num')
    ax2.grid(True, linestyle='--', alpha=0.6)
    ax2.set_ylabel('num', color=color2)
    ax2.tick_params(axis='y', labelcolor=color2)

    plt.xticks(range(len(time_label)), time_label, rotation=45)
    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()

    ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper left')
    plt.title('ctr and user_num by Time')
    plt.grid(True, linestyle='--', alpha=0.3)
    plt.tight_layout()
    plt.show()

def day_time(day):
    n = day_clk.query("day == {}".format(day))
    k = n.drop_duplicates(subset=["hour"], keep="first")
    print(k)
    print(len(k))
