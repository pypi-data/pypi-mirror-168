from typing import Iterable, Tuple
import pydantic

import numpy as np
import matplotlib.pyplot as plt
from ..signal_analysis.specpack import specdata
from ..signal_analysis.timetools import find_peaks
from ..signal_analysis.stats import empirical_cdf as ecdf


class IrregularWave():
    def __init__(self,z:Iterable[float],t:Iterable[float],d:float=1E10,g:float=9.80665):
        """Instantiates a irregular wave class based on an inputted

        Args:
            z (Iterable[float]): time series of wave elevation
            t (Iterable[float]): time
            d (float, optional): water depth. Defaults to 1E10 m (deep water)
            g (float, optional): gravity. Defaults to 9.80665 m/s/s
        """
        m0,m1,m2,m4,T1,T2,Tp,Hm0,Sf,f = specdata(z,t)  
        self.m0 = m0
        self.m1 = m1
        self.m2 = m2
        self.m4 = m4
        self.T1 = T1
        self.T2 = T2
        self.Tp = Tp
        self.Hm0 = Hm0
        self.Sf = Sf
        self.f = f
        self.z = z
        self.t = t
        self.g = g
        self.d = d
        self.sp = 2*np.pi/g*Hm0/Tp**2 # steepness parameter

    def wave_crest_distribution(self, distribution="forristall2d"):
        """Returns a probability of exceedence function f(x) for the wave crest. This
        is 1 - F(x) where F(x) is the cumulative distribution function.
        
        Note that these are ensemble distributions, so comparing against a single
        wave crest distribution may cause misinterpretation. An exception is the
        HuangPDSR distribution, which provides a mean, upper 99% and lower 99% 
        curve for the probability distribution of a single realization. 

        Args:
            distribution (str, optional): The distribution function. Options include:
            
            "forristall2d": Function given in reference /1/ for a long crested wave
            "forristall3d": Function given in reference /1/ for a short crested wave
            "rayleigh": Rayleigh distributed wave heights (ref /1/). 
            Defaults to "forristall2d".            

            References:
            
            /1/ Forristall G.Z. Wave Crest Distribution: Observations and Second-Order Theory,
            American Meteorological Society, 1 August 2000.

        Returns:
            hc(x): crest height probability of exceedence function
        """
        from .regular import StokesSecond
        s1 = 2*np.pi/self.g*self.Hm0/self.T1**2
        ss = StokesSecond(height=self.Hm0, period=self.T1, depth=self.d)
        if distribution == "forristall2d" or distribution == "forristall3d":
            k1 = ss.wavenumber # independent of StokesSecond's height
            urs = self.Hm0/k1**2/self.d**3
            if distribution == "forristall2d":
                ac = 0.3536 + 0.2892*s1 + 0.1060*urs
                bc = 2 - 2.1597*s1 + 0.0968*urs**2
            else:
                ac = 0.3536 + 0.2568*s1 + 0.0800*urs
                bc = 2 - 1.7912*s1 - 0.5302*urs + 0.2824*urs**2                
            return lambda x, ac=ac, bc=bc: np.exp( -(x/ac/self.Hm0)**bc  ) #NOTE: defaults bind at creation
        elif distribution == "rayleigh":
            return lambda x: np.exp( -8*(x/self.Hm0)**2 )
        elif distribution == "huangPDSR" or distribution == "huangPDER":
            k1 = 4*np.pi**2/self.g/self.T1**2  # Deep water dispersion eq. used by Huang
            urs = self.Hm0/k1**2/self.d**3
            pa = np.r_[1,s1,s1**2,s1**3,s1**4,urs,urs**2]
            pb = np.r_[1,s1,s1**2,s1**3,s1**4,urs**2]
            if distribution == "huangPDSR":
                # Mean, lower, upper curves for probability < 1E-2)
                a1 = np.r_[0.2894, 12.3011, -662.6320, 12153.3466, -68031.8045, 0.3779, -3.7904]
                b1 = np.r_[1.5277, 67.2118, -3683.1338, 63759.0846, -336712.3631, -8.1382]
                a2 = np.r_[0.3712,1.0087,-43.0667,567.5292,-1173.1204,0.1276,0.3115]
                b2 = np.r_[2.006,4.841,-321.181,846.332,27223.189,0.832]
                ac1, bc1 = sum(a1*pa), sum(b1*pb)
                ac2, bc2 = sum(a2*pa), sum(b2*pb)
                xlimit = (-np.log(0.01))**(1/bc1)*self.Hm0*ac1
                mean = lambda x, ac1=ac1, ac2=ac2, bc1=bc1, bc2=bc2, xlimit=xlimit: \
                    np.where(x > xlimit, np.exp( -(x/ac1/self.Hm0)**bc1 ), np.exp( -(x/ac2/self.Hm0)**bc2) )             
                a1 = np.r_[0.1334, 13.0432, -751.0935, 14727.6571, -87711.0810, 0.0840, -5.2045]    
                b1 = np.r_[0.7965, 44.9229, -2525.6956, 47184.1324, -270084.1075, -13.3160]     
                a2 = np.r_[0.3516,2.3892,-105.4167,1557.3914,-5807.4512,0.0791,0.3550]
                b2 = np.r_[1.620,19.720,-909.665,10465.556,-22952.443,-3.726]
                ac1, bc1 = sum(a1*pa), sum(b1*pb)
                ac2, bc2 = sum(a2*pa), sum(b2*pb)
                xlimit = (-np.log(0.01))**(1/bc1)*self.Hm0*ac1
                upper = lambda x, ac1=ac1, ac2=ac2, bc1=bc1, bc2=bc2, xlimit=xlimit: \
                    np.where(x > xlimit, np.exp( -(x/ac1/self.Hm0)**bc1 ), np.exp( -(x/ac2/self.Hm0)**bc2) )             
                a1 = np.r_[0.3752, 9.1269, -446.8393, 7837.5720, -42682.1177, 0.8351, -5.7942,]
                b1 = np.r_[2.4637, 82.5688, -4300.5362, 68857.4691, -337914.7489, 2.5661]
                a2 = np.r_[0.3708,0.9835,-39.9404,598.3819,-2144.4920,0.2427,-0.5379]
                b2 = np.r_[2.212,10.951,-637.673,6707.056,-10244.141,4.505]
                ac1, bc1 = sum(a1*pa), sum(b1*pb)
                ac2, bc2 = sum(a2*pa), sum(b2*pb)
                xlimit = (-np.log(0.01))**(1/bc1)*self.Hm0*ac1
                lower = lambda x, ac1=ac1, ac2=ac2, bc1=bc1, bc2=bc2, xlimit=xlimit: \
                    np.where(x > xlimit, np.exp( -(x/ac1/self.Hm0)**bc1 ), np.exp( -(x/ac2/self.Hm0)**bc2) )             
                return (mean,lower,upper)
            elif distribution == "huangPDER":
                a1 = np.r_[0.3242, 11.7467, -652.1470, 12308.3001, -70529.2504, 0.3785, -3.8837]
                b1 = np.r_[1.7321,72.7179,-4093.6916,72132.2957,-386504.7502,-9.9594]
                a2 = np.r_[0.3733, 0.9398, -40.0095, 512.0601, -849.0734, 0.1294, 0.2882]
                b2 = np.r_[2.0411, 3.6068,-272.2806,-58.9649,32786.2976,0.9003]
                ac1, bc1 = sum(a1*pa), sum(b1*pb)
                ac2, bc2 = sum(a2*pa), sum(b2*pb)
                xlimit = (-np.log(0.01))**(1/bc1)*self.Hm0*ac1
                return lambda x, ac1=ac1, ac2=ac2, bc1=bc1, bc2=bc2, xlimit=xlimit: \
                    np.where(x > xlimit, np.exp( -(x/ac1/self.Hm0)**bc1 ), np.exp( -(x/ac2/self.Hm0)**bc2) )                 
        else:
            raise NotImplementedError(f"The {distribution} distribution is not implemented")
            
    def wave_height_distribution(self, distribution="forristall"):
        """Returns a probability of exceedence function f(x) for the wave height. This
        is 1 - F(x) where F(x) is the cumulative distribution function.

        Args:
            distribution (str, optional): The distribution function. Options include:
            
            "forristall": Function given in reference /1/
            "rayleigh": Rayleigh distributed wave heights
            Defaults to "forristall".            

            References:
            
            /1/ Forristall G.Z. On the Statistical Distribution of Wave Heights in a Storm,
            Journal of Geophysical Research Atmospheres, January 1978.
            /2/ Longuet-Higgins, M.S., On the statistical distribution of heights of sea waves.
            Journal of Marine Research 11, 245–266. 1952

        Returns:
            hc(x): wave height probability of exceedence function
        """
        if distribution == "rayleigh":
            return lambda x: np.exp( -2*(x/self.Hm0)**2 )
        elif distribution == "forristall": # 1978
            return lambda x: np.exp( -2.263*(x/self.Hm0)**2.126 )        
        else:
            raise NotImplementedError(f"The {distribution} distribution is not implemented")

    def plot_wave_crest_distribution(self, Hm0:float=None, Tp:float=None, figname:str=None, figsize:Tuple[float]=(10,6)):
        fig, ax = plt.subplots(figsize=figsize)
        ax.set_yscale("log");ax.set_xlim(0,2);ax.set_ylim(1E-6,1);ax.grid(True, which="both")
        ax.set_title(f"Wave crest distribution: Measured Hs={self.Hm0:.1f}m Tp={self.Tp:.1f}s")
        # Plot empirical distribution
        ix = find_peaks(self.z, global_peaks=True)
        Fe, ze = ecdf(len(self.z[ix])), np.sort(self.z[ix])
        ax.scatter(ze/self.Hm0,1-Fe, label="Empirical", color='r')
        # Plot semi-empirical distributions
        h = np.arange(0,30)
        f_huangPDSR = self.wave_crest_distribution(distribution="huangPDSR") # single realization distro
        f_huangPDER = self.wave_crest_distribution(distribution="huangPDER")
        f_forristall2d = self.wave_crest_distribution(distribution="forristall2d")
        f_rayleigh = self.wave_crest_distribution(distribution="rayleigh")
        ax.plot(h/self.Hm0, f_huangPDSR[0](h), color="black",linewidth=2,label="Huang PDSR (mean)")
        ax.plot(h/self.Hm0, f_huangPDSR[1](h), color="black",linewidth=2,label="Huang PDSR (lower)", linestyle='--')
        ax.plot(h/self.Hm0, f_huangPDSR[2](h), color="black",linewidth=2, linestyle='--')
        ax.plot(h/self.Hm0, f_huangPDER(h), color="grey",linewidth=2,label="Huang PDER")
        ax.plot(h/self.Hm0, f_forristall2d(h), color="green",linewidth=2,label="Forristall")
        ax.plot(h/self.Hm0, f_rayleigh(h), color="blue",linewidth=2,label="Rayleigh") 
        ax.legend(loc=0)
        ax.set_xlabel("$\eta_c / H_{m0}$  [-]", fontsize=14)
        ax.set_ylabel("POE [-]", fontsize=14)
        if figname is not None: 
            plt.savefig(figname) 
            plt.close(fig)
        else: 
            plt.show()
            return (fig, ax)      
        
    def plot_wave_height_distribution(self, Hm0:float=None, Tp:float=None, figname:str=None, figsize:Tuple[float]=(10,6)):
        fig, ax = plt.subplots(figsize=figsize)
        ax.set_yscale("log");ax.set_xlim(0,2.5);ax.set_ylim(1E-6,1);ax.grid(True, which="both")
        ax.set_title(f"Wave height distribution: Measured Hs={self.Hm0:.1f}m Tp={self.Tp:.1f}s")
        # Plot empirical distribution
        ix_max, = find_peaks(self.z, global_peaks=True, maxima=True)
        ix_min, = find_peaks(self.z, global_peaks=True, maxima=False)
        k = 0 if ix_min[0] < ix_max[0] else 1
        zh = [self.z[j] - self.z[i] for i, j in zip(ix_min, ix_max[k:])]
        Fe, ze = ecdf(len(zh)), np.sort(zh)
        ax.scatter(ze/self.Hm0,1-Fe, label="Empirical", color='r')
        # Plot semi-empirical distributions
        h = np.linspace(0,2.5*self.Hm0)
        f_forristall = self.wave_height_distribution(distribution="forristall")
        f_rayleigh = self.wave_height_distribution(distribution="rayleigh")
        ax.plot(h/self.Hm0, f_forristall(h), color="green",linewidth=2,label="Forristall")
        ax.plot(h/self.Hm0, f_rayleigh(h), color="blue",linewidth=2,label="Rayleigh") 
        ax.legend(loc=0)
        ax.set_xlabel("$H / H_{m0}$  [-]", fontsize=14)
        ax.set_ylabel("POE [-]", fontsize=14)
        if figname is not None: 
            plt.savefig(figname) 
            plt.close(fig)
        else: 
            plt.show()
            return (fig, ax)     