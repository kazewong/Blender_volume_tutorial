######################################################################################
#                   MODULES, COSMOLOGY CONFIGURATION and USEFUL FUNCTIONS  
######################################################################################
import numpy as np
from astropy.cosmology import FlatLambdaCDM, wCDM, z_at_value
from scipy.interpolate import *

# QUIJOTE cosmology
config = dict()
config['Om'] = 0.3175
config['sigma8'] = 0.834
config['ns'] = 0.9624
config['Ob'] = 0.049
config['h100'] = 0.6711
config['Tcmb0'] = 2.725
cosmo = FlatLambdaCDM(H0 = config['h100']*100, Om0 = config['Om'], Tcmb0 = config['Tcmb0'])

# Function to convert coordinates into cartesians
def from_rRAdec_to_XYZ(r,RA,dec):
    x = r * np.cos(dec * np.pi / 180.) * np.sin(RA * np.pi / 180.)
    y = r * np.cos(dec * np.pi / 180.) * np.cos(RA * np.pi / 180.)
    z = r * np.sin(dec * np.pi / 180.)
    theta = 0.5 * np.pi - dec * np.pi / 180.
    phi = RA * np.pi / 180.
    return x, y, z,theta,phi
    
# Function to transform distances into redshift and viceversa
def auxint(zb):
    rb = []; Hb = []
    for i in range(len(zb)):
        rb.append(cosmo.comoving_distance(np.array(zb[i])).value)
        Hb.append(cosmo.H(zb[i]).value)
    rb = np.array(rb)
    a1 = interp1d(zb,rb,kind = 'slinear',fill_value = "extrapolate")
    a2 = interp1d(rb,zb,kind = 'slinear',fill_value = "extrapolate")
    a3 = interp1d(zb,Hb,kind = 'slinear',fill_value = "extrapolate")
    return a1,a2,a3

nz = 4000 ; zb = np.linspace(0,4,nz)
z_to_d,d_to_z,z_to_H = auxint(zb)   

######################################################################################
#                                   	     HALOS    
######################################################################################
path_halos = '/mnt/home/apisani/ceph/Share/ForBlenderMar/fiducial_100_halos.dat'

ra_g, dec_g, z_km_s_g, Magnitude_g = np.loadtxt(path_halos, skiprows=5, usecols=( 3, 4, 5, 6), unpack=True)
ra_g = ra_g[:-1]
dec_g = dec_g[:-1]
redshift_g = z_km_s_g[:-1]/299792.458 
Magnitude_g = Magnitude_g[:-1]
 

x_g,y_g,z_g,_,_=from_rRAdec_to_XYZ(z_to_d(redshift_g),ra_g,dec_g)



######################################################################################
#                                           VOIDS     
######################################################################################
path_voids = '/mnt/home/apisani/ceph/Share/ForBlenderMar/sample_Quijote_halos_fiducial_100_z0.00/untrimmed_centers_central_Quijote_halos_fiducial_100_z0.00.out'

x_v, y_v, z_v, volume_normalized_v, radius_v, redshift_v,volume_mpc3_v,void_ID,density_contrast_v,num_part_v,parent_ID_v,tree_level_v,num_children_v,central_density_v = np.loadtxt(path_voids, skiprows=1, usecols=(0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12,13), unpack=True)