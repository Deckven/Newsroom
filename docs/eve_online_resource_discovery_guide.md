# **The Socio-Technical Architecture of New Eden: A Critical Audit of 2026 EVE Online Information Ecosystems**

The persistent universe of New Eden operates as a sophisticated laboratory for virtual socio-economics, where the traditional boundaries between game mechanics and external informational infrastructure have effectively dissolved. In EVE Online, the mastery of asymmetric information is not merely a competitive advantage but a prerequisite for sovereignty. As the simulation enters its twenty-third year of operation in 2026, the digital ecosystem supporting its players—colloquially known as capsuleers—has reached a level of maturity characterized by high-fidelity data synchronization, professional-grade software development, and a deeply integrated meta-narrative. The current state of these resources reflects a shift from fragmented, hobbyist-driven tools to comprehensive, multi-platform suites that manage everything from micro-market fluctuations to macro-political wars.

The operational landscape of 2026 is defined by the EVE Online Strategic Roadmap, which outlines a three-expansion cycle designed to revitalize core game systems and expand the narrative reach of Factional Warfare (FW).1 This strategic direction has necessitated a corresponding evolution in third-party tools, as players require more granular intelligence to navigate the "Theaters of War" and "Military Campaigns" that now dictate the flow of wealth and power across the cluster.1 The following analysis provides an exhaustive categorization and evaluation of the primary, reliable, and frequently updated resources that constitute the current capsuleer information environment.

## **Developer Communications and Technical Roadmaps**

The foundation of the 2026 informational framework is established by CCP Games through official developer channels. These sources define the mechanical boundaries of the universe and provide the primary data points upon which all third-party analysis is built. The "Directors' Letter: 2026 & Beyond" serves as the definitive strategic document for the current era, committing the development team to three major expansions focused on escalating Factional Warfare into a conflict with "real stakes".1

### **The 2026 Expansion Cycle and "Theaters of War"**

The roadmap for 2026 is structured around a sequential narrative saga, where each expansion acts as a chapter in a larger conflict. This approach represents a fundamental shift in how EVE is built, moving away from isolated updates toward a model of continuous, evolving systems that are refined over several releases.1 The first of these updates, "EVE Evolved," arrived in February 2026, introducing significant visual and artistic refinements alongside gameplay updates.1

| Expansion / Strategic Milestone | Release Period | Focus and Key Features |
| :---- | :---- | :---- |
| **EVE Evolved (Version 23.02)** | February 2026 | Visual overhauls of asteroids and ORE ships; Neocom customization; search functionality 1 |
| **March Major Update** | March 2026 | Major gameplay adjustments following EVE Evolved feedback 1 |
| **Catalyst Expansion (Legacy Support)** | Late 2025 | Introduction of new ores, ships, and the 2D map interface; carrier updates 4 |
| **Expansion Chapter 2 (Legion)** | Q2 2026 | Formalization of Military Campaigns and Empire-backed contracts 1 |
| **Expansion Chapter 3** | Q4 2026 | Resolution of the 2026 saga; focus on "Theaters of War" escalation 1 |
| **EVE Vanguard Steam Early Access** | Post-Summer 2026 | Integrated ground-based gameplay; crossover world events 1 |

The technical documentation provided in patch notes is exhaustive and essential for maintaining informational parity. Version 23.02, for instance, detailed the "Mineable Asteroid Renovation," which rebuilt asteroids with new high-fidelity models and textures, while also modernizing the visual effects across ORE ship hulls.3 For industrial players, these updates are not merely cosmetic; they influence the readability of resource-rich environments and the efficiency of gathering operations.3 Furthermore, the patch notes frequently include critical balancing changes, such as the 50% reduction in Small Energy Turret activation costs and adjustments to ship powergrids and capacitor capacities.3 Such data is immediately ingested by fitting tools and theory-crafting platforms to ensure that player builds remain optimized for the current meta.

### **Official News Portals and Archive Management**

The EVE Online News portal remains the primary source for community-wide announcements, including the "Monthly Economic Reports" (MER) and the "Community Beat".4 The news archive for 2026 demonstrates a high cadence of updates, often featuring multiple posts per week regarding in-game events like the Lunar New Year celebrations or the EVE Creator Awards.8 This official feed is supplemented by specialized technical blogs, such as the "EVE Evolved: Sharper Skies" series, which provide deep dives into the graphical and technical advancements of the game engine.4

## **Data Infrastructure and API Accessibility**

