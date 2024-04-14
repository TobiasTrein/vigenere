import sys
import os

frequencias_portugues = {
    'a': 14.634, 'b': 1.043, 'c': 3.882, 'd': 4.992, 'e': 12.570,
    'f': 1.023, 'g': 1.303, 'h': 1.281, 'i': 6.186, 'j': 0.879,
    'k': 0.015, 'l': 2.779, 'm': 4.738, 'n': 4.446, 'o': 9.735,
    'p': 2.523, 'q': 1.204, 'r': 6.530, 's': 6.805, 't': 4.336,
    'u': 3.639, 'v': 1.575, 'w': 0.037, 'x': 0.453, 'y': 0.006, 'z': 0.470
}

frequencias_ingles = {
    'a': 8.167, 'b': 1.492, 'c': 2.782, 'd': 4.253, 'e': 12.702,
    'f': 2.228, 'g': 2.015, 'h': 6.094, 'i': 6.966, 'j': 0.153,
    'k': 0.772, 'l': 4.025, 'm': 2.406, 'n': 6.749, 'o': 7.507,
    'p': 1.929, 'q': 0.095, 'r': 5.987, 's': 6.327, 't': 9.056,
    'u': 2.758, 'v': 0.978, 'w': 2.360, 'x': 0.250, 'y': 1.974, 'z': 0.074
}

def indice_coincidencia(texto):
    freq = {}
    for c in texto:
        if c.isalpha():
            if c in freq:
                freq[c] += 1
            else:
                freq[c] = 1
    total = sum(freq.values())
    ic = sum((freq[c] * (freq[c] - 1)) / (total * (total - 1)) for c in freq)
    return ic

def similaridade_ic(ic1, ic2):
    return abs(ic1 - ic2)

def calcular_frequencia_letras(texto):
    frequencias = {}
    total_caracteres = 0
    for caractere in texto:
        if caractere.isalpha():
            if caractere in frequencias:
                frequencias[caractere] += 1
            else:
                frequencias[caractere] = 1
            total_caracteres += 1
    frequencias_percentual = {letra: (frequencia / total_caracteres) * 100 for letra, frequencia in frequencias.items()}
    return frequencias_percentual

def ordenar_frequencias(frequencias):
    return {letra: valor for letra, valor in sorted(frequencias.items(), key=lambda item: item[1], reverse=True)}

def encontrar_a_chave(texto_cifrado):

    linguagens = {
        'portugues': 0.074,
        'ingles': 0.066
    }

    frequencia_textos = {}

    resultados = []

    for tamanho_chave in range(1, 11):  # Itera sobre chaves de 1 a 10 caracteres
        textoselec = texto_cifrado[::tamanho_chave]  # Gera as chaves de acordo com o tamanho
        frequencia_textos[tamanho_chave] = calcular_frequencia_letras(textoselec)
        similaridades = {}
        ic_texto = indice_coincidencia(textoselec)
        for lingua, ic_lingua in linguagens.items():
            similaridade = similaridade_ic(ic_texto, ic_lingua)
            similaridades[lingua] = similaridade
        lingua_mais_proxima = min(similaridades, key=similaridades.get)
        resultados.append((tamanho_chave, ic_texto, lingua_mais_proxima))

    # Encontra o tamanho de chave com o índice de coincidência mais próximo de alguma das línguas
    tamanho_chave_mais_proximo = min(resultados, key=lambda x: min(abs(x[1] - v) for v in linguagens.values()))

    print("Tamanho da chave mais próximo:", tamanho_chave_mais_proximo[0])
    print("Índice de coincidência:", tamanho_chave_mais_proximo[1])
    print("Língua mais próxima:", tamanho_chave_mais_proximo[2])
    
    nmbchave = tamanho_chave_mais_proximo[0]

    # Exiba uma tabela de 3 colunas: 'frequencias_portugues', 'frequencias_ingles', 'frequencias_texto'
    # Cada coluna será ordenada individualmente da maior frequência para a menor
    if lingua_mais_proxima == 'portugues':
        frequencias_lingua_ordenadas = ordenar_frequencias(frequencias_portugues)
    else: 
        frequencias_lingua_ordenadas = ordenar_frequencias(frequencias_ingles)

    chave= ''

    for n in range(nmbchave):
        texto = texto_cifrado[n::nmbchave]    
        freq_texto = calcular_frequencia_letras(texto)
        frequencias_texto_ordenadas = ordenar_frequencias(freq_texto)
        deslocamento = ord(next(iter(frequencias_texto_ordenadas))) - ord(next(iter(frequencias_lingua_ordenadas)))

        # Transforma o deslocamento em um caractere
        chave += chr((deslocamento % 26) + ord('a'))

    print(f"chave encontrada: {chave}")
    return chave

def ler_arquivo(nome_arquivo):
    # Obtém o diretório atual do script
    diretorio_atual = os.path.dirname(os.path.realpath(__file__))
    # Constrói o caminho completo para o arquivo na pasta 'cifrados'
    caminho_arquivo = os.path.join(diretorio_atual, 'cifrados', nome_arquivo)
    with open(caminho_arquivo, 'r') as arquivo:
        texto = arquivo.read()
    return texto

def decrypt_vigenere(ciphertext, key):
    key_length = len(key)
    decrypted = []
    for i, char in enumerate(ciphertext):
        key_char = key[i % key_length]
        if char.isalpha():
            decrypted_char = chr(((ord(char) - ord(key_char)) % 26) + ord('A'))
        else:
            decrypted_char = char
        decrypted.append(decrypted_char)
    return ''.join(decrypted)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Por favor, forneça o nome do arquivo como argumento.")
        sys.exit(1)

    nome_arquivo = sys.argv[1]
    texto_cifrado = ler_arquivo(nome_arquivo)

# encontra a chave do texto cifrado
chave_descoberta = encontrar_a_chave(texto_cifrado)

# Descriptografa o texto cifrado usando a chave descoberta
texto_decifrado = decrypt_vigenere(texto_cifrado, chave_descoberta)

# Salvar o texto decifrado em um arquivo na pasta output
nome_arquivo_saida = nome_arquivo.replace(".txt", "_out.txt")
with open("output/" + nome_arquivo_saida, 'w') as arquivo_saida:
    arquivo_saida.write(texto_decifrado)

print("Texto decifrado salvo em", nome_arquivo_saida)
