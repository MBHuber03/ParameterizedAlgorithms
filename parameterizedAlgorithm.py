from graph_deepcopy import graph_deepcopy
from exec import exec
import time


def saveGraphData(
    t1, t2, reducedBF, tr, outputFolder
):  # Saves the times for using later in plot.py
    with open(f"{outputFolder}graphData.txt", "a") as file:
        for i in t1:
            file.write(f"{i} ")
        file.write("\n")

        for i in t2:
            file.write(f"{i} ")
        file.write("\n")

        for i in reducedBF:
            file.write(f"{i} ")
        file.write("\n")

        for i in tr:
            file.write(f"{i} ")
        file.write("\n")


def applyReductions(x, k, reductions, stop):
    while True:
        if stop.is_set():
            return None, None

        someReduction = False
        for indexFunc, func in enumerate(reductions):
            x, k, result = func(x, k)
            if result:
                someReduction = True
                # print(f"n: {x.n} m: {x.m}")

        if not someReduction:
            break

    return x, k


def paramAlgorithm(
    instances,
    instanceSize,
    bruteForce,
    reductions,
    kernelMaxSizeCondition,
    printInstance,
    timeout,
    outputFolder=".",
):  # k, algoritmo forca-bruta,
    # funcoes de reducoes e condicao.
    t1 = []  # tempos para o algoritmo forca-bruta.
    t2 = []  # tempos para o algoritmo parametrizado.
    tr = []  # reduction times.
    reducedBF_list = []
    count = 0
    # countTrue = 0
    for x, k in instances:
        count += 1
        print(f"\n{k}")  # k
        print(f"{x.n}")
        print(f"{x.m}")

        xBF = graph_deepcopy(x)
        n = instanceSize(xBF)
        starting_k = k
        # print(f"Input instance #{count}:")
        # printInstance(xBF)
        # Calcular o algoritmo de força-bruta.
        inicio1 = time.time()
        result1 = exec(bruteForce, [xBF, k], timeout)
        fim1 = time.time()
        tempo1 = fim1 - inicio1
        t1.append((n, starting_k, tempo1 if result1 != "timeout" else None))
        # print(f"Brute Force: {n} {tempo1} {result1}")
        print(f"{n} {tempo1} {result1}")

        # Executar o algoritmo parametrizado e calcular o tempo
        rt = time.time()
        r = exec(applyReductions, [x, k, reductions], timeout) 
        if r != "timeout":
            x, k = r
            frt = time.time()
            tr.append(frt - rt)
            print(f"{frt - rt}")  # Reduction's time.
            print(f"{x.n}")  # n after reductions.
            print(f"{x.m}")  # k after reductions.
            # print("Input instance after reductions:")
            # printInstance(x)
            result2 = kernelMaxSizeCondition(x, k)
            inicio2 = time.time()
            reducedBF = result2 is None
            reducedBF_list.append(reducedBF)
            if reducedBF:
                result2 = exec(bruteForce, [x, k], timeout)
            fim2 = time.time()
            tempo2 = fim2 - inicio2
        else:
            result2 = "timeout"
            tempo2 = timeout
            reducedBF = False

        t2.append((n, starting_k, tempo2 if result2 != "timeout" else None))
        # print(f"Parameterized: {n} {tempo2} {result2}")
        print(f"{n} {reducedBF} {tempo2} {result2}")

        # if result1:
        #   countTrue += 1

        if result1 != result2 and result1 != "timeout" and result2 != "timeout":
            raise Exception(
                f"Error in instance #{count}: Brute Force = {result1}, Parameterized = {result2}"
            )

    saveGraphData(t1, t2, reducedBF_list, tr, outputFolder)
    # print(f"Number of instances: {count}")
    # print(f"Yes-instances: {countTrue}; No-instances: {count - countTrue}")
