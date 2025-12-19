from matplotlib import pyplot as plt
import pandas as pd
from 点击率分析 import ctr_calculate,max_and_min
from 价格和点击率分析 import price_and_clk_analysis
pd.set_option('display.float_format', '{:.4f}'.format)  # 4位小数

sample = pd.read_csv("D:/代码集合/数据分析/ad-database-analysis-project/原始数据/raw_sample.csv")
user = pd.read_csv("D:/代码集合/数据分析/ad-database-analysis-project/已清洗数据/user_profile_clean.csv")
ad = pd.read_csv("D:/代码集合/数据分析/ad-database-analysis-project/已清洗数据/ad_feature_clean.csv")

user = pd.DataFrame({"user_id": user["userid"], "gender": user["final_gender_code"], "occupation": user["occupation"],
                     "age": user["age_level"], "shopping_level": user["shopping_level"]})
clk = pd.DataFrame({"user_id": sample["user"], "clk": sample["clk"], "work_id": sample["adgroup_id"]})
price = pd.DataFrame({"work_id": ad["adgroup_id"], "price": ad["price"]})

user_and_clk = clk.merge(user, on="user_id", how="left").dropna()
user_and_price = user_and_clk.merge(price, on="work_id")


def gender_ctr_calculate():
    male_clk = user_and_clk.query("gender == 1")
    female_clk = user_and_clk.query("gender == 2")
    gender_clk = [male_clk, female_clk]
    gender_labels = ["male", "female"]
    gender_ctr = [ctr_calculate(n) for n in gender_clk]
    gender_user_num = [len(n) for n in gender_clk]
    print(gender_ctr)
    print(gender_user_num)
    print(max_and_min(gender_user_num))
    print(max_and_min(gender_ctr))
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

    # 第一个图：点击率柱状图
    bars1 = ax1.bar(gender_labels, gender_ctr, color='blue', edgecolor='black')
    ax1.set_title('ctr', fontsize=14, fontweight='bold')
    ax1.set_ylabel('ctr', fontsize=12)
    ax1.set_xlabel('gender', fontsize=12)
    ax1.grid(True, axis='y', linestyle='--', alpha=0.3)

    # 在柱子上添加数值标签
    for bar in bars1:
        height = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width() / 2., height + 0.001,
                 f'{height:.3f}', ha='center', va='bottom', fontsize=10)

    # 第二个图：用户数柱状图
    bars2 = ax2.bar(gender_labels, gender_user_num, color='red', edgecolor='black')
    ax2.set_title('gender_user_num', fontsize=14, fontweight='bold')
    ax2.set_ylabel('num', fontsize=12)
    ax2.set_xlabel('gender', fontsize=12)
    ax2.grid(True, axis='y', linestyle='--', alpha=0.3)
    ax2.ticklabel_format(style='plain', axis='y')  # 禁用科学计数法

    # 在柱子上添加数值标签（带千分位）
    for bar in bars2:
        height = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width() / 2., height + height * 0.01,
                 f'{int(height):,}', ha='center', va='bottom', fontsize=10)

    # 调整布局
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.show()


def gender_and_price_and_clk():
    male_clk = user_and_price.query("gender == 1")
    female_clk = user_and_price.query("gender == 2")
    price_and_clk_analysis(male_clk)
    price_and_clk_analysis(female_clk)
    print("男性浏览的商品价格分布\n", male_clk["price"].describe(), "\n",
          "女性浏览的商品价格分布\n", female_clk["price"].describe(), "\n")
    print("男性点击的商品价格分布\n", male_clk.query("clk == 1")["price"].describe(), "\n",
          "女性浏览的商品价格分布\n", female_clk.query("clk == 1")["price"].describe())


def occupation_analysis():
    occupation = user_and_price.query("occupation == 1")
    occupation_ctr = ctr_calculate(occupation)
    price_and_clk_analysis(occupation)
    print("大学生的点击率", occupation_ctr)
    print("大学生浏览商品价格分布", occupation["price"].describe())
    print("大学生点击商品价格分布", occupation.query("clk == 1")["price"].describe())


def shopping_level_ctr():
    shopping_level = [1, 2, 3]
    sl_clk = [user_and_price.query("shopping_level == {}".format(n)) for n in shopping_level]
    sl_num = [len(n) for n in sl_clk]
    sl_ctr = [ctr_calculate(n) for n in sl_clk]
    print(sl_ctr)
    print(sl_num)
    print(max_and_min(sl_ctr))
    print(max_and_min(sl_num))
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    # 第一个图：点击率柱状图
    bars1 = ax1.bar(shopping_level, sl_ctr, color='blue', edgecolor='black')
    ax1.set_title('ctr', fontsize=14, fontweight='bold')
    ax1.set_ylabel('ctr', fontsize=12)
    ax1.set_xlabel('shopping_level', fontsize=12)
    ax1.grid(True, axis='y', linestyle='--', alpha=0.3)

    # 在柱子上添加数值标签
    for bar in bars1:
        height = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width() / 2., height + 0.001,
                 f'{height:.3f}', ha='center', va='bottom', fontsize=10)

    # 第二个图：用户数柱状图
    bars2 = ax2.bar(shopping_level, sl_num, color='red', edgecolor='black')
    ax2.set_title('user_num', fontsize=14, fontweight='bold')
    ax2.set_ylabel('num', fontsize=12)
    ax2.set_xlabel('shopping_level', fontsize=12)
    ax2.grid(True, axis='y', linestyle='--', alpha=0.3)
    ax2.ticklabel_format(style='plain', axis='y')  # 禁用科学计数法

    # 在柱子上添加数值标签（带千分位）
    for bar in bars2:
        height = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width() / 2., height + height * 0.01,
                 f'{int(height):,}', ha='center', va='bottom', fontsize=10)

    # 调整布局
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.show()

def age_level_ctr():
    age_level = ["0","1","2","3","4","5","6"]
    age_clk = [user_and_price.query("age == {}".format(n)) for n in age_level]
    age_num = [len(n) for n in age_clk]
    age_ctr = [ctr_calculate(n) for n in age_clk]
    print(age_ctr)
    print(age_num)
    print(max_and_min(age_ctr))
    print(max_and_min(age_num))
    for i in age_clk :
        print("各年龄层浏览价格分布：",i["price"].describe(), "\n")
    for i in age_clk:
        print("各年龄层点击价格分布：",i.query("clk == 1")["price"].describe(), "\n")
    fig, ax1 = plt.subplots(figsize=(10, 6))
    color1 = 'tab:red'
    ax1.plot(age_level, age_ctr, color=color1, marker='o', linewidth=2, label='ctr')
    ax1.grid(True, linestyle='--', alpha=0.6)
    ax1.set_xlabel('age')
    ax1.set_ylabel('ctr', color=color1)
    ax1.tick_params(axis='y', labelcolor=color1)

    ax2 = ax1.twinx()
    color2 = 'tab:blue'
    ax2.plot(age_num, color=color2, marker='s', linewidth=2, linestyle='--', label='user_num')
    ax2.grid(True, linestyle='--', alpha=0.6)
    ax2.set_ylabel('num', color=color2)
    ax2.tick_params(axis='y', labelcolor=color2)

    plt.xticks(range(len(age_level)), age_level, rotation=45)
    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()

    ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper left')
    plt.title('ctr and user_num by Price Segment')
    plt.grid(True, linestyle='--', alpha=0.3)
    plt.tight_layout()
    plt.show()

age_level_ctr()
