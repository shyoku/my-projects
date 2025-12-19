from matplotlib import pyplot as plt
import pandas as pd
from 点击率分析 import ctr_calculate,max_and_min

pd.set_option('display.float_format', '{:.4f}'.format)  # 4位小数

sample = pd.read_csv("D:/代码集合/数据分析/ad-database-analysis-project/原始数据/raw_sample.csv")
ad = pd.read_csv("D:/代码集合/数据分析/ad-database-analysis-project/已清洗数据/ad_feature_clean.csv")

business_labels = ['<50', '50-200', '200-1000', '1000-5000', '5000-2w', '2-10w', '10w+']

clk = pd.DataFrame({"adgroup_id": sample["adgroup_id"], "clk": sample["clk"]})
new_ad_db = ad.merge(clk, on='adgroup_id', how='left')
price_and_clk = pd.DataFrame({"price": new_ad_db["price"], "clk": new_ad_db["clk"]})


def price_and_clk_analysis(price_and_clk):
    price1 = price_and_clk.query("price < 50")
    price2 = price_and_clk.query("50 <= price < 200")
    price3 = price_and_clk.query("200 <= price < 1000")
    price4 = price_and_clk.query("1000 <= price < 5000")
    price5 = price_and_clk.query("5000 <= price < 20000")
    price6 = price_and_clk.query("20000 <= price < 100000")
    price7 = price_and_clk.query("100000 < price")
    price_groups = [price1, price2, price3, price4, price5, price6, price7]
    ctr = [ctr_calculate(price) for price in price_groups]
    user_num = [len(price) for price in price_groups]
    print(ctr)
    print(user_num)
    max_and_min(ctr)
    max_and_min(user_num)

    fig, ax1 = plt.subplots(figsize=(10, 6))
    color1 = 'tab:red'
    ax1.plot(business_labels, ctr, color=color1, marker='o', linewidth=2, label='ctr')
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

    plt.xticks(range(len(business_labels)), business_labels, rotation=45)
    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()

    ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper left')
    plt.title('ctr and user_num by Price Segment')
    plt.grid(True, linestyle='--', alpha=0.3)
    plt.tight_layout()
    plt.show()

