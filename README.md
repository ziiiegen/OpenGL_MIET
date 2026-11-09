# Установка и запуск лабораторных

Нужен установленный Python. На ПК университета скопируй всю папку проекта, кроме `.venv`.

**1. Открой PowerShell в папке проекта и создай окружение:**

```powershell
cd D:\university\ComputeGraphics
python -m venv .venv
```

**2. Установи PyOpenGL из папки `lib` (интернет не нужен):**

```powershell
.\.venv\Scripts\python.exe -m pip install --no-index .\lib\pyopengl-3.1.10-py3-none-any.whl
```

**3. Установи остальные библиотеки (нужен интернет):**

```powershell
.\.venv\Scripts\python.exe -m pip install Pillow numpy matplotlib
```

PyOpenGL — 3D-графика (лабы 2–4), Pillow — текстуры (лаба 4), NumPy и Matplotlib — вычисления и графики (лаба 1).

**4. Запусти нужную лабу одной из команд:**

```powershell
.\.venv\Scripts\python.exe .\lab1\CG_lab1.py
.\.venv\Scripts\python.exe .\lab2\main.py
.\.venv\Scripts\python.exe .\lab3\main.py
.\.venv\Scripts\python.exe .\lab4\main.py
```

Активация окружения не требуется. Если папка проекта находится в другом месте, измени путь в `cd`.
