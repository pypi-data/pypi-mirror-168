import spiceypy as sp
import numpy as np
from datetime import datetime


d2r = 3.141592653589793/180
r2d = 180/3.141592653589793
   

def ecef2enu_rotmat(obs_loc):
    lon, lat, _ = obs_loc
    lon = lon * d2r
    lat = lat * d2r
    r1 = [-np.sin(lon), np.cos(lon), 0]
    r2 = [-np.cos(lon)*np.sin(lat), -np.sin(lon)*np.sin(lat), np.cos(lat)]
    r3 = [np.cos(lon)*np.cos(lat), np.sin(lon)*np.cos(lat), np.sin(lat)]
    return np.array([r1, r2, r3])


def enu2altaz(pos_enu):
    e, n, u = pos_enu
    r = np.hypot(e, n)
    rng = np.hypot(r, u)
    el = np.arctan2(u, r)
    az = np.mod(np.arctan2(e, n), 2*np.pi)
    return az*r2d, el*r2d, rng


def lonlat_to_cartesian(obs_loc):
    """
    obs_loc : (lon (deg), lat (deg), alt (m))
    """
    lon, lat, alt = obs_loc
    lon = lon * d2r
    lat = lat * d2r
    alt = alt / 1000
    radii = [6378.1366, 6378.1366, 6356.7519]
    re = radii[0]
    rp = radii[2]
    f = (re-rp)/re
    obspos = sp.pgrrec(body='earth', lon=lon, lat=lat, alt=alt, re=re, f=f)
    return obspos


##def get_icrs(body, t, kernels):
##    for k in kernels:
##        sp.furnsh(k)
##    et = sp.str2et(str(t))
##    state, lt = sp.spkez(targ=body, et=et, ref='J2000', abcorr='NONE', obs=0)
##    pos = state[:3]
##    vel = state[3:]
##    sp.kclear()
##    return pos, vel, lt


##def get_topocentric(body, t, obs_loc, kernels):
##    r,az,alt = get_apparent(body, t, obs_loc, kernels, abcorr='NONE')
##    for k in kernels:
##        sp.furnsh(k)
##    topo = sp.azlrec(range=r, az=az*d2r, el=alt*d2r,
##                     azccw=False, elplsz=True)
##    sp.kclear()
##    return topo


def get_apparent(body, t, obs_loc, kernels, abcorr='LT+S'):

    if isinstance(body, int):
        body = str(body)

    for k in kernels:
        sp.furnsh(k)

    et = sp.str2et(str(t))
    
    state, lt  = sp.azlcpo(
        method='ELLIPSOID',
        target=body,
        et=et,
        abcorr=abcorr,
        azccw=False,
        elplsz=True,
        obspos=lonlat_to_cartesian(obs_loc),
        obsctr='earth',
        obsref='ITRF93')

    r, az, alt = state[:3]

    sp.kclear()

    return r, az*r2d, alt*r2d


def get_apparent_bodies(bodies, t, obs_loc, kernels, abcorr='LT+S'):

    bodies = [str(i) for i in bodies]

    for k in kernels:
        sp.furnsh(k)

    et = sp.str2et(str(t))
    obspos = lonlat_to_cartesian(obs_loc)

    r_az_alt = np.zeros((len(bodies),3))

    for i in range(len(bodies)):
        state, lt  = sp.azlcpo(
            method='ELLIPSOID',
            target=bodies[i],
            et=et,
            abcorr=abcorr,
            azccw=False,
            elplsz=True,
            obspos=obspos,
            obsctr='earth',
            obsref='ITRF93')
        r, az, alt = state[:3]
        r_az_alt[i,:] = r, az*r2d, alt*r2d

    sp.kclear()

    return r_az_alt


def get_apparent_window(body, t1, t2, steps, obs_loc, kernels, abcorr='LT+S'):

    if isinstance(body, int):
        body = str(body)

    for k in kernels:
        sp.furnsh(k)

    et1 = sp.str2et(str(t1))
    et2 = sp.str2et(str(t2))
    t_win = np.linspace(et1, et2, steps)
    
    obspos = lonlat_to_cartesian(obs_loc)

    r_az_alt = np.zeros((len(t_win),3))

    for i in range(len(t_win)):
        state, lt  = sp.azlcpo(
            method='ELLIPSOID',
            target=body,
            et=t_win[i],
            abcorr=abcorr,
            azccw=False,
            elplsz=True,
            obspos=obspos,
            obsctr='earth',
            obsref='ITRF93')
        r, az, alt = state[:3]
        r_az_alt[i,:] = r, az*r2d, alt*r2d

    sp.kclear()

    return r_az_alt


