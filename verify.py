"""Verifierar JS computeStats mot Python-implementation. Speglar index.html INGREDIENT_DB + RECIPES + TARGETS.

Kör efter recept-ändringar (`py verify.py`) för att bekräfta att alla recept ligger i sina target-zoner. Mål: 0 BAD.
Speglar computeStats() exakt — ingredienser utan DB-post eller override räknas som 0 (vatten/inert).
"""

PAC = {'sucrose': 100, 'dextrose': 190, 'fructose': 190, 'glucose_de42': 80, 'lactose': 100}
POD = {'sucrose': 100, 'dextrose': 70,  'fructose': 170, 'glucose_de42': 50, 'lactose': 16}

# INGREDIENT_DB — speglar index.html. Lactose i sugars ignoreras (räknas via msnf*0.54).
DB = {
    'Grädde 36%':                                  {'fat': 0.36, 'msnf': 0.05},
    'Grädde 40%':                                  {'fat': 0.40, 'msnf': 0.047},
    'Mjölk 3%':                                    {'fat': 0.03, 'msnf': 0.088},
    'Kaffemjölk (mjölk 3% + infusionerat kaffe)':  {'fat': 0.03, 'msnf': 0.088},
    'Skummjölkspulver':                            {'fat': 0,    'msnf': 0.96},
    'Sötad kondenserad mjölk':                     {'fat': 0.08, 'msnf': 0.21, 'sugars': {'sucrose': 0.45}},
    'Strösocker':                                  {'sugars': {'sucrose': 1.0}},
    'Strösocker (i basen)':                        {'sugars': {'sucrose': 1.0}},
    'Atomiserad dextros':                          {'sugars': {'dextrose': 1.0}},
    'Glykossirap':                                 {'sugars': {'glucose_de42': 0.80}},  # bakåtkompat, ingen preset
    'Glukossirap':                                 {'sugars': {'glucose_de42': 0.80}},  # bakåtkompat, ingen preset
    'Honung':                                      {'sugars': {'fructose': 0.38, 'glucose_de42': 0.31}},
    'Flytande äggula':                             {'fat': 0.27},
    'Mörk choklad 70%':                            {'fat': 0.40, 'sugars': {'sucrose': 0.30}},
    'Kakao (holländsk)':                           {'fat': 0.22},
    '+ Bär-koncentrat (kallt)':                    {'sugars': {'fructose': 0.18}},
    'Passionsfruktspuré (reducerad, silad)':       {'sugars': {'fructose': 0.22}},
    'Reducerad kokosmjölk (från ~500g)':           {'fat': 0.40, 'msnf': 0.04},
    'Rostad kokosflakes (valfritt, sista 2 min)':  {'fat': 0.65},
    'Rostad vit choklad':                          {'fat': 0.32, 'sugars': {'sucrose': 0.55}},
    'Pistagepasta (100%)':                         {'fat': 0.55},
    '+ Äppelkompott (kall)':                       {'sugars': {'sucrose': 0.17, 'fructose': 0.17}},
}

def props(name):
    d = DB.get(name, {})
    return {'fat': d.get('fat', 0), 'msnf': d.get('msnf', 0), 'sugars': d.get('sugars', {})}

def compute(items, totalG):
    fatG = msnfG = gelG = 0
    sugars = {'sucrose': 0, 'dextrose': 0, 'fructose': 0, 'glucose_de42': 0, 'lactose': 0}
    for it in items:
        if it.get('excludeFromBase'): continue
        p = props(it['name'])
        g = it['g']
        fatG  += g * p['fat']
        msnfG += g * p['msnf']
        sugars['lactose'] += g * p['msnf'] * 0.54
        for t, frac in p['sugars'].items():
            if t == 'lactose': continue
            sugars[t] = sugars.get(t, 0) + g * frac
        if it['name'] == 'Bladgelatin': gelG += g
    added = sugars['sucrose'] + sugars['dextrose'] + sugars['fructose'] + sugars['glucose_de42']
    pac = sum(g * PAC.get(t, 0) for t, g in sugars.items()) / totalG
    pod = sum(g * POD.get(t, 0) for t, g in sugars.items()) / totalG
    return {
        'fat':  fatG / totalG * 100,
        'msnf': msnfG / totalG * 100,
        'sugar': (added + sugars['lactose']) / totalG * 100,
        'ts':   (fatG + msnfG + added) / totalG * 100 + 1,
        'pac':  pac,
        'pod':  pod,
        'gel':  gelG / totalG * 1000,
    }

