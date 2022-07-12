from pydub import AudioSegment
import threading
from pydub.utils import get_player_name
from tempfile import NamedTemporaryFile
import os
import subprocess
from random import choice

PLAYER = get_player_name()


def _play_with_ffplay_suppress(seg):
    with NamedTemporaryFile("w+b", suffix=".wav") as f:
        seg.export(f.name, "wav")
        devnull = open(os.devnull, 'w')
        subprocess.call([PLAYER,"-nodisp", "-autoexit", "-hide_banner", f.name],stdout=devnull, stderr=devnull)

sound = AudioSegment.from_mp3("./audio.mp3")

OPTIONS = ["pedra", "papel", "tesoura"]

while True:
    score = 0
    # main game loop
    threading.Thread(target=_play_with_ffplay_suppress, args=(sound,)).start()
    while (user := input("Pedra, papel ou tesoura? ").lower().strip()) not in OPTIONS:
        print("Escolha uma opção da lista!")
    cpu = choice(OPTIONS)
    winner = (3 + OPTIONS.index(user) - OPTIONS.index(cpu)) % 3
    if winner == 0:
        print("Empate!")
    if winner == 1:
        print("Ganhou!")
        score += 1
    if winner == 2:
        print("Perdeu!")
        score -= 1
    while (retry := input("Quer continuar? [SsNn]").lower().strip()) not in "sn":
        print("Erro! Escolha S ou N")
    if retry == "n":
        print("Pontuação total:", score)
        break
