### Amanda Florian - 590673
### Fernando Dias - 591580


def gerarMatriz(maxX, maxY):
    matriz = []
    aux = []
    for y in range(0, maxY):
        for x in range(0, maxX):
            aux.append(0)
        matriz.append(aux[:])
        aux.clear()
    return matriz

def montarTabela(numvar, numres, res, b, z):
    tabela = gerarMatriz(((numvar + numres) + 1), (numres + 1))

    for y in range(0, (numres + 1)):
        for x in range(0, (numvar + 1)):
            if y < numres and x < numvar:
                tabela[y][x] = res[y][x]
            if y == numres and x < numvar:
                tabela[y][x] = (z[x] * -1)

    for y in range(0, numres):
        tabela[y][numvar + numres] = b[y]
        tabela[y][numvar + y] = 1

    return tabela

def verificarIteracao(tabela, numvar, numres):
    num = 0
    pivo = [-1, -1]

    for x in range(0, ((numvar + numres) + 1)):
        if (tabela[numres][x] < 0) and (tabela[numres][x] < num):
            num = tabela[numres][x]
            pivo[1] = x
    if num != 0:
        r = 0
        for y in range(0, numres):
            try:
                aux = (tabela[y][numvar + numres] / tabela[y][pivo[1]])
            except Exception:
                continue
            else:
                if (r > aux or r == 0) and aux > 0:
                    r = aux
                    pivo[0] = y
    return pivo

def iteracao(oldTabela, numvar, numres):
    pivo = verificarIteracao(oldTabela, numvar, numres)
    if pivo[0] == -1:
        return oldTabela
    else:
        novaTabela = gerarMatriz(((numvar + numres) + 1), (numres + 1))

        for x in range(0, ((numvar + numres) + 1)):
            novaTabela[pivo[0]][x] = (oldTabela[pivo[0]][x] / oldTabela[pivo[0]][pivo[1]])
      
        for y in range(0, (numres + 1)):
            if y != pivo[0]:
                for x in range(0, ((numvar + numres) + 1)):
                    novaTabela[y][x] = ((novaTabela[pivo[0]][x] * (oldTabela[y][pivo[1]] * -1)) + oldTabela[y][x])
        return novaTabela

def calculaColunaBase(tabelas, numvar, numres):
    pivos = []
    base = []                                                             

    for i in range(numvar, (numvar+numres)):                              
        base.append(i)

    for i in range(0, (len(tabelas) - 1)):                               
        pivos.append(verificarIteracao(tabelas[i], numvar, numres))

    for i in range(0, (len(pivos) - 1)):                                    
        base[pivos[i][0]] = pivos[i][1]

    return base

def calculoVariacao(tabela, numvar, numres, f):
    AR = [0, 0]
    aux = []
    for y in range(0, numres):
        try:
            aux.append(((tabela[y][numvar + numres] / tabela[y][f]) * -1))          
        except Exception:
            continue
        else:
            if aux[len(aux) - 1] > 0 and aux[len(aux) - 1] > AR[0]:
                AR[0] = aux[len(aux) - 1]
            if aux[len(aux) - 1] < 0 and aux[len(aux) - 1] < AR[1]:
                AR[1] = aux[len(aux) - 1]

    return AR

def printaAnalise(analise, numvar, numres):
    maxY = numvar + numres + 1
    colunas = ['Variavel', 'Variavel (Tipo)','Aumentar', 'Reduzir']
    for x in range(0, 4):
        if x == 0:
            print(f'{colunas[x]:^8}', end=' ')
        else:
            print(f'{colunas[x]:^11}', end=' ')
    print()
    
    for y in range(0, maxY):
        if y < numvar:
            var = 'X' + str(y + 1)
        elif y < numvar + numres:
            var = 'F' + str((y - numvar) + 1)
   
        print(f'{var:^8}', end=' ')
        for x in range(0, 13):
            if x == 0:
                if (type(analise[y][0]) == float):              ##Tipo variavel
                    print(f'{analise[y][0]:^11.2f}', end=' ')
                elif (type(analise[y][0]) == int):
                    print(f'{analise[y][0]:^11}', end=' ')
                elif (type(analise[y][0]) == str):
                    print(f'{analise[y][0]:^11}', end=' ')
                
                
            elif x == 9:
                if (type(analise[y][9]) == float):              ##Aumentar
                    print(f'{analise[y][9]:^11.2f}', end=' ')
                elif (type(analise[y][9]) == int):
                    print(f'{analise[y][9]:^11}', end=' ')
                elif (type(analise[y][9]) == str):
                    print(f'{analise[y][9]:^11}', end=' ')

            elif x == 10:
                if (type(analise[y][10]) == float):      
                    print(f'{analise[y][10]:^11.2f}', end=' ')        ##Reduzir
                elif (type(analise[y][10]) == int):
                    print(f'{analise[y][10]:^11}', end=' ')
                elif (type(analise[y][10]) == str):
                    print(f'{analise[y][10]:^11}', end=' ')
             
        print()
    print()

