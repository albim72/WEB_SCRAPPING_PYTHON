import time

def pobierz_w_partiach(dane, rozmiar=3):
    """
    Generator zwraca dane w 'partiach' po kilka elementów.
    """
    for i in range(0, len(dane), rozmiar):
        # symulacja opóźnienia jak przy pobieraniu z API/bazy
        time.sleep(0.2)
        yield dane[i:i+rozmiar]

def filtruj(generator, prog=50):
    """
    Generator filtrujący wartości > prog.
    """
    for partia in generator:
        for element in partia:
            if element > prog:
                yield element

# duża lista danych (np. wyniki pomiarów)
dane = list(range(1, 101))

# najpierw pobieramy w partiach, potem filtrujemy
for wynik in filtruj(pobierz_w_partiach(dane, rozmiar=10), prog=70):
    print(">>", wynik)
