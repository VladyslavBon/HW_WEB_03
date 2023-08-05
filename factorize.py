from multiprocessing import Pool

def factorize(number):
    result = []
    for ch in range(1, number + 1):
        if number % ch == 0:
            result.append(ch)
    print(result)

if __name__ == "__main__":
    with Pool() as pool:
        pool.map(factorize, [128, 255, 99999, 10651060])