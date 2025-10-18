from matplotlib import pyplot as plt
import pandas as pd

exl1 = pd.read_excel("D:/代码集合/数据分析/books-price-analysis-project/data/books(ok).xlsx")
plt.hist(exl1,bins=30,edgecolor ='black',alpha = 0.7)
plt.grid(True, linestyle='--', alpha=0.6)
plt.title('books`price')
plt.xlabel('Price')
plt.ylabel('Number')
plt.show()