def analiseSensibilidade(tabelas, numvar, numres):

    analise = gerarMatriz(13, ((numvar + numres) + 1))
    base = calculaColunaBase(tabelas, numvar, numres)
                                                                            ### y será as linhas e x as linhas da tabela sensibilidade
    for y in range(0, ((numvar+numres) + 1)):                               ### Tipo de Variavel
        if y < numvar:
            analise[y][0] = '    Decisao    '
        elif y < numvar+numres:
            analise[y][0] = '     Folga     '
       
    for y in range(0, ((numvar + numres) + 1)):                              
        if y >= numvar and y < numvar + numres:                  
            AR = calculoVariacao(tabelas[(len(tabelas)) - 1], numvar, numres, y)    ##  Retorna o quanto pode aumentar[0] ou reduzir[1]
            for i in range(9, 13):                                  #   Colunas Aumentar ao Minimo
                if i == 9 or i == 11:                               #   Colunas Aumentar e Maximo
                    if AR[0] == 0:
                        analise[y][i] = 'ZERO'
                    elif i == 9:
                        analise[y][i] = AR[0]
                    else:
                        analise[y][i] = analise[y][1] + AR[0]
                else:                                               
                    if AR[1] == 0:
                        analise[y][i] = 'ZERO'
                    elif i == 10:
                        analise[y][i] = abs(AR[1])                  #   Para nao ficar com o valor negativo
                    else:
                        analise[y][i] = analise[y][1] + AR[1]       
        else:
            for i in range(9, 13):
                analise[y][i] = '-'

    printaAnalise(analise, numvar, numres)


if __name__ == '__main__':

    z = []
    b = []
    res = []
    iterac = []

    numvar = int(input('Digite o numero de variaveis de decisao: '))
    numres = int(input('Digite o numero de restricoes: '))
    print()

    obj = bool(int(input('MAX(1) ou MIN(0) ? ')))
    print()
    print('Funcao Objetivo:')
    for i in range(0, numvar):
        if obj:
            z.append(float(input(f'Digite o valor da variavel X{i + 1}: ')))
        else:
            z.append((float(input(f'Digite o valor da variavel X{i + 1}: '))) * -1)
    print()

    aux = []
    for f in range(0, numres):
        print(f'Restricao {f+1}:')
        for i in range(0, numvar):
            aux.append(float(input(f'Digite o valor da variavel X{i+1}: ')))
        b.append(float(input('Limite da restricao: ')))
        res.append(aux[:])
        aux.clear()
        print()

    imp = False
    for i in range(0, len(b)):
        if b[i] < 0:
            imp = True

    if imp:
        print('Solução Impossivel!')
    else:
        result = bool(int(input('Resultado final(0) ? ')))
        print()

        iterac.append(montarTabela(numvar, numres, res, b, z))
      
        terminou = False
        while (terminou != True):
            iterac.append(iteracao(iterac[len(iterac)-1], numvar, numres))             ### quando nao tem solução melhor retorna a tabela de volta
            if (iterac[len(iterac)-2] == iterac[len(iterac)-1]):                       ### Se for a mesma tabela sai do loop
                terminou = True
       
        if obj:
            print(f'Z = {iterac[len(iterac)-1][numres][numvar + numres]}')
            varnum = []
            valoresZerados = []
            for i in iterac[len(iterac) - 1]:
                varnum.append({i[-1]})
                valoresZerados.append({i[0]})
            print(f'X1 = {varnum[2]}')
            print(f'X2 = {varnum[0]}')
            print(f'F1 = {valoresZerados[0]}')
            print(f'F2 = {varnum[1]}')
            print(f'F3 = {valoresZerados[1]}')
        else:
            print(f'Z = {iterac[len(iterac) - 1][numres][numvar + numres] * -1}')
        print()

        analisa = bool(int(input('Analise de Sensibilidade(1) ? ')))
        if analisa:
            print()
            analiseSensibilidade(iterac, numvar, numres)