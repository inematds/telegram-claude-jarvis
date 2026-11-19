#!/usr/bin/env python3
"""Casa a fala do avatar com as cenas.

palavras.json = [{"w": "Você", "ini": 0.12, "fim": 0.40}, ...] (Whisper com tempo por palavra)
spec.json     = {"ancoras": {"A_msg": "Você manda", ...}, ...}   (frases, na ordem em que são faladas)

ancoras(palavras, frases) -> {"A_msg": 3.21, ...}  (início da 1ª palavra de cada frase)
A busca anda só para frente, então frases repetidas casam na ordem certa.
"""
import json, re, sys, unicodedata


def norm(s):
    s = unicodedata.normalize("NFD", s.lower())
    s = "".join(c for c in s if unicodedata.category(c) != "Mn")
    return re.sub(r"[^a-z0-9]+", " ", s).strip()


def ancoras(palavras, frases):
    ws = [norm(p["w"]) for p in palavras]
    out, pos = {}, 0
    for nome, frase in frases.items():
        alvo = norm(frase).split()
        achou = None
        for i in range(pos, len(ws)):
            ok = True
            for k, a in enumerate(alvo):
                if i + k >= len(ws) or ws[i + k] != a:
                    ok = False
                    break
            if ok:
                achou = i
                break
        if achou is None:   # tolerância: 1ª palavra que bate o começo da frase
            raise SystemExit(f"âncora não achada: {nome} = '{frase}' (a partir da palavra {pos}: {' '.join(ws[pos:pos+12])})")
        out[nome] = round(palavras[achou]["ini"], 3)
        pos = achou + 1
    return out


if __name__ == "__main__":
    pal = json.load(open(sys.argv[1]))
    spec = json.load(open(sys.argv[2]))
    print(json.dumps(ancoras(pal, spec["ancoras"]), indent=1, ensure_ascii=False))
