import requests, os
from glob import glob


NAIF = 'https://naif.jpl.nasa.gov/pub/naif/generic_kernels/'
BEHR = 'https://raw.githubusercontent.com/behrouzz/astrodata/main/spice/kernels/'

path = 'bs_kernels/'

dc_kernels = {
    'naif0012.tls': 'lsk/naif0012.tls',
    'pck00010.tpc': 'pck/pck00010.tpc',
    'earth_latest_high_prec.bpc': 'pck/earth_latest_high_prec.bpc',
    #'earth_200101_990628_predict.bpc': 'pck/earth_200101_990628_predict.bpc',
    }

main_kernels = list(dc_kernels.keys())


def download_kernels(overwrite=False, solsys=True, jupiter=False):
    if not os.path.isdir(path):
        os.mkdir(path)
    old_files = glob(path + '/*')
    old_filenames = [i.split('\\')[-1] for i in old_files]

    if solsys:
        dc_kernels['de440_2030.bsp'] = 'de440_2030.bsp'
    if jupiter:
        dc_kernels['jup4_2030.bsp'] = 'jup4_2030.bsp'

    if overwrite:
        for k,v in dc_kernels.items():
            if k=='earth_latest_high_prec.bpc':
                download_file(NAIF+v, path=path)
                print(k, 'downloaded.')
            else:
                download_file(BEHR+v, path=path)
                print(k, 'downloaded.')
    else:
        for k,v in dc_kernels.items():
            if k in old_filenames:
                print(k, 'already exists.')
            else:
                if k=='earth_latest_high_prec.bpc':
                    download_file(NAIF+v, path=path)
                    print(k, 'downloaded.')
                else:
                    download_file(BEHR+v, path=path)
                    print(k, 'downloaded.')
                



def download_file(url, path=''):
    filename = url.rsplit('/', 1)[-1]
    r = requests.get(url, allow_redirects=True)
    open(path+filename, 'wb').write(r.content)
    

