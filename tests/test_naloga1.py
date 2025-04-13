from naloga1 import prestej_piklse_z_barvo_koze
from naloga1 import doloci_barvo_koze
import numpy as np


def test_doloci_barvo_koze():
    barva = (100, 150, 200)
    slika = np.full((10, 10, 3), barva, np.uint8) # ustvarimo sliko 10x10 z eno barvo

    # pravokotno obmocje iz kje bo izracunal povprecno barvo
    levo_zgoraj = (2, 2)
    desno_spodaj = (8, 8)

    povprecna_barva = doloci_barvo_koze(slika, levo_zgoraj, desno_spodaj)

    # Tukaj se preveri ce je vrnjena barva(povprecna_barva) enaka pricakovani(barva)
    assert povprecna_barva == barva, f"Expected color {barva}, received {povprecna_barva}"


def test_prestej_piklse_z_barvo_koze():
    # ustvaril neko sliko ki je velika 10x10
    img = np.zeros((10, 10, 3), np.uint8)
    img[:] = (45, 34, 30) # barva vseh piksov
    barva = (45, 34, 30) # barva ki jo iscemo

    # V tem primeru mora vrniti 100, ker je 100 pikslov enake barve (10x10)
    assert prestej_piklse_z_barvo_koze(img, barva) == 100

def test_prestej_piklse_z_barvo_koze2():
    # ustvaril neko sliko ki je velika 10x10
    img = np.zeros((10, 10, 3), np.uint8)
    img[:] = (100, 100, 100) # barva vseh piksov
    barva = (45, 34, 30) # barva ki jo iscemo

    # V tem primeru mora vrniti 0, ker je celotna slika drugacne barve
    assert prestej_piklse_z_barvo_koze(img, barva) == 100