"""Berechnet jede Paarung für „Wer würde gewinnen?“ und schreibt src/v3/fights.js."""
import itertools, json, os

STAT = ["Kraft", "Tempo", "Ausdauer", "Kampftechnik", "Köpfchen", "Spezialkraft"]
W = [2.0, 1.5, 1.8, 1.0, 0.6, 1.0]

# id, Name, Bild, Seite, Werte, Tags, Spezial-Satz
F = [
  ("superman", "Superman (Bestform, Staffel 1–3)", "e_s1e10", "held", [10, 9, 10, 7, 7, 9], {"kryp": "full"}, "Er hat Hitzeblick, Frostatem und die Kraft, einen Zug anzuhalten."),
  ("superman8", "Superman (Staffel 8, halbe Kraft)", "clark", "held", [7, 7, 7, 9, 7, 7], {"kryp": "full"}, "Weniger Kraft als früher, aber mehr Erfahrung als jeder andere."),
  ("lois", "Lois mit Superkräften (5x06)", "lois", "held", [8, 7, 8, 3, 8, 6], {"kryp": "full"}, "Supermans Kräfte – mit einem Tag Übung."),
  ("jordan", "Jordan Kent", "jordan", "held", [8, 9, 7, 6, 6, 9], {"kryp": "half"}, "Sein Sonnenstoß ist eine der stärksten Waffen im Team."),
  ("jonathan", "Jonathan Kent", "jonathan", "held", [9, 8, 8, 6, 5, 7], {"kryp": "half"}, "Rohe Kraft und das Herz eines Feuerwehrmanns."),
  ("steel", "Steel", "johnhenry", "held", [6, 6, 8, 8, 9, 8], {"tech": 1}, "Ein Genie in einer Rüstung mit einem Hammer, der Sonnenenergie speichert."),
  ("starlight", "Starlight", "natalie", "held", [5, 7, 6, 7, 9, 7], {"tech": 1}, "Schnell, wendig, und sie baut ihre Rüstung selbst."),
  ("batman", "Batman", "c_batman2", "held", [3, 4, 4, 10, 10, 9], {"kryptonite": 1, "radion": 1, "tech": 1}, "Er hat für jeden Gegner einen Plan – und Kryptonit in der Tasche."),
  ("ww", "Wonder Woman", "c_ww", "held", [9, 8, 9, 10, 7, 9], {"magic": 1}, "Jahrhunderte Kampftraining, magisches Schwert und das Lasso der Wahrheit."),
  ("flash", "The Flash", "barry", "held", [4, 10, 5, 7, 8, 9], {"speed": 1}, "Schneller als jeder Gedanke."),
  ("aquaman", "Aquaman", "c_aquaman", "held", [8, 6, 9, 8, 6, 7], {}, "Stark wie ein Panzer, im Wasser nicht zu schlagen."),
  ("talrho", "Tal-Rho", "talrho", "held", [9, 9, 9, 7, 7, 6], {"kryp": "full"}, "Kryptonische Kräfte und ein Leben voller Kämpfe."),
  ("doomsday", "Doomsday", "bizarro", "schurke", [10, 7, 10, 3, 1, 10], {"regen": 8}, "Er kommt nach jeder Niederlage stärker zurück."),
  ("brainiac", "Brainiac", "c_brainiac", "schurke", [7, 7, 8, 6, 10, 10], {"hack": 1}, "Er übernimmt jede Maschine und kopiert Kräfte."),
  ("metallo", "Metallo", "c_metallo", "schurke", [6, 5, 8, 6, 5, 8], {"kryptonite": 1, "tech": 1}, "Sein Herz ist aus Kryptonit."),
  ("zod", "General Zod", "c_zod2", "schurke", [10, 9, 10, 10, 7, 7], {"kryp": "full"}, "Supermans Kräfte plus eine Ausbildung als Soldat."),
  ("faora", "Faora", "c_faora", "schurke", [9, 9, 9, 10, 6, 7], {"kryp": "full"}, "Kryptonische Kräfte und die beste Nahkampftechnik Kryptons."),
  ("mongul", "Mongul", "c_mongul2", "schurke", [10, 7, 10, 9, 7, 8], {}, "So stark wie Superman und erfahren aus hundert Kriegen."),
  ("lobo", "Lobo", "c_lobo", "schurke", [8, 7, 9, 7, 6, 9], {"regen": 6}, "Fast unsterblich und gemein wie ein Hai."),
  ("lex", "Lex Luthor (Kriegsrüstung)", "c_lexarmor", "schurke", [6, 6, 7, 7, 10, 8], {"kryptonite": 1, "redsun": 1, "tech": 1}, "Eine Rüstung voller Kryptonit und roter Sonnenlampen."),
  ("rflash", "Reverse-Flash", "c_rflash", "schurke", [4, 10, 5, 8, 9, 9], {"speed": 1}, "Genauso schnell wie Flash und viel skrupelloser."),
  ("cheetah", "Cheetah", "c_cheetah", "schurke", [7, 8, 7, 9, 6, 7], {}, "Krallen, die sogar Amazonen verletzen."),
  ("manta", "Black Manta", "c_manta", "schurke", [5, 5, 6, 8, 8, 7], {"tech": 1}, "Hightech-Rüstung mit Laserhelm."),
  ("steppenwolf", "Steppenwolf", "c_steppen2", "schurke", [9, 7, 9, 9, 6, 8], {"god": 3}, "Darkseids General mit einer Axt aus Energie."),
  ("kalibak", "Kalibak", "c_kalibak", "schurke", [9, 6, 9, 7, 3, 6], {"god": 3}, "Darkseids Sohn, ein Berg aus Muskeln."),
  ("darkseid", "Darkseid", "c_darkseid2", "schurke", [10, 6, 10, 9, 9, 10], {"god": 15}, "Ein fast-Gott mit roten Augenstrahlen, die um Ecken fliegen."),
]
BY = {f[0]: f for f in F}
GODS = {"darkseid", "steppenwolf", "kalibak"}

