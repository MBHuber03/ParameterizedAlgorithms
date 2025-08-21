import time
import copy
import matplotlib.pyplot as plt

def applyReductions(x, k, reductions):
	while True:
		someReduction = False
		for indexFunc, func in enumerate(reductions):
			x, k, result = func(x, k)
			if result:
				someReduction = True

		if not someReduction:
			break

	return x, k
			
def plotBFxParam(t1, t2): # Plotar grafico de comparacao.
	# Plotando o gráfico comparando os tempos.
	nValues = [i[0] for i in t1]
	bfTime = [i[1] for i in t1]
	paramTime = [i[1] for i in t2]

	plt.plot(nValues, bfTime, label='Brute Force', marker='o')
	plt.plot(nValues, paramTime, label='Parameterized', marker='s')
	plt.xlabel('n')
	plt.ylabel('time (sec)')
	plt.title('Brute Force vs Parameterized')
	plt.legend()
	plt.grid(True)
	plt.show()

def paramAlgorithm(instances, instanceSize, bruteForce, reductions, kernelMaxSizeCondition, printInstance): # k, algoritmo forca-bruta, 
												 # funcoes de reducoes e condicao.
	t1 = [] # tempos para o algoritmo forca-bruta.
	t2 = [] # tempos para o algoritmo parametrizado.
	
	for (x, k) in instances:
		print("Input instance:")
		printInstance(x)
		print(f'k = {k}')

		xBF = copy.deepcopy(x)
		n = instanceSize(xBF)

		# Calcular o algoritmo de força-bruta.
		inicio1 = time.time()
		result1 = bruteForce(xBF, k)
		fim1 = time.time()
		tempo1 = fim1 - inicio1
		t1.append((n, tempo1))
		print(f'Brute Force: {n} {tempo1} {result1}\n')
		print("Input instance before reductions:")
		printInstance(x)
		print(f'k = {k}')

		# Executar o algoritmo parametrizado e calcular o tempo
		inicio2 = time.time()
		x, k = applyReductions(x, k, reductions)
		print("Input instance after reductions:")
		printInstance(x)
		print(f'k = {k}')
		result2 = kernelMaxSizeCondition(x, k)
		if result2 == None:
			result2 = bruteForce(x, k)
		fim2 = time.time()
		tempo2 = fim2 - inicio2
		t2.append((n, tempo2))
		print(f'Parameterized: {n} {tempo2} {result2}')
			
		if result1 != result2:
			print("Error!")
			exit()
	plotBFxParam(t1, t2)