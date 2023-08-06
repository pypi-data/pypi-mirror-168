# -*- coding: utf-8 -*-
"""
Created on Sat Sep 24 21:18:56 2022

@author: Darshan Rathod

This module has pipe object. Pressure drop, velocity inside pipe, Raynolds-number etc. is calculated inside the object.
"""

import numpy as _np
# from scipy.optimize import fsolve as _fsolve

if __name__ == '__main__':
    import shared as _shared
else:
    from . import shared as _shared



class pipe:
    '''
    object to calculate basic properties of pipe flow, such as flow velocity, mech number, friction factor, pressure drop etc.
    '''
    
    def __init__(self,dia,units='inch'):
        
        if units == 'inch':
            self.dia_inch = dia
            self.d_in = dia *25.4/1000
        elif units == 'mm':
            self.d_in = dia/1000
            self.dia_inch = self.d_in / (25.4 / 1000)
        elif (units == 'meters' or units == 'meter' or units == 'm'):
            self.d_in = dia
            self.dia_inch = self.d_in / (25.4 / 1000)
            
        self.area=_np.pi*self.d_in**2/4
        self.gas = _shared.air1
    
    def SLPM(self,m=1,P=_shared.one_atm,T=298):
        self.gas.TP=T,P
        rho=self.gas.density
        slpm=m/rho*60000
        return slpm

    def calc_vel(self,m,p,T=300):
        P= p * _shared.one_atm
        area = self.area
        self.gas.TP=T,P
        self.gas.equilibrate('TP')
        rho=self.gas.density
        return m/area/rho
        
    def sound_speed(self,P,T=300):
        self.gas.TP=T,P
        self.gas.equilibrate('TP')
        u1,u2,u3=u_sound(self.gas)
        return u2
        
    def mach_num(self,m,p,T=300):
        P= p * _shared.one_atm
        area = self.area
        self.gas.TP=T,P
        self.gas.equilibrate('TP')
        rho=self.gas.density
        v1 = m/area/rho
        ua = self.sound_speed(p,T)
        return v1/ua
        
    def gamma(self,p,T=300):
        P= p * _shared.one_atm
        self.gas.TP = T,P
        self.gas.equilibrate('TP')
        return self.gas.cp/self.gas.cv
    
    def Re(self,m,p,T=300):
        P= p * _shared.one_atm
        area = self.area
        self.gas.TP=T,P
        self.gas.equilibrate('TP')
        rho=self.gas.density
        v1 = m/area/rho
        Re = rho * v1 * self.d_in / self.gas.viscosity
        return Re
    
    def stag_p(self,p,M,y=1.4):
        # M = self.mach_num(m,p,T)
        # y = self.gamma(p,T)
        return p * (1 + (y-1)/ 2 * M**2)**(y/(y-1))
    
    
    # def pressure_drop(self,m,p,T=300,L=1):
    #     '''

    #     Parameters
    #     ----------
    #     m : TYPE float
    #         DESCRIPTION. mass flow rate in kg.sec
    #     p : TYPE float 
    #         DESCRIPTION. pressure
    #     T : TYPE, optional
    #         DESCRIPTION. The default is 300.
    #     L : TYPE, optional
    #         DESCRIPTION. The default is 1.

    #     Returns
    #     -------
    #     presssure drop (bar) in pipe of length L. calculated from friction factor1 function.

    #     '''
        
    #     fd = self.friction_factor1(m, p, T)
    #     P= p * _shared.one_atm
    #     area = self.area
    #     self.gas.TP=T,P
    #     self.gas.equilibrate('TP')
    #     rho=self.gas.density
    #     v1 = m/area/rho
    #     delp = fd * L * rho * v1**2 / (2*self.d_in)
    #     return delp/_shared.one_atm
        
    
    # def friction_factor1(self,m,p,T=300,x0=0.002):
    #     '''
        
    #     Parameters
    #     ----------
    #     m : TYPE : float
    #         DESCRIPTION : Mass flow rate through pipe in kg/sec
    #     p : TYPE : float
    #         DESCRIPTION : pressure in pipe in bar
    #     T : TYPE, optional : float
    #         DESCRIPTION. Temperature of gas in pipe in Kelvin. The default is 300.

    #     Returns
    #     -------
    #     Friction factor computd through Kármán–Prandtl resistance equation for turbulent flow in smooth pipes.

    #     '''
    #     def func1(x):
    #         # return 1.930 * _np.log(Re1 * x) * x - 0.537 * x - 1 
    #         return 2 * _np.log(Re1 * x) * x - 0.8 * x - 1 
        
    #     Re1 = self.Re(m,p,T)
    #     fe_sqroot = _fsolve(func1,x0 = x0)
    #     print(f'For friction factor calculations:- \n\tFunction output at root value is {func1(fe_sqroot)}')
    #     return fe_sqroot[0]**2
        
    
    # def fanno_flow(self, m,p,T=300,L=1):
        
    #     def func1(M2):
    #         return y*M2**2 * 4 * fd * L / D1 -1 - (y+1) * M2**2 / 2 * (_np.log(M2**2) - _np.log(1+(y-1)/2*M2**2))- y*M2**2 *C1
        
        
    #     y = self.gamma(p,T)
    #     fd = 0.005
    #     D1 = self.d_in
    #     M1 = self.mach_num(m,p,T)
    #     C1 = (-1 / (y * M1**2) - (y+1) / (2*y) * (_np.log(M1**2) - _np.log(1+(y-1)/2*M1**2)))
        
    #     M2 = self.mach_num(m,p/2,T)
    #     M2 = _fsolve(func1,x0 = M2)
    #     M2 = M2[0]
    #     print(f'For fanno flow calculations:- \n\tFunction output at root value is {func1(M2)}')
        
    #     p01 = self.stag_p(p,M1,y)
        
    #     p02 = p01 * M1/M2 * ((2+(y-1)*M2**2) / (2+(y-1)*M1**2))**((y+1)/2/(y-1))
        
    #     return p01 - p02
    
    