def base(f):
    return sum(s * w for s, w in zip(f[4], W))

def mods(a, b):
    """Bonuspunkte für a im Kampf gegen b, mit Begründung."""
    s, notes = 0, []
    ta, tb = a[5], b[5]
    if ta.get("kryptonite") and tb.get("kryp") == "full":
        s += 18; notes.append(f"{a[1]} hat Kryptonit dabei – das lähmt jeden echten Kryptonier.")
    if ta.get("kryptonite") and tb.get("kryp") == "half":
        s += 9; notes.append(f"Kryptonit hilft {a[1]}, aber {b[1]} ist als Halb-Mensch weniger anfällig.")
    if ta.get("redsun") and tb.get("kryp"):
        s += 6; notes.append(f"Rote Sonnenlampen saugen {b[1]} die Kraft ab.")
    if ta.get("magic") and tb.get("kryp"):
        s += 5; notes.append(f"Kryptonier sind gegen Magie verwundbar – und {a[1]}s Schwert ist magisch.")
    if ta.get("speed") and not tb.get("speed"):
        if b[4][2] >= 9:
            s += 4; notes.append(f"{a[1]} ist viel schneller, aber {b[1]} ist so zäh, dass die Schläge kaum wehtun.")
        else:
            s += 10; notes.append(f"{a[1]} ist so schnell, dass {b[1]} ihn kaum trifft.")
    if ta.get("hack") and tb.get("tech"):
        s += 10; notes.append(f"{a[1]} übernimmt einfach die Technik von {b[1]}.")
    if ta.get("hack") and tb.get("kryp"):
        s += 6; notes.append(f"{a[1]} kann kryptonische Kräfte kopieren und abziehen.")
    if ta.get("regen"):
        s += ta["regen"]; notes.append(f"{a[1]} steht nach jedem Treffer wieder auf.")
    if ta.get("god") and b[0] not in GODS:
        s += ta["god"]
        if a[0] == "darkseid":
            notes.append("Darkseid ist ein fast-Gott – seine Augenstrahlen verfehlen nie.")
    if ta.get("radion") and b[0] in GODS:
        s += 20; notes.append(f"{a[1]} hat Radion – den einzigen Stoff, der die Götter von Apokolips verletzt.")
    return s, notes

