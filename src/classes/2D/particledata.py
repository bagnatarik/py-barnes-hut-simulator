class PlainOldDataState : 
    def __init__(self, x : float, y : float, vx : float, vy: float) -> None:
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy

class PlainOldDataAuxState :
    def __init__(self, mass : float) -> None:
        self.mass = mass

class PlainOldDataDerivation :
    def __init__(self, vx : float, vy : float, ax : float, ay : float) -> None:
        self.vx = vx
        self.vy = vy
        self.ax = ax
        self.ay = ay

class ParticleData :
    def __init__(self, pstate : PlainOldDataState = None, pauxstate : PlainOldDataAuxState = None) -> None:
            self.pstate = pstate
            self.pauxstate = pauxstate

    def reset(self) : 
        self.pstate = None
        self.pauxstate = None
        
    def isnull(self) : 
         return (self.pstate is not None) and (self.pauxstate is not None)
    
    @classmethod
    def constructor(cls, particledata) :
        return cls(particledata.pstate, particledata.pauxstate)