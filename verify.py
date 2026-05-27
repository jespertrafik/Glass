"""Verifierar JS computeStats mot Python-implementation för alla 6 recept."""

PAC = {'sucrose': 100, 'dextrose': 190, 'fructose': 190, 'glucose_de42': 80, 'lactose': 100}
POD = {'sucrose': 100, 'dextrose': 70,  'fructose': 170, 'glucose_de42': 50, 'lactose': 16}

DB = {
    'Grädde 36%':                                {'fat': 0.36, 'msnf': 0.05,  'sugars': {}},
    'Mjölk 3%':                                  {'fat': 0.03, 'msnf': 0.088, 'sugars': {}},
    'Kaffemjölk (mjölk 3% + infusionerat kaffe)':{'fat': 0.03, 'msnf': 0.088, 'sugars': {}},
    'Skummjölkspulver':                          {'fat': 0,    'msnf': 0.96,  'sugars': {}},
    'Strösocker':                                {'fat': 0,    'msnf': 0,     'sugars': {'sucrose': 1.0}},
    'Strösocker (i basen)':                      {'fat': 0,    'msnf': 0,     'sugars': {'sucrose': 1.0}},
    'Glykossirap':                               {'fat': 0,    'msnf': 0,     'sugars': {'glucose_de42': 0.80}},
    'Glukossirap':                               {'fat': 0,    'msnf': 0,     'sugars': {'glucose_de42': 0.80}},
    'Flytande äggula':                           {'fat': 0.27, 'msnf': 0,     'sugars': {}},
    'Mörk choklad 70%':                          {'fat': 0.40, 'msnf': 0,     'sugars': {'sucrose': 0.30}},
    'Kakao (holländsk)':                         {'fat': 0.22, 'msnf': 0,     'sugars': {}},
    '+ Bär-koncentrat (kallt)':                  {'fat': 0,    'msnf': 0,     'sugars': {'fructose': 0.18}},
    'Passionsfruktspuré (reducerad, silad)':     {'fat': 0,    'msnf': 0,     'sugars': {'fructose': 0.11}},
    'Reducerad kokosmjölk (från ~500g)':         {'fat': 0.40, 'msnf': 0.04,  'sugars': {}},
    'Rostad kokosflakes (valfritt, sista 2 min)':{'fat': 0.65, 'msnf': 0,     'sugars': {}},
}

def props(name): return DB.get(name, {'fat': 0, 'msnf': 0, 'sugars': {}})

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

RECIPES = {
    'vanilj': (698, [
        {'name': 'Grädde 36%', 'g': 215},
        {'name': 'Mjölk 3%', 'g': 275},
        {'name': 'Skummjölkspulver', 'g': 30},
        {'name': 'Strösocker', 'g': 95},
        {'name': 'Glykossirap', 'g': 30},
        {'name': 'Flytande äggula', 'g': 50},
        {'name': 'Bladgelatin', 'g': 2.5},
        {'name': 'Vaniljextrakt (eller 2g vaniljpulver)', 'g': 10},
        {'name': 'Salt', 'g': 1},
    ]),
    'choklad': (701, [
        {'name': 'Grädde 36%', 'g': 150},
        {'name': 'Mjölk 3%', 'g': 285},
        {'name': 'Skummjölkspulver', 'g': 20},
        {'name': 'Mörk choklad 70%', 'g': 90},
        {'name': 'Kakao (holländsk)', 'g': 20},
        {'name': 'Strösocker', 'g': 65},
        {'name': 'Glykossirap', 'g': 30},
        {'name': 'Flytande äggula', 'g': 40},
        {'name': 'Bladgelatin', 'g': 2.5},
        {'name': 'Salt', 'g': 1},
    ]),
    'jordgubb': (701, [
        {'name': 'Grädde 36%', 'g': 155},
        {'name': 'Mjölk 3%', 'g': 170},
        {'name': 'Skummjölkspulver', 'g': 20},
        {'name': 'Strösocker (i basen)', 'g': 45},
        {'name': 'Glykossirap', 'g': 35},
        {'name': 'Flytande äggula', 'g': 30},
        {'name': 'Bladgelatin', 'g': 2.5},
        {'name': 'Salt', 'g': 1},
        {'name': '+ Bär-koncentrat (kallt)', 'g': 235},
    ]),
    'passion': (663, [
        {'name': 'Grädde 36%', 'g': 137.5},
        {'name': 'Mjölk 3%', 'g': 112.5},
        {'name': 'Passionsfruktspuré (reducerad, silad)', 'g': 250},
        {'name': 'Strösocker', 'g': 90},
        {'name': 'Flytande äggula', 'g': 60},
        {'name': 'Glukossirap', 'g': 12.5},
        {'name': 'Bladgelatin', 'g': 0.85},
    ]),
    'kokos': (663, [
        {'name': 'Grädde 36%', 'g': 137.5},
        {'name': 'Mjölk 3%', 'g': 112.5},
        {'name': 'Reducerad kokosmjölk (från ~500g)', 'g': 250},
        {'name': 'Strösocker', 'g': 90},
        {'name': 'Flytande äggula', 'g': 60},
        {'name': 'Glukossirap', 'g': 12.5},
        {'name': 'Bladgelatin', 'g': 2.5},
        {'name': 'Rostad kokosflakes (valfritt, sista 2 min)', 'g': 25},
    ]),
    'kaffe': (768, [
        {'name': 'Grädde 36%', 'g': 275},
        {'name': 'Kaffemjölk (mjölk 3% + infusionerat kaffe)', 'g': 225},
        {'name': 'Strösocker', 'g': 120},
        {'name': 'Flytande äggula', 'g': 120},
        {'name': 'Glykossirap', 'g': 25},
        {'name': 'Bladgelatin', 'g': 3.4},
        {'name': 'Mald kaffe (för infusion, filtreras bort)', 'g': 35, 'excludeFromBase': True},
    ]),
}