OVR = {
  ("superman", "batman"): ("superman", "Ohne Vorbereitung gewinnt Superman in einer Sekunde. Mit Kryptonit, Zeit und einem Plan könnte Batman ihn besiegen – aber auf offener Straße bleibt Superman vorn. In unserer Geschichte sind die beiden ab Staffel 6 beste Freunde und würden diesen Kampf nie führen."),
  ("superman8", "batman"): ("batman", "Mit halber Kraft ist Clark verwundbar. Batman trägt Kryptonit und hat, wie er in 6x04 sagt, für jeden einen Notfallplan – auch für seinen besten Freund."),
  ("superman", "doomsday"): ("doomsday", "Kanon: In 4x01 hat Doomsday Superman getötet. Jeder Tod macht ihn stärker. Nur mit Hilfe der Familie und dem Flug in die Sonne war er zu stoppen."),
  ("superman", "darkseid"): ("darkseid", "Selbst in Bestform ist Superman gegen einen fast-Gott unterlegen. Darkseids Augenstrahlen folgen ihm um jede Ecke. In 9x12 brauchte es die ganze Justice League und eine Radion-Kugel."),
  ("superman", "zod"): ("superman", "Hauchdünn. Gleiche Kräfte, Zod ist besser ausgebildet. Aber Superman kämpft für etwas, Zod nur gegen etwas – und als Clark in 6x10 voll aufgeladen war, hielt er Zod stand."),
  ("superman", "ww"): ("ww", "Knapp. Beide gleich stark, aber Diana hat Jahrhunderte Kampftraining und ein magisches Schwert, gegen das Kryptonier nicht geschützt sind. In den Comics ist dieses Duell ein ewiges Kopf-an-Kopf-Rennen."),
  ("flash", "rflash"): ("flash", "Beide gleich schnell. Barry gewinnt, weil er für Iris rennt und nicht aus Hass – und weil er Reverse-Flash in 8x11 zurück in die Speedkraft schickt."),
  ("ww", "cheetah"): ("ww", "Cheetahs Krallen können Diana verletzen, aber Diana kennt jeden ihrer Sprünge. Das Lasso beendet den Kampf."),
  ("aquaman", "manta"): ("aquaman", "Manta hat Hightech und Hass. Arthur hat Kraft, Erfahrung und den Ozean auf seiner Seite."),
  ("jonathan", "mongul"): ("mongul", "Allein verliert Jonathan gegen Mongul. In 7x11 gewann er nur, weil die roten Lampen aus waren und sein Vater, sein Bruder und Wonder Woman neben ihm standen."),
  ("superman", "lex"): ("superman", "Kanon: In 4x10 hat Superman Lex' Rüstung zerlegt und ihn vor laufender Kamera besiegt – sogar mit geschwächtem Herzen. In Bestform erst recht."),
  ("batman", "darkseid"): ("darkseid", "Batmans Radion-Kugel trifft Darkseid und schwächt ihn wirklich. Aber ein Schuss reicht nicht gegen einen Gott – in 9x12 brauchte es danach noch die ganze Justice League."),
  ("lois", "metallo"): ("lois", "In 5x06 hat Lois Metallo in die Flucht geschlagen – mit geliehenen Kräften, einer Bleischürze und purer Sturheit."),
  ("jordan", "jonathan"): ("jordan", "Hauchdünn. Jonathan ist stärker, Jordan hat den Sonnenstoß und mehr Erfahrung, denn seine Kräfte kamen schon in Staffel 1. Nach drei Minuten würden sie aufhören und Pizza bestellen."),
  ("superman", "flash"): ("superman", "Ein Wettrennen gewinnt Flash. Einen Kampf nicht: Flash trifft Superman hundertmal pro Sekunde, aber das tut ihm kaum weh. Ein einziger Treffer von Superman reicht."),
  ("superman", "mongul"): ("superman", "Außerhalb der Arena knapp Superman. In Monguls Arena mit roten Lampen hätte er keine Chance – das hat Staffel 7 gezeigt."),
  ("superman", "talrho"): ("superman", "Knapp. In Staffel 1 hat Superman seinen Halbbruder besiegt, allerdings mit John Henrys Hilfe."),
  ("ww", "batman"): ("ww", "Diana gewinnt. Bruce würde es nie zugeben – und in Staffel 8 hat sie ihm das schon auf einem Dach in Gotham bewiesen."),
  ("jordan", "flash"): ("flash", "Barry hat Jordan in Staffel 8 trainiert. Der Lehrer ist noch schneller als der Schüler."),
}

