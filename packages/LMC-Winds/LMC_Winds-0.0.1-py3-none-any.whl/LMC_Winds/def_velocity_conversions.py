#exec(open('def_velocity_conversions.py').read())
import numpy as np
from astropy import units as u
from astropy.coordinates import SkyCoord
from astropy.coordinates import ICRS, Galactic, FK4, FK5 
from astropy.coordinates.representation import UnitSphericalRepresentation
def vhelio_to_vlsr(coord, vhelio=0*u.km/u.s, lsr_definition='kinematic'): #coord is the coordinates of the background flashlight (the RA and DEC in deg)
    """
    this definition is from the work of erikutils. https://github.com/eteq/erikutils/blob/master/erikutils/velocities.py
    Convert heliocentric radial velocity to Local Standard of Rest radial velocity
    Parameters
    ----------
    coord : SkyCoord
        The direction at which to compute the conversion factor.
    vhelio : Quantity with velocity units
        The heliocentric radial velocity.  Should be a scalar quantity or match the shape of `coord`.
    lsr_definition : str or Quantity with velocity units
        The definition of LSR to assume.  This can be one of three options:
        * 'kinematic' : 20 km/s towards 18h,+30 deg (at 1900)
        * 'dynamical' : IAU definition of (9, 12, 7) km/sec in Galactic cartesian coordinates
        * A length-3 vector with the U, V, and W components (velocity along the galactic x, y, and z axes)
          to assume for the LSR.
    Returns
    -------
    vlsr : Quantity
        The velocity in the Local Standard of Rest frame.
    """
    if lsr_definition == 'kinematic':
        direction = SkyCoord('18h', '30d', frame='fk5', equinox='J1900') #definition of kinematic reference frame
        velocity = 20*u.km/u.s #definition of kinematic reference frame
        uvw_lsr = direction.galactic.cartesian.xyz * velocity #puts the direction in galactic frame and then in the cartesian
        #The xyz says remember all three coordinates, the x,y and z in the cartesian frame
    elif lsr_definition == 'dynamical':
        uvw_lsr = (9, 12, 7)*u.km/u.s
    else:
        uvw_lsr = lsr_definition

    # the unitspherical conversion ensures that the resulting cartesian is a *unit* vector
    usr = coord.galactic.represent_as(UnitSphericalRepresentation) #UnitSphericalRepresentation represents the points on a unit sphere
    cart = usr.to_cartesian()

    vlsr_vector = (cart.xyz.T*uvw_lsr).T #anytime you see the .xyz it is just return the x,y, and z components of the vector
    #the .T is the transpose of the numpy array. Apparently, the .T is np.transpose()
    return vhelio + np.sum(vlsr_vector)

def vlsr_to_lmcsr(coord, VLSR):
    """
    Converts from the Local Standard of Reset to LMC Standard of Rest reference frame
    Parameters
    ----------
    coord : SkyCoord
        The the RA and DEC of the sightline in degrees
    VLSR : Quantity with units of km/s

    Returns
    -------
    vlmcsr : the velocity in the LMCSR reference frame

    Notes
    ------
    This conversion to LMCSR is using a modified version of equation 3 in Ciampa et al. 2021. In Ciampa et al. 2021, the central velocity offset
    is found from the following equation: delta_vlmcsr = 262.55-3.25(glon-280)+3.66(glat-33). Then the central velocity offset was added to the local standard
    of rest velocity. The corrections for this code include the following new equation: (262.55-3.25*(glon-280.)+3.66*(glat-(-33.))) and this offset is 
    subtracted from the local standard of rest velocity.

    Written by April Horton 05/17/2022
    """
    c = coord #represents an ICRS (RA and DEC sky position), coord should be a SkyCoord object SkyCoord(ra=10.625*u.degree, dec=41.2*u.degree, frame='icrs')
    #To get the coordinate in Galactic Frame, use the .galactic attribute
    galactic_c = c.galactic 
    galactic_l = galactic_c.l.value
    galactic_b = galactic_c.b.value
    # Talking point in my paper
    central_v_offset = 262.55-3.25*(galactic_l-280)+3.66*(galactic_b-(-33)) # Modified equation 3 from Ciampa et al. 2021, The modifications include subtracting (-33) from the galactic longitude 
    #central_v_offset = 1293.22 - 3.25*(galactic_l)+3.66*(galactic_b) #this equation is from the screenshot (Drew_original_equation.png) in my journal articles directory. It has what originally Drew had in his paper before the referee comments
    
    vlmcsr = VLSR - central_v_offset #this is also modified from Ciampa et al. 2021. We subtract the central velocity offset from the LSR velocity, still subtract with the equation from the screenshot
    #print(central_v_offset)
    
    return (vlmcsr)
