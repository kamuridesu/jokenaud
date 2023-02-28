from pydub import AudioSegment
import threading
from pydub.utils import get_player_name
from tempfile import NamedTemporaryFile
import os
import subprocess
from random import randint

from io import BytesIO
import base64
from conf import AUDIO

PLAYER = get_player_name()


def _play_with_ffplay_suppress(seg):
    with NamedTemporaryFile("w+b", suffix=".wav") as f:
        seg.export(f.name, "wav")
        devnull = open(os.devnull, 'w')
        subprocess.call([PLAYER,"-nodisp", "-autoexit", "-hide_banner", f.name],stdout=devnull, stderr=devnull)


sound = AudioSegment.from_file(BytesIO(base64.b64decode(AUDIO)))

OPTIONS = ["pedra", "papel", "tesoura"]

while True:
    score = 0
    # main game loop
    threading.Thread(target=_play_with_ffplay_suppress, args=(sound,)).start()
    while (user := input("Pedra, papel ou tesoura? ").lower().strip()) not in OPTIONS:
        print("Escolha uma opção da lista!")
    cpu = OPTIONS[randint(0, len(OPTIONS) - 1)]
    winner = (3 + OPTIONS.index(user) - OPTIONS.index(cpu)) % 3
    match winner:
        case 0:
            print("Empate!")
        case 1:
            print("Ganhou!")
            score += 1
        case 2:
            print("Perdeu!")
            score -= 1

    while (retry := input("Quer continuar? [SsNn] ").lower().strip()) not in "sn":
        print("Erro! Escolha S ou N")
    if retry == "n":
        print("Pontuação total:", score)
        break
