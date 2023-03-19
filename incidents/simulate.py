from Daedalus import Daedalus

if __name__ == "__main__":
    daedalus = Daedalus(0.09275, 0.03224)
    for _ in range(16*8):
        daedalus.change_cycle(print_incidents=True)