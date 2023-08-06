
class modNum:
    def __init__(self, value, prime):
        assert type(value) == int, 'This only creates Fields with integers'
        assert type(prime) == int, 'This only creates Fields with integers'
        
        if prime <= 0:
            raise Exception("Can't create a Field over 0 or less")
        self.prime = prime
        self.value = value % prime
    
    def __str__(self):
        return f"{self.value} in Field N{self.prime}"

    def __repr__(self):
        return f"{self.value} in Field N{self.prime}"
    
    def __eq__(self,other):
      if self.prime == other.prime:
          if self.value == other.value:
              return True
      return False
      
    def __add__(self,other):
        modNum.__type_val_check(self,other)
        
        value = (self.value + other.value) % self.prime
        return modNum(value,self.prime)
    
    #def __radd__(self,other):
    #    modNum.__type_val_check(self,other)
    #    
    #    if other.value == 0:
    #        return self.value
    #    else:
    #        return self + other
        
    def __sub__(self,other):
        modNum.__type_val_check(self,other)
        
        temp = self.value + modNum.addInverse(other).value
        return modNum(temp,self.prime)

    
    def __mul__(self,other):
        modNum.__type_val_check(self,other)
        
        value = (self.value * other.value) % self.prime
        return modNum(value,self.prime)

    def __imul__(self,other):
        modNum.__type_val_check(self,other)
        
        self.value = (self.value * other.value) % self.prime
        return self

    def __floordiv__(self,other):
        modNum.__type_val_check(self,other)
        
        temp = (self.value * modNum.mulInverse(other).value)
        return modNum(temp,self.prime)
    
    def __truediv__(self,other):
        modNum.__type_val_check(self,other)
        
        temp = (self.value * modNum.mulInverse(other).value)
        return modNum(temp,self.prime)

    def __pow__(self,exp):
        if type(exp) != int:
            raise Exception
        else:
            if exp == 0:
                return modNum(1,self.prime)
            elif exp <0:
                temp = modNum.mulInverse(self).value
                exp = -1 * exp
            else:
                temp = self.value
            value = temp ** exp
            return modNum(value,self.prime)
    
    def addInverse(self):

        if self.value == 0:
            return self
        else:
            return modNum((-self.value),self.prime)
    
    def mulInverse(self):

        if self.value == 0 or self.value == 1:
            return self
        else:
            rOne = self.value
            rZero = self.prime
            tZero = 0
            tOne = 1
            rTemp = 100
            q= 0
            
            while rTemp != 0: 
                q = (rZero//rOne)
                rTemp = ( rZero - (q * rOne) )
                rZero = rOne
                rOne = rTemp
                tTemp = tZero - (q * tOne) 
                tZero = tOne
                tOne = tTemp
            
            return modNum(tZero,self.prime)
    
    def __type_val_check(self,other):
        assert type(other) == type(self), 'In a / other, either a or other is not a modNum'
        assert self.prime == other.prime, f"Can't do operations on modNums from different groups N{self.prime} and N{other.prime}"

    
    def sqrt(self):
        assert type(self) == modNum, "Can't use finite square root on non finite field number"
        
        def legendre_symbol(self):
            ls = pow(self.value, (self.prime - 1) // 2, self.prime)
            if ls == self.prime-1:
                return -1
            else:
                return ls
            
        if legendre_symbol(self) != 1:
            return modNum(0,self.prime)
        if self.value     == 0:
            return modNum(0,self.prime)
        if self.prime % 4 == 3:
            return modNum(pow(self.value, (self.prime + 1) // 4, self.prime),self.prime)
        s,e  = self.prime-1, 0
        
        while s % 2 == 0:
            s,e  = s // 2, e + 1
            n = 2
        while legendre_symbol(n) != -1:
            n += 1
            x,b,g,r = pow(self.value, (s + 1) // 2, self.prime), pow(self.value, s, self.prime), pow(n, s, self.prime), e
        while True:
            t,m = b, 0
            for m in range(r):
                if t == 1:
                    break
                t = pow(t, 2, self.prime)
            if m == 0:
                return modNum(x,self.prime)
            gs = pow(g, 2 ** (r - m - 1), self.prime)
            g = (gs * gs) % self.prime
            x = (x * gs) % self.prime
            b = (b * g) % self.prime
            r = m

