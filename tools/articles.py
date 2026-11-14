"""Energy knowledge hub articles for enerfab.lk (/insights/).

Each article mixes two kinds of content, kept clearly apart:
  - general engineering knowledge, with its sources listed;
  - EnerFab facts, taken only from efpl.org and the Tech Monitor (2007) review.
Before publishing changes, ask an EnerFab engineer to review the article.

Fields: slug, title (H1), seo (title tag), desc (meta description), img,
date (ISO), divs (related division slugs), takeaways, body (HTML), sources.
"""

ARTICLES = [
# ---------------------------------------------------------------------------
{
"slug": "how-biomass-gasification-works",
"title": "How biomass gasification works",
"seo": "How Biomass Gasification Works: Producer Gas Explained | EnerFab",
"desc": "A plain-English guide to biomass gasification: the four reaction zones, updraft vs downdraft gasifiers, what producer gas contains and how factories use it.",
"img": "commissioning-250kw-gasifier.jpg",
"date": "2026-11-14",
"divs": ["biomass-gasifiers", "fuelwood-biomass-supply"],
"takeaways": [
    "Gasification heats wood with less air than it needs to burn completely, turning it into a combustible gas called producer gas.",
    "Inside a gasifier the wood passes through four zones: drying, pyrolysis, oxidation and reduction.",
    "Wood producer gas is mostly nitrogen, carbon monoxide and hydrogen, with a heating value of roughly 5 to 6 MJ per cubic metre.",
    "Downdraft gasifiers make a cleaner gas, which is why they are used to run engines.",
],
"body": """
<h2>Burning versus gasifying</h2>
<p>When wood burns in an open fire or a wood-fired boiler, it gets all the air it needs and turns straight into heat, carbon dioxide and water vapour. A gasifier works differently. It deliberately supplies <strong>less air than complete combustion needs</strong>. Only part of the wood burns, and the heat from that burning breaks the rest of the wood down into a combustible gas.</p>
<p>That gas, called <strong>producer gas</strong> or wood gas, can be piped to a burner and burned like LPG, or cleaned and used to run an engine. Gasification effectively turns a solid fuel that is awkward to handle into a gaseous fuel that behaves much like the fossil fuels it replaces.</p>

<h2>The four zones inside a gasifier</h2>
<p>As wood moves through a gasifier it passes through four overlapping zones:</p>
<ol>
  <li><strong>Drying.</strong> Heat from below drives the moisture out of the wood.</li>
  <li><strong>Pyrolysis.</strong> As the dry wood heats further, without enough oxygen to burn, it breaks down into charcoal, tar vapours and gases.</li>
  <li><strong>Oxidation.</strong> Air enters here. Part of the fuel and pyrolysis products burn, producing the high temperatures that drive the whole process.</li>
  <li><strong>Reduction.</strong> Hot charcoal reacts with the carbon dioxide and water vapour from the oxidation zone, forming carbon monoxide and hydrogen: the combustible parts of producer gas.</li>
</ol>
<p>The key reduction reactions are C + CO<sub>2</sub> → 2CO and C + H<sub>2</sub>O → CO + H<sub>2</sub>. Both absorb heat, which is why the oxidation zone has to stay hot.</p>

<h2>Updraft, downdraft and other designs</h2>
<div class="table-wrap"><table>
<thead><tr><th scope="col">Type</th><th scope="col">How the gas flows</th><th scope="col">Typical use</th></tr></thead>
<tbody>
<tr><td>Updraft</td><td>Air enters at the bottom; gas leaves at the top, passing up through fresh fuel</td><td>Direct heating; gas carries more tar</td></tr>
<tr><td>Downdraft</td><td>Gas is drawn down through the hot oxidation zone before leaving</td><td>Engines and generators; tars are largely cracked in the hot zone, so the gas is cleaner</td></tr>
<tr><td>Cross-draft</td><td>Air and gas move sideways across the fuel bed</td><td>Small units with low-ash fuels such as charcoal</td></tr>
<tr><td>Fluidised bed</td><td>Air bubbles up through a hot bed of sand and fuel</td><td>Larger plants with varied fuels</td></tr>
</tbody></table></div>

<h2>What producer gas contains</h2>
<p>Because the air used for gasification is about four-fifths nitrogen, wood producer gas is roughly half nitrogen. The FAO's reference guide on wood gas gives the following typical composition for wood gas from a downdraft gasifier:</p>
<div class="table-wrap"><table>
<thead><tr><th scope="col">Component</th><th scope="col">Typical share by volume</th></tr></thead>
<tbody>
<tr><td>Nitrogen (N<sub>2</sub>)</td><td>50 – 54%</td></tr>
<tr><td>Carbon monoxide (CO)</td><td>17 – 22%</td></tr>
<tr><td>Hydrogen (H<sub>2</sub>)</td><td>12 – 20%</td></tr>
<tr><td>Carbon dioxide (CO<sub>2</sub>)</td><td>9 – 15%</td></tr>
<tr><td>Methane (CH<sub>4</sub>)</td><td>2 – 3%</td></tr>
<tr><td>Heating value</td><td>about 5 – 5.9 MJ per m³</td></tr>
</tbody></table></div>
<p>That heating value is much lower than natural gas or LPG, so burners and gas lines are sized for a larger gas flow. It is still enough to fire boilers, furnaces, kilns and dryers, and to run gas engines.</p>

<h2>What gasifiers need from the fuel</h2>
<ul>
  <li><strong>Dry wood.</strong> Wet fuel wastes heat on evaporating water and cools the reaction zones. The FAO guide says downdraft gasifiers need reasonably dry fuel, below 25% moisture (dry basis).</li>
  <li><strong>Even-sized pieces.</strong> Sticks are chopped into small blocks so the fuel bed flows evenly and air passes through it uniformly.</li>
  <li><strong>Clean fuel.</strong> Soil, stones and very high-ash materials cause slag and blockages.</li>
</ul>

<h2>Cleaning gas for engines</h2>
<p>For heating, producer gas can go hot and almost directly to a burner. An engine is far less tolerant: dust and condensed tar damage it. Gas for engines is therefore cleaned and cooled, typically in a cyclone to remove dust, then coolers and filters, before it reaches the engine.</p>

<h2>How EnerFab uses gasification</h2>
<p>EnerFab has designed, fabricated and installed biomass gasifiers in Sri Lanka since 2005. Its systems replace diesel, furnace oil and LPG in boilers, furnaces, kilns and dryers, and fuel internal combustion engines that drive generators. A University of Moratuwa review in 2007 named EnerFab the leading gasifier designer and manufacturer in Sri Lanka.</p>
""",
"sources": [
    ("FAO Forestry Paper 72: Wood gas as engine fuel (FAO, 1986)", "https://www.fao.org/4/t0512e/T0512e00.htm"),
    ("Tech Monitor, July–August 2007: biomass gasification in Sri Lanka, Dr. A.G.T. Sugathapala", "/assets/docs/tech-monitor-2007-biomass-gasification.pdf"),
],
},
# ---------------------------------------------------------------------------
{
"slug": "furnace-oil-to-biomass-boiler-conversion",
"title": "Furnace oil to biomass: converting an industrial boiler",
"seo": "Furnace Oil to Biomass Boiler Conversion Sri Lanka | EnerFab",
"desc": "How Sri Lankan factories switch diesel and furnace-oil boilers to biomass with a gasifier and dual-fuel burner: the two routes, the steps, and what data to gather first.",
"img": "producer-gas-flame.jpg",
"date": "2026-11-14",
"divs": ["biomass-gasifiers", "esco-energy-solutions", "fuelwood-biomass-supply"],
"takeaways": [
    "There are two ways to move a boiler to biomass: replace it with a wood-fired boiler, or keep it and fire it with producer gas from a gasifier.",
    "With a gasifier and dual-fuel burner you keep your existing boiler, and your old fuel stays connected as a backup.",
    "Good projects start with data: how much fuel you burn, for how many hours, and how your heat demand varies.",
    "Securing the fuelwood supply matters as much as the equipment.",
],
"body": """
<h2>Why factories move off oil</h2>
<p>Furnace oil (heavy fuel oil, HFO), diesel and LPG are imported fuels, so their cost follows world oil prices and the exchange rate. Biomass such as fuelwood is grown locally, is renewable when it comes from managed plantations, and keeps fuel spending inside the rural economy. For factories that need heat every day, such as tea, rubber, food processing and hotels, that is a strong reason to look at biomass.</p>

<h2>Two ways to convert</h2>
<div class="table-wrap"><table>
<thead><tr><th scope="col"></th><th scope="col">Gasifier + dual-fuel burner</th><th scope="col">New wood-fired boiler</th></tr></thead>
<tbody>
<tr><th scope="row">Existing boiler</th><td>Kept and fired with producer gas</td><td>Replaced</td></tr>
<tr><th scope="row">Backup fuel</th><td>Original oil or diesel stays connected</td><td>None, unless a second boiler is kept</td></tr>
<tr><th scope="row">Efficiency</th><td>Better (EnerFab)</td><td>Lower</td></tr>
<tr><th scope="row">Response to load changes</th><td>Better: a gas flame is easy to control (EnerFab)</td><td>Slower: a solid fuel bed takes time to respond</td></tr>
<tr><th scope="row">Particulate emissions</th><td>Less (EnerFab)</td><td>More</td></tr>
</tbody></table></div>
<p>The comparisons marked EnerFab are EnerFab’s own published assessment of its conversion method against wood-fired boilers.</p>

<h2>Step by step</h2>
<ol>
  <li><strong>Measure what you use today.</strong> Litres of oil or diesel per hour and per month, operating hours and days, steam or heat demand, and how the load rises and falls through the day.</li>
  <li><strong>Fix the losses first.</strong> An energy audit often finds savings in steam traps, insulation, condensate return and combustion settings. There is no point sizing a gasifier for heat that is being wasted.</li>
  <li><strong>Size the gasifier</strong> to the real heat demand, including peaks.</li>
  <li><strong>Plan the fuel.</strong> Decide where the fuelwood comes from, how it will be delivered, stored, dried and chopped, and who manages supply through the year.</li>
  <li><strong>Lay out the site.</strong> Room for wood storage, a chopper, the gasifier, the gas line to the boiler house, and access for deliveries.</li>
  <li><strong>Install and connect.</strong> Gasifier, gas piping, dual-fuel burner and controls, so the boiler can switch between producer gas and its original fuel.</li>
  <li><strong>Commission and train.</strong> Tune the system and train operators in daily running, fuel loading and ash removal.</li>
  <li><strong>Maintain.</strong> Plan regular maintenance and spare parts, or hand operation to a contractor.</li>
</ol>

<h2>What to send when you ask for a quote</h2>
<ul>
  <li>Boiler or heater type, make, rated capacity and current fuel</li>
  <li>Fuel use: litres per hour at typical load, and per month</li>
  <li>Operating hours per day and days per week</li>
  <li>Steam pressure or process temperature needed</li>
  <li>Space available near the boiler house</li>
  <li>Any biomass you already have on site, such as off-cuts or husks</li>
</ul>

<h2>EnerFab conversions in practice</h2>
<p>EnerFab replaced the diesel burner on a rubber processing plant’s dryer, which used 50 litres of diesel an hour, with a producer-gas burner and gasifier; it has run from 2006 to date. Kandalama Hotel, Tea Factory Hotel, CW Mackie and other establishments have operated EnerFab gasifiers for more than a decade. EnerFab can also supply the fuelwood on contract, and offers management contracts, spare parts and breakdown maintenance.</p>
""",
"sources": [
    ("EnerFab: biomass gasifiers and installations (efpl.org)", "https://efpl.org/page2.html"),
],
},
# ---------------------------------------------------------------------------
{
"slug": "gliricidia-fuelwood-sri-lanka",
"title": "Gliricidia and fuelwood for industrial biomass in Sri Lanka",
"seo": "Gliricidia Fuelwood & Biomass Supply in Sri Lanka | EnerFab",
"desc": "Why Gliricidia and other fuelwoods suit biomass gasifiers in Sri Lanka: coppicing, moisture, sizing, energy content and how to secure a reliable supply.",
"img": "plantation-mature.jpg",
"date": "2026-11-14",
"divs": ["fuelwood-biomass-supply", "biomass-gasifiers"],
"takeaways": [
    "Gliricidia is a fast-growing, nitrogen-fixing tree that regrows after cutting, so it can be harvested again and again.",
    "Moisture is the biggest factor in fuel quality: downdraft gasifiers need wood below 25% moisture (dry basis), so fresh wood must be dried.",
    "Dry wood of most species holds a broadly similar amount of energy per kilogram, roughly 18 to 20 MJ.",
    "A biomass plant needs real control over its fuel supply; EnerFab recommends at least half.",
],
"body": """
<h2>Why Gliricidia</h2>
<p><em>Gliricidia sepium</em> is a leguminous tree, native to Mexico and Central America, that is now common across Sri Lanka as a live fence and a shade tree in plantations. Three things make it a good energy crop:</p>
<ul>
  <li><strong>It coppices.</strong> When the stems are cut, the stump sends up new shoots, so the same trees can be harvested repeatedly without replanting. This is called short-rotation coppicing.</li>
  <li><strong>It fixes nitrogen.</strong> Like other legumes, it adds nitrogen to the soil, and its leaves are widely used as green manure.</li>
  <li><strong>It grows fast</strong> on land that is too poor for many other crops.</li>
</ul>

<h2>What makes good fuelwood</h2>
<div class="table-wrap"><table>
<thead><tr><th scope="col">Factor</th><th scope="col">Why it matters</th></tr></thead>
<tbody>
<tr><td>Moisture</td><td>Water in the wood has to be evaporated before it can release energy. Freshly cut wood often contains as much water as dry matter. The FAO guide says downdraft gasifiers need fuel below 25% moisture (dry basis), so wood is air-dried first.</td></tr>
<tr><td>Size</td><td>Gasifiers need evenly sized pieces so the fuel bed flows and air passes through evenly. Sticks are chopped into small blocks.</td></tr>
<tr><td>Cleanliness</td><td>Soil and stones add ash and can form slag. Fuel is kept off the ground and handled carefully.</td></tr>
<tr><td>Energy content</td><td>Completely dry wood of most species contains roughly 18 to 20 MJ per kilogram. The usable energy falls as moisture rises.</td></tr>
</tbody></table></div>

<h2>Other biomass fuels</h2>
<p>EnerFab’s supply base handles Gliricidia, Ipil Ipil, cinnamon wood, timber off-cuts, coconut shells and other approved fuelwood. Each has its own advantages, growing areas and season, and a good supplier plans around all three.</p>

<h2>A model energy plantation</h2>
<p>EnerFab established a model fuelwood plantation at Nawagaththegama in the Puttalam district in the Maha season of 2008: 40,000 plants at 2 by 1 metre spacing, on land that had been scrubland. The plantation is now mature. It enriches the soil with nitrogen, supplies fuel to industry and improves the local microclimate.</p>

<h2>Securing a reliable supply</h2>
<p>A biomass plant is only as reliable as its fuel. If you invest in a power plant, you need real control over your fuelwood supply. Authorities expect it when you seek approvals, and if outside suppliers fall short, your own supply has to carry the plant. In EnerFab’s view, a plant should control at least 50% of its own supply.</p>
<p>EnerFab collects biomass through a network of 3,000 farmers and a supplier base of more than 2,000 across Sri Lanka, outside the North and East, with its own transport that can scale up or down. Its DM500 wood chopper processes 500 kg of fuelwood an hour, and its EWG 1 wood grab lifts a cubic metre of chips at a time.</p>
""",
"sources": [
    ("Feedipedia: Gliricidia (Gliricidia sepium)", "https://www.feedipedia.org/node/552"),
    ("FAO Forestry Paper 72: Wood gas as engine fuel (FAO, 1986)", "https://www.fao.org/4/t0512e/T0512e00.htm"),
    ("EnerFab: fuelwood plantation and processing (efpl.org)", "https://efpl.org/page2.html"),
],
},
# ---------------------------------------------------------------------------
{
"slug": "biomass-chp-gasifier-generator",
"title": "Biomass CHP: electricity and heat from one gasifier",
"seo": "Biomass CHP & Gasifier Generators Sri Lanka | EnerFab",
"desc": "How a biomass gasifier generator makes electricity from wood, why most of the fuel's energy leaves as heat, and how combined heat and power (CHP) puts that heat to work.",
"img": "gasifier-installation.jpg",
"date": "2026-11-14",
"divs": ["biomass-gasifiers", "esco-energy-solutions"],
"takeaways": [
    "A gasifier generator burns producer gas in an internal combustion engine that turns a generator.",
    "Most of the fuel's energy leaves the engine as heat in the exhaust and cooling water.",
    "Combined heat and power (CHP) captures that heat for drying or process heat, so far more of the fuel does useful work.",
    "CHP pays best where a site needs heat and power at the same time, for long hours, with fuel available on site.",
],
"body": """
<h2>From wood to electricity</h2>
<p>To generate electricity, producer gas from a gasifier is cleaned and cooled, then fed to an internal combustion engine in place of diesel or natural gas. The engine turns a generator. This is a mature, well-documented technology: wood gas has powered engines for over a century.</p>
<p>Engines need gas that is much cleaner than a burner does, so a power gasifier includes gas cleaning, typically a cyclone, coolers and filters, between the gasifier and the engine.</p>

<h2>Where the energy goes</h2>
<p>An engine converts only part of its fuel energy into shaft power. The rest leaves as heat, mainly in the hot exhaust and in the engine’s cooling water. For small gasifier generators, overall electrical efficiency from wood to electricity is modest. A 2007 University of Moratuwa review reported around 30% overall efficiency for EnerFab’s electrical gasifier plants.</p>
<p>That means a large share of the energy in the wood is available as heat. Throwing it away wastes fuel that has already been paid for.</p>

<h2>Combined heat and power</h2>
<p>Combined heat and power (CHP), also called cogeneration, captures this heat:</p>
<ul>
  <li><strong>Exhaust heat recovery:</strong> hot exhaust gas passes through a heat exchanger to make hot air, hot water or steam.</li>
  <li><strong>Jacket-water recovery:</strong> heat from the engine’s cooling water is used for hot water or low-temperature drying.</li>
</ul>
<p>The recovered heat can dry fuelwood, timber or agricultural products, or supply process hot water, reducing fuel use elsewhere on the site.</p>

<h2>A Sri Lankan example</h2>
<p>EnerFab installed a gasifier generator at a wood processing plant in Sri Lanka that produces 200 kW of electricity from the factory’s own waste wood. EnerFab notes that the unit also has an unused potential of 400 kW of thermal energy that could be recovered from the engine’s exhaust and cooling system: twice the electrical output, available as heat.</p>

<h2>When CHP makes sense</h2>
<ul>
  <li>The site needs heat and electricity <strong>at the same time</strong>.</li>
  <li>It runs <strong>long hours</strong>, so the equipment is well used.</li>
  <li><strong>Fuel is on site</strong> or close by, such as sawmill off-cuts or plantation wood.</li>
  <li>There is a clear use for the recovered heat, such as drying.</li>
</ul>
<p>A 2007 review reported EnerFab gasifiers for electricity in the range of 1 to 250 kWe. EnerFab can install CHP plants that supply electricity while using the waste heat for thermal energy.</p>
""",
"sources": [
    ("FAO Forestry Paper 72: Wood gas as engine fuel (FAO, 1986)", "https://www.fao.org/4/t0512e/T0512e00.htm"),
    ("Tech Monitor, July–August 2007: biomass gasification in Sri Lanka", "/assets/docs/tech-monitor-2007-biomass-gasification.pdf"),
    ("EnerFab: electrical applications (efpl.org)", "https://efpl.org/page2.html"),
],
},
# ---------------------------------------------------------------------------
{
"slug": "industrial-energy-audit-sri-lanka",
"title": "Industrial energy audits: what they find and what they cost you not to do",
"seo": "Industrial Energy Audit Sri Lanka | Preliminary vs Detailed | EnerFab",
"desc": "What a factory energy audit involves in Sri Lanka: preliminary vs detailed audits, what engineers measure in boilers, steam, compressed air and motors, and how ESCO projects pay back.",
"img": "energy-audit-pipework.jpg",
"date": "2026-11-14",
"divs": ["esco-energy-solutions", "biomass-gasifiers"],
"takeaways": [
    "A preliminary audit is a short walk-through that spots obvious savings; a detailed audit measures and quantifies them.",
    "Boilers and steam systems, compressed air, motors and lighting are where most factories lose energy.",
    "The result should be a list of measures, each with a cost, a saving and a payback period.",
    "Under an ESCO arrangement, the contractor implements the measures and guarantees the payback.",
],
"body": """
<h2>Preliminary and detailed audits</h2>
<div class="table-wrap"><table>
<thead><tr><th scope="col"></th><th scope="col">Preliminary audit</th><th scope="col">Detailed audit</th></tr></thead>
<tbody>
<tr><th scope="row">Purpose</th><td>Find the main opportunities quickly</td><td>Quantify savings accurately enough to invest</td></tr>
<tr><th scope="row">Method</th><td>Site walk-through, energy bills, interviews</td><td>Measurements, data logging, analysis of each system</td></tr>
<tr><th scope="row">Output</th><td>Short list of likely measures</td><td>Costed measures with savings and payback</td></tr>
</tbody></table></div>

<h2>What engineers look at</h2>
<h3>Boilers and steam</h3>
<ul>
  <li>Combustion efficiency, measured from flue gas oxygen and temperature</li>
  <li>Steam traps that leak or are stuck open</li>
  <li>Missing or damaged insulation on pipes, valves and flanges</li>
  <li>Condensate that is dumped instead of returned to the boiler</li>
  <li>Blowdown rates and feed-water treatment</li>
</ul>
<h3>Compressed air</h3>
<ul>
  <li>Leaks, which often go unnoticed on a noisy factory floor</li>
  <li>Generation pressure set higher than the process needs</li>
  <li>Compressors running unloaded</li>
</ul>
<h3>Electrical systems</h3>
<ul>
  <li>Motors, pumps and fans running at full speed when variable speed drives would match the load</li>
  <li>Power factor and demand charges</li>
  <li>Lighting levels and controls</li>
</ul>
<h3>Process heat</h3>
<ul>
  <li>Dryers, kilns and ovens: air flows, heat recovery and insulation</li>
  <li>Whether the fuel itself should change, for example from furnace oil to biomass</li>
</ul>

<h2>Turning findings into savings</h2>
<p>A useful audit report ranks each measure by cost and payback, so management can act on the quick wins straight away and plan the larger projects. Measuring again after implementation confirms the savings.</p>
<p>Under the energy service company (ESCO) model, the same contractor that audits the plant implements the measures and guarantees the result, sharing the risk with the factory.</p>

<h2>EnerFab’s ESCO services</h2>
<p>EnerFab provides preliminary and detailed energy audits and other energy studies, and implements energy-saving projects on a turnkey basis with a payback guarantee. It uses modern energy metering instruments and has completed more than 15 detailed energy audits in knitted-garment factories, tea factories and other sectors.</p>
""",
"sources": [
    ("Sri Lanka Sustainable Energy Authority: energy management resources", "https://www.energy.gov.lk/"),
    ("EnerFab: ESCO and innovative engineering (efpl.org)", "https://efpl.org/page2.html"),
],
},
# ---------------------------------------------------------------------------
{
"slug": "mini-hydro-turbine-selection",
"title": "Choosing a mini-hydro turbine: Pelton, Francis or Kaplan",
"seo": "Mini Hydro Turbine Selection: Pelton vs Francis vs Kaplan | EnerFab",
"desc": "How mini-hydro power is calculated from head and flow, and how engineers choose between Pelton, Francis and Kaplan turbines for small hydropower plants in Sri Lanka.",
"img": "hydro-generators.jpg",
"date": "2026-11-14",
"divs": ["mini-hydro-power-plants", "steel-fabrication"],
"takeaways": [
    "Hydropower depends on two numbers: head (the height the water falls) and flow (how much water passes).",
    "Power in kW is roughly 9.81 × flow in m³/s × head in metres × overall efficiency.",
    "Pelton turbines suit high head and low flow, Kaplan turbines low head and high flow, and Francis turbines the range in between.",
    "Reliable flow data over the whole year matters more than any single measurement.",
],
"body": """
<h2>Head and flow</h2>
<p>A hydropower plant turns the energy of falling water into electricity. The power available depends on:</p>
<ul>
  <li><strong>Head:</strong> the vertical height the water drops between the intake and the turbine, in metres.</li>
  <li><strong>Flow:</strong> the volume of water passing through the turbine, in cubic metres per second.</li>
</ul>
<p>The standard estimate is:</p>
<p class="formula">P (kW) ≈ 9.81 × Q (m³/s) × H (m) × η</p>
<p>where η is the overall efficiency of the turbine, generator and drive. For example, 0.5 m³/s falling through 40 m with 80% overall efficiency gives about 9.81 × 0.5 × 40 × 0.8 ≈ 157 kW.</p>

<h2>The three main turbine types</h2>
<div class="table-wrap"><table>
<thead><tr><th scope="col">Turbine</th><th scope="col">How it works</th><th scope="col">Best suited to</th></tr></thead>
<tbody>
<tr><td>Pelton</td><td>Impulse turbine: high-speed jets of water strike cups on a wheel</td><td>High head, relatively low flow</td></tr>
<tr><td>Francis</td><td>Reaction turbine: water flows inward through guide vanes and a fully submerged runner</td><td>Medium head and flow</td></tr>
<tr><td>Kaplan</td><td>Propeller turbine with adjustable blades, often with adjustable guide vanes too</td><td>Low head, high flow, and flows that vary a lot</td></tr>
</tbody></table></div>
<p>The ranges overlap. The final choice comes from the manufacturer’s selection charts for the exact head and flow, along with part-load efficiency, cost and site layout. Turbines can be arranged horizontally or vertically, depending on size and powerhouse design.</p>

<h2>Steps in a mini-hydro project</h2>
<ol>
  <li><strong>Hydrology:</strong> how the stream’s flow varies through the year, ideally as a flow-duration curve built from long-term records.</li>
  <li><strong>Survey:</strong> accurate head measurement and the route for the intake, channel and penstock.</li>
  <li><strong>Design flow and turbine selection:</strong> choosing the design flow and turbine type, and how many units.</li>
  <li><strong>Civil and steel works:</strong> weir, intake, channel, forebay, penstock and powerhouse.</li>
  <li><strong>Electromechanical supply and installation:</strong> turbine, generator, controls and grid connection.</li>
  <li><strong>Commissioning and servicing.</strong></li>
</ol>

<h2>EnerFab and GUGLER</h2>
<p>EnerFab (Pvt) Ltd is the sole agent in Sri Lanka for GUGLER Water Turbines, which supplies Kaplan, Pelton and Francis turbines with outputs from 5 kW to 10 MW, horizontal or vertical. EnerFab offers design, engineering, manufacturing, installation and servicing for all heads and outputs. It also fabricates steel penstock pipelines and small hydro plant structures, and installed the GUGLER machinery at an Aitken Spence Power mini-hydro site in 2009.</p>
""",
"sources": [
    ("US Department of Energy: Types of hydropower turbines", "https://www.energy.gov/eere/water/types-hydropower-turbines"),
    ("EnerFab: mini-hydro power plants (efpl.org)", "https://efpl.org/page2.html"),
],
},
]
