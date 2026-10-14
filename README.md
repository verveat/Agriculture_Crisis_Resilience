![Banner](images/readme_banner_github.png)

# Agricultural Market Resilience in Germany

*A Comparative Analysis of Soft Wheat, Barley and Potato Markets*

# Project Overview

**Problem.**<br> Agricultural markets are exposed to external shocks that can disrupt supply chains, increase price volatility, and affect domestic production and trade. However, the effects of these shocks may differ across agricultural commodities, as markets vary in their vulnerability and capacity to adjust to changing conditions. Comparing soft wheat, barley, and potato markets in Germany can provide insights into these differences and their implications for market resilience.

**Goal.**<br> Analyze the economic mechanisms of selected agricultural commodities across three dimensions and throughout the pre-crisis, crisis, and post-crisis phases to answer the following research questions.

1. Availability and Supply Balance. How do domestic production, imports, exports, stocks, and domestic use change?
2. Price Stability. How do the three agricultural markets differ in their vulnerability to external shocks and their capacity to adapt?
3. Adjustment and Recovery. How do supply balances and prices evolve during and after crises, and how quickly do they return toward pre-crisis conditions?

**Approach.**<br> Data collection and preparation, exploratory analysis, and visualisation of market and price dynamics, as well as international trade dependencies, to investigate shock magnitude, response timing, shock duration, and recovery patterns.


## Conceptual Framework: Risk Categories and Transmission Mechanisms

There is no single universally applicable classification of all crises affecting agricultural markets. This overview draws on established institutional frameworks, particularly the OECD's agricultural risk management framework and the FAO's work on agricultural supply chains. The categories below provide a structured synthesis rather than a verbatim reproduction of one official taxonomy.

| **Risk Category**                   | **Examples of Risk Drivers**                                          | **Potential Transmission Mechanisms**                                     |
| ----------------------------------- | --------------------------------------------------------------------- | ------------------------------------------------------------------------- |
| **Production Risks**                | Droughts, heatwaves, floods, pests and diseases                       | Crop yields, production volumes and domestic supply                       |
| **Market and Price Risks**          | Shifts in supply and demand, global commodity price shocks and market disruptions              | Transmission of international price changes to domestic producer prices, changes in farm revenues and production incentives                     |
| **Input Cost Risks**                | Energy, fertiliser, fuel and other input price increases              | Production costs, input use and production decisions                      |
| **Trade and Supply Chain Risks**    | Export restrictions, transport disruptions and logistical bottlenecks | Import availability, trade flows, delivery times and transport costs      |
| **Financial Risks**                 | Interest rate changes, credit constraints and liquidity shortages     | Financing costs, investment and farm liquidity                            |
| **Policy and Institutional Risks**  | Changes in agricultural, trade or environmental policies              | Market incentives, trade conditions and production decisions              |
| **Geopolitical and Systemic Risks** | Armed conflicts, pandemics and major cross-border economic disruptions     | Disruptions to energy and input supplies and prices; labour shortages, interruptions to international trade, shifts in aggregate demand |

