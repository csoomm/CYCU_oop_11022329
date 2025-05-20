import pandas as pd
import matplotlib.pyplot as plt

#讀取CSV檔案C:\Users\User\Desktop\CYCU_oop_11022329\20250520\midterm_scores.csv
df = pd.read_csv('C:\\Users\\User\\Desktop\\CYCU_oop_11022329\\20250520\\midterm_scores.csv')
#讀取檔案中名稱為Chinese的欄位
chinese_scores = df['Chinese']
#如果chinese_scores大於60，則將其設為1，否則設為0
chinese_scores = chinese_scores.apply(lambda x: 1 if x > 60 else 0)
#讀取檔案中名稱為English的欄位
english_scores = df['English']
english_scores = english_scores.apply(lambda x: 1 if x > 60 else 0)
#讀取檔案中名稱為Math的欄位
math_scores = df['Math']
math_scores = math_scores.apply(lambda x: 1 if x > 60 else 0)
#history
histhory_scores = df['History']
histhory_scores = histhory_scores.apply(lambda x: 1 if x > 60 else 0)
#geography
geography_scores = df['Geography']
geography_scores = geography_scores.apply(lambda x: 1 if x > 60 else 0)
#physics
physics_scores = df['Physics']
pyysics_scores = physics_scores.apply(lambda x: 1 if x > 60 else 0)
#chemistry 
chemistry_scores = df['Chemistry']
chemistry_scores = chemistry_scores.apply(lambda x: 1 if x > 60 else 0)

#統計Chinese,English,Math,History,Geography,Physics,Chemistry的資料，如果一個橫排有超過四個科目為0，將欄位名為name的內容放入列表
# 統計每一列的科目成績，若超過四個科目為 0，將 name 欄位的內容放入列表
low_score_students = []

# 將各科目成績組合成一個 DataFrame
scores_df = pd.DataFrame({
    'Chinese': chinese_scores,
    'English': english_scores,
    'Math': math_scores,
    'History': histhory_scores,
    'Geography': geography_scores,
    'Physics': physics_scores,
    'Chemistry': chemistry_scores
})

# 遍歷每一列數據
for index, row in scores_df.iterrows():
    # 計算該列中成績為 0 的科目數量
    zero_count = (row == 0).sum()
    # 如果成績為 0 的科目數量超過 4，將對應的 name 欄位加入列表
    if zero_count >= 4:
        low_score_students.append(df.loc[index, 'Name'])

# 輸出結果
print("學生名稱列表（超過四個科目不及格）：", low_score_students)

#將列表製成CSV檔
low_score_df = pd.DataFrame(low_score_students, columns=['Name'])
low_score_df.to_csv('low_score_students.csv', index=False)
