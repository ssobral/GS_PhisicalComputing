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
