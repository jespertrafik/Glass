# Speglar computeStats() i index.html exakt. Anvands for att kalibrera socker+dextros.
PAC = {'sucrose':100,'dextrose':190,'fructose':190,'glucose_de42':80,'lactose':100}
POD = {'sucrose':100,'dextrose':70, 'fructose':170,'glucose_de42':50,'lactose':16}

DB = {
 'Gradde 36%': dict(fat=.36, msnf=.05),
 'Mjolk 3%': dict(fat=.03, msnf=.088),
 'Kaffemjolk': dict(fat=.03, msnf=.088),
 'SMP': dict(fat=0, msnf=.96),
 'Strosocker': dict(sugars={'sucrose':1.0}),
 'Dextros': dict(sugars={'dextrose':1.0}),
 'Honung': dict(sugars={'fructose':.38,'glucose_de42':.31}),
 'Aggula': dict(fat=.27),
 'Choklad70': dict(fat=.40, sugars={'sucrose':.30}),
 'Kakao': dict(fat=.22),
 'Barkonc': dict(sugars={'fructose':.18}),
 'Passion': dict(sugars={'fructose':.22}),
 'Kokoskonc': dict(fat=.40, msnf=.04),
 'Kokosflakes': dict(fat=.65),
}

def stats(items, total):
    fatG=msnfG=gelG=0
    sug={'sucrose':0,'dextrose':0,'fructose':0,'glucose_de42':0,'lactose':0}
    for name,g,*rest in items:
        ex = rest and rest[0]=='ex'
        if ex: continue
        d=DB.get(name,{})
        fatG+=g*d.get('fat',0); msnfG+=g*d.get('msnf',0)
        sug['lactose']+=g*d.get('msnf',0)*0.54
        for t,fr in d.get('sugars',{}).items():
            if t=='lactose': continue
            sug[t]+=g*fr
        if name=='Gelatin': gelG+=g
    added=sug['sucrose']+sug['dextrose']+sug['fructose']+sug['glucose_de42']
    tot=added+sug['lactose']
    pac=sum(sug[t]*PAC[t] for t in sug)/total
    pod=sum(sug[t]*POD[t] for t in sug)/total
    return dict(fat=fatG/total*100, msnf=msnfG/total*100, sugar=tot/total*100,
                pac=pac, pod=pod)

def zone_pac(v,fruit=False):
    if fruit: return 'ok' if 22<=v<=32 else 'BAD'
    return 'BAD' if v<20 or v>32 else ('ok' if 22<=v<=28 else 'warn')
def zone_pod(v):
    return 'BAD' if v<12 or v>24 else ('ok' if 14<=v<=20 else 'warn')

def show(label, items, total, fruit=False):
    s=stats(items,total)
    print(f"\n{label} (bas {total}g)")
    print(f"  fat {s['fat']:.1f}%  msnf {s['msnf']:.1f}%  sugar {s['sugar']:.1f}%")
    print(f"  PAC {s['pac']:.1f} [{zone_pac(s['pac'],fruit)}]  POD {s['pod']:.1f} [{zone_pod(s['pod'])}]")
    return s

# ---- KANDIDATER: socker + dextros, ingen glukossirap, ingen honung ----
# Vanilj: ersatt 30g glukossirap. Behall PAC ~21, POD ~16.
show('VANILJ', [('Gradde 36%',215),('Mjolk 3%',275),('SMP',30),
    ('Strosocker',80),('Dextros',22),('Aggula',50),('Gelatin',1.7)], 698)

# Choklad: ta bort 20g honung + 30g glukossirap, ersatt med sucrose+dextros
show('CHOKLAD', [('Gradde 36%',150),('Mjolk 3%',285),('SMP',20),('Choklad70',90),
    ('Kakao',20),('Strosocker',52),('Dextros',30),('Aggula',40),('Gelatin',1.7)], 706)

# Jordgubb: ersatt 35g glukossirap. fruit-target.
show('JORDGUBB', [('Gradde 36%',155),('Mjolk 3%',170),('SMP',30),('Strosocker',45),
    ('Dextros',22),('Aggula',30),('Gelatin',1.7),('Barkonc',235)], 711, fruit=True)

# Passion: ersatt 12.5g glukossirap. fruit-target. Sankt socker for POD ur warn.
show('PASSION', [('Gradde 36%',137.5),('Mjolk 3%',112.5),('SMP',20),('Passion',125),
    ('Strosocker',48),('Dextros',14),('Aggula',60),('Gelatin',1.7)], 539, fruit=True)

# Kokos: dextros-fix pa riktigt nu. Lyfter PAC ur BAD.
show('KOKOS', [('Gradde 36%',137.5),('Mjolk 3%',112.5),('SMP',15),('Kokoskonc',180),
    ('Strosocker',70),('Dextros',38),('Aggula',60),('Gelatin',1.7),('Kokosflakes',25)], 608)

# Kaffe: ersatt 23g glukossirap.
show('KAFFE', [('Gradde 36%',251),('Kaffemjolk',205),('SMP',15),('Strosocker',95),
    ('Dextros',23),('Aggula',110),('Gelatin',1.7)], 715)
