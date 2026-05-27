# Glasskalkylator

Premium custard-baserad glasskalkylator med italiensk PAC/POD-balansering, optimerad för Wilfa ICM-C15. Sex smaker som flikar — alla nyckeltal räknas live från ingredienserna och färgkodas mot target-zoner.

Live: https://glass.jespertrafik.com

## Vad det här är (och inte är)

Det här är **inte gelato** (fett 4–9%). Det är **premium custard-glass** i fransk stil (fett 12–20%) som använder **italienska balanseringsverktyg** (PAC, POD, MSNF, dextros) för att räkna ut sockerprofil och frystextur. Slutprodukten ligger närmare amerikansk premium ice cream än italiensk gelato — det är medvetet val.

## Flikar (alla recept gelato-mässigt balanserade)

| Smak | Bas | Notering |
|---|---|---|
| **Vanilj** | 698 g | Klassisk crème anglaise, vaniljextrakt eller -pulver |
| **Choklad** | 706 g | Dubbel chokladkälla (70% choklad + holländsk kakao), 24h mognad. Honung som PAC-booster tills dextros köps in |
| **Jordgubb** | 711 g | Bär-koncentrat-teknik (390→235g), fruit-PAC-target |
| **Passion** | 539 g | Reducerad puré 125g (från ~400g fryst), kall inblandning efter mognad, fruit-PAC-target |
| **Kokos** | 608 g | Aroy-D reducerad 500→180g, valfri rostad kokos, rich-fat-target. PAC kvar BAD tills dextros köps |
| **Kaffe** | 715 g | Mjölk-kaffe-infusion (filtreras), hög äggula 15% italiensk caffè-stil |

## Logik

- **Auto-räknade stats live från ingredienserna:** Fett %, Socker %, MSNF %, TS %, PAC, POD, Gelatin g/kg
- **Färgkodning** mot target-zoner: grön (ok) / gul (warn) / röd (bad)
- **Volym-skalning:** ange total bas-vikt → alla ingredienser skalas proportionellt
- **Wilfa-zon-check:** varnar under 400g, över 850g (spill/stall-risk), flaggar sweet spot 600–750g
- **Bladgelatin** visas både som antal blad (primärt) och gram (referens) — 1 blad = 1.7g
- **Excludion av filtrerade ingredienser** (t.ex. kaffegrums som filtreras bort räknas inte i basvikten)
- **PAC/POD-konvention:** modern (Underbelly/Goff) som inkluderar laktos

## Target-zoner

| Mått | Standard | Frukt-variant | Rich-variant |
|---|---|---|---|
| PAC | 22–28 ok, 28–32 warn | 22–32 ok | — |
| POD | 14–20 ok, 20–24 warn | — | — |
| Fett | 6–12 ok, 12–18 warn, >20 BAD | — | 6–12 ok, 12–30 warn, >30 BAD |
| MSNF | 8–12 ok, 6–8 warn | — | — |
| Gelatin | 1.5–3 g/kg ok, >3.5 BAD | — | — |

Frukt-variant (jordgubb, passion): högre PAC OK eftersom fruktvattnet behöver mer antifrys.
Rich-variant (kokos): honest labeling — fett-rik glass är medvetet val, inte BAD.

## Tekniska val

- **Flytande äggula** (pastöriserad) — säker vid 83°C
- **Sucrose + glykossirap (42 DE)** — PAC-balansering. Atomiserad dextros (PAC 190) köps separat för fixar
- **Honung** — temporär PAC-booster i choklad tills dextros köps in (PAC ~130 effektivt)
- **Skummjölkspulver** — MSNF-höjning till 8–11%
- **Bladgelatin** — 1 blad (1.7g) per 700g batch (~2.4 g/kg)
- **Mognad** 12h standard, 24h på choklad

## Filer

- `index.html` — kalkylatorn, självförsörjande
- `verify.py` — Python-implementation av computeStats för verifiering efter recept-ändringar (`py verify.py`)
- `CNAME` — domän för GitHub Pages

## Stack
Statisk HTML, hostas på GitHub Pages, DNS via Cloudflare.
