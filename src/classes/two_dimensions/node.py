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

    def isroot(self) -> bool :
        return self.parent is None
    
    def isexeternal(self) -> bool :
        return None
    
    def wastooclose(self) -> bool :
        return None
    
    def getnumberofrenegades(self) -> int :
        return 0
    
    def getnumberofparticles(self) -> int :
        return 0
    
    def getcenterofmass(self) -> Vector2D :
        return None
    
    def getminimum(self) -> int :
        return 0
    
    def getmaximum(self) -> int :
        return 0
    
    def gettheta(self) -> float :
        return 0

    def getquadrant(self, x : float, y : float) -> Equadrant :
        return None

    # others methods

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