OLD = {
    'vanilj':   {'fat': 14.7, 'sugar': 17.8, 'msnf': 8.5,  'ts': 42,  'pac': 26},
    'choklad':  {'fat': 16.5, 'sugar': 16.4, 'msnf': 6,    'ts': 46,  'pac': 25},
    'jordgubb': {'fat': 10.1, 'sugar': 21.5, 'pac': 30,    'ts': 38},
    'passion':  {'fat': 11.0, 'sugar': 15.1, 'pac': 32},
    'kokos':    {'fat': 19,   'sugar': 15.1, 'pac': 17},
    'kaffe':    {'fat': 18.9, 'sugar': 18.2, 'msnf': 2.6,  'pac': 20},
}

def cls(target, v):
    bands = {
        'pac':     ('bad' if v < 20 or v > 32 else 'ok' if 22 <= v <= 28 else 'warn'),
        'pod':     ('bad' if v < 12 or v > 24 else 'ok' if 14 <= v <= 20 else 'warn'),
        'fat':     ('ok' if 6 <= v <= 12 else 'bad' if v > 20 else 'warn'),
        'msnf':    ('bad' if v < 6 or v > 14 else 'ok' if 8 <= v <= 12 else 'warn'),
        'gelatin': ('bad' if v > 3.5 else 'ok' if 1.5 <= v <= 3 else 'warn'),
    }
    return bands[target]

print(f"{'Recept':10} {'Fett':>10} {'MSNF':>10} {'Socker':>10} {'TS':>8} {'PAC':>10} {'POD':>10} {'Gel':>10}")
print('-' * 90)
for name, (base, items) in RECIPES.items():
    s = compute(items, base)
    old = OLD[name]
    diff_pac = f"(gml {old['pac']})" if 'pac' in old else ''
    diff_fat = f"(gml {old['fat']})" if 'fat' in old else ''
    print(f"{name:10} "
          f"{s['fat']:>5.1f}% [{cls('fat', s['fat']):4}] "
          f"{s['msnf']:>5.1f}% [{cls('msnf', s['msnf']):4}] "
          f"{s['sugar']:>5.1f}%      "
          f"{s['ts']:>5.1f}% "
          f"{s['pac']:>5.1f} [{cls('pac', s['pac']):4}] "
          f"{s['pod']:>5.1f} [{cls('pod', s['pod']):4}] "
          f"{s['gel']:>5.1f} [{cls('gelatin', s['gel']):4}]")
    print(f"{'  diff:':10} fett {s['fat']-old.get('fat', s['fat']):+.1f}  socker {s['sugar']-old.get('sugar', s['sugar']):+.1f}  pac {s['pac']-old.get('pac', s['pac']):+.1f}")
    print()
