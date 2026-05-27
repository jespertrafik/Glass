"""Verifierar JS computeStats mot Python-implementation. Speglar index.html INGREDIENT_DB + RECIPES.

Kör efter recept-ändringar för att bekräfta att JS-värdena matchar förväntat. Mål: 0 BAD.
"""

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
    # NY: honung (38% fruktos + 31% glukos + 17% vatten + 14% övrigt)
    'Honung':                                    {'fat': 0,    'msnf': 0,     'sugars': {'fructose': 0.38, 'glucose_de42': 0.31}},
    'Flytande äggula':                           {'fat': 0.27, 'msnf': 0,     'sugars': {}},
    'Mörk choklad 70%':                          {'fat': 0.40, 'msnf': 0,     'sugars': {'sucrose': 0.30}},
    'Kakao (holländsk)':                         {'fat': 0.22, 'msnf': 0,     'sugars': {}},
    '+ Bär-koncentrat (kallt)':                  {'fat': 0,    'msnf': 0,     'sugars': {'fructose': 0.18}},
    # ÄNDRAD: passion-puré nu från 250g→125g, dubblad sockerkoncentration
    'Passionsfruktspuré (reducerad, silad)':     {'fat': 0,    'msnf': 0,     'sugars': {'fructose': 0.22}},
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

# PREVIEW-RECEPT (efter alla planerade fixar)
RECIPES = {
    'vanilj': (698, [   # oförändrad förutom gelatin 2.5 → 1.7 (gjordes redan)
        {'name': 'Grädde 36%', 'g': 215},
        {'name': 'Mjölk 3%', 'g': 275},
        {'name': 'Skummjölkspulver', 'g': 30},
        {'name': 'Strösocker', 'g': 95},
        {'name': 'Glykossirap', 'g': 30},
        {'name': 'Flytande äggula', 'g': 50},
        {'name': 'Bladgelatin', 'g': 1.7},  # NY
        {'name': 'Vaniljextrakt (eller 2g vaniljpulver)', 'g': 10},
        {'name': 'Salt', 'g': 1},
    ]),
    'choklad': (706, [  # -15g sucrose, +20g honung, total +5g
        {'name': 'Grädde 36%', 'g': 150},
        {'name': 'Mjölk 3%', 'g': 285},
        {'name': 'Skummjölkspulver', 'g': 20},
        {'name': 'Mörk choklad 70%', 'g': 90},
        {'name': 'Kakao (holländsk)', 'g': 20},
        {'name': 'Strösocker', 'g': 50},   # NY (var 65)
        {'name': 'Honung', 'g': 20},        # NY (var 0)
        {'name': 'Glykossirap', 'g': 30},
        {'name': 'Flytande äggula', 'g': 40},
        {'name': 'Bladgelatin', 'g': 1.7},  # NY (var 2.5)
        {'name': 'Salt', 'g': 1},
    ]),
    'jordgubb': (711, [  # +10g SMP, total +10
        {'name': 'Grädde 36%', 'g': 155},
        {'name': 'Mjölk 3%', 'g': 170},
        {'name': 'Skummjölkspulver', 'g': 30},  # NY (var 20)
        {'name': 'Strösocker (i basen)', 'g': 45},
        {'name': 'Glykossirap', 'g': 35},
        {'name': 'Flytande äggula', 'g': 30},
        {'name': 'Bladgelatin', 'g': 1.7},      # NY (var 2.5)
        {'name': 'Salt', 'g': 1},
        {'name': '+ Bär-koncentrat (kallt)', 'g': 235},
    ]),
    'passion': (500, [  # rebalanserad till exakt 500g bas (1 paket → 500g)
        {'name': 'Grädde 36%', 'g': 125},
        {'name': 'Mjölk 3%', 'g': 100},
        {'name': 'Skummjölkspulver', 'g': 18},
        {'name': 'Passionsfruktspuré (reducerad, silad)', 'g': 125},
        {'name': 'Strösocker', 'g': 65},
        {'name': 'Flytande äggula', 'g': 55},
        {'name': 'Glukossirap', 'g': 11},
        {'name': 'Bladgelatin', 'g': 1.7},
    ]),
    'kokos': (608, [    # +15g SMP, kokosmjölk 250→180
        {'name': 'Grädde 36%', 'g': 137.5},
        {'name': 'Mjölk 3%', 'g': 112.5},
        {'name': 'Skummjölkspulver', 'g': 15},   # NY (var 0)
        {'name': 'Reducerad kokosmjölk (från ~500g)', 'g': 180},  # NY (var 250)
        {'name': 'Strösocker', 'g': 90},
        {'name': 'Flytande äggula', 'g': 60},
        {'name': 'Glukossirap', 'g': 12.5},
        {'name': 'Bladgelatin', 'g': 1.7},       # NY (var 2.5)
        {'name': 'Rostad kokosflakes (valfritt, sista 2 min)', 'g': 25},
    ]),
    'kaffe': (715, [    # skalat 768→700 + 15g SMP (regular-milk-fix räcker inte mot MSNF-BAD)
        {'name': 'Grädde 36%', 'g': 251},
        {'name': 'Kaffemjölk (mjölk 3% + infusionerat kaffe)', 'g': 205},
        {'name': 'Skummjölkspulver', 'g': 15},   # NY (fallback eftersom +30g mjölk inte nådde green)
        {'name': 'Strösocker', 'g': 110},
        {'name': 'Flytande äggula', 'g': 110},
        {'name': 'Glykossirap', 'g': 23},
        {'name': 'Bladgelatin', 'g': 1.7},       # NY (var 3.4)
        {'name': 'Mald kaffe (för infusion, filtreras bort)', 'g': 32, 'excludeFromBase': True},
    ]),
}

