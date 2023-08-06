# -*- coding: utf-8 -*-
"""
Created on Fri Sep 23 15:36:08 2022

@author: Darshan

fuel class provides the basic information about combustion of nDodacane fuel. The gas file used is nDodecane_Reitz.cti
"""


import cantera as _ct

class fuel:
    
    def __init__(self):
        self.gas=_ct.Solution('nDodecane_Reitz.cti')
        self.density_liquid= 750
        
    def __call__(self):
        return self.gas()
    
    @property
    def mfuel(self):
        return self.gas.mass_fraction_dict()['c12h26']
    
    @property
    def mair(self):
        return 1-self.mfuel
    
    @property
    def FA_ratio(self):
        mfuel=self.mfuel
        
        return mfuel/(1-mfuel)
    
    @property
    def AF_ratio(self):
        return 1/self.FA_ratio
    
    @property
    def eq_ratio(self):
        gas1=_ct.Solution('nDodecane_Reitz.cti')
        gas1.set_equivalence_ratio(1, {'c12h26':1}, {'o2':1.0, 'n2':3.76})
        df1=gas1.mass_fraction_dict()
        mf1=df1['c12h26']
        FA1=mf1/(1-mf1)
        
        return self.FA_ratio/FA1
      
    @property
    def FA_stoich(self):
        gas1=_ct.Solution('nDodecane_Reitz.cti')
        gas1.set_equivalence_ratio(1, {'c12h26':1}, {'o2':1.0, 'n2':3.76})
        df1=gas1.mass_fraction_dict()
        mf1=df1['c12h26']
        return mf1/(1-mf1)
    
    @property
    def AF_stoich(self):
        return 1 / self.FA_stoich
    
    def set_params(self,eq_ratio,T=300,P=_ct.one_atm):
        self.gas.set_equivalence_ratio(eq_ratio, {'c12h26':1}, {'o2':1.0, 'n2':3.76})
        self.gas.TP=T,P
        
    # def equilibrate_HP(self,eq_ratio,T=300,P=_ct.one_atm):
    #     self.gas.set_equivalence_ratio(eq_ratio, {'c12h26':1}, {'o2':1.0, 'n2':3.76})
    #     self.gas.TP=T,P    
    #     self.gas.equilibrate('HP')
    
    # def equilibrate_TP(self,eq_ratio,T=300,P=_ct.one_atm):
    #     self.gas.set_equivalence_ratio(eq_ratio, {'c12h26':1}, {'o2':1.0, 'n2':3.76})
    #     self.gas.TP=T,P    
    #     self.gas.equilibrate('TP')
    
    def heat_release(self,eq_ratio,T=300,P=_ct.one_atm):
        """
        Parameters
        ----------
        eq_ratio : TYPE
            DESCRIPTION.
        T : TYPE, optional
            DESCRIPTION. The default is 300.
        P : TYPE, optional
            DESCRIPTION. The default is _ct.one_atm.

        Returns
        -------
        TYPE
            heat release in J/kg

        """
        self.set_params(eq_ratio,T,P)
        h1=self.gas.enthalpy_mass
        self.gas.equilibrate('TP')
        h2=self.gas.enthalpy_mass
        
        return h1-h2
        
    def T_ad(self,eq_ratio,T=300,P=_ct.one_atm):
        """
        Parameters
        ----------
        eq_ratio : TYPE
            DESCRIPTION.
        T : TYPE, optional
            DESCRIPTION. The default is 300.
        P : TYPE, optional
            DESCRIPTION. The default is _ct.one_atm.

        Returns
        -------
        TYPE
            return adiabatic flame temperature in K.

        """
        self.set_params(eq_ratio,T,P)
        self.gas.equilibrate('HP')
        
        return self.gas.T
        