# RECIPES — speglar index.html. (bas, items). Alla recept har sötad kondenserad mjölk (wow-kropp).
RECIPES = {
    'vanilj': (725, [
        {'name': 'Grädde 40%', 'g': 215}, {'name': 'Mjölk 3%', 'g': 275},
        {'name': 'Skummjölkspulver', 'g': 30}, {'name': 'Sötad kondenserad mjölk', 'g': 40},
        {'name': 'Strösocker', 'g': 63}, {'name': 'Atomiserad dextros', 'g': 24},
        {'name': 'Flytande äggula', 'g': 50}, {'name': 'Bladgelatin', 'g': 1.7},
        {'name': 'Vaniljextrakt', 'g': 10}, {'name': 'Salt', 'g': 0.7},
    ]),
    'choklad': (736, [
        {'name': 'Grädde 40%', 'g': 150}, {'name': 'Mjölk 3%', 'g': 285},
        {'name': 'Skummjölkspulver', 'g': 20}, {'name': 'Sötad kondenserad mjölk', 'g': 55},
        {'name': 'Mörk choklad 70%', 'g': 90}, {'name': 'Kakao (holländsk)', 'g': 20},
        {'name': 'Strösocker', 'g': 27}, {'name': 'Atomiserad dextros', 'g': 30},
        {'name': 'Flytande äggula', 'g': 40}, {'name': 'Bladgelatin', 'g': 1.7}, {'name': 'Salt', 'g': 1},
    ]),
    'jordgubb': (739, [
        {'name': 'Grädde 40%', 'g': 155}, {'name': 'Mjölk 3%', 'g': 170},
        {'name': 'Skummjölkspulver', 'g': 30}, {'name': 'Sötad kondenserad mjölk', 'g': 50},
        {'name': 'Strösocker (i basen)', 'g': 23}, {'name': 'Atomiserad dextros', 'g': 22},
        {'name': 'Flytande äggula', 'g': 30}, {'name': 'Bladgelatin', 'g': 1.7}, {'name': 'Salt', 'g': 1},
        {'name': '+ Bär-koncentrat (kallt)', 'g': 235},
    ]),
    'passion': (571, [
        {'name': 'Grädde 40%', 'g': 137.5}, {'name': 'Mjölk 3%', 'g': 112.5},
        {'name': 'Skummjölkspulver', 'g': 20}, {'name': 'Sötad kondenserad mjölk', 'g': 60},
        {'name': 'Passionsfruktspuré (reducerad, silad)', 'g': 125}, {'name': 'Strösocker', 'g': 20},
        {'name': 'Atomiserad dextros', 'g': 14}, {'name': 'Flytande äggula', 'g': 60},
        {'name': 'Bladgelatin', 'g': 1.7},
    ]),
    'kokos': (630, [
        {'name': 'Grädde 40%', 'g': 137.5}, {'name': 'Mjölk 3%', 'g': 112.5},
        {'name': 'Skummjölkspulver', 'g': 15}, {'name': 'Sötad kondenserad mjölk', 'g': 40},
        {'name': 'Reducerad kokosmjölk (från ~500g)', 'g': 180}, {'name': 'Strösocker', 'g': 52},
        {'name': 'Atomiserad dextros', 'g': 38}, {'name': 'Flytande äggula', 'g': 60},
        {'name': 'Bladgelatin', 'g': 1.7}, {'name': 'Rostad kokosflakes (valfritt, sista 2 min)', 'g': 25},
    ]),
    'kaffe': (740, [
        {'name': 'Grädde 40%', 'g': 251}, {'name': 'Kaffemjölk (mjölk 3% + infusionerat kaffe)', 'g': 205},
        {'name': 'Skummjölkspulver', 'g': 15}, {'name': 'Sötad kondenserad mjölk', 'g': 45},
        {'name': 'Strösocker', 'g': 75}, {'name': 'Flytande äggula', 'g': 110},
        {'name': 'Atomiserad dextros', 'g': 23}, {'name': 'Bladgelatin', 'g': 1.7},
        {'name': 'Mald kaffe (för infusion, filtreras bort)', 'g': 32, 'excludeFromBase': True},
    ]),
    'lakrits': (710, [
        {'name': 'Grädde 40%', 'g': 210}, {'name': 'Mjölk 3%', 'g': 280},
        {'name': 'Skummjölkspulver', 'g': 30}, {'name': 'Sötad kondenserad mjölk', 'g': 35},
        {'name': 'Strösocker', 'g': 62}, {'name': 'Atomiserad dextros', 'g': 24},
        {'name': 'Flytande äggula', 'g': 50}, {'name': 'Bladgelatin', 'g': 1.7},
        {'name': 'Lakritspulver (rå)', 'g': 14}, {'name': 'Flingsalt', 'g': 3},
    ]),
    'vitchoklad': (669, [
        {'name': 'Grädde 40%', 'g': 150}, {'name': 'Mjölk 3%', 'g': 293},
        {'name': 'Skummjölkspulver', 'g': 25}, {'name': 'Sötad kondenserad mjölk', 'g': 40},
        {'name': 'Rostad vit choklad', 'g': 70}, {'name': 'Strösocker', 'g': 22},
        {'name': 'Atomiserad dextros', 'g': 20}, {'name': 'Flytande äggula', 'g': 45},
        {'name': 'Bladgelatin', 'g': 1.7}, {'name': 'Kardemumma (mald)', 'g': 2}, {'name': 'Salt', 'g': 0.5},
    ]),
    'pistage': (705, [
        {'name': 'Grädde 40%', 'g': 165}, {'name': 'Mjölk 3%', 'g': 285},
        {'name': 'Skummjölkspulver', 'g': 30}, {'name': 'Sötad kondenserad mjölk', 'g': 35},
        {'name': 'Pistagepasta (100%)', 'g': 55}, {'name': 'Strösocker', 'g': 62},
        {'name': 'Atomiserad dextros', 'g': 22}, {'name': 'Flytande äggula', 'g': 48},
        {'name': 'Bladgelatin', 'g': 1.7}, {'name': 'Salt', 'g': 1},
    ]),
    'earlgrey': (696, [
        {'name': 'Grädde 40%', 'g': 215}, {'name': 'Mjölk 3%', 'g': 280},
        {'name': 'Skummjölkspulver', 'g': 30}, {'name': 'Sötad kondenserad mjölk', 'g': 30},
        {'name': 'Strösocker', 'g': 66}, {'name': 'Atomiserad dextros', 'g': 22},
        {'name': 'Flytande äggula', 'g': 50}, {'name': 'Bladgelatin', 'g': 1.7}, {'name': 'Salt', 'g': 1},
        {'name': 'Earl Grey-te (löst, infuseras)', 'g': 9, 'excludeFromBase': True},
    ]),
    'matcha': (700, [
        {'name': 'Grädde 40%', 'g': 210}, {'name': 'Mjölk 3%', 'g': 278},
        {'name': 'Skummjölkspulver', 'g': 30}, {'name': 'Sötad kondenserad mjölk', 'g': 30},
        {'name': 'Strösocker', 'g': 68}, {'name': 'Atomiserad dextros', 'g': 22},
        {'name': 'Flytande äggula', 'g': 50}, {'name': 'Bladgelatin', 'g': 1.7},
        {'name': 'Matcha (ceremoniell)', 'g': 10}, {'name': 'Salt', 'g': 0.5},
    ]),
    'romrussin': (712, [
        {'name': 'Grädde 40%', 'g': 212}, {'name': 'Mjölk 3%', 'g': 278},
        {'name': 'Skummjölkspulver', 'g': 30}, {'name': 'Sötad kondenserad mjölk', 'g': 35},
        {'name': 'Strösocker', 'g': 64}, {'name': 'Atomiserad dextros', 'g': 22},
        {'name': 'Flytande äggula', 'g': 50}, {'name': 'Bladgelatin', 'g': 1.7}, {'name': 'Salt', 'g': 1},
        {'name': 'Mörk rom', 'g': 18}, {'name': 'Rom-russin (sista 2 min)', 'g': 55, 'excludeFromBase': True},
    ]),
    'saffran': (694, [
        {'name': 'Grädde 40%', 'g': 215}, {'name': 'Mjölk 3%', 'g': 275},
        {'name': 'Skummjölkspulver', 'g': 30}, {'name': 'Sötad kondenserad mjölk', 'g': 35},
        {'name': 'Strösocker', 'g': 64}, {'name': 'Atomiserad dextros', 'g': 22},
        {'name': 'Flytande äggula', 'g': 50}, {'name': 'Bladgelatin', 'g': 1.7},
        {'name': 'Saffran', 'g': 0.5}, {'name': 'Salt', 'g': 1},
    ]),
    'applekanel': (690, [
        {'name': 'Grädde 40%', 'g': 180}, {'name': 'Mjölk 3%', 'g': 195},
        {'name': 'Skummjölkspulver', 'g': 32}, {'name': 'Sötad kondenserad mjölk', 'g': 30},
        {'name': 'Strösocker', 'g': 8}, {'name': 'Atomiserad dextros', 'g': 18},
        {'name': 'Flytande äggula', 'g': 42}, {'name': 'Bladgelatin', 'g': 1.7},
        {'name': 'Kanel (mald)', 'g': 3}, {'name': 'Salt', 'g': 0.5},
        {'name': '+ Äppelkompott (kall)', 'g': 180},
    ]),
    'citronlakrits': (714, [
        {'name': 'Grädde 40%', 'g': 200}, {'name': 'Mjölk 3%', 'g': 250},
        {'name': 'Skummjölkspulver', 'g': 30}, {'name': 'Sötad kondenserad mjölk', 'g': 35},
        {'name': 'Strösocker', 'g': 74}, {'name': 'Atomiserad dextros', 'g': 22},
        {'name': 'Flytande äggula', 'g': 50}, {'name': 'Bladgelatin', 'g': 1.7},
        {'name': 'Citronskal (rivet, 3 citroner)', 'g': 6}, {'name': 'Lakritspulver (rå)', 'g': 10},
        {'name': 'Citronsaft (kall, sista)', 'g': 35}, {'name': 'Salt', 'g': 0.5},
    ]),
}

