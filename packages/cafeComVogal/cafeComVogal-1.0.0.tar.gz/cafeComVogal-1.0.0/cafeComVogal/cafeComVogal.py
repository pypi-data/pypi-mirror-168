from unicodedata import normalize, combining


def eu_disse_que_faria(stringCompleta: str):
    decom = normalize('NFD', stringCompleta)
    stringFormatada = ''.join(letra for letra in decom if not combining(letra))
    return [stringCompleta[v] for v in range(len(stringFormatada)) if stringFormatada[v].casefold() in 'aeiou']


def vogais(stringCompleta: str):
    decom = normalize('NFD', stringCompleta)
    vogaisDict = {'vogais': [], 'vogais_com_indice': []}
    stringFormatada = ''.join(letra for letra in decom if not combining(letra))
    for i, vogal in enumerate(stringCompleta):
        if stringFormatada[i].casefold() in 'aeiou':
            vogaisDict['vogais_com_indice'].append((i, vogal))
            vogaisDict['vogais'].append(vogal)
        else:
            pass
    return vogaisDict


if __name__ == '__main__':
    print(f'As vogais são: {eu_disse_que_faria("Wanderson Renê")}')