*Conceptual sources: [OECD – Strengthening Agricultural Resilience in the Face of Multiple Risks (2020)](https://doi.org/10.1787/2250453e-en) · [FAO – Guidelines to Increase the Resilience of Agricultural Supply Chains](https://www.fao.org/markets-and-trade/areas-of-work/emerging-trends-challenges-and-opportunities/guidelines-to-increase-the-resilience-of-agricultural-supply-chains/).The risk categories presented here constitute a structured synthesis of established institutional frameworks and may overlap. They do not represent a single, universally adopted official classification. The risk drivers illustrate factors and developments that may generate or amplify risks, while the transmission mechanisms describe potential pathways through which these risks may affect agricultural markets. Their relevance and empirical effects on the German soft wheat, barley and potato markets will be investigated in this project. Additional sources: [FAO – Agricultural Commodity Markets](https://www.fao.org/publications/fao-flagship-publications/the-state-of-agricultural-commodity-markets/) · [European Commission – Fertiliser Markets](https://agriculture.ec.europa.eu/data-and-analysis/markets/overviews/market-observatories/fertilisers_en) · [UNCTAD – Maritime Trade Disruptions](https://unctad.org/system/files/official-document/rmt2024_en.pdf). These sources provide complementary perspectives and inform the synthesis developed for this project.*


## Historical Events and Potential Market Transmission (1990–2026)

| Period | Event and Classification | Primary Risk Category | Potential Transmission Mechanism | Relevance to the Research | Sources |
|---|---|---|---|---|---|
| 1990–1991 | German reunification and restructuring of East German agriculture (*structural transition*) | Policy and Institutional Risks | Institutional change, restructuring of farms and changing market conditions may have affected production decisions and market integration. | Provides structural context for the long-term analysis; not treated as a short-term crisis. | Lambrecht (1990), DIW Berlin, [DDR-Landwirtschaft vor erneutem Umstrukturierungsprozess](https://www.diw.de/de/diw_01.c.486342.de/publikationen/wochenberichte/1990_33_3/ddr-landwirtschaft_vor_erneutem_umstrukturierungsprozess.html) |
| 1992 | Reform of the Common Agricultural Policy (CAP) (*policy change*) | Policy and Institutional Risks | Changes in agricultural policy incentives may have influenced production decisions and market conditions. | Provides institutional context; specific effects require evidence on individual reform measures and implementation. | European Commission, [CAP expenditure and reform history](https://agriculture.ec.europa.eu/data-and-analysis/financing/cap-expenditure_en) |
| 2003 | Severe drought and heat in Germany (*production shock*) | Production Risks | Heat and water stress can reduce yields, affecting production volumes and potentially domestic availability and prices. | Relevant for testing production fluctuations. Crop-specific effects on barley and potatoes require separate assessment. | Umweltbundesamt, [Yield fluctuations](https://www.umweltbundesamt.de/en/monitoring-on-das/cluster/agriculture/lw-I-2/indicator) |
| 2007–2008 | Global food-price crisis (*international market shock*) | Market and Price Risks; Trade and Supply Chain Risks | International commodity-price changes and trade conditions may transmit to domestic markets, with varying degrees of price transmission. | Provides context for international price volatility; global prices must not be equated with German producer prices. | FAO (2009), [The State of Agricultural Commodity Markets: High food prices and the food crisis](https://www.fao.org/4/i0854e/i0854e00.htm) |
| 2018–2019 | Severe drought and heat stress in Germany (*production shock*) | Production Risks | Weather-related yield losses may affect production, domestic supply and trade requirements. | Important for comparing production stability across the three crops. Crop-specific impacts must be assessed using the BLE data and relevant crop statistics. | Umweltbundesamt, [Yield fluctuations](https://www.umweltbundesamt.de/en/monitoring-on-das/cluster/agriculture/lw-I-2/indicator) |
| 2020–2021 | COVID-19 pandemic and associated restrictions (*systemic and logistical shock*) | Geopolitical and Systemic Risks; Trade and Supply Chain Risks | Restrictions, labour constraints, demand shifts and logistical bottlenecks may affect agricultural supply chains. | Provides a system-wide context. Effects on barley, potatoes and soft wheat must be assessed rather than presumed. | European Commission Joint Research Centre (2022), [The COVID-19 pandemic in the agri-food supply chain: Impacts and responses](https://publications.jrc.ec.europa.eu/repository/handle/JRC128581) |
| 2021–2022 | Energy and fertiliser price shock (*input-cost shock*) | Input Cost Risks; Market and Price Risks | Higher energy and fertiliser prices can increase production costs and affect input use, margins and potentially yields. | Relevant to adjustment under cost pressure. The shock began before the full-scale invasion of Ukraine, so the periods should not be conflated. | European Commission, [Fertilisers Market Observatory](https://agriculture.ec.europa.eu/data-and-analysis/markets/overviews/market-observatories/fertilisers_en); European Commission (2022), [Safeguarding food security and reinforcing the resilience of food systems](https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:52022DC0133) |
| From February 2022 | Russia’s full-scale invasion of Ukraine (*geopolitical shock*) | Geopolitical and Systemic Risks; Trade and Supply Chain Risks | Disruptions and uncertainty in grain, energy and agricultural-input markets may affect prices, availability and trade flows. | Important context for supply and trade adjustments; temporal association alone does not establish causality. | European Commission (2022), [Safeguarding food security and reinforcing the resilience of food systems](https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:52022DC0133) |
| 2022–2024 | Persistent inflation and food-price pressures (*macroeconomic development*) | Market and Price Risks; Input Cost Risks | Changes in input, energy and transport costs, alongside broader inflation, may influence agricultural prices and margins. | Context for a price-stability analysis. Define the period using a consistent price series; do not treat inflation as a single isolated event. | European Commission (2022), [Safeguarding food security and reinforcing the resilience of food systems](https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:52022DC0133); [Destatis price statistics](https://www.destatis.de/EN/Themes/Economy/Prices/_node.html) |
| Late 2023–2024 | Red Sea and Suez shipping disruptions (*logistics shock*) | Trade and Supply Chain Risks; Geopolitical and Systemic Risks | Route diversions and longer shipping distances can increase freight costs, transit times and supply-chain uncertainty. | A plausible indirect transmission channel; a direct effect on the three German crop markets remains to be established. | UNCTAD (2024), [Review of Maritime Transport 2024: Navigating maritime chokepoints](https://unctad.org/publication/review-maritime-transport-2024) |
| February–October 2026 | Conflict in the Middle East and associated energy and fertiliser price pressures (*ongoing geopolitical shock*) | Geopolitical and Systemic Risks; Input Cost Risks | Higher energy and fertiliser import prices may raise agricultural input costs; effects on farm margins, output and crop prices require separate investigation. | A current case for monitoring cost pressures, not a completed episode of recovery. Destatis reported April 2026 import prices for energy 31.0% above April 2025 and fertiliser and nitrogen-compound import prices 22.9% above April 2025. These are import-price indicators, not German agricultural producer prices. | Destatis (29 May 2026), [Import prices in April 2026](https://www.destatis.de/EN/Press/2026/05/PE26_180_614.html); European Commission, [Ensuring availability and affordability of fertilisers](https://agriculture.ec.europa.eu/common-agricultural-policy/agri-food-supply-chain/ensuring-availability-and-affordability-fertilisers_en) |

*### Conceptual Framework and Methodological Note*

*The risk categories used in this study are an analytical synthesis informed by the OECD’s framework for agricultural risk management and resilience and by FAO work on agricultural supply chains. They are not presented as a universally standardised or official taxonomy. The framework distinguishes production risks, market and price risks, input-cost risks, trade and supply-chain risks, financial risks, policy and institutional risks, and geopolitical and systemic risks.*

*The historical timeline identifies external shocks and structural changes that may be relevant to the resilience of German barley, potato and soft wheat markets. The transmission mechanisms listed are hypotheses rather than established causal effects. Their relevance must be assessed using product-specific evidence and the observed BLE supply-balance indicators. Calendar-year events must be aligned carefully with the BLE financial-year observations (e.g. 2018/19). Annual harvest outcomes are treated as empirical observations rather than classified as crises by default. The 2026 entry reflects information available as of October 2026 and should be updated as new evidence becomes available.*

***Framework source:*** OECD (2020), *Strengthening Agricultural Resilience in the Face of Multiple Risks*. [https://doi.org/10.1787/2250453e-en](https://doi.org/10.1787/2250453e-en)*


# Rationale for Data Selection and Observation Periods

The data selection is guided by the project's three research dimensions: **Availability and Supply Balance, Price Stability, and Adjustment and Recovery**. Rather than relying on a single indicator, the analysis integrates agricultural production and yield statistics, supply balances, foreign-trade data, agricultural price series, and input price indices. This multidimensional approach provides a basis for examining market developments and comparing soft wheat, barley and potatoes in Germany.

## Historical Data Horizon and Observation Periods

Where sufficiently comparable observations are available, historical data extending back to 1991 are retained to provide long-term context and help assess whether more recent market developments differ from earlier fluctuations. The 2003 drought and heatwave in Germany are considered as part of this historical context, illustrating the relevance of production-related disturbances. However, 2003 is not a primary case in the quantitative comparative analysis. This distinction avoids treating the subsequent years as a recovery period without first establishing whether the relevant market indicators support such an interpretation.

The main comparative business intelligence analysis covers the period from 2008 to 2025, subject to the availability and comparability of the individual datasets. This period is consistent with the available Destatis series for monthly foreign trade and provides a common starting point for the core trade analysis. Individual price, production and supply indicators may cover longer or shorter periods, depending on their historical availability and reporting frequency. Accordingly, the historical data horizon and the observation period of the main analysis are not necessarily identical.

## Data Selection and Analytical Purpose

Each dataset is selected according to its contribution to the research dimensions. Supply balances provide information on production, trade and domestic use. Harvest statistics capture changes in cultivated area, yields and production volumes. Foreign-trade statistics enable the analysis of imports and exports, including monthly fluctuations. Agricultural price series support the examination of price movements and volatility, while input price indices provide context for potential cost-related transmission mechanisms.

The datasets differ in frequency, product definitions, reporting periods and historical coverage. These differences will be documented during data preparation and considered when selecting indicators and interpreting results. Where reporting periods or product categories cannot be aligned sufficiently, comparisons will be restricted to those supported by the available data. Agricultural marketing years and calendar years will not be treated as interchangeable without appropriate justification.

## Selection of Historical Events and Potential Transmission Mechanisms

The project uses selected historical disturbances to examine how market developments may coincide with different types of shocks. The primary cases are the 2018 drought and heatwave in Germany and the energy, input-cost and geopolitical disturbances that intensified from 2021 onwards, including Russia's full-scale invasion of Ukraine in February 2022. The COVID-19 period from 2020 to 2021 may be included as an additional case where time and data availability permit.

These cases represent different but potentially overlapping transmission mechanisms. Weather-related production shocks may be reflected in yields and harvest volumes. Trade and supply-chain disruptions may coincide with changes in import and export quantities, while increases in energy and fertiliser prices may influence production costs and subsequent production decisions. These relationships are treated as hypotheses rather than assumed causal effects. The temporal coincidence of an event with a change in prices, production or trade is not sufficient to establish causality.

## Comparative Assessment of Pre-Crisis, Crisis and Post-Crisis Periods

Pre-crisis, crisis and post-crisis periods will be defined separately for each selected case, taking into account the timing of the disturbance, the expected delay between the event and its potential market effects, and the availability of comparable observations. The same time windows will not automatically be applied to every event or commodity. Initial observation windows will be adjusted where necessary to reflect the frequency of the data and the characteristics of each market.

Potential reference periods will be evaluated using the relevant indicators rather than assumed to represent normal market conditions in advance. Adjustment and recovery will be assessed only where the available observations support a meaningful comparison with the selected reference period. A return towards an earlier price or production level will not, on its own, be interpreted as evidence that all dimensions of market resilience have been restored.

Finally, the analysis distinguishes between documented historical events, observed market developments and causal explanations. Because multiple disturbances may overlap, descriptive time-series analysis alone cannot isolate their individual effects. The main quantitative analysis ends in 2025. Data for 2026 may be used for supplementary context where sufficiently complete and comparable observations are available, but will not be treated as a complete post-event period when the evidence is insufficient to assess adjustment and recovery reliably.


## Data Sources

### 1. Availability and Supply Balance

This dimension uses publicly available official statistics for Germany.

**BMELH – Official Agricultural Statistics (Production Balance, Market Balance, Overall Balance, Financial Year, 2011-2025)**

[*Soft Wheat - Barley Supply Balance*](https://www.bmel-statistik.de/ernaehrung/versorgungsbilanzen/getreide) | [*Potato Supply Balance*](https://www.bmel-statistik.de/ernaehrung/versorgungsbilanzen/kartoffeln)

**BLE – Open Data (Overall supply balance, Financial Year, 1991-2025)**

[*Soft Wheat - Barley Supply Balance*](https://open-data.ble.de/dataset/versorgungsbilanz-getreide) | [*Potato Supply Balance*](https://open-data.ble.de/dataset/versorgungsbilanz-kartoffeln)

*Data quality note: The combined dataset contains 1,646 records: 578 for barley, 490 for potatoes, and 578 for soft wheat. The differences in record counts were checked against the original source data and were confirmed to exist in the raw data. Therefore, the differences were not caused by the data consolidation process. Missing values are retained for further investigation rather than being automatically replaced or removed. The dataset contains 17 records per year for barley and soft wheat and 14 records per year for potatoes. A comparison of balance positions for the financial year 1991/92 showed that the product balances differ in their structure and include product-specific positions and differently named categories. The differences in record counts were also verified against the original source data. No records have been deleted, and no missing values have been replaced. The original data structure is retained for further analysis.*

**DESTATIS - Harvest and Farm Report (Area under Cultivation, Production, Yield, Year, 2010-2026)**

[*Winter Wheat - Spring Wheat - Winter Barley - Summer Barley - Potato*](https://genesis.destatis.de/datenbank/online/url/fb99c6a2)

**DESTATIS - Foreign Trade Statistics (Monthly, 2008-2025)**

[*Foreign Trade Wheat and Meslin - Barley - Potato*](https://genesis.destatis.de/datenbank/online/url/aeb0bf5d)

**Methodological references**

**Agricultural commodity balances:** [BMEL – Grundlagen der Versorgungsbilanzen](https://www.bmel-statistik.de/ernaehrung/versorgungsbilanzen/grundlagen)

**Foreign trade product classification:** [Destatis – Warenverzeichnis für die Außenhandelsstatistik](https://www.destatis.de/DE/Methoden/Klassifikationen/Aussenhandel/warenverzeichnis-aussenhandel.html)

### 2. Price Stability

**DESTATIS - Price Index (Monthly, 2020=100, 1991-2026)**

[*Price Index Bread Wheat - Feed Wheat - Feed Barley - Malting Barley - Seed Potato - Ware Potato*](https://genesis.destatis.de/datenbank/online/url/465076c8)

**BMELH - Agricultural Producer Prices (Year, 2009-2024)**

[*Soft Wheat - Barley - Malting Barley - Ware Potato*](https://bmel-statistik.de/preise/absolute-agrarpreise?utm_source=chatgpt.com)

**FAOSTAT - AGricultural Producer Prices (Monthly, 1991-2026)**

[*Wheat - Barley - Potato*](https://www.fao.org/faostat/en/#data/PP)

**DESTATIS - Purchase Price Indices of Agricultural Inputs (Quarterly, 2020=100, 1991-2026)**

[*Energy and Lubricants - Fertiliser*](https://genesis.destatis.de/datenbank/online/url/a049c6fc)


## Methodology and Analytical Framework

## Analysis and Visualisations

## Key Findings and Limitations

### Limitations

**Differences in Product Classifications.** The data sources use different product classifications and levels of aggregation. For example, wheat and barley statistics may distinguish between crop types or intended uses, while potato statistics follow their own product definitions. Direct comparisons are therefore only appropriate where the underlying definitions are sufficiently comparable.

**Data Availability and Coverage.** Historical coverage varies across sources and indicators. The effective analysis period may consequently differ depending on data availability and the research question.

**Differences in Reporting Periods and Frequency.** The datasets include annual, monthly and quarterly observations and may refer to calendar years or agricultural and marketing years. These differences must be considered when aligning observations and defining crisis and recovery periods.

**Differences in Price Measures.** Price indices and absolute producer prices measure different aspects of price development. Comparisons require consideration of their units, reference periods, product definitions and statistical methodologies.

**Descriptive Nature of the Analysis.** The analysis identifies patterns and potential relationships between production, trade, prices and input costs. However, descriptive time-series analysis alone cannot establish that specific crises caused the observed market changes.

**Assessment of Market Resilience.** The assessment depends on the selected indicators, reference periods and availability of post-crisis data. Changes in production, supply or prices capture only selected dimensions of resilience and do not necessarily establish the overall capacity of a market to absorb, adapt to or recover from shocks.

**Incomplete Data for Recent Periods.** 
Data for the most recent period may be incomplete, preliminary or subject to revision. The main quantitative analysis therefore focuses on 2008–2025, subject to the coverage and comparability of the individual datasets. More recent observations may be included as supplementary context where appropriate.

## Project Status

* 🟢 Project Concept
* 🟢 Data Collection
* 🟢 Data Exploration
* 🟡 Data Cleaning and Preparation
* 🔴 Data Analysis
* 🔴 Data Visualisation
* 🔴 Final Report and Insights

**Legend:** 🟢 Completed · 🟡 In Progress · 🔴 Not Started


# Author

Kordula Pfeiffer. Agricultural and Food Economist. [LinkedIn.](https://www.linkedin.com/in/kordulapfeiffer/)


