# Glasskalkylator

Gelato-nivå glasskalkylator kalibrerad för Wilfa ICM-C15. Fem smaker som flikar, alla skalbara mot vald total-vikt.

Live: https://glass.jespertrafik.com (efter GitHub Pages-setup)

## Flikar

- **Vanilj** — klassisk crème anglaise med MSNF, dextros, 1.5 bladgelatin. 700g default.
- **Choklad** — dubbel chokladkälla (70% choklad + holländsk kakao), 24h mognad.
- **Jordgubb** — bär-koncentrat-teknik (390g bär → 235g koncentrat) för smak utan iskristaller.
- **Passion** — Jespers eget recept, reducerad passion silad från kärnor, kall inblandning efter mognad (citronsyran curdlar mjölk vid värme).
- **Kokos** — Aroy-D reducerad 500g→250g, valfri rostad kokosflakes via locket sista 2 min.

## Logik

- Alla recept default 700g bas → Wilfa C15 säker zon (~47% fyllnad efter +20–30% overrun)
- Wilfa-zon-check: varnar under 400g, över 850g (spill/stall-risk), och flaggar sweet spot 600–750g
- Volym-skalning: ange total bas-vikt → alla ingredienser skalas proportionellt (gelatin med 0.1g precision, vaniljstång till halv-steg, övrigt till hel/avrundat-5g)
- Stats per recept: fett %, socker %, MSNF %, TS %, PAC, mognadstid, tempering-temp, Wilfa-tid
- Tekniska skillnader inbakade i stegen: 83°C (P-äggula), kakao värms separat, passion KALL i KALL, kokos kan värmas (ingen syra)

## Tekniska val

- **P-äggula** (pastöriserad flytande) — säker vid 83°C
- **Dextros + socker** — PAC-balansering för mjuk skopbar konsistens vid -18°C
- **Skummjölkspulver** — MSNF-höjning till gelato-zon 8–11%
- **Bladgelatin** — 1.7g/blad (svenskt), 2–3 g/kg target (frukt med naturlig syra/pektin tål mindre)
- **Mognad** 12h standard, 24h på choklad

## Stack
Statisk HTML, hostas på GitHub Pages, DNS via Cloudflare.

## Att göra
- [ ] Skapa GitHub-repo `jespertrafik/glass`
- [ ] Push initial commit
- [ ] Aktivera GitHub Pages (main branch, root)
- [ ] CNAME i Cloudflare: `glass` → `jespertrafik.github.io`
- [ ] Eventuellt lägg till kaffe-flik när receptet bollats
