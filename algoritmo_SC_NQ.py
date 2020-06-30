import random, math, sys

def generarIndividuosAleatorios(N, numeroIndividuos, numeroIteracion, conCorreccion, record): 
  poblacion = []
  for i in range(numeroIndividuos): 
    individuo = []
    for j in range(N): 
      individuo.append(random.randint(0,N-1))
    if conCorreccion == 1: 
      individuo = correccion(individuo,N)
    fitness, record = calcularFitness(individuo,N,numeroIteracion,conCorreccion, record)
    poblacion.append([fitness,individuo])
  poblacion.sort()
  return poblacion,record

def correccion(individuo,N): 
  todosNumeros = []
  for i in range (N): 
    todosNumeros.append(i)
  posicionesCambiar = []
  k = 0
  for i in individuo: 
    if i in todosNumeros: 
      todosNumeros.remove(i)
    else: 
      posicionesCambiar.append(k)
    k+=1
  for i in posicionesCambiar: 
    elemento = random.randint(0,len(todosNumeros)-1)
    individuo[i]=todosNumeros.pop(elemento)
  return individuo

def calcularFitness(individuo,N,numeroIteracion,conCorreccion,record): 
  numeroColisiones = 0
  
  if conCorreccion == 0: 
    for i in range(N): 
      for j in range(i+1,N): 
        if individuo[j] == individuo[i]: 
          numeroColisiones+=1
  
  for i in range(N): 
    for j in range(i+1,N): 
      if abs(individuo[j]-individuo[i])==j-i: 
        numeroColisiones+=1
  if (numeroColisiones == 0): 
    print("Solucion:",individuo)
    print("Iteracion:",numeroIteracion)
    sys.exit()
  if numeroColisiones < record: 
    record = numeroColisiones
    print("NUEVO RECORD:",record,"colisiones")
  return numeroColisiones,record

def clonacion_mutacion (poblacion,N,numeroIteracion,conCorreccion,record):
  umbral1 = int(math.ceil(0.1 * len(poblacion)))
  umbral2 = umbral1 + int(math.ceil(0.2 * len(poblacion)))
  nuevaPoblacion = []
  
  for i in range(len(poblacion)): 
    if i < umbral1: 
      for j in range(4): 
        nuevoIndividuo = poblacion[i][1].copy()
        for k in range(len(nuevoIndividuo)): 
          aux = random.randint(0,9)
          if aux == 0: 
            aux2 = random.randint(0,1)
            if aux2 == 0: 
              aux2 = -1
            nuevoIndividuo[k]=(nuevoIndividuo[k]+aux2)%N 
        if conCorreccion == 1: 
          nuevoIndividuo = correccion(nuevoIndividuo,N) 
        fitness, record = calcularFitness(nuevoIndividuo,N,numeroIteracion,conCorreccion, record)
        nuevaPoblacion.append([fitness,nuevoIndividuo])
    
    elif i >= umbral1 and i < umbral2: 
      for j in range(3): 
        nuevoIndividuo = poblacion[i][1].copy()
        for k in range(len(nuevoIndividuo)): 
          aux = random.randint(0,9)
          if aux <= 1: 
            aux2 = random.randint(0,1)
            if aux2 == 0: 
              aux2 = -1
            nuevoIndividuo[k]=(nuevoIndividuo[k]+aux2)%N 
        if conCorreccion == 1: 
          nuevoIndividuo = correccion(nuevoIndividuo,N) 
        fitness, record = calcularFitness(nuevoIndividuo,N,numeroIteracion,conCorreccion, record)
        nuevaPoblacion.append([fitness,nuevoIndividuo])
      
    else: 
      for j in range(2): 
        nuevoIndividuo = poblacion[i][1].copy()
        for k in range(len(nuevoIndividuo)): 
          aux = random.randint(0,9)
          if aux <= 2: 
            aux2 = random.randint(0,1)
            if aux2 == 0: 
              aux2 = -1
            nuevoIndividuo[k]=(nuevoIndividuo[k]+aux2)%N 
        if conCorreccion == 1: 
          nuevoIndividuo = correccion(nuevoIndividuo,N) 
        fitness, record = calcularFitness(nuevoIndividuo,N,numeroIteracion,conCorreccion, record)
        nuevaPoblacion.append([fitness,nuevoIndividuo])

  return nuevaPoblacion,record

def eliminarClones (poblacion):
  nuevaPoblacion = [poblacion[0]]
  individuoAnterior = nuevaPoblacion[0]
  for i in range(1,len(poblacion)): 
    if sonDiferentes(individuoAnterior,poblacion[i]): 
      nuevaPoblacion.append(poblacion[i])
      individuoAnterior = poblacion[i]
  return nuevaPoblacion

def sonDiferentes(indv1,indv2): 
  if indv1[0] != indv2[0]: 
    return True
  for i in range(len(indv1)): 
    if indv1[i] != indv2[i]: 
      return True
  return False

def unir (nuevaPoblacion,nuevosIndividuos):
  for i in nuevosIndividuos: 
    nuevaPoblacion.append(i)
  nuevaPoblacion.sort()
  return nuevaPoblacion

def reemplazoProporcionalAleatorio (nuevaPoblacion,N,numeroIteracion,conCorreccion,record):
  fitnessTotal = 0
  fitnessAcumulado = []
  for i in nuevaPoblacion: 
    fitnessTotal += i[0]
    fitnessAcumulado.append(fitnessTotal)
    
  numeroCambios = int(math.ceil(0.1 * len(nuevaPoblacion)))
  posicionesCambiar = []
  while len(posicionesCambiar) < numeroCambios:
    valor = random.randint(1,fitnessTotal)
    for i in range(len(fitnessAcumulado)): 
      if valor <= fitnessAcumulado[i]: 
        if i not in posicionesCambiar: 
          posicionesCambiar.append(i)
        break
  
  for posicion in posicionesCambiar: 
    nuevoIndividuo,record = generarIndividuosAleatorios(N, 1, numeroIteracion, conCorreccion, record)
    nuevaPoblacion[posicion] = nuevoIndividuo[0]
  return nuevaPoblacion,record

def main(): 
  N = int(sys.argv[1])
  tamanhoPoblacion = int(sys.argv[2])
  mejores = int(sys.argv[3])
  conCorreccion = int(sys.argv[4])
  numeroMaxIteraciones = int(sys.argv[5])
  record = N**2

  poblacion,record = generarIndividuosAleatorios(N,tamanhoPoblacion,0,conCorreccion, record)
  numeroIteracion = 1

  while (numeroIteracion <= numeroMaxIteraciones): 
    nuevaPoblacion = poblacion[:mejores]
    nuevaPoblacion,record = clonacion_mutacion(nuevaPoblacion,N,numeroIteracion,conCorreccion, record)
    nuevaPoblacion.append(poblacion[0])
    nuevaPoblacion.sort()
    nuevaPoblacion = eliminarClones(nuevaPoblacion)
    if len(nuevaPoblacion) >= tamanhoPoblacion: 
      nuevaPoblacion = nuevaPoblacion[:tamanhoPoblacion]
    else: 
      nuevosIndividuos,record = generarIndividuosAleatorios(N,tamanhoPoblacion-len(nuevaPoblacion),numeroIteracion,conCorreccion, record)
      nuevaPoblacion = unir(nuevaPoblacion,nuevosIndividuos)
    poblacion,record = reemplazoProporcionalAleatorio(nuevaPoblacion,N,numeroIteracion,conCorreccion, record)
    poblacion.sort()
    numeroIteracion+=1
  print("solucion no encontrada") 
  
main()