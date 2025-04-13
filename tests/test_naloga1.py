from naloga1 import prestej_piklse_z_barvo_koze
from naloga1 import doloci_barvo_koze
import numpy as np


def test_doloci_barvo_koze():
    barva = (100, 150, 200)
    slika = np.full((10, 10, 3), barva, np.uint8)

    levo_zgoraj = (2, 2)
    desno_spodaj = (8, 8)

    povprecna_barva = doloci_barvo_koze(slika, levo_zgoraj, desno_spodaj)

    assert povprecna_barva == barva, f"Expected color {barva}, received {povprecna_barva}"


def test_prestej_piklse_z_barvo_koze():
    img = np.zeros((10, 10, 3), np.uint8)
    img[:] = (45, 34, 30)
    barva = (45, 34, 30)

    assert prestej_piklse_z_barvo_koze(img, barva) == 100
