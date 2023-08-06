
from multiprocessing import Pool

import loguru


def task(a):
    loguru.logger.warning(f"{a}asfasfasfasfasf")
    loguru.logger.warning(f"{a}asfasfasfasfasf")
    loguru.logger.warning(f"{a}asfasfasfasfasf")
    loguru.logger.warning(f"{a}asfasfasfasfasf")

def main():
    with Pool(5) as pl:
        pl.map(task,[i for i in range(0,19)])


if __name__ == '__main__':
    main()