def gcrs_to_altaz(t, obs_loc, pos_gcrs, kernels):
    ecef2enu_rot = ecef2enu_rotmat(obs_loc)

    # Calculate J2000 to body-equator-and-prime-meridian rotation matrix
    for k in kernels:
        sp.furnsh(k)
    et = sp.str2et(str(t))
    #j2000_to_earthfixed_rot = sp.tisbod(ref='J2000', body=399, et)[:3,:3]
    j2000_to_earthfixed_rot = sp.sxform('J2000', 'ITRF93', et)[:3,:3] # et or et+lt ?
    sp.kclear()

    # Calculate itrf, enu, altaz
    pos_itrf = np.matmul(j2000_to_earthfixed_rot, pos_gcrs)
    pos_enu = np.matmul(ecef2enu_rot, pos_itrf)
    return enu2altaz(pos_enu)


def get_crs(body, t, abcorr, obs, kernels):
    for k in kernels:
        sp.furnsh(k)
    et = sp.str2et(str(t))
    state, lt = sp.spkez(targ=body, et=et, ref='J2000', abcorr=abcorr, obs=obs)
    sp.kclear()
    pos = state[:3]
    vel = state[3:]
    return pos, vel, lt


def icrs(body, t, kernels, abccorr='NONE'):
    pos, vel, lt = get_crs(body=body, t=t, abcorr=abccorr, obs=0, kernels=kernels)
    return pos, vel, lt


def gcrs(body, t, kernels, abccorr='NONE'):
    pos, vel, lt = get_crs(body=body, t=t, abcorr=abccorr, obs=399, kernels=kernels)
    return pos, vel, lt


def earth_icrs(t, kernels, abccorr='NONE'):
    pos, _, _ = get_crs(body=399, t=t, abcorr=abccorr, obs=0, kernels=kernels)
    return pos

def icrs_to_gcrs(pos_icrs, t, kernels, abccorr='NONE'):
    earth = earth_icrs(t, kernels, abccorr)
    return pos_icrs - earth

def gcrs_to_icrs(pos_gcrs, t, kernels, abccorr='NONE'):
    earth = earth_icrs(t, kernels, abccorr)
    return pos_gcrs + earth


def gfsep(t1, t2, targ1, targ2, shape1, shape2, abcorr, relate, refval, step, kernels, return_utc):

    for k in kernels:
        sp.furnsh(k)

    MAXWIN = 1000
    result = sp.Cell_Double(2*MAXWIN)
    cnfine = sp.Cell_Double(2)

    et1 = sp.str2et(t1)
    et2 = sp.str2et(t2)

    sp.wninsd(et1, et2, cnfine)

    sp.gfsep(
        targ1=targ1,
        shape1=shape1,
        inframe1='NULL',
        targ2=targ2,
        shape2=shape2,
        inframe2='NULL',
        abcorr=abcorr,
        obsrvr='EARTH',
        relate=relate,
        refval=refval,
        adjust=0.0,
        step=step,
        nintvls=1000,
        cnfine=cnfine,
        result=result
        )

    count = sp.wncard(result)

    times = []

    for i in range(count):
        t1_tdb, t2_tdb = sp.wnfetd(result, i)
        
        if return_utc:
            t1_utc = sp.et2utc(t1_tdb, 'ISOC', 0, 20)
            t2_utc = sp.et2utc(t2_tdb, 'ISOC', 0, 20)
            t1_utc = datetime.strptime(t1_utc, '%Y-%m-%dT%H:%M:%S')
            t2_utc = datetime.strptime(t2_utc, '%Y-%m-%dT%H:%M:%S')
            times.append((t1_utc, t2_utc))
        else:
            times.append((t1_tdb, t2_tdb))
        
    sp.kclear()
    return times


def conjunction(t1, t2, targ1, targ2, kernels, shape1='SPHERE', shape2='SPHERE', relate='LOCMIN'):
    times = gfsep(
        t1=t1, t2=t2, targ1=targ1, targ2=targ2,
        shape1=shape1, shape2=shape2, abcorr='LT+S',
        relate=relate, refval=0.0, step=3600,
        kernels=kernels, return_utc=True)
    times = [i[0] for i in times]
    return times
