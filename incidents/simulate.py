from Daedalus import Daedalus

if __name__ == "__main__":
    daedalus = Daedalus(
        c1=0.23,
        c2=-1.6,
        nb_heroes_alive=11.57,
        daily_ap_consumption=128.1956
    )
    for _ in range(10*8):
        daedalus.change_cycle(print_incidents=True)