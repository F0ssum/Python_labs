import pygame
import tkinter as tk
from tkinter import filedialog
from OpenGL.GL import *
from OpenGL.GLU import *
import math


def read_file(name):
    try:
        with open(name, "r") as f:
            lines = f.readlines()
            map = []
            for line in lines:
                numbers = [int(x) for x in line.split()]
                map.append(numbers)
        return map
    except:
        print("Ошибка с файлом!")
        return []


class MapViewer:
    def __init__(self, w, h, map, file):
        self.w = w  # Ширина окна
        self.h = h  # Высота окна
        self.map = map  # Данные карты
        self.file = file
        self.zoom = 10
        self.move_x = 0
        self.move_y = 0
        self.angle = 0  # Угол поворота
        self.max_z = max([max(row) for row in map]) if map else 1  # Максимальная высота
        self.min_z = min([min(row) for row in map]) if map else 0  # Минимальная высота
        self.setup_opengl()
        self.make_lines()
        self.make_window()

    def setup_opengl(self):
        pygame.init()
        pygame.display.set_mode((self.w, self.h), pygame.DOUBLEBUF | pygame.OPENGL)
        glClearColor(0, 0, 0, 1)  # Чёрный фон
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluOrtho2D(-self.w / 2, self.w / 2, -self.h / 2, self.h / 2)
        glMatrixMode(GL_MODELVIEW)

    def make_window(self):
        self.window = tk.Tk()
        self.window.title("Настройки карты")
        self.window.geometry("200x200")

        # Ползунок для масштаба
        tk.Label(self.window, text="Масштаб").pack()
        self.zoom_slider = tk.Scale(
            self.window, from_=1, to=20, orient=tk.HORIZONTAL, command=self.change_zoom
        )
        self.zoom_slider.set(self.zoom)
        self.zoom_slider.pack()

        # Кнопка для нового файла
        tk.Button(
            self.window, text="Загрузить новый файл", command=self.new_file
        ).pack()

    # Меняем масштаб
    def change_zoom(self, value):
        self.zoom = float(value)

    # Загружаем новый файл
    def new_file(self):
        file = filedialog.askopenfilename(
            title="Выберите файл FDF",
            filetypes=[("Файлы FDF", "*.fdf"), ("Все файлы", "*.*")],
        )
        if file:
            new_map = read_file(file)
            if new_map:
                self.map = new_map
                self.file = file
                self.max_z = max([max(row) for row in new_map])
                self.min_z = min([min(row) for row in new_map])
                self.make_lines()

    # Преобразуем координаты в изометрию
    def iso(self, x, y, z):
        angle = math.radians(30)  # Угол для изометрии
        x_new = (x - y) * math.cos(angle)
        y_new = (x + y) * math.sin(angle) - z
        return x_new, y_new

    def make_lines(self):
        glNewList(1, GL_COMPILE)
        glBegin(GL_LINES)
        for y in range(len(self.map)):
            for x in range(len(self.map[y])):
                z = self.map[y][x]
                x_iso, y_iso = self.iso(x, y, z)
                # Цвет зависит от высоты
                color = (z - self.min_z) / (self.max_z - self.min_z + 0.0001)
                glColor3f(color, 1 - color, 0)  # Красный-зелёный цвет

                # Линия вправо
                if x < len(self.map[y]) - 1:
                    z_next = self.map[y][x + 1]
                    x_next, y_next = self.iso(x + 1, y, z_next)
                    glVertex2f(x_iso, y_iso)
                    glVertex2f(x_next, y_next)

                # Линия вниз
                if y < len(self.map) - 1:
                    z_next = self.map[y + 1][x]
                    x_next, y_next = self.iso(x, y + 1, z_next)
                    glVertex2f(x_iso, y_iso)
                    glVertex2f(x_next, y_next)
        glEnd()
        glEndList()

    def draw(self):
        glClear(GL_COLOR_BUFFER_BIT)
        glLoadIdentity()
        glTranslatef(self.move_x, self.move_y, 0)
        glRotatef(self.angle, 0, 0, 1)
        glScalef(self.zoom, self.zoom, 1)
        glCallList(1)
        pygame.display.flip()

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False
                if event.key == pygame.K_PLUS:
                    self.zoom += 1
                    self.zoom_slider.set(self.zoom)
                if event.key == pygame.K_MINUS:
                    self.zoom = max(1, self.zoom - 1)
                    self.zoom_slider.set(self.zoom)
                if event.key == pygame.K_LEFT:
                    self.move_x -= 10
                if event.key == pygame.K_RIGHT:
                    self.move_x += 10
                if event.key == pygame.K_UP:
                    self.move_y += 10
                if event.key == pygame.K_DOWN:
                    self.move_y -= 10
                if event.key == pygame.K_r:
                    self.angle += 10
        return True

    def run(self):
        running = True
        while running:
            running = self.check_events()
            try:
                self.window.update()
            except:
                running = False
            self.draw()
        pygame.quit()


# Выбираем файл
def choose_file():
    root = tk.Tk()
    root.withdraw()
    file = filedialog.askopenfilename(
        title="Выберите файл FDF",
        filetypes=[("Файлы FDF", "*.fdf"), ("Все файлы", "*.*")],
    )
    root.destroy()
    return file


if __name__ == "__main__":
    file = choose_file()
    if not file:
        print("Файл не выбран! Закрываем.")
        exit()
    map = read_file(file)
    if map:
        viewer = MapViewer(800, 600, map, file)
        viewer.run()
    else:
        print("Не удалось загрузить карту!")
