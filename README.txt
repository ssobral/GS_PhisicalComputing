# Detecção de Dedos Levantados com MediaPipe

## Descrição do Problema

Como parte do projeto Global Solution, cujo tema central é a gestão de quedas de energia, foi desenvolvido um sistema interativo com o objetivo de auxiliar funcionários durante situações de queda de energia. Em cenários em que a comunicação convencional pode estar comprometida, o sistema permite que o colaborador solicite ajuda de forma visual, por meio da detecção de gestos com as mãos, como levantar uma quantidade específica de dedos. Essa solução visa aumentar a segurança e agilidade na resposta a emergências em ambientes industriais e corporativos.

Caso o programa detecte 2 dedos levantados: 
Situação OK - Sem necessidade de auxílio.

Caso o programa detecte 5 dedos levantados: 
Situação de alerta - Necessário auxílio.

---

## Visão Geral da Solução

O sistema utiliza a biblioteca MediaPipe para realizar a detecção de mãos. A partir dos pontos de referência (landmarks) extraídos da mão, calculamos quantos dedos estão levantados.

### Tecnologias Utilizadas
- Python 3.10
- OpenCV
- MediaPipe

---

## Visão Geral da Solução

Os exemplos utilizados são vídeos gravados em alta e baixa luminosidade, para teste do sistema.
Ambos serão enviados juntos do código fonte e README

---

## Vídeo Demonstrativo

→ https://drive.google.com/file/d/1GrcCYXiRVJ9lXoZFwx_Szi4EYzpCDD4e/view?usp=sharing

---

## Repositório GITHUB

→ https://github.com/ssobral/GS_PhisicalComputing

---

## Integrantes

Lucas Sobral Roxo (RM98188)
Maitê Savicius Menezes (RM98435)
Murilo Henrique Obinata (RM99855)

---

## Código Fonte

import cv2
import mediapipe as mp
import time

def select_video():
    video = input('Selecione o vídeo em que deseja testar:\n1 - Luminosidade alta\n2 - Luminosidade baixa\n\n→')

    if video == "1":
        return "dedos.mp4"
    elif video == "2":
        return "dedos_baixa_luminosidade.mp4"

def dedos_levantados(landmarks):
    dedos = []

    dedos.append(landmarks[4].x < landmarks[3].x)
    for id in [8, 12, 16, 20]:
        dedos.append(landmarks[id].y < landmarks[id - 2].y)
    return dedos.count(True)

video = select_video()

mp_hands = mp.solutions.hands
hands = mp_hands.Hands()
mp_draw = mp.solutions.drawing_utils


captura = cv2.VideoCapture(video)

ultimo_print_ok = 0
ultimo_print_aberto = 0
intervalo = 0.5
cont_ok = 0
cont_alert = 0

while True:
    ret, frame = captura.read()

    img_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(img_rgb)

    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            mp_draw.draw_landmarks(frame, handLms, mp_hands.HAND_CONNECTIONS)

            dedos = dedos_levantados(handLms.landmark)
            tempo_atual = time.time()

            if dedos == 2 and (tempo_atual - ultimo_print_ok) > intervalo:
                print("Dois dedos levantados - OK! Sem necessidade de alarme.")
                ultimo_print_ok = tempo_atual
                cont_ok += 1

            if dedos == 5 and (tempo_atual - ultimo_print_aberto) > intervalo:
                print("Mão aberta detectada – ALERTA!")
                ultimo_print_aberto = tempo_atual
                cont_alert += 1

    if cont_ok == 5:
        print("DESATIVANDO! Não há necessidade de acionar alerta!")
        break
    elif cont_alert == 5:
        print("ACIONANDO ALERTA!!")
        break

    cv2.imshow("Deteccao de Gestos", frame)
    if cv2.waitKey(1) & 0xFF == 27:
        break

captura.release()
cv2.destroyAllWindows()

