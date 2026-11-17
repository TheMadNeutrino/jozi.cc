# Jozi — osobní web

Statický vícestránkový web v češtině a angličtině. Sytá žlutá `#ffda00`, černá `#111210`, vlastní SVG ilustrace, responzivní layout. Bez frameworku, externích fontů, cookies a závislostí. Hotové HTML funguje i bez JavaScriptu; JavaScript přidává mobilní menu a filtry.

## Rychlý náhled

Otevři `dist/index.html` v prohlížeči. Není potřeba nic instalovat. Všechny odkazy jsou relativní, takže web funguje i pod adresou `uzivatel.github.io/nazev-repozitare/`.

Pro místní server můžeš v kořenové složce spustit:

```sh
python -m http.server 8000 --directory dist
```

Potom otevři `http://localhost:8000`.

## Nasazení na GitHub Pages (automatické)

1. Vytvoř repozitář na GitHubu s výchozí větví `main`.
2. Nahraj do jeho kořene **obsah složky `jozi-portfolio`**, včetně `.github/workflows/pages.yml`. Nenahrávej ZIP jako jediný soubor a nevkládej projekt do další podsložky. Pozor: některé správce souborů skryté složky nezobrazují.
3. V repozitáři otevři **Settings → Pages → Build and deployment → Source: GitHub Actions**.
4. V záložce **Actions** spusť workflow **Build and deploy to GitHub Pages** přes **Run workflow**, nebo odešli nový commit do `main`.
5. Po úspěšném běhu bude adresa v **Settings → Pages** a u prostředí `github-pages`.

Workflow spustí `python build.py` a nahraje pouze výstup `dist/`. Na hostingu běží jen HTML, CSS, JavaScript a SVG. Python se používá při sestavení, nikoli na serveru.

Alternativa bez Actions: vlož přímo obsah `dist/` do kořene publikační větve a v Pages zvol nasazení z této větve, složka `/ (root)`. V tomto režimu musíš po úpravě obsahu sestavit web lokálně a nahrát nový výstup.

## Kde upravovat obsah

- `content.json`: jméno, město, bio, e-mail, sociální profily a všechny projekty.
- `build.py`: společné texty a šablony stránek. Překlady rozhraní jsou ve slovníku `T`.
- `assets/style.css`: barvy, typografie, rozložení.
- `assets/app.js`: mobilní menu a filtry projektů.
- `assets/favicon.svg`: ikonka v záložce.
- `dist/`: automaticky generovaný výstup. Neupravuj ho ručně — při příštím sestavení se přepíše.

Jméno Jozi a popisy projektů jsou výchozí návrh podle dodaného kontextu. Před publikací zkontroluj aktuálnost a formulace. Kontakty jsou záměrně prázdné, žádné falešné adresy. Po doplnění `email`, `github` a/nebo `instagram` se kontaktní odkazy zobrazí automaticky. Prázdné položky se nezobrazují. Fotky ani analytika nejsou součástí webu.

Po změně obsahu:

```sh
python build.py
```

Na Windows lze použít také `py build.py`. Stačí Python 3; žádné balíčky se neinstalují. Při použití přiložených Actions stačí změnit `content.json` přímo na GitHubu a uložit commit — sestavení i nasazení proběhnou automaticky.

## Jak přidat projekt

Zkopíruj jednu položku v seznamu `projects` v `content.json`, vlož ji jako další položku a uprav hodnoty. Nezapomeň na čárku mezi položkami JSON. Nejjednodušší je kopírovat celý existující projekt.

Příklad položky:

```json
{
  "slug": "novy-projekt",
  "number": "04",
  "visual": "pad",
  "category": "electronics",
  "featured": true,
  "title": {"cs": "Nový projekt", "en": "New project"},
  "label": {"cs": "Osobní projekt", "en": "Personal project"},
  "summary": {"cs": "Krátký popis projektu.", "en": "A short project description."},
  "role": {"cs": "Návrh a realizace", "en": "Design and implementation"},
  "tags": ["Hardware", "Python"],
  "paragraphs": {
    "cs": ["První odstavec detailu.", "Druhý odstavec detailu."],
    "en": ["First detail paragraph.", "Second detail paragraph."]
  },
  "link": ""
}
```

| Položka | Význam |
| --- | --- |
| `slug` | Jedinečná část adresy; malá písmena bez diakritiky, číslice a pomlčky. Po zveřejnění ji raději neměň, aby zůstaly funkční sdílené odkazy. |
| `number` | Pořadové číslo zobrazené na kartě. |
| `visual` | Ilustrace: `car`, `pad` nebo `nano`. Vlastní kresby můžeš přidat do funkce `art()` v `build.py`. |
| `category` | Jedna z kategorií `engineering`, `electronics`, `science`. |
| `featured` | `true` zobrazí projekt i na úvodu, `false` pouze v přehledu. |
| `title`, `label`, `summary`, `role` | Česká a anglická varianta textu. |
| `tags` | Libovolný počet krátkých štítků. Mohou být přirozeně v angličtině v obou verzích. |
| `paragraphs` | Odstavce detailní stránky v obou jazycích. |
| `link` | Volitelný odkaz na repozitář nebo živý projekt, celý včetně `https://`. |

Po sestavení automaticky vznikne karta, detail `/projects/novy-projekt/index.html` a jeho anglická varianta. Pořadí projektů odpovídá pořadí v JSON. V HTML obsahu se automaticky escapují speciální znaky; do textů v JSON vkládej obyčejný text.

## Stránky a jazyk

- Čeština: `index.html`, `about.html`, `projects.html`, `contact.html`.
- Angličtina: stejné soubory ve složce `en/`.
- Každý projekt má vlastní adresu v obou jazycích.
- Přepínač zachovává otevřenou stránku/projekt. Výchozí adresa zůstává česká; anglickou verzi lze sdílet přímo přes `/en/`.
- Navigace funguje bez JavaScriptu. Na úzké obrazovce se otevírá tlačítkem Menu (JavaScript).

## Ověření

Zkontrolováno: sestavení 15 HTML stránek, místní cíle odkazů a assetů, přepínání jazyků z přehledu i detailu, filtr elektroniky a vizuální kontrola desktopového úvodu. Mobilní rozložení je připravené pomocí CSS breakpointů; samostatná vizuální kontrola na fyzickém telefonu nebyla provedena. Skutečné nasazení na GitHub Pages nebylo provedeno, protože nebyl dodán cílový repozitář.