The reliability of the entire third-party ecosystem is predicated on the EVE Swagger Interface (ESI), the primary API provided by the developers. The ESI allows external applications to retrieve real-time data on everything from market orders to character skills.9 In 2026, the management of this data has become more sophisticated, with the emergence of specialized Model Context Protocol (MCP) servers that act as streamlined interfaces for market data.9

### **The API Paradigm and Market Information Disclosure**

Market data in EVE is governed by strict rules regarding location, price, and volume. The ESI provides order book data that is typically refreshed every five minutes.10 Developers must manage these refresh rates alongside ESI's rate limits and error handling to provide accurate analysis. The "EVE Online Market MCP Server" represents a significant step forward in this area, offering a public interface that intelligently manages rate limits to provide real-time order books for various regions and structures.9

The disclosure of information through these APIs includes:

* **Order Book Data**: Detailed instructions on buy and sell limit orders, including unique order IDs, location IDs, and volume remaining.10  
* **Historical Trends**: Daily high, low, and average trade prices, along with total volume for assets dating back as far as one year.10  
* **Structure Resolution**: The ability to resolve the location of player-owned structures (Citadels, Engineering Complexes), though non-public structures often require crowd-sourced data for accurate out-of-game analysis.10

This data layer is further supported by the "Static Data Extract" (SDE), which contains non-changing information like the locations of stars and planets, ship attributes, and blueprint requirements.11 Developers like Steve Ronuken provide converted versions of the SDE in MySQL, SQLite, and Postgresql formats, which are foundational for almost all third-party industrial and planning tools.11

## **Ship Configuration and Simulation Tools**

Ship fitting is perhaps the most critical technical activity in EVE Online. The ability to simulate how a ship will perform under various conditions—without risking the actual hull—is essential for tactical planning.

### **Python Fitting Assistant (Pyfa)**

As of early 2026, Pyfa remains the premier cross-platform ship fitting assistant. The tool allows capsuleers to create, experiment with, and save ship fittings using a high-fidelity simulation engine that accounts for character skills, implants, and environmental effects.12 Pyfa is an open-source project written in Python, and its continued relevance is maintained through frequent updates on its GitHub repository.12

The version history of Pyfa in late 2025 and early 2026 demonstrates the tool's commitment to staying synchronized with the game client.

| Pyfa Version | Release Date | Critical Updates and Context |
| :---- | :---- | :---- |
| **v2.65.4** | January 13, 2026 | Reverted clipboard management changes that caused issues on Windows systems 14 |
| **v2.65.3** | January 11, 2026 | Integrated Succubus buffs and other changes from the 23.02 release 14 |
| **v2.65.2** | December 11, 2025 | Added support for Anhinga and Skua prize ships; fixed crash regressions 14 |
| **v2.65.1** | December 9, 2025 | Integrated the Perseverance ice mining destroyer and Wightstorm boosters 14 |

Pyfa's strength lies in its depth. It provides a level of detail far beyond the in-game simulator, allowing users to calculate effective hit points (EHP), capacitor stability, and damage application against specific target profiles.15 Its integration with the ESI allows users to import their character's skills directly, ensuring that simulations are tailored to their specific capabilities.12

### **EVE Workbench and Web-Based Alternatives**

While Pyfa is the tool of choice for deep theory-crafting, **EVE Workbench** has established itself as a versatile, web-based alternative. It focuses on social integration and market awareness. EVE Workbench allows users to browse a live feed of sell and buy orders from major trade hubs like Jita and Amarr, providing estimated ISK costs for fittings in real-time.16 One of its standout features is the "Fittings" module, where players can upload fits using the EFT/Pyfa standard and share them with the community, complete with Reddit-style upvoting and commenting systems.16

For capsuleers on the move, the **Mobile EVE Fitting Tool** (MEFT) and the web-based tool **Rift** provide alternatives to desktop-based simulation.15 MEFT leverages technologies like Java and Cloud Storage to provide a simulation experience on Android devices, addressing a long-standing gap in the mobile resource landscape.15

## **Market Analytics and Trading Infrastructure**

The EVE Online economy is a legitimate field of study, and the tools available for market analysis are among the most sophisticated in the gaming world. Successful traders utilize these resources to identify market inefficiencies, track price movements, and manage large-scale logistics.

### **Comprehensive Suites: EVE OS and jEveAssets**

