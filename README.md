# Glasskalkylator

Premium custard-baserad glasskalkylator med italiensk PAC/POD-balansering, optimerad för Wilfa ICM-C15. Sex smaker som flikar, alla skalbara mot vald total-vikt, alla siffror räknas live från ingredienserna.

Live: https://glass.jespertrafik.com (efter GitHub Pages-setup)

## Vad det här är (och inte är)

Det här är **inte gelato** (fett 4–9%). Det är **premium custard-glass** i fransk stil (fett 14–25%) som använder **italienska balanseringsverktyg** (PAC, POD, MSNF, dextros) för att räkna ut sockerprofil och frystextur. Slutprodukten ligger närmare amerikansk premium ice cream än italiensk gelato — det är medvetet val.

## Flikar

- **Vanilj** — klassisk crème anglaise med MSNF, glykossirap, gelatin. Vaniljextrakt eller -pulver.
- **Choklad** — dubbel chokladkälla (70% choklad + holländsk kakao), 24h mognad.
- **Jordgubb** — bär-koncentrat-teknik (390g bär → 235g koncentrat) för smak utan iskristaller.
- **Passion** — reducerad puré silad från kärnor, kall inblandning efter mognad (citronsyran curdlar mjölk vid värme).
- **Kokos** — Aroy-D reducerad 500g→250g, valfri rostad kokosflakes via locket sista 2 min.
- **Kaffe** — kaffeinfusion i mjölken som filtreras, klassisk italiensk caffè-stil med hög äggula.

## Logik

- Default 700g bas → Wilfa C15 säker zon (~47% fyllnad efter +20–30% overrun)
- Wilfa-zon-check: varnar under 400g, över 850g (spill/stall-risk), flaggar sweet spot 600–750g
- Volym-skalning: ange total bas-vikt → alla ingredienser skalas proportionellt
- **Auto-räknade stats live från ingredienserna** (Fett %, Socker %, MSNF %, TS %, PAC, POD, Gelatin g/kg) — färgkodade mot target-zoner (grön=ok, gul=varning, röd=utanför)
- PAC/POD-konvention: modern (Underbelly/Goff) som inkluderar laktos
- Tekniska skillnader inbakade i stegen per smak: 83°C (flytande äggula), kakao värms separat, passion KALL i KALL, kokos kan värmas (ingen syra), kaffe-infusion + filtrering

## Target-zoner

| Mått | Target | Källa |
|---|---|---|
| PAC | 22–28 (frukt 28–32) | Italiensk balanseringsregel — gäller även custard-glass |
| POD | 18–22 (under 16 = "platt", över 24 = för sött) | — |
| MSNF | 8–12% | Italiensk balanseringsregel |
| Fett | 12–18% | Fransk-amerikansk premium ice cream-stil |
| Gelatin | 1.5–3 g/kg | Över 3.5 = gummikänsla |

## Tekniska val

- **Flytande äggula** (pastöriserad) — säker vid 83°C
- **Sucrose + glykossirap (42 DE)** — PAC-balansering för mjuk skopbar konsistens vid -18°C
- **Skummjölkspulver** — MSNF-höjning till 8–11%
- **Bladgelatin** — 1.7g/blad (svenskt), 2–3 g/kg target (frukt med naturlig syra/pektin tål mindre)
- **Mognad** 12h standard, 24h på choklad

## Filer

- `index.html` — kalkylatorn, självförsörjande
- `verify.py` — Python-implementation av computeStats för att verifiera räkningar efter recept-ändringar (`py verify.py`)
- `CNAME` — domän för GitHub Pages

## Stack
Statisk HTML, hostas på GitHub Pages, DNS via Cloudflare.

## Att göra
- [ ] Skapa GitHub-repo `jespertrafik/glass`
- [ ] Push initial commit
- [ ] Aktivera GitHub Pages (main branch, root)
- [ ] CNAME i Cloudflare: `glass` → `jespertrafik.github.io`
