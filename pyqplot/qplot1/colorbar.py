class CBar:
    clim = [0, 1]
    orient = 'x'
    xywh_d = [0,0,1,1]
    xywh_p = [0,0,1,1]
    rev = False
    def ctodat(self, cc):
        crel = (cc-self.clim[0]) / (self.clim[1]-self.clim[0])
        if self.orient=='y':
            rng = self.xywh_d[3]
            d0 = self.xywh_d[1]
        elif self.orient=='x':
            rng = self.xywh_d[2]
            d0 = self.xywh_d[0]
        if self.rev:
            d0 = d0+rng
            rng = -rng
        return d0 + rng*crel

    def ctopap(self, cc):
        crel = (cc-self.clim[0]) / (self.clim[1]-self.clim[0])
        if self.orient=='y':
            rng = self.xywh_p[3]
            d0 = self.xywh_p[1]
        elif self.orient=='x':
            rng = self.xywh_p[2]
            d0 = self.xywh_p[0]
        if not self.rev:
            d0 = d0+rng
            rng = -rng
        return d0 + rng*crel
