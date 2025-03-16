import cv2 as cv
import numpy as np


def zmanjsaj_sliko(slika, sirina, visina):
    return cv.resize(slika, (sirina, visina))


def obdelaj_sliko_s_skatlami(slika, sirina_skatle, visina_skatle, barva_koze) -> list:
    '''Sprehodi se skozi sliko v velikosti škatle (sirina_skatle x visina_skatle) in izračunaj število pikslov kože v vsaki škatli.
    Škatle se ne smejo prekrivati!
    Vrne seznam škatel, s številom pikslov kože.
    Primer: Če je v sliki 25 škatel, kjer je v vsaki vrstici 5 škatel, naj bo seznam oblike
      [[1,0,0,1,1],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[1,0,0,0,1]]. 
      V tem primeru je v prvi škatli 1 piksel kože, v drugi 0, v tretji 0, v četrti 1 in v peti 1.'''
    pass


def prestej_piklse_z_barvo_koze(slika, barva_koze) -> int:
    '''Prestej število pikslov z barvo kože v škatli.'''
    pass


def doloci_barvo_koze(slika, levo_zgoraj, desno_spodaj) -> tuple:
    '''Ta funkcija se kliče zgolj 1x na prvi sliki iz kamere. 
    Vrne barvo kože v območju ki ga definira oklepajoča škatla (levo_zgoraj, desno_spodaj).
      Način izračuna je prepuščen vaši domišljiji.'''
    # slika[y1:y2, x1:x2]
    sredina = slika[levo_zgoraj[1]:desno_spodaj[1], levo_zgoraj[0]:desno_spodaj[0]]
    cv.imshow('sredina', sredina)
    cv.waitKey(0)
    avg_color = cv.mean(sredina)[:3]

    return tuple(map(int, avg_color))


if __name__ == '__main__':
    # Pripravi kamero
    camera = cv.VideoCapture(1)
    # Zajami prvo sliko iz kamere
    if not camera.isOpened():
        print('Kamera ni bila odprta.')
    else:
        for _ in range(5):
            ret, slika = camera.read()

        if ret:
            cv.imshow('Prva slika', slika)
            cv.imwrite('prva_slika.jpg', slika)
            cv.waitKey(0)
            # Izračunamo barvo kože na prvi sliki
            # Izbral sem sredino slike saj obraz bo se vecino casa tam nahajal 240x320
            zmanjsana_slika = zmanjsaj_sliko(slika, 320, 240)

            levo_zgoraj = (110, 70)
            desno_spodaj = (210, 170)

            barva_koze = doloci_barvo_koze(zmanjsana_slika, levo_zgoraj, desno_spodaj)
            print('Barva koze:', barva_koze)
    # Zajemaj slike iz kamere in jih obdeluj

    # Označi območja (škatle), kjer se nahaja obraz (kako je prepuščeno vaši domišljiji)
    # Vprašanje 1: Kako iz števila pikslov iz vsake škatle določiti celotno območje obraza (Floodfill)?
    # Vprašanje 2: Kako prešteti število ljudi?

    # Kako velikost prebirne škatle vpliva na hitrost algoritma in točnost detekcije? Poigrajte se s parametroma velikost_skatle
    # in ne pozabite, da ni nujno da je škatla kvadratna.
    pass
