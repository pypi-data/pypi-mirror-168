def felhantering_av_heltal(fråga):
    # Sätter en condition för loopen, inmatning_av_heltal fungerar som en på och av knapp, när den har värdet 1
    # så körs funktionen, när värdet ändras så vet vi har ett godkänt värde
    inmatning_av_heltal = 1
    while inmatning_av_heltal == 1:
        try:
            heltal = int(input(fråga))
            if heltal != 0:
                inmatning_av_heltal = 0
                return heltal
                # Endast om alla dessa värden är korrekta ändras variabelen inmatning_av_heltal och
                # Loopen bryts och vi kan nu vara säkra på att det är ett heltal som retuneras
            else:
                print("Talet måste vara skiljt ifrån 0")
        except:
            print("Det där var inte ett heltal. Vänligen försök igen")


def felhantering_av_flyttal(fråga):

    global inmatning_av_flyttal
    inmatning_av_flyttal = 1
    while inmatning_av_flyttal == 1:
        try:
            flyttal = float(input(fråga))
            inmatning_av_flyttal = 0
            return flyttal
        except:
            print("Det där var inte ett flyttal. Vänligen försök igen")