def cls(target, v, is_fruit=False, is_rich=False):
    if target == 'pac':
        if is_fruit:
            return 'bad' if v < 22 or v > 32 else 'ok'
        return 'bad' if v < 20 or v > 32 else 'ok' if 22 <= v <= 28 else 'warn'
    if target == 'fat':
        if is_rich:
            return 'ok' if 6 <= v <= 12 else 'bad' if v > 30 else 'warn'
        return 'ok' if 6 <= v <= 12 else 'bad' if v > 20 else 'warn'
    bands = {
        'pod':     ('bad' if v < 12 or v > 24 else 'ok' if 14 <= v <= 20 else 'warn'),
        'msnf':    ('bad' if v < 6 or v > 14 else 'ok' if 8 <= v <= 12 else 'warn'),
        'gelatin': ('bad' if v > 3.5 else 'ok' if 1.5 <= v <= 3 else 'warn'),
    }
    return bands[target]

FRUIT_RECIPES = {'jordgubb', 'passion'}
RICH_RECIPES = {'kokos'}

print(f"{'Recept':10} {'Total':>6} {'Fett':>14} {'MSNF':>14} {'Socker':>8} {'TS':>8} {'PAC':>14} {'POD':>14} {'Gel':>14}")
print('-' * 110)
bad_count = 0
warn_count = 0
for name, (base, items) in RECIPES.items():
    s = compute(items, base)
    is_fruit = name in FRUIT_RECIPES
    is_rich = name in RICH_RECIPES
    pac_cls = cls('pac', s['pac'], is_fruit)
    pod_cls = cls('pod', s['pod'])
    fat_cls = cls('fat', s['fat'], is_rich=is_rich)
    msnf_cls = cls('msnf', s['msnf'])
    gel_cls = cls('gelatin', s['gel'])
    for c in [pac_cls, pod_cls, fat_cls, msnf_cls, gel_cls]:
        if c == 'bad': bad_count += 1
        elif c == 'warn': warn_count += 1
    print(f"{name:10} {base:>6} "
          f"{s['fat']:>5.1f}% [{fat_cls:4}]  "
          f"{s['msnf']:>5.1f}% [{msnf_cls:4}]  "
          f"{s['sugar']:>5.1f}% "
          f"{s['ts']:>5.1f}% "
          f"{s['pac']:>5.1f} [{pac_cls:4}{' F' if is_fruit else '  '}] "
          f"{s['pod']:>5.1f} [{pod_cls:4}]  "
          f"{s['gel']:>5.1f} [{gel_cls:4}]")
print()
print(f"TOTALT: {bad_count} BAD, {warn_count} warn (av 30 mätpunkter)")
