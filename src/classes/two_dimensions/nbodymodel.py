import random

from math import sqrt, sin, cos, pi
from sys import float_info

from classes.two_dimensions.particledata import PlainOldDataAuxState, PlainOldDataState
from classes.two_dimensions.node import Node
from classes.two_dimensions.vector import Vector2D
from classes.two_dimensions.constants import Constants
from classes.two_dimensions.particledata import ParticleData,PlainOldDataAuxState,PlainOldDataState

class NBodyModel :
    gamma = Constants.gamma / (Constants.parsecinmeter ** 3) * Constants.massofsun * ((365.25 * 86400) ** 2)

    def __init__(self) -> None:
        
        self.initialpstate : PlainOldDataState = None
        self.initialpauxstate : PlainOldDataAuxState = None
        self.root : Node = Node(Vector2D(), Vector2D())
        self.minimum : Vector2D = Vector2D()
        self.maximum : Vector2D = Vector2D()
        self.center : Vector2D = Vector2D()
        self.roi : float = 1
        self.timestep : float = 1
        self.numberofparticle : int = 0
        self.verbose = False
        self.dimension = 1

        Node.gamma = NBodyModel.gamma

    # Setters
    
    def setroi(self, roi : float) :
        self.roi = roi

    def setdimension(self, dimension : int) :
        self.dimension = dimension

    def setverbose(self,verbose : bool) :
        self.verbose = verbose

    def settheta(self, theta : float) :
        self.root.settheta(theta = theta)

    # Getters
    
    def getroi(self) -> float :
        return self.roi
    
    def getcenterofmass(self) -> Vector2D:
        # TODO: Normalement il retourne un Vector3D mais je vais use le 2D d'abord vu que dans le 3D le z = 0
        return self.root.getcenterofmass()
    
    def gettimestep(self) -> float :
        return self.timestep
    
    def getinitialstate(self) -> float :
        return self.initialpstate
    
    def getpauxstate(self) :
        return self.initialpauxstate
    
    def getrootnode(self) -> Node:
        return self.root
    
    def getnumberofparticles(self) -> int :
        return self.numberofparticle

    def gettheta(self) -> float: 
        return self.root.gettheta()
    # others methods

    def getorbitalvelocity(self, particledataone : ParticleData, particledatatwo : ParticleData) :
        x1 = particledataone.pstate.x
        y1 = particledataone.pstate.y
        m1 = particledataone.pauxstate.mass

        x2 = particledatatwo.pstate.x
        y2 = particledatatwo.pstate.y

        r = [x1 - x2, y1 - y2]

        dist : float = sqrt((r[0]**2) + (r[1]**2))

        v :  float = sqrt(NBodyModel.gamma * m1 / dist)

        particledatatwo.pstate.vx = (r[1] / dist) * v
        particledatatwo.pstate.vy = (-r[0] / dist) * v

    def resetdimension(self, numberofparticle : int, stepsize : float) :
        
        self.numberofparticle = numberofparticle

        self.setdimension(self.numberofparticle * 4)

        self.initialpstate = [PlainOldDataState() for _ in range(0, numberofparticle)]
        self.initialpauxstate = [PlainOldDataAuxState() for _ in range(0, numberofparticle)]

        self.timestep = stepsize

        self.maximum.x = self.maximum.y = float_info.min
        self.minimum.x = self.minimum.y = float_info.max
        self.center = Vector2D()

    def hell(self, mass) :
        self.center.x /= mass
        self.center.y /= mass

        self.minimum.x = self.center.x - self.roi
        self.maximum.x = self.center.x + self.roi
        self.minimum.y = self.center.y - self.roi
        self.maximum.y = self.center.y + self.roi

        print('Initial particle distribution area')
        print('----------------------------------')
        print('Particle spread :')
        print(f'minimum = ({self.minimum.x},{self.minimum.y})')
        print(f'maximum = ({self.maximum.x},{self.maximum.y})')
        print('Bounding box : ')
        print(f'center = ({self.center.x},{self.center.y})')
        print(f'roi = {self.roi}')

    def initialization(self) :
        self.resetdimension(5000, 100000)

        mass : float = 0

        ct : int = 0

        blackhole : ParticleData = ParticleData()
        macho = [ParticleData() for _ in range(0, 10)]

        for k in range(0, 40) :
            for l in range(0, 100) :
                if ct >= self.numberofparticle :
                    self.hell(mass)

                state : PlainOldDataState  = self.initialpstate[ct]
                auxstate : PlainOldDataAuxState = self.initialpauxstate[ct]

                if ct == 0 :
                    blackhole.pstate = state
                    blackhole.pauxstate = auxstate

                    self.initialpstate[ct].x = self.initialpstate[ct].y = 0
                    self.initialpauxstate[ct].mass = 1000000
                elif ct == 1 :
                    macho[0].pstate = state
                    macho[0].pauxstate = auxstate

                    auxstate.mass = blackhole.pauxstate.mass / 10.0
                    state.x = 5000
                    state.y = 5000

                    self.getorbitalvelocity(blackhole, ParticleData(pstate = state, pauxstate = auxstate))
                elif ct == 2 :
                    macho[1].pstate = state
                    macho[1].pauxstate = auxstate

                    auxstate.mass = blackhole.pauxstate.mass / 10.0
                    state.x = -5000
                    state.y = -5000

                    self.getorbitalvelocity(blackhole, ParticleData(pstate = state, pauxstate = auxstate))
                else:
                    auxstate.mass = 0.76 + 100 * (random.random())
                    rad = 1200 + k * 100
                    state.x = rad * sin(2 * pi * l / 100.0)
                    state.y = rad * cos(2 * pi * l / 100.0)

                    self.getorbitalvelocity(blackhole, ParticleData(pstate = state, pauxstate = auxstate))

                self.maximum.x = max(self.maximum.x, state.x)
                self.maximum.y = max(self.maximum.y, state.y)
                self.minimum.x = min(self.minimum.x, state.x)
                self.minimum.y = min(self.minimum.y, state.y)

                self.center.x += state.x * auxstate.mass
                self.center.y += state.x * auxstate.mass

                mass += auxstate.mass
                ct += 1

    def initializationofcollisions(self) : 
        self.resetdimension(5000, 100)

        blackhole : ParticleData = ParticleData()
        blackholetwo : ParticleData = ParticleData()

        for i in range(0, self.numberofparticle) :
            state : PlainOldDataState = self.initialpstate[i]
            auxstate : PlainOldDataState = self.initialpauxstate[i]

            if i == 0 :
                blackhole.pstate = state
                blackhole.pauxstate = auxstate

                self.initialpstate[i].x = self.initialpstate[i].y = 0
                self.initialpstate[i].vx = self.initialpstate[i].vy = 0
                self.initialpauxstate[i].mass = 1000000

            elif i < 4000 :
                rad : float = 10
                r : float = 0.1 + 0.8 * (rad * random.random())
                a : float = 2.0 * pi * random.random()

                self.initialpauxstate[i].mass = 0.03 + 20 * random.random()
                self.initialpstate[i].x = r * sin(a)
                self.initialpstate[i].y = r * cos(a)

                self.getorbitalvelocity(blackhole, ParticleData(self.initialpstate[i], self.initialpauxstate[i]))
            
            elif i == 4000 :
                blackholetwo.pstate = state
                blackholetwo.pauxstate = auxstate

                self.initialpstate[i].x = self.initialpstate[i].y = 10
                self.initialpauxstate[i].mass = 100000

                self.getorbitalvelocity(blackhole, blackholetwo)

                blackholetwo.pstate.vx *= 0.9
                blackholetwo.pstate.vy *= 0.9

            else : 
                rad : float = 3
                r : float = 0.1 + 0.8 * rad * random.random()
                a : float = 2.0 * pi * random.random()

                self.initialpauxstate[i].mass = 0.03 + 20 * random.random()
                self.initialpstate[i].x = blackholetwo.pstate.x + r * sin(a)
                self.initialpstate[i].y = blackholetwo.pstate.y + r * cos(a)

                self.getorbitalvelocity(blackholetwo, ParticleData(self.initialpstate[i], self.initialpauxstate[i]))

                self.initialpstate[i].vx += blackholetwo.pstate.vx
                self.initialpstate[i].vy += blackholetwo.pstate.vy
            
            self.maximum.x = max(self.maximum.x, self.initialpstate[i].x)
            self.maximum.y = max(self.maximum.y, self.initialpstate[i].y)
            self.minimum.x = max(self.minimum.x, self.initialpstate[i].x)
            self.minimum.y = max(self.minimum.y, self.initialpstate[i].y)

        l : float = 1.05 * max (self.maximum.x - self.minimum.x, self.maximum.y - self.minimum.y)

        self.roi = l * 1.5

        c : Vector2D = Vector2D(x = self.minimum.x + (self.maximum.x - self.minimum.x) / 2.0, y = self.minimum.y + (self.maximum.y - self.minimum.y) / 2.0)

        self.minimum.x = c.x - l / 2.0
        self.maximum.x = c.x + l / 2.0
        self.minimumy.y = c.y - l / 2.0
        self.maximum.y = c.y + l / 2.0

        print('Initial particle distribution area')
        print('----------------------------------')
        print('Particle spread :')
        print(f'minimum = ({self.minimum.x},{self.minimum.y})')
        print(f'maximum = ({self.maximum.x},{self.maximum.y})')
        print('Bounding box : ')
        print(f'center = ({c.x},{c.y})')
        print(f'l = {l}')

    def initializationbody(self) :
        self.resetdimension(3, 0.5)
        self.root.settheta(0.9)

        self.initialpstate[0].x = 1
        self.initialpstate[0].y = 3
        self.initialpstate[0].vx = self.initialpstate[0].vy = 0
        self.initialpauxstate[0].mass = 3

        self.initialpstate[0].x = -2
        self.initialpstate[0].y = -1
        self.initialpstate[0].vx = self.initialpstate[0].vy = 0
        self.initialpauxstate[0].mass = 4

        self.initialpstate[0].x = -1
        self.initialpstate[0].y = -1
        self.initialpstate[0].vx = self.initialpstate[0].vy = 0
        self.initialpauxstate[0].mass = 5

        for i in range(0, self.numberofparticle) :
            state : PlainOldDataState = self.initialpstate[i]

            self.maximum.x = max(self.maximum.x, state.x)
            self.maximum.y = max(self.maximum.y, state.y)
            self.minimum.x = min(self.minimum.x, state.x)
            self.minimum.y = min(self.minimum.y, state.y)

        l : float = 1.05 * max(self.maximum.x - self.minimum.x, self.maximum.y - self.minimum.y)

        self.roi = l * 1.5

        c : Vector2D = Vector2D(x = self.minimum.x + (self.maximum.x - self.minimum.x) / 2.0, y = self.minimum.y + (self.maximum.y - self.minimum.y) / 2.0)

        self.minimum.x = c.x - l / 2.0
        self.maximum.x = c.x + l / 2.0
        self.minimumy.y = c.y - l / 2.0
        self.maximum.y = c.y + l / 2.0

        print('Initial particle distribution area')
        print('----------------------------------')
        print('Particle spread :')
        print(f'minimum = ({self.minimum.x},{self.minimum.y})')
        print(f'maximum = ({self.maximum.x},{self.maximum.y})')
        print('Bounding box : ')
        print(f'center = ({c.x},{c.y})')
        print(f'l = {l}')
    
    def builttree(self, particles) : 
        self.root.reset(Vector2D(x = self.center.x - self.roi, y = self.center.y - self.roi), Vector2D(x = self.center.x + self.roi, y = self.center.y + self.roi))

        ct : int = 0

        for i in range(0, self.numberofparticle) :
            try :
                particle = ParticleData(pstate = particles[i].pstate, pauxstate = particles[i].pauxstate)
                self.root.insert(particle, 0)

                ct += 1
            except Exception as e :
                print(e)
        
        self.root.computemassdistribution()

        if self.verbose :
            print('TREE DUMP')
            print('---------')
            self.root.dumpnode(-1, 0)
        
        self.center = self.root.getcenterofmass()

    def isfinished() :
        return False