def key(a, b):
    return (a, b) if (a, b) in OVR else ((b, a) if (b, a) in OVR else None)

def verdict(a, b):
    k = key(a[0], b[0])
    pa = base(a) + mods(a, b)[0]
    pb = base(b) + mods(b, a)[0]
    if k:
        w, text = OVR[k]
        return w, "override", round(pa, 1), round(pb, 1), text
    na, nb = mods(a, b)[1], mods(b, a)[1]
    d = pa - pb
    w, l = (a, b) if d >= 0 else (b, a)
    gap = abs(d)
    cat = "hauchdünn" if gap < 3 else "knapp" if gap < 8 else "klar" if gap < 16 else "deutlich"
    diffs = [(STAT[i], w[4][i] - l[4][i]) for i in range(6)]
    best = max(diffs, key=lambda x: x[1] * W[STAT.index(x[0])])
    worst = min(diffs, key=lambda x: x[1] * W[STAT.index(x[0])])
    parts = [f"{w[1]} gewinnt {cat}. {w[6]}"]
    if best[1] > 0:
        parts.append(f"Den Unterschied macht vor allem {best[0]} ({w[4][STAT.index(best[0])]} gegen {l[4][STAT.index(best[0])]}).")
    if w[5].get("kryp") and l[5].get("kryp") == w[5].get("kryp") and best[0] in ("Kampftechnik", "Köpfchen"):
        parts.append("Bei gleichen Kräften entscheidet Training.")
    parts += (na if w is a else nb) + (nb if w is a else na)
    if worst[1] < 0:
        parts.append(f"{l[1]} ist bei {worst[0]} besser, aber das reicht nicht.")
    return w[0], cat, round(pa, 1), round(pb, 1), " ".join(dict.fromkeys(parts))

out = []
for a, b in itertools.combinations(F, 2):
    w, cat, pa, pb, text = verdict(a, b)
    out.append([a[0], b[0], w, cat, pa, pb, text])

fighters = [{"id": f[0], "name": f[1], "img": f[2], "side": f[3], "s": f[4]} for f in F]
root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
with open(os.path.join(root, "src", "v3", "fights.js"), "w", encoding="utf-8") as fh:
    fh.write("const STATS = " + json.dumps(STAT, ensure_ascii=False) + ";\n")
    fh.write("const FIGHTERS = " + json.dumps(fighters, ensure_ascii=False) + ";\n")
    fh.write("const MATCHUPS = " + json.dumps(out, ensure_ascii=False) + ";\n")
wins = {f[0]: 0 for f in F}
for r in out:
    wins[r[2]] += 1
print(len(out), "Paarungen")
print(sorted(wins.items(), key=lambda x: -x[1]))
