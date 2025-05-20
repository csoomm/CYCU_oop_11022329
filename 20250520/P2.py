import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# 讀取CSV檔案
df = pd.read_csv('C:\\Users\\User\\Desktop\\CYCU_oop_11022329\\20250520\\midterm_scores.csv')

# 提取科目名稱
subjects = ['Chinese', 'English', 'Math', 'History', 'Geography', 'Physics', 'Chemistry']

# 定義分數組距
bins = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
bin_labels = [f"{bins[i]}-{bins[i+1]-1}" for i in range(len(bins)-1)]

# 設置圖表大小
plt.figure(figsize=(12, 8))

# 計算每個科目在每個分數組距的人數，並將長條圖分開
bar_width = 0.1  # 每個長條的寬度
x = np.arange(len(bin_labels))  # X 軸位置

for i, subject in enumerate(subjects):
    # 使用 pandas 的 cut 方法將分數分組
    score_groups = pd.cut(df[subject], bins=bins, right=False, labels=bin_labels)
    group_counts = score_groups.value_counts(sort=False)  # 計算每個分數組距的人數
    
    # 繪製長條圖，將每個科目的長條圖分開
    plt.bar(x + i * bar_width, group_counts, width=bar_width, alpha=0.7, label=subject)

# 添加標籤和標題
plt.xlabel('Score Range')
plt.ylabel('Number of Students')
plt.title('Score Distribution by Subject')
plt.xticks(x + (len(subjects) - 1) * bar_width / 2, bin_labels, rotation=45)
plt.legend(title='Subjects')
plt.grid(axis='y', linestyle='--', alpha=0.7)

# 調整佈局並顯示圖表
plt.tight_layout()
plt.show()

#儲存圖表
plt.savefig('score_distribution_by_subject.png')