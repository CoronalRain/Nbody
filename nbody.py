import os
import sys
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
import matplotlib.animation as animation
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from PyQt4 import QtGui, uic

if hasattr(sys, '_MEIPASS'):
    ui_path = os.path.join(sys._MEIPASS, "nbody.ui")
else:
    ui_path = "nbody.ui"

Ui_MainWindow, QMainWindow = uic.loadUiType(ui_path)


class MyWindowClass(QMainWindow, Ui_MainWindow):
    def __init__(self, ):
        super(MyWindowClass, self).__init__()
        self.setupUi(self)
        self.setWindowTitle("N-Body Simulator")
        self.last_click = None

        palette = self.mpl_window.palette()
        role = self.mpl_window.backgroundRole()
        palette.setColor(role, QtGui.QColor("black"))
        self.mpl_window.setPalette(palette)

        self.animate_button.clicked.connect(self.animate_button_clicked)
        self.terminate_button.clicked.connect(self.terminate_button_clicked)

    def animate_button_clicked(self):
        if self.last_click != self.animate_button:
            self.last_click = self.animate_button

            n = self.num_stars_spin_box.value()
            cmap = self.colormap_combo_box.currentText()
            initial = self.tan_vel_check_box.isChecked()
            trails = self.star_trails_check_box.isChecked()
            track = self.track_ejecta_check_box.isChecked()

            self.figure = Figure()
            self.canvas = FigureCanvas(self.figure)
            self.axis = self.figure.add_subplot(111, axisbg="black")
            self.axis.get_xaxis().set_visible(False)
            self.axis.get_yaxis().set_visible(False)
            self.figure.tight_layout(pad=0, w_pad=0, h_pad=0)

            self.cluster = Cluster(n, initial)
            self.cluster.animate(trails, track, cmap, self)

            self.mplvl.addWidget(self.canvas)
            self.canvas.draw()

    def terminate_button_clicked(self):
        if self.last_click == self.animate_button:
            self.last_click = self.terminate_button
            self.mplvl.removeWidget(self.canvas)
            self.cluster.ani._stop()


class Cluster():
    def __init__(self, n, initial):
        self.stars = np.empty(n, dtype=object)
        self.radius = 1.5e17

        for i in range(n):
            pos = np.array([np.random.randn(), np.random.randn()]) * 4.2e16
            vel = np.array([0, 0])
            if initial:
                vel = 4e-15 * np.array([pos[1], -pos[0]])
            force = np.array([0, 0])
            mass = 2e30 * np.random.gamma(1.5, 1)
            color = mass
            if np.random.randint(2) == 0:
                color = -mass
            color += np.random.randn()
            self.stars[i] = Star(pos, vel, force, mass, color)

    def update(self, x, trails, cmap, window):
        for star_a in self.stars:
            star_a.reset_force()
            for star_b in self.stars:
                if star_a != star_b:
                    star_a.compute_force(star_b)
        for star in self.stars:
            star.update()

        pos_x = [self.stars[i].pos[0] for i in range(len(self.stars))]
        pos_y = [self.stars[i].pos[1] for i in range(len(self.stars))]
        radius = [self.stars[i].radius for i in range(len(self.stars))]
        color = [self.stars[i].color for i in range(len(self.stars))]

        if not trails:
            self.scat.remove()
        self.scat = window.axis.scatter(pos_x, pos_y, s=radius, c=color, cmap=plt.get_cmap(cmap))

    def animate(self, trails, track, cmap, window):
        if not track:
            window.axis.set_xlim([-self.radius, self.radius])
            window.axis.set_ylim([-self.radius, self.radius])

        pos_x = [self.stars[i].pos[0] for i in range(len(self.stars))]
        pos_y = [self.stars[i].pos[1] for i in range(len(self.stars))]
        radius = [self.stars[i].radius for i in range(len(self.stars))]
        color = [self.stars[i].color for i in range(len(self.stars))]

        self.scat = window.axis.scatter(pos_x, pos_y, s=radius, c=color, cmap=plt.get_cmap(cmap))
        self.ani = animation.FuncAnimation(window.figure, self.update, interval=25, repeat=False, fargs=[trails, cmap, window])
        window.canvas.draw()


class Star():
    def __init__(self, pos, vel, force, mass, color):
        self.pos = pos.astype(np.float64)
        self.vel = vel.astype(np.float64)
        self.force = force.astype(np.float64)
        self.mass = float(mass)
        self.radius = float(mass / 0.25e29)
        self.color = float(color)

    def update(self):
        dt = 2000000000000
        self.vel += (self.force / self.mass * dt).astype(np.float64)
        self.pos += (self.vel * dt).astype(np.float64)

    def reset_force(self):
        self.force = np.array([0, 0], dtype=np.float64)

    def compute_force(self, other):
        eps = float(1e16)
        g = float(6.674e-11)
        m1 = float(self.mass)
        m2 = float(other.mass)
        r = float(self.distance(other))
        f = float(-g * m1 * m2 / (r ** 2 + eps ** 2))
        f_x = float(f * (self.pos[0] - other.pos[0]) / r)
        f_y = float(f * (self.pos[1] - other.pos[1]) / r)
        self.force[0] += f_x
        self.force[1] += f_y

    def distance(self, other):
        return np.sqrt((self.pos[0] - other.pos[0]) ** 2 + (self.pos[1] - other.pos[1]) ** 2)

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    main = MyWindowClass()
    main.show()
    sys.exit(app.exec_())