Modern market analysis has moved toward consolidated suites. **EVE OS** is a premier example, providing a dashboard that tracks net worth, market orders, and asset breakdowns across all characters on an account.18 Its "Market Browser" and "Screener" modules allow traders to scout for high-volume items and identify potential trade "flips" by evaluating the spread between buy and sell orders.18

**jEveAssets** remains an essential utility for asset management. It is a desktop application that tracks all items across all accounts, allowing users to search for specific modules or hulls and calculate the total value of their holdings.19 In a universe with thousands of star systems, the ability to centralize inventory data is crucial for preventing capital stagnation.

### **Hub-Specific Analysis: Fuzzwork and MCP Servers**

For a granular look at trade hub activity, the resources provided by **Fuzzwork** are invaluable. Fuzzwork Market Data provides daily updates on the "Forge Aggregates" (Jita) and other major hubs, tracking weighted averages, medians, and total volumes for nearly every item in the game.20

| Market Statistics (Hub: Jita IV-4) | Metric Type (Feb 28, 2026\) | Value / Volume |
| :---- | :---- | :---- |
| **Sell Orders** | Total Active Orders | 256,204 20 |
| **Buy Orders** | Total Active Orders | 95,739 20 |
| **Tritanium (Buy)** | 5% Buy Average | 3.86 ISK 20 |
| **Tritanium (Sell)** | 5% Sell Average | 4.38 ISK 20 |

The emergence of MCP servers like **mcpmarket.com** has further democratized access to this data, providing a programmatic interface that allows players to build their own automated price tracking and trading strategy tools.9 These tools are increasingly necessary as players contend with the "phantom liquidity" of player-owned structures, which can often misrepresent the actual availability of goods in a region.18

## **Industrial Production and Supply Chain Management**

Industry in EVE Online involves a multi-stage production process that includes resource extraction, refining, reaction processing, and final assembly. Managing this chain requires precise calculations of material requirements and profit margins.

### **Production Planners: Ravworks and Triff.Tools**

**Ravworks** has emerged as a favorite among industrialists due to its intuitive design. Inspired by the ease of use of Evepraisal and the technical depth of Fuzzwork, Ravworks allows users to paste in a list of desired products and their current material stocks.21 The tool then iterates through the entire production tree, accounting for industry configuration (efficiencies, taxes, job slots) to generate a complete production plan.21 This include "Invention" analysis, which helps players determine the expected costs and successes when attempting to create Tech II blueprints.21

A newer entrant, **Triff.Tools**, focuses on the "Industrial Revolution" meta of 2026\. It provides accurate calculators for costs across multiple different products simultaneously, featuring structural and rig modifiers for reactions and final assembly.23 The tool includes an "Ore Reprocessor" that helps miners figure out the optimal ore mix to refine for a specific production batch.23

### **Planetary Production and Colony Management**

Planetary Industry (PI) is a significant source of passive income but requires meticulous management of extraction cycles and factory links. **Planets in Space** provides an online viewer for PI setups and Discord reminders for extraction resets, helping players maintain constant production.24

The **EVE PI Manager** is a more comprehensive tool that synchronizes skills and PI data via ESI.26 It features a dashboard that alerts users to expiring extractors, stalled factories, or storage overflow. One of its most innovative features is the "PIBLE" (Planetary Interaction Bible), an AI-generated wiki that helps players understand the complex relationships between different planetary commodities.26

## **Navigational Intelligence and Wormhole Mapping**

In the information-scarce environment of wormhole space (J-space), mapping tools are the difference between life and death. Because wormhole connections are temporary and hidden from the standard map, community-developed software is used to track "chains" of systems.

### **Primary Mapping Tools: Pathfinder, GalaxyFinder, and Tripwire**

Three tools dominate the navigational landscape in 2026, each with distinct philosophies. **Pathfinder** is favored by large, organized corporations for its complexity and "Session Sharing" features, which allow multiple players to collaborate on a single map in real-time.27 It is often self-hosted by alliances to ensure maximum data security.

**GalaxyFinder** emphasizes simplicity and ease of use. It is a browser-based app that tracks a player's location via ESI and automatically registers connections as they are jumped.28 Its "information at a glance" approach makes it ideal for smaller groups or newer players.28

**Tripwire** remains a staple, particularly for its integration with the **EVE-Scout** community. Because EVE-Scout shares its data publicly through Tripwire, all users have access to live scanning data for the Thera system, the most famous wormhole hub in the game.30

