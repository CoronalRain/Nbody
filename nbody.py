"""
N-body Simulator 1.0

Usage:
  nbody.py [options]
  nbody.py (-h | --help)
  nbody.py --version

Options:
  -n --num <int>       Number of stars.
                       [default: 50]
  -t --trails          Show star trails?
  -i --initial         Initial velocities?
  -m --ms <int>        Milliseconds between frames in the animation.
                       [default: 10]
  -c --cmap <string>   Colormap to use for star luminosity.
                       [default: RdYlBu]
  -h --help            Show this screen.
  --version            Show version.
"""

from docopt import docopt

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

class Cluster():
    def __init__(self, n, initial):
        self.stars = np.empty(n, dtype=object)
        for i in range(n):
            pos = np.array([np.random.randn(), np.random.randn()])*4.2e16
            vel = np.array([0, 0])
            if initial:
                vel = 4e-15*np.array([pos[1], -pos[0]])
            force = np.array([0, 0])
            mass = 2e30*np.random.gamma(1.5,1)
            color = mass
            if np.random.randint(2) == 0:
                color = -mass
            color += np.random.randn()
            self.stars[i] = Star(pos, vel, force, mass, color)
    
    def update(self, x, trails):
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
        self.scat = self.ax.scatter(pos_x, pos_y, s=radius, c=color, cmap=plt.get_cmap("RdYlBu"))
    
    def animate(self, trails, ms, cmap):
        self.fig = plt.figure(figsize=(10,10))
        self.ax = self.fig.add_subplot(111, axisbg="black")
        lim = 1.5e17
        self.ax.set_xlim([-lim,lim])
        self.ax.set_ylim([-lim,lim])
        pos_x = [self.stars[i].pos[0] for i in range(len(self.stars))]
        pos_y = [self.stars[i].pos[1] for i in range(len(self.stars))]
        radius = [self.stars[i].radius for i in range(len(self.stars))]
        color = [self.stars[i].color for i in range(len(self.stars))]
        self.scat = self.ax.scatter(pos_x, pos_y, s=radius, c=color, cmap=plt.get_cmap(cmap))
        self.ani = animation.FuncAnimation(self.fig, self.update, interval=ms, repeat=False, fargs=[trails])
        plt.show()



class Star():
    def __init__(self, pos, vel, force, mass, color):
        self.pos = pos.astype(np.float64)
        self.vel = vel.astype(np.float64)
        self.force = force.astype(np.float64)
        self.mass = float(mass)
        self.radius = float(mass/0.25e29)
        self.color = float(color)
    
    def update(self):
        dt = 2000000000000
        self.vel += (self.force / self.mass * dt).astype(np.float64)
        self.pos += (self.vel * dt).astype(np.float64)
    
    def reset_force(self):
        self.force = np.array([0, 0], dtype=np.float64)
    
    def compute_force(self, other):
        eps = float(1e16)
        G = float(6.674e-11)
        m1 = float(self.mass)
        m2 = float(other.mass)
        r = float(self.distance(other))
        F = float(-G*m1*m2 / (r**2+eps**2))
        f_x = float(F * (self.pos[0] - other.pos[0]) / r)
        f_y = float(F * (self.pos[1] - other.pos[1]) / r)
        self.force[0] += f_x
        self.force[1] += f_y
    
    def distance(self, other):
        return np.sqrt((self.pos[0] - other.pos[0])**2 + (self.pos[1] - other.pos[1])**2)





if __name__ == '__main__':
    arguments = docopt(__doc__, version = "N-body Simulator 1.0")
    
    n = int(arguments["--num"])
    trails = arguments["--trails"]
    initial = arguments["--initial"]
    ms = int(arguments["--ms"])
    cmap = arguments["--cmap"]
    
    cluster = Cluster(n, initial)
    cluster.animate(trails, ms, cmap)
