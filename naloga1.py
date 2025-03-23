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

    visina, sirina = slika.shape[:2]

    rezultati = []

    for y in range(0, visina - visina_skatle + 1, visina_skatle):
        vrstica_slike = []
        for x in range(0, sirina - sirina_skatle + 1, sirina_skatle):
            skatla = slika[y:y + visina_skatle, x:x + sirina_skatle]

            stevilo_pikslov_koze = prestej_piklse_z_barvo_koze(skatla, barva_koze)

            vrstica_slike.append(stevilo_pikslov_koze)

        rezultati.append(vrstica_slike)

    return rezultati


def prestej_piklse_z_barvo_koze(slika, barva_koze) -> int:
    '''Prestej število pikslov z barvo kože v škatli.'''
    spodnja_meja = np.array([barva_koze[0] - 10, barva_koze[1] - 10, barva_koze[2] - 10])
    zgornja_meja = np.array([barva_koze[0] + 10, barva_koze[1] + 10, barva_koze[2] + 10])

    maska = cv.inRange(slika, spodnja_meja, zgornja_meja)
    stevilo_pikslov = cv.countNonZero(maska)

    return stevilo_pikslov


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


def floodfill(slika, x, y, sirina_skatle, visina_skatle):
    center = (x + sirina_skatle // 2, y + visina_skatle // 2)

    maska_floodfill = np.zeros((slika.shape[0] + 2, slika.shape[1] + 2), np.uint8)

    cv.floodFill(slika, maska_floodfill, center, (0, 255, 0), (1, 1, 1), (2, 2, 2), flags=4)

    return slika


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
            visina = 240
            sirina = 320
            zmanjsana_slika = zmanjsaj_sliko(slika, sirina, visina)
            cv.imwrite('zmanjsana.jpg', zmanjsana_slika)

            size = 50
            center_x = sirina // 2
            center_y = visina // 2

            levo_zgoraj = (center_x - size // 2, center_y - size // 2)
            desno_spodaj = (center_x + size // 2, center_y + size // 2)

            barva_koze = doloci_barvo_koze(zmanjsana_slika, levo_zgoraj, desno_spodaj)
            print('Barva koze:', barva_koze)

            # Zajemaj slike iz kamere in jih obdeluj
            sirina_skatle = 15
            visina_skatle = 15

            while True:
                ret, slika = camera.read()
                rezultat = obdelaj_sliko_s_skatlami(slika, sirina_skatle, visina_skatle, barva_koze)

                # rezultat = obdelaj_sliko_s_skatlami(zmanjsana_slika, sirina_skatle, visina_skatle, barva_koze)
                # for vrstica in rezultat:
                #    print(vrstica)

                # Označi območja (škatle), kjer se nahaja obraz (kako je prepuščeno vaši domišljiji)
                # cv.imshow('Obraz', slika)
                # Vprašanje 1: Kako iz števila pikslov iz vsake škatle določiti celotno območje obraza (Floodfill)?
                for i, vrstica in enumerate(rezultat):
                    for j, stevilo_pikslov_koze in enumerate(vrstica):
                        if stevilo_pikslov_koze > 50:
                            x = j * sirina_skatle
                            y = i * sirina_skatle

                            floodfill(slika, x, y, sirina_skatle, visina_skatle)
                            cv.rectangle(slika, (x, y), (x + sirina_skatle, y + visina_skatle), (204, 255, 204), 2)

                cv.imshow('Obraz', slika)
                # Vprašanje 2: Kako prešteti število ljudi?

                # Kako velikost prebirne škatle vpliva na hitrost algoritma in točnost detekcije? Poigrajte se s parametroma velikost_skatle
                # in ne pozabite, da ni nujno da je škatla kvadratna.
                if cv.waitKey(1) & 0xFF == ord('q'):
                    break
    camera.release()
    cv.destroyAllWindows()
    pass
