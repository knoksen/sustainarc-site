{
 "slug": "lca-ready-bim-tek17-climate-account-checks",
 "title": "Seven Checks Before Your BIM Model Becomes a TEK17 Climate Account",
 "seo_title": "LCA-Ready BIM: Seven Checks Before a TEK17 Climate Account",
 "description": "A BIM model is not a climate account. Seven practical checks on scope, layers, thin materials, reinforcement, rounding, simplified objects and data sources before TEK17 §17-1 reporting.",
 "dek": "Most Norwegian climate accounts start as a quantity export from a BIM model. That export is where many of the errors are made, and they matter more once limit values arrive.",
 "date": "2026-11-15",
 "updated": "2026-11-15",
 "minutes": 9,
 "tags": [
  "BIM",
  "LCA",
  "TEK17",
  "Climate account",
  "Revit"
 ],
 "image": "lca-ready-bim",
 "image_alt": "Illustration of a layered wall build-up linked by lines to quantities in a climate account table",
 "no_title": "Sju kontroller før BIM-modellen blir et klimagassregnskap etter TEK17",
 "no_summary": "TEK17 § 17-1 krever klimagassregnskap for boligblokker og yrkesbygg etter NS 3720, og de fleste regnskap starter som et mengdeuttrekk fra BIM-modellen. En internasjonal sammenligning fra 2025 fant manglende materialer i 55 tilfeller og avvik opp mot en faktor 10 i slike uttrekk. Artikkelen går gjennom sju kontroller: omfang etter NS 3451, sjiktvise materialer, tynne sjikt, armering, enheter og avrunding, forenklede objekter og valg av EPD-data. Direktoratet for byggkvalitet har foreslått grenseverdier (f.eks. 354 kg CO2-ekv./m² BTA for boligblokk); forslaget var på høring til 5. mai 2026, og vi har ikke funnet vedtak per november 2026.",
 "no_dek": "Sju konkrete kontroller før mengdene fra BIM-modellen brukes i klimagassregnskapet etter TEK17."
}
---
A climate account under TEK17 is a calculation about materials. In practice, most of those materials are first counted by a BIM model. The account can only be as good as the quantity export that feeds it, and that export is usually the least documented step in the whole chain.

This article sets out seven checks we apply before a model's quantities are allowed into a climate account. None of them needs special software. All of them can be written into an information requirement and tested.

## What the regulation asks for today

TEK17 § 17-1 requires a climate gas account for new apartment blocks and non-residential buildings, and for major rebuilds of them. The account follows the method in NS 3720:2018 and must cover at least modules A1–A4, B2 and B4, plus waste from the construction site. The building parts are listed by NS 3451 code: piled and direct foundations (215 and 216), structural systems (22), external walls (23), internal walls (24), floors (25) and roofs (26) [1].

The guidance adds three points that matter for modelling. The account is documented for the finished building, not just the design. Biogenic carbon, for example in timber, is not included. And where no product-specific EPD exists, generic values from a national database may be used with a 25 % surcharge, unless the data source already includes one. The calculation period is 50 years [1]. The requirement came into force on 1 July 2022, with a one-year transition [7].

## Why the quantity export matters more from now on

In February 2026 the Norwegian Building Authority (DiBK) proposed two changes to chapter 17. The first widens § 17-1: all of module A5, stairs and balconies (28) and prefabricated rooms (61) for all covered projects, building services for projects of at least 5,000 m² BTA, and small-house developments of at least 1,000 m² BTA. The second introduces a new § 17-2 with limit values per building category, for example 354 kg CO₂e/m² BTA for apartment blocks, 396 for offices and 294 for schools and kindergartens, measured over 50 years [2].

The hearing closed on 5 May 2026. At the time of writing we have not found an adopted amendment, so check dibk.no before relying on the figures. The direction is still clear. Once a number is compared with a limit, a quantity error is no longer a reporting detail. It is a compliance risk.

## What goes wrong between model and spreadsheet

A 2025 study compared how teams from eight countries exported a bill of quantities from the same BIM model of an office building for life-cycle assessment. Five teams delivered detailed quantities that could be compared, and most workflows still relied on manual transfer [3].

The errors were mundane, and that is the point. The authors report 55 cases of missing materials, most of them because composite elements were not split into their materials, some because thin layers such as foils had zero thickness and therefore zero volume. They found reinforcement quantities off by a factor of 1/16 from a generic factor, stone wool understated by 78 % through a wrong decomposition factor, a factor-five error from an area-to-volume conversion and a factor-ten error from one transposed digit. Rounding of volumes to two decimals in Revit schedules also showed up [3].

An earlier review of 60 BIM–LCA case studies found that spreadsheets were still the most common link between model and assessment [4]. The manual step has not gone away.

## The seven checks

### 1. Map the model to the required scope

