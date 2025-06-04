N = int(input("請輸入元素組數 N (N >= 1)："))
num = N + 2
points = []

for i in range(num):
    x = float(input(f"請輸入第 {i+1} 組的 X 座標："))
    y = float(input(f"請輸入第 {i+1} 組的 Y 座標："))
    points.append((x, y))
    

print("你輸入的座標如下：")
for idx, (x, y) in enumerate(points, 1):
    print(f"X{idx} 為 {x}，Y{idx} 為 {y}")

triangles = []
for i in range(N):
    indices = input(f"請輸入第 {i+1} 個三角形的三個點編號（以空白分隔，例如 1 2 3）：")
    idx_list = [int(idx) - 1 for idx in indices.split()]
    triangle = [points[idx_list[0]], points[idx_list[1]], points[idx_list[2]]]
    triangles.append(triangle)

print("\n每個三角形的點如下：")
for i, triangle in enumerate(triangles, 1):
    print(f"第 {i} 個三角形：{triangle}")

print("\n每個三角形的面積與 Beta、Gamma 值如下：")
for i, triangle in enumerate(triangles, 1):
    x1, y1 = triangle[0]
    x2, y2 = triangle[1]
    x3, y3 = triangle[2]
    area = abs((x1*(y2-y3) + x2*(y3-y1) + x3*(y1-y2)) / 2.0)
    β1 = y2 - y3
    β2 = y3 - y1
    β3 = y1 - y2
    γ1 = x3 - x2
    γ2 = x1 - x3
    γ3 = x2 - x1
    print(f"第 {i} 個三角形的面積為：{area:.4f}")
    print(f"β1 = {β1:.4f}, β2 = {β2:.4f}, β3 = {β3:.4f}")
    print(f"γ1 = {γ1:.4f}, γ2 = {γ2:.4f}, γ3 = {γ3:.4f}")

# 對每個三角形計算一個 3x3 的 K 矩陣
K_matrices = []
for i, triangle in enumerate(triangles):
    # 直接使用之前計算的 β, γ, area
    x1, y1 = triangle[0]
    x2, y2 = triangle[1]
    x3, y3 = triangle[2]
    area = abs((x1*(y2-y3) + x2*(y3-y1) + x3*(y1-y2)) / 2.0)
    β = [y2 - y3, y3 - y1, y1 - y2]
    γ = [x3 - x2, x1 - x3, x2 - x1]
    K = [[0.0 for _ in range(3)] for _ in range(3)]
    for j in range(3):
        for k in range(3):
            K[j][k] = (β[j] * β[k] + γ[j] * γ[k]) / (4 * area)
    K_matrices.append(K)

for idx, (K, triangle) in enumerate(zip(K_matrices, triangles), 1):
    # 取得該三角形的點編號（原本輸入時是減1的，這裡要加回來）
    indices = []
    for point in triangle:
        indices.append(points.index(point) + 1)
    print(f"\n第 {idx} 個三角形的 K 矩陣各元素為：")
    for i in range(3):
        for j in range(3):
            print(f"K{indices[i]}{indices[j]} = {K[i][j]:.4f}", end="  ")
        print()

# 建立 N+2 x N+2 的大矩陣
big_K = [[0.0 for _ in range(num)] for _ in range(num)]

# 將每個三角形的 K 矩陣加到大矩陣對應位置
for triangle, K in zip(triangles, K_matrices):
    indices = [points.index(point) for point in triangle]  # 這裡是 0-based
    for i in range(3):
        for j in range(3):
            big_K[indices[i]][indices[j]] += K[i][j]

# 輸出大矩陣
print("\n總和後的大 K 矩陣：")
for i in range(num):
    for j in range(num):
        print(f"K{i+1}{j+1} = {big_K[i][j]:.4f}", end="  ")
    print()

print("\n計算完成！")

#輸出每個矩陣各為何值，範例
