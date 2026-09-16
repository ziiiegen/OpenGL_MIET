import matplotlib.pyplot as plt
import numpy as np

# Зададим случайные точки K и L через которые будет проиходить отражение.
K = [-1, 2.9]
L = [2, -3.7]
k = (L[1]-K[1])/(L[0]-K[0])
b = K[1]-k*K[0]
phi = np.arctan(k) 
cos_phi = np.cos(phi)
sin_phi = np.sin(phi)
# получим уравнение y = -2.2*x + 0.7
# Отрисуем линию по точкам
x_arr = np.linspace(-5, 5)
def plotLine():
    plt.plot(x_arr, k * x_arr + b)
    plt.plot(K[0], K[1], 'ro')
    plt.plot(L[0], L[1], 'ro')

plotLine()
plt.axis('equal')
plt.xlim(-5, 5)  
plt.ylim(-5, 5) 
plt.grid()
plt.show()


# Задание 1
# Пусть объектом отражения будет треугольник ABC:
def plotTriangle(a, b, c):
    plt.plot([a[0], b[0], c[0], a[0]], [a[1], b[1], c[1], a[1]], marker='o')

A = [-3.8, -4.0]
B = [-3.5, -0.2]
C = [-2.0, -2.0]
# Отрисуем его
plotLine()
plotTriangle(A, B, C)
plt.axis('equal')
plt.xlim(-5, 5)  
plt.ylim(-5, 5) 
plt.grid()
plt.show()

# матрица переноса
T1 = np.array([
    [1, 0, -K[0]],
    [0, 1, -K[1]],
    [0, 0, 1]
])

# Матрица поворота на -phi 
R1 = np.array([
    [cos_phi, sin_phi, 0],  
    [-sin_phi, cos_phi, 0], 
    [0, 0, 1]
])

# Матрица отражения относительно оси X
S = np.array([
    [1, 0, 0],
    [0, -1, 0],
    [0, 0, 1]
])

# Матрица обратного поворота на +phi
R2 = np.array([
    [cos_phi, -sin_phi, 0],
    [sin_phi, cos_phi, 0],
    [0, 0, 1]
])

# Матрица обратного переноса
T2 = np.array([
    [1, 0, K[0]],
    [0, 1, K[1]],
    [0, 0, 1]
])

M = T2 @ R2 @ S @ R1 @ T1

print("Итоговая матрица преобразования M:")
print(M)

# Применим матрицу к нашим точкам (труегольнику)
P = np.array([
    [A[0], B[0], C[0]], # x
    [A[1], B[1], C[1]], # y
    [1,    1,    1   ]  # w
])

P_transformed = M @ P

# Переводим из однородных координат в декартовы
x_res = P_transformed[0, :] / P_transformed[2, :]; print(x_res)
y_res = P_transformed[1, :] / P_transformed[2, :]; print(y_res)

# Получили:
plotLine()
plotTriangle(A, B, C)
plotTriangle([x_res[0], y_res[0]], [x_res[1], y_res[1]], [x_res[2], y_res[2]])
plt.axis('equal')
plt.xlim(-5, 5)  
plt.ylim(-5, 5) 
plt.grid()
plt.show()

# Задание 2 (4 балла)
# Прямая k*x - y + b = 0 имеет нормаль n = (k, -1).

a_line = k
b_line = -1
d_line = b

# Вектор направления лучей от бесконечно удаленного источника света.
l_vec = np.array([1.0, 0.5])
n_dot_l = a_line*l_vec[0] + b_line*l_vec[1]

M4 = np.array([
    [1 - a_line*l_vec[0]/n_dot_l, -b_line*l_vec[0]/n_dot_l, -d_line*l_vec[0]/n_dot_l],
    [-a_line*l_vec[1]/n_dot_l, 1 - b_line*l_vec[1]/n_dot_l, -d_line*l_vec[1]/n_dot_l],
    [0, 0, 1]
])

print("Матрица параллельного проектирования:")
print(M4)

P_shadow = M4 @ P
x_shadow = P_shadow[0, :] / P_shadow[2, :]
y_shadow = P_shadow[1, :] / P_shadow[2, :]
print("Координаты тени:")
print(x_shadow)
print(y_shadow)


plt.figure()
plotLine()
plotTriangle(A, B, C)
plt.plot([], [], color='orange', label='Объект ABC')
plt.plot(x_shadow, y_shadow, 'ko-', linewidth=4, label='Тень')

# Источник на бесконечности нельзя показать конечной точкой.
# Обозначим его параллельными стрелками, направленными к объекту.
for i in range(3):
    start = P[:2, i] - l_vec
    plt.annotate('', xy=P[:2, i], xytext=start, arrowprops=dict(arrowstyle='->', color='goldenrod'))
    plt.plot([P[0, i], x_shadow[i]], [P[1, i], y_shadow[i]], '--', color='goldenrod')

plt.plot([], [], '--', color='goldenrod', label=f'Лучи света, l = ({l_vec[0]}, {l_vec[1]})')
plt.title('Параллельное проектирование. Бесконечно удаленный источник.')
plt.axis('equal')
plt.xlim(-5, 5)
plt.ylim(-5, 5)
plt.legend(loc='upper right', fontsize=8)
plt.grid()
plt.show()


# Задание 3 
# Источник света в конечной точке S
S = np.array([-5.0, -3.9])
n_dot_s = a_line*S[0] + b_line*S[1]

# Двумерный вариант второй матрицы
M5 = np.array([
    [a_line*S[0] - d_line - n_dot_s, b_line*S[0], d_line*S[0]],
    [a_line*S[1], b_line*S[1] - d_line - n_dot_s, d_line*S[1]],
    [a_line, b_line, -n_dot_s]
])

print("Матрица центрального проектирования:")
print(M5)

P_shadow5 = M5 @ P

w = P_shadow5[2, :]

x_shadow5 = P_shadow5[0, :] / w
y_shadow5 = P_shadow5[1, :] / w
print("Координаты тени (5 баллов):")
print(x_shadow5)
print(y_shadow5)

plt.figure()
plotLine()
plotTriangle(A, B, C)
plt.plot([], [], color='orange', label='Объект ABC')
plt.plot(x_shadow5, y_shadow5, 'ko-', linewidth=4, label='Тень')
plt.plot(S[0], S[1], '*', color='goldenrod', markersize=15, label='Источник S')
plt.text(S[0] + 0.15, S[1] - 0.35, 'S')

for i in range(3):
    plt.plot([S[0], x_shadow5[i]], [S[1], y_shadow5[i]],'--', color='goldenrod')
    plt.annotate('', xy=P[:2, i], xytext=S,arrowprops=dict(arrowstyle='->', color='goldenrod'))

plt.title('5 баллов: центральное проектирование')
plt.axis('equal')
plt.xlim(-6, 5)
plt.ylim(-5, 5)
plt.legend(loc='upper right', fontsize=8)
plt.grid()
plt.show()
