from typing import List
from math import sqrt

from classes.two_dimensions.vector import Vector2D
from classes.two_dimensions.particledata import ParticleData, PlainOldDataState, PlainOldDataAuxState
from classes.two_dimensions.quandrantenum import Equadrant

class Node :
    # class attribut
    theta : float = 0.9
    gamma : float = 0
    soft : float = 0.1 * 0.1

    def __init__(self, minimum : Vector2D, maximumm : Vector2D, massofallparticles : float = 0, centerofmass : Vector2D = None, numberofparticles : int = 0, isSubdivided : bool = False, renegades : List[ParticleData] = [], parent : 'Node' = None , children : List['Node'] = [None, None, None, None], particle : ParticleData = None) -> None:
        self.minimum = minimum
        self.maximumm = maximumm

        self.particle = particle
        self.massofallparticles = massofallparticles
        self.centerofmass = centerofmass
        self.center = Vector2D(minimum.x + ((maximumm.x - minimum.x) / 2.0), minimum.y + ((maximumm.y - minimum.y) / 2.0))
        self.numberofparticles = numberofparticles
        self.isSubdivided = isSubdivided
        self.renegades = renegades
        self.parent = parent

        if len(children) > 4 :
            raise ValueError('The Node can only contain 4 children')
        else :
            self.children = children

    # Setter
            
    def settheta(self, theta : float) -> None:
        Node.theta = theta
    
    # Getter
    
    def getnumberofrenegades(self) -> int :
        return self.renegades
    
    def getnumberofparticles(self) -> int :
        return self.numberofparticles
    
    def getcenterofmass(self) -> Vector2D :
        return self.centerofmass
    
    def getminimum(self) -> Vector2D :
        return self.minimum
    
    def getmaximum(self) -> Vector2D :
        return self.maximumm
    
    def gettheta(self) -> float :
        return Node.theta

    def getquadrant(self, x : float, y : float) -> Equadrant :
        if x <= self.center.x and y <= self.center.y :
            return Equadrant.SW
        elif x <= self.center.x and y >= self.center.y :
            return Equadrant.NW
        elif x >= self.center.x and y >= self.center.y :
            return Equadrant.NE
        elif x >= self.center.x and y <= self.center.y :
            return Equadrant.SE
        elif x > self.maximumm.x or y > self.maximumm.y or x < self.minimum.x or y < self.minimum.y :
            raise ValueError(f'Cannot determine quadrant ! \n' + f'Particle = ({x},{y}) not in quad')
        else:
            raise ValueError('Cannot determine the quadrant !')

    # others methods

    def isroot(self) -> bool :
        return self.parent is None
    
    def isexeternal(self) -> bool :
        return all(quadrant is None for quadrant in self.children)
    
    def wastooclose(self) -> bool :
        return self.isSubdivided

    def reset(self, minimum : Vector2D, maximum : Vector2D) -> None :
        if not self.isroot() :
            raise ValueError('Only the root node may reset the tree')
        
        self.children = [None, None, None, None]

        self.minimum = minimum
        self.maximumm = maximum
        self.center = Vector2D(x = minimum.x + ((maximum.x - minimum.x) / 2.0), y = minimum.y + ((maximum.y - minimum.y) / 2.0))
        self.numberofparticles = 0
        self.massofallparticles = 0
        self.centerofmass = Vector2D(x = 0, y = 0)
        self.renegades = []
    
    def insert(self, newparticle : ParticleData, level : int) -> None :
        particlestate : PlainOldDataState = newparticle.pstate

        if (particlestate.x < self.minimum.x or particlestate.x > self.maximumm.x) or (particlestate.y < self.minimum.y or particlestate.y > self.maximumm.y) :
            raise ValueError('Particle is outside of tree node')
        
        if self.numberofparticles > 1 :

            quandrant : Equadrant = self.getquadrant(particlestate.x, particlestate.y)
            
            if not self.children[quadrant] :
                self.children[quadrant] = self.createquadrantnode(quandrant)
            
            self.children[quandrant].insert(newparticle, level + 1)

        elif self.numberofparticles == 1 :

            if not self.isexeternal() or not self.isroot() :
                raise ValueError('Must be external or the root node')
            
            particlestatetwo : PlainOldDataState = self.particle.pstate

            if (particlestate.x == particlestatetwo.x) and (particlestate.y == particlestatetwo.y) :
                self.renegades.append(newparticle)
            else :
                quadrant : Equadrant = self.getquadrant(x = particlestatetwo.x, y = particlestatetwo.y)

                if self.children[quadrant] == None :
                    self.children[quadrant] = self.createquadrantnode(quadrant)

                self.children[quandrant].insert(self.particle, level + 1)
                self.particle.reset()

                quandrant = self.getquadrant(particlestate.x, particlestate.y)

                if not self.children[quadrant] :
                    self.children[quadrant] = self.createquadrantnode(quadrant)

                self.children[quadrant].insert(newparticle, level + 1)
                
        elif self.numberofparticles == 0 :

            self.particle = newparticle
        
        self.numberofparticles += 1
    
    def createquadrantnode(self, equadrant : Equadrant) -> 'Node':
        match equadrant :
            case Equadrant.SW :
                return Node(minimum = self.minimum, maximumm = self.center, parent = self)
            case Equadrant.NW :
                return Node(minimum = Vector2D(x = self.minimum.x, y = self.center.y), maximumm = Vector2D(x = self.center.x, y = self.maximumm.y), parent = self)
            case Equadrant.NE :
                return Node(minimum = self.center, maximumm = self.maximumm, parent = self)
            case Equadrant.SE :
                return Node(minimum = Vector2D(x = self.center.x, y = self.minimum.y), maximumm = Vector2D(x = self.maximumm.x, y = self.center.y), parent = self)
            case _ : 
                raise ValueError('Cannot determine quadrant !')
    
    def computemassdistribution(self) -> None :
        if self.numberofparticles == 1 :
            particlestate : PlainOldDataState = self.particle.pstate
            particleauxstate : PlainOldDataAuxState = self.particle.pauxstate
            
            assert(particlestate)
            assert(particleauxstate)

            self.massofallparticles = particleauxstate.mass
            self.centerofmass = Vector2D(x = particlestate.x, y = particlestate.y)

        else :
            self.massofallparticles = 0
            self.centerofmass = Vector2D(x = 0, y = 0)

            for i in range(0, len(self.children)) :
                quadrant = self.children[i]
                if quadrant :
                    quadrant.computemassdistribution()
                    self.massofallparticles += quadrant.massofallparticles
                    self.centerofmass.x += quadrant.centerofmass.x * quadrant.massofallparticles
                    self.centerofmass.y += quadrant.centerofmass.y * quadrant.massofallparticles

            self.centerofmass.x /= self.massofallparticles
            self.centerofmass.y /= self.massofallparticles
    
    def calculateforce(self, particle : ParticleData) -> Vector2D :
        acceleration : Vector2D = self.calculattreeforce(particle = particle)

        if len(self.renegades) > 0 : 
            for vector in self.renegades :
                buffer : Vector2D = self.calculateacceleration(particle, vector)
                acceleration.x += buffer.x
                acceleration.y += buffer.y

        return acceleration
    
    def dumpnode(self, quadrant : int, level : int) -> None :
        description : str = ''

        for i in range(0, level) :
            space += ' '

        print(f'Quadrant {quadrant} (numberofparticle = {self.numberofparticles}, massofallparticles = {self.massofallparticles}, cx = {self.centerofmass.x}, cy = {self.centerofmass.y})')

        for i in range(0, len(self.children)) :
            if self.children[i] :
                self.children[i].dumpnode(i, level + 1)

    def calculateacceleration(self, particleone : ParticleData, particletwo : ParticleData) -> Vector2D :
        acceleration : Vector2D = Vector2D(x = 0, y = 0)

        if particleone == particletwo :
            return acceleration
        
        particleonex = particleone.pstate.x
        particletwox = particletwo.pstate.x
        particleoney = particleone.pstate.y
        particletwoy = particletwo.pstate.y

        particletwomass = particletwo.pauxstate.mass

        r : float = sqrt( ( ( particleonex - particletwox )**2 ) + ( ( particleoney - particletwoy )**2 ) + Node.soft)

        if r > 0 :
            k : float = (Node.gamma * particletwomass) / (r**3)

            acceleration.x += k * (particletwox - particleonex)
            acceleration.y += k * (particletwoy - particleoney)
        else :
            acceleration.x = acceleration.y = 0

        return acceleration
    
    def calculattreeforce(self, particle : ParticleData) -> Vector2D :
        acceleration : Vector2D = Vector2D(x = 0, y = 0)
        r = k = d = 0

        if self.numberofparticles == 1 :
            acceleration = self.calculateacceleration(particle, self.particle)
        else :
            r = sqrt(((particle.pstate.x - self.centerofmass.x)**2) + ((particle.pstate.y - self.centerofmass.y)**2))
            d = self.maximumm - self.minimum

            if (d / r) <= Node.theta :
                self.isSubdivided = False
                k = (Node.gamma * self.massofallparticles) / (r**3)
                acceleration.x = k * (self.centerofmass.x - particle.pstate.x) 
                acceleration.x = k * (self.centerofmass.y - particle.pstate.y) 
            else :
                self.isSubdivided = True

                for i in range(0, self.children) :
                    quadrant = self.children[i]
                    if(quadrant) :
                        buffer = quadrant.calculateforce(particle=particle)

                        acceleration.x += buffer.x
                        acceleration.y += buffer.y

        return acceleration