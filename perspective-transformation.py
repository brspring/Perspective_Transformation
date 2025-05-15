import cv2
import numpy as np

resposta = input("1 - opala ou 2 - labirinto? ").strip().lower()

if resposta in ["1", "opala"]:
    caso = "opala"
    imagem_nome = "opala.jpeg"
    pontos_originais = np.float32([
        [488, 428],    # canto superior esquerdo
        [1072, 562],   # canto superior direito
        [479, 1280],   # canto inferior esquerdo
        [1039, 1010]   # canto inferior direito
    ])
elif resposta in ["2", "labirinto"]:
    caso = "labirinto"
    imagem_nome = "labirinto.jpeg"
    pontos_originais = np.float32([
        [399, 510],    # canto superior esquerdo
        [737, 560],    # canto superior direito
        [426, 1136],   # canto inferior esquerdo
        [744, 961]    # canto inferior direito
    ])
else:
    raise ValueError("Opção inválida. Digite '1', '2', 'opala' ou 'labirinto'.")

img = cv2.imread(f"images/{imagem_nome}")
assert img is not None, f"Erro: imagem '{imagem_nome}' não encontrada."

# calcular distância entre dois pontos
def distancia(p1, p2):
    return int(np.linalg.norm(np.array(p1) - np.array(p2)))

# largura e altura da imagem de destino
largura = distancia(pontos_originais[0], pontos_originais[1])
altura = distancia(pontos_originais[0], pontos_originais[2])

# pontos analisados
pontos_destino = np.float32([
    [0, 0],
    [largura, 0],
    [0, altura],
    [largura, altura]
])


# Calcula a matriz de homografia que transforma os quatro pontos na imagem original
# para os respectivos pontos da imagem de destino. Essa matriz representa uma transformação
# de perspectiva (projetiva) que endireita a imagem original.
H = cv2.getPerspectiveTransform(pontos_originais, pontos_destino)

# Aplica a matriz de homografia anterior a imagem original, produzindo uma nova imagem com a perspectiva corrigida.
# O resultado é como se o estivesse sendo visto de cima,
# com as características preservadas de acordo com os pontos destino definidos. O tamanho da nova imagem
# é especificado pelas variáveis 'largura' e 'altura'.
imagem_transformada = cv2.warpPerspective(img, H, (largura, altura))

# Salva a imagem
saida_nome = f"{caso}_transformado.jpg"
cv2.imwrite(f"results/{saida_nome}", imagem_transformada)

print(f"Imagem transformada salva como '{saida_nome}' ({largura}x{altura})")
