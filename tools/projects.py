"""EnerFab project pages: one page per real project.

Every fact here comes from efpl.org (home, page1, page2, testimonials).
Do not add figures, clients or dates that are not on that site or that
EnerFab has not confirmed in writing. The "how" sections describe the
general technology only, not project-specific numbers.

Fields:
  slug, img, tag, name, sub, card (one-line summary for the list page),
  seo (title tag), desc (meta description),
  facts: list of (label, value) shown in the side panel,
  body: HTML for the project story,
  how: (heading, HTML) describing the technology in general terms,
  video: list of (youtube id, title) or [],
  gallery: list of (image, alt) or [],
  div: related solution slug, guides: related insight slugs,
  sources: list of (label, url)
"""

EFPL_SOLUTIONS = ("EnerFab (efpl.org): Our solutions", "https://efpl.org/page2.html")

PROJECTS = [
    {
        "slug": "kandalama-tea-factory-hotel-gasifiers",
        "img": "kandalama-gasifier.jpg", "tag": "Hotels",
        "name": "Kandalama Hotel and Tea Factory Hotel",
        "sub": "Aitken Spence Group",
        "card": "EnerFab gasifiers have operated at both hotels for more than a decade, with EnerFab after-sales service.",
        "seo": "Hotel Biomass Gasifiers, Kandalama & Tea Factory Hotel | EnerFab",
        "desc": "EnerFab biomass gasifiers have run at Aitken Spence's Kandalama Hotel and Tea Factory Hotel for more than a decade, backed by EnerFab after-sales service.",
        "facts": [("Client", "Aitken Spence Group hotels"), ("Sites", "Kandalama Hotel, Tea Factory Hotel"), ("System", "Biomass gasifier"), ("In service", "More than a decade"), ("Support", "EnerFab after-sales service"), ("Press", "Daily News, November 2007")],
        "body": """<p>Two of Sri Lanka’s best-known hotels in the Aitken Spence group, Kandalama Hotel and the Tea Factory Hotel, run EnerFab biomass gasifiers. Both installations have operated for more than a decade, and EnerFab has provided after-sales service throughout.</p>
<p>The Tea Factory Hotel installation was covered by the Daily News in November 2007.</p>
<p>Hotels need steady heat every day of the year. A gasifier lets them make that heat from locally grown biomass instead of imported fuel, with EnerFab supplying spare parts and breakdown maintenance to keep the plant running.</p>""",
        "how": ("How a gasifier serves a hotel", """<p>A gasifier heats wood with a limited supply of air, so instead of burning it turns the wood into a combustible gas called producer gas. The gas is piped to a burner on the existing heating equipment, where it burns with a clean, controllable flame.</p>
<p>Because the fuel is wood, the hotel’s heating no longer depends on the price of diesel or furnace oil. Read <a href="/insights/how-biomass-gasification-works/">how biomass gasification works</a> for the full process.</p>"""),
        "video": [], "gallery": [("tea-factory-hotel.jpg", "Tea Factory Hotel, home to an EnerFab biomass gasifier")],
        "div": "biomass-gasifiers", "guides": ["how-biomass-gasification-works", "furnace-oil-to-biomass-boiler-conversion"],
        "sources": [EFPL_SOLUTIONS, ("Daily News, 5 November 2007", "http://archives.dailynews.lk/2007/11/05/bus10.asp")],
    },
    {
        "slug": "cw-mackie-gasifier",
        "img": "gasifier-collage.jpg", "tag": "Industry",
        "name": "CW Mackie", "sub": "Industrial gasifier",
        "card": "One of several establishments that have operated EnerFab gasifiers for more than a decade.",
        "seo": "CW Mackie Biomass Gasifier, Sri Lanka | EnerFab Projects",
        "desc": "CW Mackie is one of the Sri Lankan establishments that have operated an EnerFab biomass gasifier for more than a decade, with EnerFab after-sales service.",
        "facts": [("Client", "CW Mackie"), ("Sector", "Industry"), ("System", "Biomass gasifier"), ("In service", "More than a decade"), ("Support", "EnerFab after-sales service")],
        "body": """<p>CW Mackie is one of several establishments, alongside the Kandalama Hotel and the Tea Factory Hotel, that have operated EnerFab gasifiers for more than a decade.</p>
<p>EnerFab has supplied gasifiers since 2005 and has provided after-sales service ever since: spare parts, breakdown maintenance and, where clients want it, management contracts to operate the plant.</p>""",
        "how": ("Why gasifiers last", """<p>A gasifier has few moving parts. Wood is fed into a reactor, turned into producer gas, cleaned and sent to a burner or engine. With regular maintenance and dry, well-sized fuel, a plant can run for many years. EnerFab also supplies the fuelwood, so the plant has a steady supply.</p>
<p>See <a href="/insights/how-biomass-gasification-works/">how biomass gasification works</a> and <a href="/insights/gliricidia-fuelwood-sri-lanka/">Gliricidia fuelwood in Sri Lanka</a>.</p>"""),
        "video": [("tKnqCnPaES8", "EnerFab WBG 10 biomass gasifier")], "gallery": [],
        "div": "biomass-gasifiers", "guides": ["how-biomass-gasification-works", "gliricidia-fuelwood-sri-lanka"],
        "sources": [EFPL_SOLUTIONS],
    },
    {
        "slug": "rubber-dryer-diesel-to-producer-gas",
        "img": "producer-gas-flame.jpg", "tag": "Thermal · since 2006",
        "name": "Rubber processing plant dryer", "sub": "50 litres of diesel an hour replaced",
        "card": "A dryer that burned 50 litres of diesel an hour, switched to an EnerFab gasifier in 2006 and still running.",
        "seo": "Diesel Dryer to Biomass Gasifier, Rubber Plant | EnerFab",
        "desc": "EnerFab replaced a rubber processing dryer's 50 L/hr diesel burner with a producer-gas burner and biomass gasifier. It has run from 2006 to date.",
        "facts": [("Sector", "Rubber processing"), ("Equipment", "Dryer"), ("Fuel replaced", "Diesel, 50 litres an hour"), ("New fuel", "Producer gas from biomass"), ("Year", "2006"), ("Status", "Operating to date")],
        "body": """<p>The dryer at a rubber processing plant burned 50 litres of diesel every hour. EnerFab replaced the diesel burner with a producer-gas burner fed by an EnerFab biomass gasifier.</p>
<p>The conversion was made in 2006, and the dryer has operated on producer gas from then to date.</p>
<p>The video below shows the installation.</p>""",
        "how": ("How a diesel dryer switches to biomass", """<p>The dryer itself stays. Only the burner changes: the diesel burner is replaced with one designed for producer gas, and a gasifier beside the dryer makes the gas from wood. The flame heats the dryer air just as the diesel flame did.</p>
<p>The same approach works for boilers, furnaces and kilns running on diesel, furnace oil or LPG. Read <a href="/insights/furnace-oil-to-biomass-boiler-conversion/">converting from furnace oil to biomass</a>.</p>"""),
        "video": [("Az4ZQNXVZ7U", "Gasifier installed by EnerFab to replace 50 litres per hour of diesel in a rubber processing plant")], "gallery": [],
        "div": "biomass-gasifiers", "guides": ["furnace-oil-to-biomass-boiler-conversion", "how-biomass-gasification-works"],
        "sources": [EFPL_SOLUTIONS],
    },
    {
        "slug": "200kw-gasifier-generator-wood-processing",
        "img": "commissioning-250kw-gasifier.jpg", "tag": "Electrical · 2017",
        "name": "Wood processing plant", "sub": "200 kW gasifier generator",
        "card": "200 kW of electricity from the factory’s own waste wood, with a further 400 kW of heat available.",
        "seo": "200 kW Biomass Gasifier Generator, Sri Lanka | EnerFab",
        "desc": "In 2017 EnerFab installed a 200 kW gasifier generator at a wood processing plant, making electricity from mill waste wood. 400 kW of heat is also available.",
        "facts": [("Sector", "Wood processing"), ("Year", "2017"), ("Output", "200 kW electricity"), ("Fuel", "Factory waste wood"), ("Heat available", "A further 400 kW thermal"), ("System", "Gasifier, gas cleaning, engine generator")],
        "body": """<p>In 2017 EnerFab installed a 200 kW electrical system at a wood processing plant. The gasifier runs on the factory’s own waste wood and feeds an internal combustion engine that drives a generator.</p>
<p>The project showed that producer gas from EnerFab’s gasifier is clean enough to run an internal combustion engine. A further 400 kW of thermal energy is available from the engine’s exhaust and cooling system.</p>
<p>Waste that once had to be disposed of is now the plant’s power source.</p>""",
        "how": ("From waste wood to electricity", """<p>For power generation the gas must be much cleaner and cooler than for a burner. After the reactor, it passes through a cyclone and cleaning vessels to remove dust and tar, then into a gas engine coupled to a generator.</p>
<p>Recovering the engine’s heat for drying or hot water turns the plant into combined heat and power (CHP). Read <a href="/insights/biomass-chp-gasifier-generator/">biomass CHP with a gasifier generator</a>, or explore the 3D plant on the <a href="/solutions/biomass-gasifiers/">gasifier page</a>.</p>"""),
        "video": [("334j_wDnESI", "200 kW gasifier generator by EnerFab"), ("088d9Otk_18", "EnerFab biomass gasifier generator set")], "gallery": [],
        "div": "biomass-gasifiers", "guides": ["biomass-chp-gasifier-generator", "how-biomass-gasification-works"],
        "sources": [EFPL_SOLUTIONS],
    },
    {
        "slug": "poultry-farm-lpg-to-biomass-puttalam",
        "img": "gasifier-installation.jpg", "tag": "Thermal · 2018",
        "name": "Poultry farm, Puttalam", "sub": "LPG to biomass",
        "card": "In July 2018 EnerFab undertook a gasification plant to replace LPG at a poultry farm in Puttalam.",
        "seo": "LPG to Biomass Gasifier, Poultry Farm Puttalam | EnerFab",
        "desc": "In July 2018 EnerFab undertook to install a biomass gasification plant replacing LPG heating at a poultry farm in Puttalam, Sri Lanka.",
        "facts": [("Sector", "Poultry farming"), ("Location", "Puttalam district"), ("Fuel replaced", "LPG"), ("New fuel", "Producer gas from biomass"), ("Started", "July 2018")],
        "body": """<p>In July 2018 EnerFab undertook to install a biomass gasification plant at a poultry farm in Puttalam, replacing the LPG the farm used for heating.</p>
<p>Puttalam is also home to EnerFab’s model fuelwood plantation at Nawagaththegama, so the farm sits close to a source of sustainably grown fuelwood.</p>""",
        "how": ("Replacing LPG with producer gas", """<p>Producer gas burns in a gas burner much like LPG, but it is made on site from wood instead of being bought in cylinders or bulk tanks. The farm’s heat supply then depends on locally grown biomass rather than imported gas.</p>
<p>See <a href="/insights/how-biomass-gasification-works/">how biomass gasification works</a> and <a href="/insights/gliricidia-fuelwood-sri-lanka/">Gliricidia fuelwood</a>.</p>"""),
        "video": [], "gallery": [],
        "div": "biomass-gasifiers", "guides": ["how-biomass-gasification-works", "gliricidia-fuelwood-sri-lanka"],
        "sources": [EFPL_SOLUTIONS],
    },
    {
        "slug": "nawagaththegama-fuelwood-plantation",
        "img": "plantation-hills.jpg", "tag": "Plantation · 2008",
        "name": "Nawagaththegama energy plantation", "sub": "40,000 plants on former scrubland",
        "card": "A model fuelwood plantation planted on scrubland in the Maha season of 2008, now mature.",
        "seo": "Nawagaththegama Fuelwood Energy Plantation, Puttalam | EnerFab",
        "desc": "EnerFab's model fuelwood plantation at Nawagaththegama, Puttalam: 40,000 plants at 2 × 1 m spacing, planted on scrubland in the 2008 Maha season, now mature.",
        "facts": [("Location", "Nawagaththegama, Puttalam district"), ("Planted", "Maha season, 2008"), ("Plants", "40,000"), ("Spacing", "2 m × 1 m"), ("Land before", "Scrubland"), ("Status", "Mature")],
        "body": """<p>EnerFab established a model fuelwood plantation at Nawagaththegama in the Puttalam district. It has 40,000 plants at a spacing of 2 by 1 metres, planted in the Maha season of 2008, and the plants have now grown to maturity.</p>
<p>Before planting, the land was scrubland. It is now green vegetation that enriches the soil with nitrogen, supplies fuel to industry and improves the local microclimate.</p>
<p>The plantation shows how EnerFab’s gasifiers can run on wood that is grown, cut and regrown, alongside the network of farmers who supply EnerFab with fuelwood.</p>""",
        "how": ("How an energy plantation works", """<p>Fast-growing leguminous trees such as Gliricidia are cut back regularly and regrow from the stump, a method called short-rotation coppicing. The trees fix nitrogen, so the land improves while it produces fuel.</p>
<p>Read <a href="/insights/gliricidia-fuelwood-sri-lanka/">Gliricidia fuelwood in Sri Lanka</a>.</p>"""),
        "video": [("P8rSUtO4fnU", "Energy Plantation")],
        "gallery": [("plantation-scrubland.jpg", "Nawagaththegama site before planting"), ("plantation-2008-seedlings.jpg", "Young plants at 2 by 1 metre spacing"), ("plantation-young.jpg", "Plantation establishing"), ("plantation-growing.jpg", "Plantation growing"), ("plantation-mature.jpg", "Mature energy crop"), ("plantation-hills.jpg", "The plantation across the hills")],
        "div": "fuelwood-biomass-supply", "guides": ["gliricidia-fuelwood-sri-lanka", "how-biomass-gasification-works"],
        "sources": [EFPL_SOLUTIONS],
    },
    {
        "slug": "aitken-spence-power-mini-hydro",
        "img": "hydro-generators.jpg", "tag": "Hydro · 2009",
        "name": "Aitken Spence Power mini-hydro", "sub": "GUGLER turbines",
        "card": "EnerFab was assigned the installation of the GUGLER machinery and local technical support.",
        "seo": "Aitken Spence Power Mini-Hydro, GUGLER Turbines | EnerFab",
        "desc": "In December 2009 Aitken Spence Power signed for GUGLER hydro turbines for a mini-hydro site. EnerFab was assigned installation and local technical support.",
        "facts": [("Client", "Aitken Spence Power"), ("Signed", "December 2009"), ("Equipment", "GUGLER Water Turbines"), ("EnerFab role", "Installation and local technical support")],
        "body": """<p>In December 2009 Aitken Spence Power signed for GUGLER hydro turbines for one of its mini-hydro sites. EnerFab, the sole agent in Sri Lanka for GUGLER Water Turbines, was assigned the installation of the machinery and local technical support.</p>
<p>Having the turbine maker’s local agent on site means installation, commissioning and later support come from one team in Sri Lanka.</p>""",
        "how": ("Choosing a hydro turbine", """<p>GUGLER makes Kaplan, Pelton and Francis turbines from 5 kW to 10 MW, in horizontal and vertical layouts. Which type suits a site depends mainly on the head (the height the water falls) and the flow.</p>
<p>Read <a href="/insights/mini-hydro-turbine-selection/">mini-hydro turbine selection</a>.</p>"""),
        "video": [], "gallery": [],
        "div": "mini-hydro-power-plants", "guides": ["mini-hydro-turbine-selection"],
        "sources": [EFPL_SOLUTIONS],
    },
    {
        "slug": "kirkoswald-hydropower-francis-turbines",
        "img": "hydro-battalgalla.jpg", "tag": "Hydro · 2010",
        "name": "Kirkoswald hydropower project", "sub": "3 Francis turbines, 4.5 MW",
        "card": "A turnkey GUGLER contract for three Francis turbines, 4.5 MW in total, including all electromechanical equipment.",
        "seo": "Kirkoswald Hydropower, 4.5 MW Francis Turbines | EnerFab",
        "desc": "In March 2010 Bogo Power awarded GUGLER Water Turbines, represented in Sri Lanka by EnerFab, a turnkey contract for three Francis turbines totalling 4.5 MW.",
        "facts": [("Client", "Bogo Power (Pvt) Ltd"), ("Awarded", "March 2010"), ("Turbines", "3 × Francis"), ("Capacity", "4.5 MW total"), ("Contract", "Turnkey, all electromechanical equipment"), ("Supplier", "GUGLER Water Turbines")],
        "body": """<p>In March 2010 Bogo Power (Pvt) Ltd awarded GUGLER Water Turbines a turnkey contract for the Kirkoswald hydropower project: three Francis turbines with a total capacity of 4.5 MW, including all the electromechanical equipment.</p>
<p>GUGLER is represented in Sri Lanka by EnerFab, its sole agent.</p>""",
        "how": ("Why Francis turbines", """<p>Francis turbines suit medium heads and moderate flows. Splitting a plant into several units lets it keep generating efficiently when river flow drops in the dry season.</p>
<p>Read <a href="/insights/mini-hydro-turbine-selection/">mini-hydro turbine selection</a>.</p>"""),
        "video": [], "gallery": [],
        "div": "mini-hydro-power-plants", "guides": ["mini-hydro-turbine-selection"],
        "sources": [EFPL_SOLUTIONS],
    },
    {
        "slug": "factory-energy-audits",
        "img": "energy-audit-pipework.jpg", "tag": "ESCO",
        "name": "15+ detailed energy audits", "sub": "Garment and tea factories",
        "card": "Detailed energy audits completed in knitted-garment factories, tea factories and other sectors.",
        "seo": "Factory Energy Audits Sri Lanka, Garment & Tea | EnerFab",
        "desc": "EnerFab has completed more than 15 detailed energy audits in Sri Lankan knitted-garment factories, tea factories and other sectors, with turnkey energy-saving projects.",
        "facts": [("Audits", "More than 15 detailed audits"), ("Sectors", "Knitted garments, tea, others"), ("Services", "Preliminary and detailed audits, energy studies"), ("Follow-on", "Turnkey energy-saving projects with a payback guarantee")],
        "body": """<p>EnerFab’s ESCO division has completed more than 15 detailed energy audits in knitted-garment factories, tea factories and other sectors.</p>
<p>An audit measures where a factory’s energy goes and where it is wasted. EnerFab then implements the energy-saving measures on a turnkey basis, with a payback guarantee.</p>""",
        "how": ("What an energy audit covers", """<p>A preliminary audit is a walk-through that finds the obvious savings. A detailed audit uses metering instruments to measure steam, compressed air, electricity and heat use, then costs each saving and its payback period.</p>
<p>Read <a href="/insights/industrial-energy-audit-sri-lanka/">industrial energy audits in Sri Lanka</a>.</p>"""),
        "video": [], "gallery": [],
        "div": "esco-energy-solutions", "guides": ["industrial-energy-audit-sri-lanka", "furnace-oil-to-biomass-boiler-conversion"],
        "sources": [EFPL_SOLUTIONS],
    },
]