| Mapping Tool | Development Status (2026) | Key Strengths |
| :---- | :---- | :---- |
| **GalaxyFinder** | Active (© 2026 Jeremy Shore) | User-friendly UI; fast onboarding 28 |
| **Pathfinder** | Active (Community-maintained) | High complexity; extensive customization; session sharing 27 |
| **Tripwire** | Active (New Public App Instance) | Organized chain drawing; public Thera/EVE-Scout data 30 |
| **EVEeye** | Active (Cross-platform) | Combines Dotlan, in-game maps, and WH mapping 28 |

The choice of mapper is often a matter of organizational preference. While Pathfinder offers more depth, the "buggy" behavior sometimes noted in Tripwire's chain drawing is often outweighed by the reliability of its public data sharing.28

## **Intelligence Gathering and PvP Analysis**

Information is the primary weapon in PvP warfare. Tools that track player movement, kill history, and fleet activity are essential for both offensive planning and defensive posture.

### **Essential Intel Tools: zKillboard and DOTLAN**

**zKillboard** is the premier platform for tracking combat activity. By ingesting killmails from the ESI, it provides a permanent record of every ship destroyed in the game.19 Commanders use zKillboard to analyze the ship fits and tactics of their rivals, as well as to monitor the activity levels of corporations in a particular region.

**DOTLAN EVE Maps** provides vector-based maps that display sovereignty, occupancy, and movement statistics.19 In 2026, DOTLAN is still the standard for route planning and monitoring Factional Warfare occupancy, allowing pilots to see at a glance which systems are currently changing hands.32

### **Specialized Intelligence: EVE Who and Uedama Scout**

For more granular intelligence, **EVE Who** provides a directory for listing corporation and alliance members, which is vital for vetting potential recruits or identifying corporate infiltrators.19 In high-sec, the **Uedama Scout** Twitch feed offers 24/7 live monitoring of ganking hotspots, giving haulers a real-time view of the dangers they may face when transiting through systems like Uedama, Sivala, or Ahbazon.19

The **NPSI Community Gateway** (Not Purple Shoot It) serves as a central calendar for public fleets.19 This resource is essential for players who wish to engage in high-level PvP without joining a major political bloc, as it lists open fleets from groups like **Bombers Bar** and **Spectre Fleet**.33

## **Educational Resources and Community Knowledge**

The steep learning curve of EVE Online is mitigated by a robust educational infrastructure maintained by veteran players.

### **EVE University Wiki: The Gold Standard**

The **EVE University Wiki** is the most comprehensive learning resource for the game. As of February 28, 2026, it is a highly active project with over 4,550 articles and a dedicated community of contributors.34 The wiki is part of the CCP Partnership Program, ensuring its information is accurate and aligned with current developer intentions.34 It covers everything from basic "Career Agent" tutorials to advanced wormhole mechanics and diplomatic protocols.34

| Wiki Activity Metric | February 2026 Data | Relevance to Pilots |
| :---- | :---- | :---- |
| **Total Articles** | 4,550 | Exhaustive coverage of all game sectors 34 |
| **Total Edits** | 233,754 | Continuous updating ensures information accuracy 34 |
| **Last Modified Date** | Feb 28, 2026 | Real-time maintenance of current meta 34 |

The wiki also provides standardized ship fits and serves as a clearinghouse for information on the **AIR Career Program**, a key component of the new player experience in 2025 and 2026\.34

### **CapsuleerKit and Curated Directories**

For players overwhelmed by the sheer number of third-party applications, **CapsuleerKit** provides a "Must-Have" directory.19 It curates tools across categories like hauling, market, PvP, exploration, and education, ensuring that pilots are using active and proven applications.19 This directory includes links to independent forks of classic tools, such as the community-maintained version of **EveMon**, ensuring that legacy tools remain functional in the modern era.19

## **Media, Podcasts, and Geopolitical Analysis**

The meta-game of EVE Online is discussed extensively in various media formats. These resources provide the context and narrative that turn the cold data of market orders and killmails into a living history of New Eden.

### **Active Podcasts and News Outlets**

The podcast landscape in 2026 is vibrant, with several long-running shows providing weekly updates. **The Oz Report** is the definitive source for market analysis and economic commentary, hosted by market guru and CSM member Oz.35 With over 200 episodes, the show provides granular detail on fluctuations in PLEX prices, raw material flooding, and the impact of quarterly earnings from CCP’s parent company, Pearl Abyss.35