Every element that belongs in the account needs an NS 3451 code, and every required code needs elements. Run both directions. Elements without a code are a gap list. Required codes with no elements, for example 216 in a model where foundations sit in a separate structural file, are a scope error. If the 2026 proposal is adopted, 28 and 61 join the list, and in larger projects so do parts of the building services [2].

### 2. Count layers, not elements

A compound wall, floor or roof is one element with several materials. The climate account needs the materials. Export per layer and material, and check that the sum of the layer volumes equals the element volume. That single plausibility check catches most decomposition errors [3].

### 3. Give thin layers an area

Wind barriers, vapour membranes and foils are often modelled with zero or near-zero thickness. In a volume export they vanish. Report them by area, and match the area to the declared unit of the EPD you use. If a layer is not modelled at all, add it as a documented line in the account rather than leaving it out.

### 4. Treat reinforcement as an engineering input

Reinforcement is rarely modelled in early stages, and generic kilograms-per-cubic-metre factors can be badly wrong [3]. Ask the structural engineer for project-specific ratios by element type, record who gave them and when, and replace them with modelled or scheduled quantities as the design matures. The same applies to connectors and fixings in timber and steel systems.

### 5. Control units and precision

Check that model units, export units and EPD declared units agree: m³, m², kg or pieces. Converting volume to mass needs a density, and the density must come from the same product as the EPD. Avoid exporting rounded schedule values; sum quantities in the model or export with enough decimals [3]. A quick total comparison between the model and the spreadsheet should be part of every handover.

### 6. Do not trust simplified objects

Windows, doors, curtain walls, railings and prefabricated bathroom pods are usually simplified families. Their geometry says little about their material content. Count them as pieces or areas and use the manufacturer's EPD or a documented generic value per unit, rather than calculating their volume [3].

### 7. Make every data choice traceable

For each line in the account, keep the product or generic dataset used, the EPD registration number and version, its validity date, the modules it covers and whether the 25 % surcharge was applied [1]. When a product is substituted on site, the as-built account must follow. That record is what turns a carbon figure into something a client, a controller or an authority can check.

## Writing the checks into the project

Most of these checks can be written as information requirements and tested automatically. buildingSMART's Information Delivery Specification (IDS) became a final standard in June 2024 and lets a project state, in machine-readable form, which IFC entities must carry which properties, such as an NS 3451 code or a material name per layer [5]. ISO 7817-1:2024 gives a shared vocabulary for the level of information need at each stage [6]. We described an IDS-based quality gate in more detail in [The BIM Model That Says Not Ready](https://jarlhalla.com/bim-data-quality-ids-preflight-ai-analysis/) on jarlhalla.com, and how to turn carbon results into design decisions in [Whole-Life Carbon in Buildings](https://jarlhalla.com/whole-life-carbon-buildings-epd-decision-register/).

A practical order is to agree the scope map and data rules in the BIM execution plan, run the checks at each design milestone, and keep a short log of deviations and assumptions next to the account. The log is often more useful to the next reader than the final number.

## How SustainArc can help

Through Taksdal Bygg Teknisk we prepare Revit and IFC models so that quantities, materials and classification are ready for a climate account, and we review existing exports against the checks above. We do not issue the account on behalf of the responsible applicant, and we will say clearly where a figure rests on an assumption.

*This article describes current rules and a published proposal as we understand them in November 2026. It is not legal advice. The responsible applicant must confirm the requirements that apply to a specific project.*

## Sources

1. Direktoratet for byggkvalitet. [TEK17 § 17-1 Klimagassregnskap fra materialer, with guidance](https://www.dibk.no/regelverk/byggteknisk-forskrift-tek17/17/17-1). Accessed 15 November 2026.
2. Direktoratet for byggkvalitet. [Forslag til endringer i klimakrav i byggteknisk forskrift](https://www.dibk.no/regelverk/horinger/hoyringar/horingsnotat-om-klimakrav-i-byggteknisk-forskrift). Hearing opened 5 February 2026, deadline 5 May 2026. Proposal, not adopted regulation.
3. Potrč Obrecht, T. et al. [The Impact of the Bill of Quantity Export Process from BIM on the Accuracy of the LCA Results](https://www.mdpi.com/2071-1050/17/20/9354). *Sustainability* 17(20), 9354. Published 21 October 2025.
4. Potrč Obrecht, T., Röck, M., Hoxha, E., Passer, A. [BIM and LCA Integration: A Systematic Literature Review](https://doi.org/10.3390/su12145534). *Sustainability* 12(14), 5534. 2020.
5. buildingSMART International. [Information Delivery Specification (IDS) v1.0 approved as a final standard](https://comms.buildingsmart.org/the-buildingsmart-newsletter-is-here-for-june-2024). June 2024.
6. ISO. [ISO 7817-1:2024 Building information modelling — Level of information need — Part 1](https://www.iso.org/standard/82914.html). Published June 2024.
7. Direktoratet for byggkvalitet. [Veileder om klimagassregnskap](https://www.dibk.no/byggtekniske-omrader/veileder-om-klimagassregnskap). Last changed 18 August 2023.
