from . import modNum as md
import random


#class object to store and handle elliptic curve points and operations
# all class variables are private to prevent modification in bad faith or mistake
class EllipticCurve:

    # http://www.secg.org/sec2-v2.pdf
    # The following numbers specifying the field, curve, and inital point were obtained from the following paper.
    # Curve 'nicknamed' -  secp256r1
    
    __prime = 0xFFFFFFFF00000001000000000000000000000000FFFFFFFFFFFFFFFFFFFFFFFF
    
    __a = md.modNum(0xFFFFFFFF00000001000000000000000000000000FFFFFFFFFFFFFFFFFFFFFFFC,__prime)

    __b = md.modNum(0x5AC635D8AA3A93E7B3EBBD55769886BC651D06B0CC53B0F63BCE3C3E27D2604B,__prime)

    __init_point = (0x6B17D1F2E12C4247F8BCE6E563A440F277037D812DEB33A0F4A13945D898C296, 0x4FE342E2FE1A7F9B8EE7EB4A7C0F9E162BCE33576B315ECECBB6406837BF51F5)

    __w = 2**8
    
    def __init__(self,x,y):
        assert (type(x) == int), "Can't initiate Elliptic Curve with anything but an int for x value"
        assert (type(y) == int), "Can't initiate Elliptic Curve with anything but an int for y value"
        
        if x == 0 and y == 0: # zero/infinity in elliptic curves are the same. This boolean allows for easy checking of state
            self.__zero_inf = True
        else:
            self.__zero_inf = False
            
        self.__x = md.modNum( x, EllipticCurve.__prime)
        self.__y = md.modNum( y, EllipticCurve.__prime)

        if not self.__zero_inf: # just checking that the given point is on the curve, could cause weird bugs otherwise
            assert (self.__x ** 3 + self.__a*self.__x + self.__b) == (self.__y ** 2), f"Not a valid point on curve y^2 = x^3 + {self.__a}x + {self.__b}"
        else:
            assert (self.__x.value == 0) and (self.__y.value == 0), 'Weird bug, zero_inf flag set to true but x and y are not both zero)'
            
    def __str__(self):
        if self.__zero_inf:
            return f"Infinity on curve y^2 = x^3 + {self.__a.value}x + {self.__b.value}"
        else:
            return f"Point ({self.__x.value},{self.__y.value}) on curve y^2 = x^3 + {self.__a.value}x + {self.__b.value}"

    def __repr__(self):
        if self.__zero_inf:
            return f"Infinity on curve y^2 = x^3 + {self.__a.value}x + {self.__b.value}"
        else:
            return f"Point ({self.__x.value},{self.__y.value}) on curve y^2 = x^3 + {self.__a.value}x + {self.__b.value}"

    def __eq__(self,other):
        if self.__zero_inf: # self is at zero/inifity
            if other.__zero_inf: # self and other is at zero/infinity
                return True
            return False
        elif other.__zero_inf: # other is at zero/infinity but we already know from
            return False       # not being in the above logic cluster that self is not
                               # at zero/inifinity so can save time by not evaluating the values of self/other
        elif (self.__x.value == other.__x.value): # self and other have same x value
            if (self.__y.value == other.__y.value): # self and other have same y value
                return True # Can't have dif prime/a/b b/c they're immutable so only x/y can ever be different
        return False

    # Want to rewrite this so that Elliptic Curve objects can be multiplied
    #  outside of this file just like regular numbers
    #
    def __mul__(self,other):
        if self.__zero_inf == True:
            return other
        elif other.__zero_inf == True:
            return self
        elif (self.__x == other.__x):
            if (self.__y == md.modNum.addInverse(other.__y)): # self.__y = -other.__y
                return EllipticCurve(0,0)
            else:
                m = (md.modNum(3,self.__prime) * (self.__x ** 2) + self.__a)/(md.modNum(2,self.__prime)*self.__y)
        else:
            m = (other.__y - self.__y)/(other.__x - self.__x)

        tempX = (m ** 2 - self.__x - other.__x)
        tempY = md.modNum.addInverse(self.__y) - ( m * (tempX - self.__x))
        return EllipticCurve(tempX.value,tempY.value)

    def group_inv(self):
        
        if self.__zero_inf:
            return self
        else:
            return EllipticCurve(self.__x.value, md.modNum.addInverse(self.__y).value)

    def __pow__(self,exp):
        if type(exp) != int:
            print(exp)
            raise Exception
        else:
            if exp == 0:
                return EllipticCurve(0,0)
            elif exp<0:
                temp = self.group_inv()
                exp = -1 * exp
            else:
                temp = self

            if exp == 1:
                return temp
            elif (exp % 2) == 0:
                z = EllipticCurve.__pow__(temp,exp//2)
                return z * z
            else:
                z = EllipticCurve.__pow__(temp,(exp-1)//2)
                return z*z*temp
                

    # Get functions
    # Just generic stuff to get values that are hidden so they can't be
    # modified

    def get_prime(self):
        return EllipticCurve.__prime

    def get_a(self):
        return EllipticCurve.__a

    def get_b(self):
        return EllipticCurve.__b

    def get_init_point(self):
        return EllipticCurve.__init_point

    def get_w(self):
        return EllipticCurve.__w

    def get_zero_inf(self):
        return self.__zero_inf

    def get_x(self):
        return self.__x

    def set_w(self,new_w):
        assert type(new_w) == int, 'w must be of type int'
        assert w>=7, 'w can not be to small or else there is significant risk of the encryption process failing'

        EllipticCurve.__w = new_w