**Federation Front Line Report (FFLR)** focuses specifically on Factional Warfare from a Gallente perspective, providing weekly updates on warzone dynamics and interviews with key military commanders.38 The show is broadcast live on Twitch and archived on YouTube and Spotify, making it one of the most accessible sources for lowsec news.39

Other notable shows include:

* **Talking in Stations (TiS)**: Provides meta-analysis of large-scale wars and developer interviews.41  
* **Voices of New Eden**: A podcast series launched in 2025 that tells the personal stories of real players, from "space famous" leaders to niche industrialist pilots.44  
* **Chronicles of New Eden**: Dedicated to the deep lore and backstory of the EVE universe.40

### **Community News and Blogs**

The traditional news outlets for EVE have evolved. While sites like **EVE News 24** continue to report on major expansions, much of the discourse has moved to dedicated blogs and Reddit.5 **TAGN (The Ancient Gaming Noob)** provides a veteran's perspective on the game's evolution, including detailed reports on coalition splits and the "stagnation" of nullsec.47

**The Nosy Gamer** and **The Greybill** are frequently cited as reliable sources for exploration guides and market commentary.46 These blogs often provide a level of qualitative analysis that the automated data tools cannot, offering insights into the human motivations behind market shifts and alliance moves.

## **Community Social Hubs and Verification Systems**

The social infrastructure of EVE Online has increasingly centralized around the official Discord server and the r/eve subreddit.

### **The Official EVE Online Discord**

Since its launch in 2022, the official EVE Online Discord has become the "coffee shop" of the community.48 It uses a verification bot that allows players to link their in-game characters to their Discord accounts, granting them access to specialized chat channels for fleets and developer Q\&A sessions.49 This server is a vital resource for finding new corporations, hanging out with developers, and getting early news on upcoming events.48

### **The r/eve Ecosystem**

Reddit remains the "town square" for New Eden. It is where propaganda is posted, battle reports are debated, and the general mood of the player base is measured. Subreddits like **r/evejobs** are the primary destination for recruitment, featuring thousands of postings for corps across all sectors of space.51 The subreddit also hosts the "Weekly No Question is Stupid Thread," which provides a safe space for new citizens to seek advice from veterans.7

## **Second-Order Implications of the 2026 Resource Landscape**

The current state of EVE Online resources indicates a profound professionalization of the capsuleer community. The data suggests three primary trends that will define the future of the game’s information environment.

### **The Rise of Integrated Management Suites**

The era of using fifteen separate websites for a single industrial project is ending. In 2026, the trend is toward integrated suites like **EVE OS** and **Triff.Tools** that synthesize market, industrial, and mapping data into a single dashboard.18 This integration allows for "third-order insights," such as calculating how a market price shift in Jita will affect the expected return on investment (ROI) for a currently running reaction job in a distant lowsec system.18

### **Information Democracy vs. Organizational Opacity**

While tools like **GalaxyFinder** and the **EVE University Wiki** have democratized knowledge, major alliances still maintain proprietary tools that are "guarded like precious secrets".52 The development of public alternatives like **EVE OS** and **Ravworks** is a direct response to this, aiming to provide solo players and small corporations with the same analytical power as the multi-thousand-pilot blocs.21 This ongoing struggle between public tools and private intelligence is a central theme of the 2026 informational meta-game.

### **The Impact of AI and Automated Intelligence**

The inclusion of AI-generated content in resources like the **EVE PI Manager** (specifically its PIBLE wiki) suggests a new frontier in community knowledge management.26 As the game’s data becomes more complex, the ability of AI to summarize patch notes, generate industrial schemes, and identify market opportunities will become a critical differentiator between successful and unsuccessful capsuleers. However, as noted by community developers, these tools require careful bug testing and feedback to ensure that "trash code" does not lead to significant financial loss in the virtual economy.23

## **Conclusion**

The online resource ecosystem for EVE Online in 2026 is a testament to the resilience and creativity of its player base. From the technical rigor of **Pyfa** and **ESI-based MCP servers** to the communal wisdom found in the **EVE University Wiki** and **The Oz Report**, capsuleers have access to an unprecedented level of intelligence. The reliability of these resources is maintained through a high cadence of updates that match the developers' own aggressive roadmap.

For any capsuleer seeking to navigate the complex socio-political landscape of 2026, the strategy is clear: leverage the integrated suites for asset management, utilize the specialized podcasts for geopolitical context, and contribute to the communal data pools that keep New Eden's information flowing. In the world of EVE Online, information is the only resource that is truly infinite, and those who master its acquisition and application are the ones who will ultimately dominate the cluster.

