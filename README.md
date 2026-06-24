# Glasskalkylator

Premium custard-baserad glasskalkylator med italiensk PAC/POD-balansering, optimerad för Wilfa ICM-C15. Femton smaker som flikar — alla nyckeltal räknas live från ingredienserna och färgkodas mot target-zoner.

Live: https://glass.jespertrafik.com

## Vad det här är (och inte är)

Det här är **inte gelato** (fett 4–9%). Det är **premium custard-glass** i fransk stil (fett 12–18%) som använder **italienska balanseringsverktyg** (PAC, POD, MSNF, dextros) för att räkna ut sockerprofil och frystextur. Slutprodukten ligger närmare amerikansk premium ice cream än italiensk gelato — det är medvetet val.

## Smaker (flikar)

| Smak | Bas | Target | Notering |
|---|---|---|---|
| **Vanilj** | 698 g | standard | Klassisk crème anglaise, vaniljextrakt eller -pulver. Mild profil (salt 0,7 g, dämpad sötma) |
| **Choklad** | 706 g | standard | Dubbel chokladkälla (70% choklad + holländsk kakao), 24h mognad |
| **Jordgubb** | 711 g | frukt-PAC | Bär-koncentrat-teknik (390→235 g), kall inblandning |
| **Passion** | 571 g | frukt-PAC | Reducerad puré 125 g (kall inblandning) + sötad kondenserad mjölk för tät, len "wow"-kropp (MSNF-lyft) |
| **Kokos** | 608 g | rich-fat | Reducerad kokosmjölk 500→180 g, valfri rostad kokos |
| **Kaffe** | 715 g | standard | Mjölk-kaffe-infusion (filtreras), hög äggula ~15% italiensk caffè-stil |
| **Salt lakrits** | 691 g | standard | Rå lakritspulver + flingsalt |
| **Rostad vit choklad & kardemumma** | 647 g | standard | Rostad vit choklad + mald kardemumma |
| **Pistage** | 686 g | standard | 100% pistagepasta |
| **Earl Grey** | 680 g | standard | Earl Grey-te infuseras i basen (filtreras bort) |
| **Matcha** | 684 g | standard | Ceremoniell matcha |
| **Rom & russin** | 693 g | standard | Mörk rom + rom-russin (sista 2 min) |
| **Saffran** | 675 g | standard | Saffran i vaniljbas |
| **Äpple & kanel** | 674 g | frukt-PAC | Äppelkompott (kall inblandning) + mald kanel |
| **Citron & sötlakrits** | 695 g | standard | Citronskal + lakritspulver + kall citronsaft sist |

## Logik

- **Auto-räknade stats live från ingredienserna:** Fett %, Socker %, MSNF %, TS %, PAC, POD, Gelatin g/kg
- **Färgkodning** mot target-zoner: grön (ok) / gul (warn) / röd (bad)
- **Volym-skalning:** ange total bas-vikt → alla ingredienser skalas proportionellt
- **Wilfa-zon-check:** varnar under 400 g, över 850 g (spill/stall-risk), flaggar sweet spot 600–750 g
- **Bladgelatin** visas både som antal blad (primärt) och gram (referens) — 1 blad = 1.7 g
- **Exkludering av filtrerade ingredienser** (t.ex. kaffegrums/te som filtreras bort räknas inte i basvikten)
- **PAC/POD-konvention:** modern (Underbelly/Goff) som inkluderar laktos

## Target-zoner

| Mått | ok | warn | bad |
|---|---|---|---|
| PAC (standard) | 22–28 | 20–22, 28–32 | <20, >32 |
| PAC (frukt) | 22–32 | — | <22, >32 |
| POD | 14–20 | 12–14, 20–24 | <12, >24 |
| Fett (standard) | 9–18 | 6–9, 18–24 | <6, >24 |
| Fett (rich) | 9–18 | 18–30 | >30 |
| MSNF | 8–12 | 6–8, 12–14 | <6, >14 |
| Gelatin (g/kg) | 1.5–3 | <1.5, 3–3.5 | >3.5 |

Frukt-variant (jordgubb, passion, äpple & kanel): högre PAC OK eftersom fruktvattnet behöver mer antifrys.
Rich-variant (kokos): honest labeling — fett-rik glass är medvetet val, tål upp till 30% fett innan bad.

## Tekniska val

- **Flytande äggula** (pastöriserad) — säker vid 83°C
- **Strösocker + atomiserad dextros** (PAC 190, POD 70) — höjer antifrys utan extra sötma. Glukossirap och honung är utfasade ur alla recept (finns kvar i ingrediens-DB:n bara för bakåtkompatibilitet)
- **Skummjölkspulver** — MSNF-höjning till 8–12%
- **Sötad kondenserad mjölk** (passion) — ~45% socker + ~21% MSNF + ~8% fett. Lyfter MSNF för tät, len kropp; strösocker sänks i gengäld så sötman hålls konstant
- **Bladgelatin** — 1 blad (1.7 g) per ~700 g batch (~2.4 g/kg)
- **Mognad** 12h standard, 24h på choklad

## Filer

- `index.html` — kalkylatorn, självförsörjande (presets, ingrediens-DB, computeStats, target-zoner)
- `verify.py` — Python-implementation av computeStats för verifiering efter recept-ändringar (`py verify.py`)
- `rebalance.py` — speglar kalkylatorns `computeStats()` för att räkna om nyckeltal vid recept-justeringar (`py rebalance.py`)
- `CNAME` — domän för GitHub Pages

## Stack
Statisk HTML, hostas på GitHub Pages, DNS via Cloudflare.
