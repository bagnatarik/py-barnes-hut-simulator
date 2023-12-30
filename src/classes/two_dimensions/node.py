from typing import List

from classes.two_dimensions.vector import Vector2D
from classes.two_dimensions.particledata import ParticleData
from classes.two_dimensions.quandrantenum import Equadrant

class Node :
    # class attribut
    theta : float = 0.9
    gamma : float = 0

    def __init__(self, minimum : Vector2D, maximumm : Vector2D, massofallparticles : float = 0, centerofmass : Vector2D = None, numberofparticles : int = 0, isSubdivided : bool = False, renegades : List[ParticleData] = [], parent : 'Node' = None , children : List['Node'] = None) -> None:
        self.minimum = minimum
        self.maximumm = maximumm

        self.massofallparticles = massofallparticles
        self.centerofmass = centerofmass
        self.center = Vector2D(minimum.x + ((maximumm.x - minimum.x) / 2.0), minimum.y + ((maximumm.y - minimum.y) / 2.0))
        self.numberofparticles = numberofparticles
        self.isSubdivided = isSubdivided
        self.renegades = renegades
        self.parent = parent

        if children is None :
            self.children = []
        elif len(children) > 4 :
            raise ValueError('The Node can only contain 4 children')
        else :
            self.children = children

    # Setter
        
    def settheta(self, theta : float) -> None:
        return None
    
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
        return None
    
    def insert(self, newparticle : ParticleData, level : int) -> None :
        return None
    
    def createquadrantnode(self, equadrant : Equadrant) -> 'Node':
        return None
    
    def computemassdistribution(self) -> None :
        return None
    
    def calculateforce(self, particle : ParticleData) -> Vector2D :
        return 0
    
    def dumpnode(self, quadrant : int, level : int) -> None :
        return 0

    def calculateacceleration(self, particleone : ParticleData, particletwo : ParticleData) -> Vector2D :
        return 0
    
    def calculattreeforce(self, particle : ParticleData) -> Vector2D :
        return 0