import pandas as pd

books = pd.read_excel("D:/代码集合/数据分析/books-price-analysis-project/data/books.xlsx")
price = books["price"]
price = price.str.replace("Â£", "", regex=False).astype(float)  #去掉多余字符并转换为浮点数
price = price.dropna().drop_duplicates()  #删除缺失值，重复值
df1 = pd.DataFrame(price)
df1.to_excel("books(ok).xlsx",index=False)
print(price.describe())