FRUIT_RECIPES = {'jordgubb', 'passion', 'applekanel'}
RICH_RECIPES = {'kokos'}

# TARGETS — speglar index.html TARGETS exakt
def cls(target, v, is_fruit=False, is_rich=False):
    if target == 'pac':
        if is_fruit:
            return 'bad' if v < 22 or v > 32 else 'ok'
        return 'bad' if v < 20 or v > 32 else 'ok' if 22 <= v <= 28 else 'warn'
    if target == 'pod':
        return 'bad' if v < 12 or v > 24 else 'ok' if 14 <= v <= 20 else 'warn'
    if target == 'fat':
        if is_rich:
            return 'ok' if 9 <= v <= 18 else 'bad' if v > 30 else 'warn'
        return 'ok' if 9 <= v <= 18 else 'bad' if v < 6 or v > 24 else 'warn'
    if target == 'msnf':
        return 'bad' if v < 6 or v > 14 else 'ok' if 8 <= v <= 12 else 'warn'
    if target == 'gelatin':
        return 'bad' if v > 3.5 else 'ok' if 1.5 <= v <= 3 else 'warn'

print(f"{'Recept':14} {'Total':>6} {'Fett':>14} {'MSNF':>14} {'Socker':>8} {'TS':>7} {'PAC':>16} {'POD':>14} {'Gel':>14}")
print('-' * 120)
bad_count = warn_count = 0
for name, (base, items) in RECIPES.items():
    s = compute(items, base)
    is_fruit = name in FRUIT_RECIPES
    is_rich = name in RICH_RECIPES
    pac_cls = cls('pac', s['pac'], is_fruit=is_fruit)
    pod_cls = cls('pod', s['pod'])
    fat_cls = cls('fat', s['fat'], is_rich=is_rich)
    msnf_cls = cls('msnf', s['msnf'])
    gel_cls = cls('gelatin', s['gel'])
    for c in [pac_cls, pod_cls, fat_cls, msnf_cls, gel_cls]:
        if c == 'bad': bad_count += 1
        elif c == 'warn': warn_count += 1
    print(f"{name:14} {base:>6} "
          f"{s['fat']:>5.1f}% [{fat_cls:4}]  "
          f"{s['msnf']:>5.1f}% [{msnf_cls:4}]  "
          f"{s['sugar']:>5.1f}% "
          f"{s['ts']:>5.1f}% "
          f"{s['pac']:>5.1f} [{pac_cls:4}{' F' if is_fruit else '  '}] "
          f"{s['pod']:>5.1f} [{pod_cls:4}]  "
          f"{s['gel']:>5.1f} [{gel_cls:4}]")
print()
n = len(RECIPES) * 5
print(f"TOTALT: {bad_count} BAD, {warn_count} warn (av {n} mätpunkter, {len(RECIPES)} recept)")
