**Author:** [Behrouz Safari](https://astrodatascience.net/)<br/>
**License:** [MIT](https://opensource.org/licenses/MIT)<br/>

# bspice
*Working with SPICE kernels*


## Installation

You can install the latest version of *bspice* from [PyPI](https://pypi.org/project/bspice/):

    pip install bspice

The requirements are *numpy*, *requests* and *spiceypy*.


## Download Kernels

```python
import bspice as bs

bs.download_kernels(overwrite=False, solsys=True, jupiter=True)
```

## Apparent position of Saturn

```python
import bspice as bs
from datetime import datetime

t = datetime.utcnow()
obs_loc = (7.744083817548831, 48.58313582900411, 140)

adr = 'C:/Moi/_py/Astronomy/Solar System/kernels/'

kernels = [adr+i for i in bs.main_kernels]
kernels = kernels + [adr+'de440_2030.bsp']

r, az, alt = bs.get_apparent(6, t, obs_loc, kernels)
print(az, alt)
```

## Apparent position of Jupiter Moons

```python
import bspice as bs
from datetime import datetime
import matplotlib.pyplot as plt

t = datetime.utcnow()
obs_loc = (7.744083817548831, 48.58313582900411, 140)

adr = 'C:/Moi/_py/Astronomy/Solar System/kernels/'

kernels = [adr+i for i in bs.main_kernels]
kernels = kernels + [adr+'jup4_2030.bsp']

bodies = [599, 501, 502, 503, 504]
r_az_alt = bs.get_apparent_bodies(bodies, t, obs_loc, kernels, abcorr='LT+S')
print(r_az_alt)

fig, ax = plt.subplots()
ax.scatter(r_az_alt[0,1], r_az_alt[0,2])
ax.scatter(r_az_alt[1:,1], r_az_alt[1:,2])
plt.show()
```

## Apparent position of the Sun during 24 hours

```python
import bspice as bs
from datetime import datetime

obs_loc = (7.744083817548831, 48.58313582900411, 140)

adr = 'C:/Moi/_py/Astronomy/Solar System/kernels/'

kernels = [adr+i for i in bs.main_kernels]
kernels = kernels + [adr+'de440_2030_earth_sun_moon.bsp']

t1 = datetime(2022, 9, 10)
t2 = datetime(2022, 9, 11)

r_az_alt = bs.get_apparent_window(10, t1, t2, 24, obs_loc, kernels, abcorr='LT+S')

for i in r_az_alt:
    print(f'Az:{i[1]} ||| Alt:{i[2]}')
```

## Local and absolute minimum angular positions of Sun and Moon

```python
import bspice as bs

t1 = '2022-01-01'
t2 = '2023-01-01'

adr = 'C:/Users/H21/Desktop/Desktop/Behrouz/Astronomy/kernels/'

kernels = [
    adr + 'naif0012.tls',
    adr + 'pck00010.tpc',
    adr + 'de440s.bsp',
    ]

print('Local:')
times = bs.conjunction(t1=t1, t2=t2, targ1='sun', targ2='moon', kernels=kernels)

for i in times:
    print(i)

print('Absolute:')
times = bs.conjunction(t1=t1, t2=t2, targ1='sun', targ2='moon', kernels=kernels, relate='ABSMIN')

for i in times:
    print(i)
```

```
Local:
2022-01-02 18:08:14
2022-02-01 05:32:21
2022-03-02 17:49:18
2022-04-01 06:53:57
2022-04-30 20:41:32
2022-05-30 11:11:34
2022-06-29 02:19:09
2022-07-28 17:40:45
2022-08-27 08:34:53
2022-09-25 22:24:24
2022-10-25 11:00:06
2022-11-23 22:40:53
2022-12-23 09:52:10
Absolute:
2022-10-25 11:00:06
```