#### **Works cited**

1. Directors' Letter: 2026 & Beyond \- EVE Online, accessed February 28, 2026, [https://www.eveonline.com/news/view/directors-letter-2026-and-beyond](https://www.eveonline.com/news/view/directors-letter-2026-and-beyond)  
2. EVE Online shares 2026 roadmap featuring 3 expansions & a year of improved warfare, accessed February 28, 2026, [https://www.shacknews.com/article/147704/eve-online-2026-roadmap-3-expansions-military-campaigns](https://www.shacknews.com/article/147704/eve-online-2026-roadmap-3-expansions-military-campaigns)  
3. Patch Notes \- Version 23.02 \- EVE Online, accessed February 28, 2026, [https://www.eveonline.com/news/view/patch-notes-version-23-02](https://www.eveonline.com/news/view/patch-notes-version-23-02)  
4. EVE Online News \- Updates, blogs, events, patch notes & more, accessed February 28, 2026, [https://www.eveonline.com/news](https://www.eveonline.com/news)  
5. EVE News24: The Galaxy's Most Resilient EVE Online News Site., accessed February 28, 2026, [https://evenews24.com/](https://evenews24.com/)  
6. Posts tagged with \#patch-notes \- EVE Online, accessed February 28, 2026, [https://www.eveonline.com/news/t/patch-notes](https://www.eveonline.com/news/t/patch-notes)  
7. Eve News, Weather, and Sports Feb 2 2026 : r/Eve \- Reddit, accessed February 28, 2026, [https://www.reddit.com/r/Eve/comments/1qulxu6/eve\_news\_weather\_and\_sports\_feb\_2\_2026/](https://www.reddit.com/r/Eve/comments/1qulxu6/eve_news_weather_and_sports_feb_2_2026/)  
8. EVE News Archive, accessed February 28, 2026, [https://www.eveonline.com/news/archive/2026](https://www.eveonline.com/news/archive/2026)  
9. EVE Online Market Data API | Real-Time ESI Access & Tools \- MCP Market, accessed February 28, 2026, [https://mcpmarket.com/server/eve-online-market](https://mcpmarket.com/server/eve-online-market)  
10. EVE Market Strategies – \- GitHub Pages, accessed February 28, 2026, [https://orbitalenterprises.github.io/eve-market-strategies/index](https://orbitalenterprises.github.io/eve-market-strategies/index)  
11. eve Archives \- Fuzzwork Enterprises, accessed February 28, 2026, [https://www.fuzzwork.co.uk/tag/eve/](https://www.fuzzwork.co.uk/tag/eve/)  
12. pyfa-org/Pyfa: Python fitting assistant, cross-platform fitting tool for EVE Online \- GitHub, accessed February 28, 2026, [https://github.com/pyfa-org/Pyfa](https://github.com/pyfa-org/Pyfa)  
13. EVE Workbench \- GitHub, accessed February 28, 2026, [https://github.com/EVE-Workbench](https://github.com/EVE-Workbench)  
14. Releases · pyfa-org/Pyfa \- GitHub, accessed February 28, 2026, [https://github.com/pyfa-org/Pyfa/releases](https://github.com/pyfa-org/Pyfa/releases)  
15. Mobile EVE Fitting Tool \- Digital Showcase @ University of Lynchburg, accessed February 28, 2026, [https://digitalshowcase.lynchburg.edu/studentshowcase/2021/presentations/65/](https://digitalshowcase.lynchburg.edu/studentshowcase/2021/presentations/65/)  
16. EVE Workbench \- Third Party Developers, accessed February 28, 2026, [https://forums.eveonline.com/t/eve-workbench/142249](https://forums.eveonline.com/t/eve-workbench/142249)  
17. External Fitting Tool : r/Eve \- Reddit, accessed February 28, 2026, [https://www.reddit.com/r/Eve/comments/1pw0835/external\_fitting\_tool/](https://www.reddit.com/r/Eve/comments/1pw0835/external_fitting_tool/)  
18. Market Tools Suite \- EVE OS, accessed February 28, 2026, [https://www.eveos.space/markets](https://www.eveos.space/markets)  
19. CapsuleerKit \- Must-Have EVE Online Tools & Utilities Directory ..., accessed February 28, 2026, [https://www.capsuleerkit.com/](https://www.capsuleerkit.com/)  
20. Fuzzwork Market Data, accessed February 28, 2026, [https://market.fuzzwork.co.uk/](https://market.fuzzwork.co.uk/)  
21. Ravworks \- Home, accessed February 28, 2026, [https://ravworks.com/](https://ravworks.com/)  
22. Industry Tools : r/Eve \- Reddit, accessed February 28, 2026, [https://www.reddit.com/r/Eve/comments/1992kiu/industry\_tools/](https://www.reddit.com/r/Eve/comments/1992kiu/industry_tools/)  
23. \[Tool Release\] Triff.Tools \- Industrial Revolution (Now with more spreadsheet replacements\!) : r/Eve \- Reddit, accessed February 28, 2026, [https://www.reddit.com/r/Eve/comments/1pa0uge/tool\_release\_trifftools\_industrial\_revolution\_now/](https://www.reddit.com/r/Eve/comments/1pa0uge/tool_release_trifftools_industrial_revolution_now/)  
24. Planetary Interaction \- Goon Wiki, accessed February 28, 2026, [https://wiki.goonswarm.org/w/Planetary\_Interaction](https://wiki.goonswarm.org/w/Planetary_Interaction)  
25. Planetary Interaction Resources : r/Eve \- Reddit, accessed February 28, 2026, [https://www.reddit.com/r/Eve/comments/1gmxau4/planetary\_interaction\_resources/](https://www.reddit.com/r/Eve/comments/1gmxau4/planetary_interaction_resources/)  
26. EVE PI Manager \- Third Party Developers \- EVE Online Forums, accessed February 28, 2026, [https://forums.eveonline.com/t/eve-pi-manager/503645](https://forums.eveonline.com/t/eve-pi-manager/503645)  
27. Wormhole mapper : r/Eve \- Reddit, accessed February 28, 2026, [https://www.reddit.com/r/Eve/comments/z4fqwc/wormhole\_mapper/](https://www.reddit.com/r/Eve/comments/z4fqwc/wormhole_mapper/)  
28. Galaxyfinder vs Tripwire vs Pathfinder : r/Eve \- Reddit, accessed February 28, 2026, [https://www.reddit.com/r/Eve/comments/14owt9d/galaxyfinder\_vs\_tripwire\_vs\_pathfinder/](https://www.reddit.com/r/Eve/comments/14owt9d/galaxyfinder_vs_tripwire_vs_pathfinder/)  
29. GalaxyFinder, accessed February 28, 2026, [https://wormholes.new-eden.io/](https://wormholes.new-eden.io/)  
30. Tripwire is an amazing wormhole mapping tool that comes with basically no instructions, so here's a how-to video : r/Eve \- Reddit, accessed February 28, 2026, [https://www.reddit.com/r/Eve/comments/2qqe46/tripwire\_is\_an\_amazing\_wormhole\_mapping\_tool\_that/](https://www.reddit.com/r/Eve/comments/2qqe46/tripwire_is_an_amazing_wormhole_mapping_tool_that/)  
31. WH mapping tool : r/Eve \- Reddit, accessed February 28, 2026, [https://www.reddit.com/r/Eve/comments/1hlngg9/wh\_mapping\_tool/](https://www.reddit.com/r/Eve/comments/1hlngg9/wh_mapping_tool/)  
32. DOTLAN :: EveMaps, accessed February 28, 2026, [https://evemaps.dotlan.net/](https://evemaps.dotlan.net/)  
33. Covert Ops social content opportunities in 2026? : r/Eve \- Reddit, accessed February 28, 2026, [https://www.reddit.com/r/Eve/comments/1q5fl6e/covert\_ops\_social\_content\_opportunities\_in\_2026/](https://www.reddit.com/r/Eve/comments/1q5fl6e/covert_ops_social_content_opportunities_in_2026/)  
34. EVE University Wiki, accessed February 28, 2026, [https://wiki.eveuniversity.org/Main\_Page](https://wiki.eveuniversity.org/Main_Page)  
35. Eve Online \- The Oz Report \- Apple Podcasts, accessed February 28, 2026, [https://podcasts.apple.com/us/podcast/eve-online-the-oz-report/id1532135413](https://podcasts.apple.com/us/podcast/eve-online-the-oz-report/id1532135413)  
36. The Oz . Space, accessed February 28, 2026, [https://www.theoz.space/](https://www.theoz.space/)  
37. The Oz Report \- Feb 14, 2026–Eve Online \- Apple Podcasts, accessed February 28, 2026, [https://podcasts.apple.com/gb/podcast/the-oz-report-feb-14-2026/id1532135413?i=1000749884874](https://podcasts.apple.com/gb/podcast/the-oz-report-feb-14-2026/id1532135413?i=1000749884874)  
38. Best EVE Online Podcasts (2026) \- Player FM, accessed February 28, 2026, [https://player.fm/podcasts/Eve-Online](https://player.fm/podcasts/Eve-Online)  
39. Federation Front Line Report \- Eve Online Podcast, accessed February 28, 2026, [https://podcasts.apple.com/gb/podcast/federation-front-line-report-eve-online-podcast/id1585862029](https://podcasts.apple.com/gb/podcast/federation-front-line-report-eve-online-podcast/id1585862029)  
40. EVE ONLINE PODCASTS : r/Eve \- Reddit, accessed February 28, 2026, [https://www.reddit.com/r/Eve/comments/1ap5vbd/eve\_online\_podcasts/](https://www.reddit.com/r/Eve/comments/1ap5vbd/eve_online_podcasts/)  
41. Talking in Stations \- Eve Online News and Community, accessed February 28, 2026, [https://www.talkinginstations.com/](https://www.talkinginstations.com/)  
42. Best EVE Online Podcasts (2026) \- Player FM, accessed February 28, 2026, [https://player.fm/featured/eve-online](https://player.fm/featured/eve-online)  
43. Talking in Stations — From Highsec to Null (Invasion Episode 44\) \- YouTube, accessed February 28, 2026, [https://www.youtube.com/watch?v=rKbE5tr8NEE](https://www.youtube.com/watch?v=rKbE5tr8NEE)  
44. Voices of New Eden \- New Podcast \- EVE Online Forums, accessed February 28, 2026, [https://forums.eveonline.com/t/voices-of-new-eden-new-podcast/474127](https://forums.eveonline.com/t/voices-of-new-eden-new-podcast/474127)  
45. Help me complete the definitive list of active EVE podcasts & shows (w/ links), accessed February 28, 2026, [https://forums.eveonline.com/t/help-me-complete-the-definitive-list-of-active-eve-podcasts-shows-w-links/505312](https://forums.eveonline.com/t/help-me-complete-the-definitive-list-of-active-eve-podcasts-shows-w-links/505312)  
46. News sites for Eve to keep myself updated : r/Eve \- Reddit, accessed February 28, 2026, [https://www.reddit.com/r/Eve/comments/1gjyi70/news\_sites\_for\_eve\_to\_keep\_myself\_updated/](https://www.reddit.com/r/Eve/comments/1gjyi70/news_sites_for_eve_to_keep_myself_updated/)  
47. The Initiative Leaves the Imperium Compact | The Ancient Gaming Noob \- WordPress.com, accessed February 28, 2026, [https://tagn.wordpress.com/2023/06/05/the-initiative-leaves-the-imperium-compact/](https://tagn.wordpress.com/2023/06/05/the-initiative-leaves-the-imperium-compact/)  
48. EVE Online \- Discord Servers, accessed February 28, 2026, [https://discord.com/servers/eve-online-940573867192221696](https://discord.com/servers/eve-online-940573867192221696)  
49. Join the discussion on Discord \- EVE Online, accessed February 28, 2026, [https://www.eveonline.com/discord](https://www.eveonline.com/discord)  
50. Join the discussion on Discord | EVE Online, accessed February 28, 2026, [https://www.eveonline.com/ko/discord](https://www.eveonline.com/ko/discord)  
51. Looking for a really good corp in Eve to join. \- Reddit, accessed February 28, 2026, [https://www.reddit.com/r/Eve/comments/1rccb1u/looking\_for\_a\_really\_good\_corp\_in\_eve\_to\_join/](https://www.reddit.com/r/Eve/comments/1rccb1u/looking_for_a_really_good_corp_in_eve_to_join/)  
52. Industry Tools \- EVE Online's Premiere Web Tool \- EVE OS, accessed February 28, 2026, [https://www.eveos.space/industry](https://www.eveos.space/industry)  
53. New Industry Tool \- What Do You Want : r/Eve \- Reddit, accessed February 28, 2026, [https://www.reddit.com/r/Eve/comments/1pu6e2s/new\_industry\_tool\_what\_do\_you\_want/](https://www.reddit.com/r/Eve/comments/1pu6e2s/new_industry_tool_what_do_you_want/)