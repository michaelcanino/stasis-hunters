# JRPG Lore & Seed–Payoff

**Changelog**
- Confirmed and set S22 and S23 as `essential_for_payoff: true` and mirror-to-Chronicle on pickup (assumption; please confirm narrative leads). <!-- EDIT -->
- Defaulted Engine Heart placement to climax in Chapter 11 / penultimate flow; Ch13 preserved as epilogue (option to move Engine Heart to post-credits). <!-- EDIT -->
- Added explicit Chronicle mirroring implementation notes and QA tests for S22/S23 and Engine Heart placement. <!-- EDIT -->
- Minor clarity edits: Emi rank set to Officer II (assumption), explicit fallback timing requirements added for weak fallbacks. <!-- EDIT -->
- Assumptions made while integrating edits:
  - I used the uploaded file `jrpg_lore_seed_payoff_template_8.md` as the base because that is the file you provided. If you intended a different file number (3), tell me later and I will re-run the checklist. <!-- EDIT -->
  - S22 and S23 marked essential to avoid blocking canonical payoffs; if you want either optional, update the seed table. <!-- EDIT -->
  - Engine Heart is assumed to be the climax in Ch11 for pacing reasons; if you prefer it in Ch13, update the "Decisions" section to mark it optional. <!-- EDIT -->

**Changelog / Version metadata (file):**
- CANONICAL_CHAPTER_COUNT: 13
- Version: 1.4 - Date: 2025-10-02
- CHANGELOG: Added Monsters subsections (Shrine Guardian, Stasis Wisps, Reliquary Warden, Engine Heart). Inserted in-world combat triggers. Added seeds S22 and S23 and set mirroring instructions. Added payoff validation notes. Clarified S22/S23 essential flags and Engine Heart placement. <!-- EDIT -->

**Assumptions**
- Mapping: N = 13 (canonical chapters), so:
  - N-2 → Chapter 11 (Rescue & Plan / Archive Vault / Back alleys). <!-- EDIT -->
  - N-1 → Chapter 12 (Exposure / Reliquary Vault / Penultimate). <!-- EDIT -->
  - Final → Chapter 13 (Epilogue / Engine Heart — optional if kept). Default: Engine Heart used as climax in Ch11 to preserve epilogue tone. <!-- EDIT -->
- If the team prefers the final boss be the story climax earlier than Epilogue, move M_Final to Ch11/Ch12 and treat Ch13 purely as resolution. This is recommended to preserve epilogue tone. Default applied: Engine Heart = Ch11. <!-- EDIT -->

**Changelog / Version metadata (file):**
- CANONICAL_CHAPTER_COUNT: 13
- Version: 1.4 - Date: 2025-10-02
- CHANGELOG: Normalized chapters to support monster placements; added monsters and seed-mirroring workflow; added payoff validation notes. <!-- EDIT -->

## World Overview
- **Setting:** Uminara City - a modern Japanese coastal city (near-present) with hidden shrine districts and urban “stasis” pockets.
- **In-world present:** 2016. <!-- EDIT -->
- **Core Themes:** Time, secrecy, corruption, memory as cost.
- **Tone:** Stylish urban drama with quiet supernatural dread.
- **City flavor (quick):** Uminara combines seaside festivals and fishing wharves, a shrine quarter clustered on a cliffside, a modern corporate district with glass towers, and an old port market where the festival scenes take place — useful anchors for scene placement.
- **Cliffside shrine quarter (anchor):** narrow stone steps rising from the port, salt-scented wind mixed with incense smoke, paper lanterns at eye-level, and vendors selling lantern oil and shrine charms — use these sensory touchpoints for festival beats and stasis pockets near the shrine.
- **Festival/stress anchor note:** Public festivals and crowded civic events are recurring temporal stress nodes that concentrate collective human emotion (regret, hope, nostalgia), making it easier for Stasis pockets to form and for anomalies to spawn. This explains their frequent appearance around public celebrations.
- **Recurring motifs:** lanterns, clocks/watches, paper slips (ema), seaside waves/ship horns — use these motifs as visual and mechanical callbacks. <!-- EDIT -->

---

## 1) Title & Concept
- **Game title (working):** The Stasis Hunters
- **One-sentence concept:** A group of youths who fight supernatural beings that nest inside frozen time because they feed on humans’ “lost seconds.”
- **One-sentence concept:** Independent student Hunters with a chronosense battle frozen-time anomalies while navigating secret government factions and corporate exploitation.

---

## 2) Pillars (lock these now)
- **Core themes (comma-separated):** Time, secrecy, corruption
- **Tone (one-line):** Stylish, urban, and quietly eerie beneath everyday school life.
- **Central mystery / twist (one sentence):** Anomalies are revealed to be born from people’s own regrets and stalled moments, forcing the Hunters to question whether they are saving time or erasing pieces of humanity itself.
- **Non-negotiable world rules (list each on its own line):**
  1. Chrono Stasis exists as pockets of frozen time, born from human regrets and stalled moments.
  2. Anomalies are predatory beings that feed on stolen time within these pockets.
  3. Stasis Hunters are bound to fight anomalies to prevent wider temporal collapse.
  4. Interacting with or stabilizing an anomaly has a cost: either temporary stat drain, loss of a minor memory fragment, or permanent change to one social relationship. The exact cost is tied to method (ritual vs tech).
  5. Stabilization can be performed non-destructively (preserve victim’s life/memory) but requires combining a validated anchor-charm + pulse energy and team coordination.
  6. Memory rule: Memory loss cannot erase essential seeds required for canonical payoffs. Memory loss may remove optional flavor seeds, relationship points, or cosmetic notes, but it must never remove any item, flag, or document marked `essential_for_payoff: true` or any entry stored in the Chronicle.
- **Chronicle (definition):** The Chronicle is an in-game, persistent log of canonical evidence and essential seeds. Entries marked as Chronicle items or `essential_for_payoff: true` are backed to secure storage and are immune to player-triggered memory-cost removals. The UI should present a "Protected in Chronicle" badge for those entries.
  - Implementation note: Seeds flagged `essential_for_payoff: true` are automatically mirrored into `chronicle_entries` when first discovered; Chronicle entries are write-once and stored in a protected save region so they cannot be removed by Memory Cost actions. The UI must explicitly show these items as "Protected in Chronicle." <!-- EDIT -->
  - Dev note: When an essential seed is discovered, mirror to `chronicle_entries` immediately with `protected: true` and `write_once: true`. Show badge in UI and prevent any game action from clearing the entry. <!-- EDIT -->
  - UX rule (Memory Cost): When a player attempts a Memory Cost action, the Memory Cost Confirmation dialog must list optional fragments that will be removed AND list all "Protected in Chronicle" entries inline, with the protected entries greyed/checked and the wording "Protected in Chronicle - cannot be removed". Any attempt to remove an essential/Chronicle item should be blocked by the UI with the message "This item is protected in the Chronicle and cannot be removed." <!-- EDIT -->
  - **Suggested implementation pseudocode:**  
    - On seed pickup:
      - `if seed.essential_for_payoff == true: chronicle_entries.add(seed); seed.protected = true; seed.write_once = true; flag_seed_<id>_mirrored = true` <!-- EDIT -->

- **Chronicle mirroring note:** Essential seeds flagged `essential_for_payoff: true` must be mirrored to the Chronicle and are save-protected; the UI should explicitly list these as "Protected in Chronicle."
  - Dev note: When an essential seed is discovered, mirror to `chronicle_entries` immediately with `protected: true` and `write_once: true`. Show badge in UI and prevent any game action from clearing the entry. <!-- EDIT -->
  - UX rule (Memory Cost): When a player attempts a Memory Cost action, the Memory Cost Confirmation dialog must list optional fragments that will be removed AND list all "Protected in Chronicle" entries inline, with the protected entries greyed/checked and the wording "Protected in Chronicle - cannot be removed". Any attempt to remove an essential/Chronicle item should be blocked by the UI with the message "This item is protected in the Chronicle and cannot be removed." <!-- EDIT -->

- **Main factions (Name — motive):**
  - Faction A: Time Anomaly Response Bureau (TARB) — The official government agency tasked with managing temporal incidents. Operates under public oversight and legal constraints, often acting as the public face of containment efforts.
  - Faction B: Chronos Division — A semi-autonomous, black-budget research and weaponization unit operating under hidden funding streams within TARB. Led by Director Kurogane, it bypasses normal oversight via shell contracts to weaponize temporal phenomena.
  - Faction C: Hunters’ Circle — Student clubs; anomaly-sensitive youths acting outside official systems.
  - Faction D: Shrine Guardians — Tradition keepers; treat anomalies as curses, distrust government meddling.
  - Faction E: Sable Group (corporate backer) — private contractor that provides Chronos Division equipment and secures temporal assets for corporate profit.

- **Main cast (Name — role — motivation):**
  - Protagonist: Akihiko (Aki) Sato — 2nd-year student / reluctant Hunter — Wants to understand his chronosense and protect his friends, even as he fears destroying the very regrets that birthed anomalies.
  - Antagonist: Director Kurogane — Head of Chronos Division / government exploiter — Seeks to weaponize stolen time to consolidate power and rewrite advantage into the state’s hands.
  - Important NPC: Priestess Ayaka — Shrine Guardian / spiritual guide — Provides rituals and historical knowledge; protects sacred anchors but conceals a painful secret about past Hunters.
    - Age: mid-20s (approx. 24–27).
    - Inherited knowledge: Ayaka inherited family ritual knowledge and secret records from her shrine lineage. She was a child at the Origin Event (2001) and did not act as an adult participant; instead, the rites and related documents were preserved and taught to her privately as she grew up. <!-- EDIT -->
    - Motivation: Her access to inherited ritual lore creates internal conflict — she feels responsibility/guilt for what her family protected, but is not an original actor. This makes her a believable romance/confidant option without requiring her to be older.
    - Additional motive clarification: Ayaka resists public disclosure partly out of family honor and fear that the ritual knowledge will be exploited or sensationalized — this internal conflict should be explicit during Ch6 confession scenes to make her choices clear to players.
    - Gameplay note: Ayaka can provide unique ritual hints and a small ledger (see S10) but cannot be presented as an eyewitness adult of the Origin Event in any in-game documents.
    - Timeline clarification — Origin Event & Ayaka:
    - Origin Event occurred ~15 yrs before present (2001).
    - Ayaka is mid-20s and was a child at the time of the Origin Event. Her knowledge comes from inherited family ritual records and private instruction, not from being an adult participant. Any photograph or document from the Origin Event that lists names or ages should reference her parents/elders, not Ayaka herself. <!-- EDIT -->
    - Ayaka birth-year (derived): assuming present = 2016, Ayaka's birth is in the range 1989–1992 (approx.). This confirms she was a child (age ~9–12) at the Origin Event in 2001.
    - Clarifying line: Ayaka was a child during the Origin Event; any first-hand adult witness accounts will reference her elders, not her — ensure dialogue and documents never imply otherwise. <!-- EDIT -->
  - Support Cast: Kai Fujiwara — 3rd-year senior / secret Hunter — Protects civilians and prevents government exploitation of anomalies, driven by a promise to her late father, a TARB researcher lost during the Origin Event in 2001.
  - Support Cast: Emi Fujiwara — TARB liaison / good-government rep — Uses her official role to limit collateral damage, restrain the Chronos Division, and quietly protect her sister and the Hunters. This shared family tragedy makes exposing Chronos's abuses deeply personal and drives her to protect Kai at any cost. - Emi rank: Officer II (assumed; confirm with narrative lead). <!-- EDIT -->
  - Support Cast: Hana Fujimoto — 1st-year junior / shrine-connected solo Hunter — Hunt anomalies alone to atone for a traumatic past incident, distrusting institutions while fiercely protecting those she cares about.
  - Support Cast: Mira Takahashi — Classmate / tech-savvy anomaly tracker — Investigates anomalies through her secret blog, balancing her drive for truth with keeping people safe.
  - Support Cast: Kenta Mori — Classmate / brawler & morale engine — Outgoing and reckless but fiercely loyal, he fights to protect Aki while holding the group together.

| Name | Arc start state | Arc end state | Key seeds that drive arc | Chapter payoff |
|---|---|---|---|---|
| Kai | guarded, duty-first | opens to personal happiness | S14, S12 | Ch9–Ch11 |
| Hana | solitary atonement | trusts others | S05, S06 | Ch7 |
| Mira | sensationalist blogger | responsible whistleblower | S03, S11 | Ch5/Ch11 |
| Aki (protagonist) | uncertain, self-doubting novice | confident leader who accepts cost of saving time | S05, S16, S14 | Ch11–Ch13 (P05 / finale) |
| Ayaka | private, guilt-burdened shrine guardian | reconciled keeper who shares ritual knowledge | S10, S08, S09 | Ch6 (P03) |
| Emi | career-minded TARB officer | sacrifices career for public good / family protection | S12, S13, S11 | Ch12 (P04) |
| Kenta | brash morale-engine / comic relief | dependable team anchor; matures into strategist | S14, S15 | Ch11 (contributes to P05) |

- **Romance / Confidant Arcs (Name — role — Romanceable (Y/N) — Arc summary — Ties to main theme?):**
  - Kai Fujiwara — 3rd-year senior / secret Hunter — Romanceable: Y — Arc summary: Learns to let Aki in and choose between duty and personal happiness as graduation looms. — Ties: Time, Secrecy, Corruption.
  - Hana Fujimoto — 1st-year junior / shrine-linked solo Hunter — Romanceable: Y — Arc summary: Moves from solitary atonement to trust and communal healing through Aki’s support. — Ties: Time, Secrecy, Tradition.
  - Mira Takahashi — Classmate / tech-savvy tracker — Romanceable: Y — Arc summary: Trades sensationalism for responsible truth-telling while becoming the Hunters’ tactical backbone. — Ties: Time, Secrecy, Truth.
  - Priestess Ayaka — Shrine Guardian / spiritual guide — Romanceable: Y — Arc summary: Confronts inherited secrets and chooses human connection over ritual silence, unlocking vital history for the Hunters. — Ties: Time, Secrecy, Memory.

  **Romance System Note:** Multiple romances are allowed, but a special Festival-of-Lanterns comedic punishment scene triggers if **2+** romances are active by Chapter 8. After the scene, active romances downgrade to friendship and require an extra affinity cost (`romance_rebuild_cost = 2`) to restore full romance status. The tone is comedic and non-permanent — romances can be rebuilt but require additional investment.

- **Mechanics (narrative → gameplay mapping):**
  - Chronosense: toggled ability that highlights stasis pockets and “temporal traces” in environment (visual filter + timer UI). Usable limited times per chapter (stamina resource).
  - Anchor Charm: inventory item. When used with a Tech Pulse (consumable resource) initiates a mini-game (timed inputs or choice puzzle) to stabilize an anchor.
  - Anchor mini-game outcomes:
    - Perfect Success: No memory cost. Full stat/relationship reward.
    - Partial Success: Small memory fragment cost (flavor or optional flags only), temporary stat drain for next encounter, minor relationship impact.
    - Failure: Larger memory fragment cost (flavor/optional only), temporary stat penalties, and story variant consequences. Failure must NOT remove any seed marked `essential_for_payoff: true` nor any Chronicle entry.
  - Tech Pulse: rechargeable resource (recharges at safe zones or via Mira’s devices). Using Pulse costs stamina; using charm + pulse combo may cost a small memory fragment (flagged in save data).
  - Memory cost: represented as optional narrative choice (lose a piece of sidequest recall / temporarily reduce a social stat). Has story consequences.
  - Memory Cost Preview Tooltip: "This action may remove the following optional memory fragments and associated flavor. Essential seeds and Chronicle entries will NOT be removed." <!-- EDIT -->
    - Example preview text suggestion: "This action will remove: [Festival side-visit memory], [Mira's blog tease]. Protected: [Chronicle - Shrine Ledger (S10)]. Continue?" <!-- EDIT -->
    - Memory Cost Confirmation Dialog (copy to use in UI):  
      - Title: "Confirm Memory Cost"  
      - Body: "This choice will remove X optional memory fragment(s): [list]. Protected: [Chronicle entries — listed and greyed]. Essential seeds and Chronicle entries will NOT be removed. Continue?"  
      - Buttons: [Yes - Pay Cost] [No - Cancel] <!-- EDIT -->
  - Chronosense cooldown: 2 uses per chapter; UI shows remaining uses with pulsing icon.
  - Tech Pulse inventory: single consumable per stabilization; UI tooltip shows "Pulse: recharges at safe zones".
  - Chronosense rule: Baseline 2 uses per area. Chronosense uses are tracked per area and can be upgraded via items, relationship rank, or specific upgrades.
  - **Chronicle UI note:** The game UI should present a "Chronicle" tab listing protected items/documents and their `essential_for_payoff` status so players can see what evidence cannot be lost to memory-cost actions.
    - Design note: Include a visible "Protected in Chronicle" badge next to S05 and S10 entries. <!-- EDIT -->
  - **Design integration note:** When presenting a Memory Cost Confirmation Dialog, list the protected Chronicle entries inline so the player can see which items are safe before paying the cost.
  - **Dev UX note:** Any attempt to remove a Chronicle/essential item must be intercepted client-side — show message "Protected in Chronicle — cannot remove" and prevent the action. The dialog must also confirm that protected items are never charged against memory fragment counters. <!-- EDIT -->

---

## 3) High-level timeline (8–12 beats)
_Copy one row per beat. Keep each beat to 10–12 words._

| Beat # | Short name | When (e.g. 20 yrs before / Chapter 1) | Cause → Effect (brief) |
|---:|---|---|---|
| 1 | Origin Event | 15 yrs before (2001) | Forgotten shrine ritual collapses → first anomaly births from communal regret. |
| 2 | Inciting Incident | Chapter 1 | Aki photographs frozen festival → awakens chronosense, finds nestling in bag. |
| 3 | Form Group | Chapter 2 | Aki, Mira, Kenta recruit Kai, Hana → Hunters’ Circle forms covertly. |
| 4 | First Success | Chapter 3 | Contain small nestling at station → public unaffected; team's confidence grows. |
| 5 | Midpoint Reveal | Chapter 5 | Evidence shows anomalies originate from human regrets; Chronos Division intervenes. |
| 6 | Complication | Chapter 6 | Chronos Division experiments abducts civilians → TARB pressures Hunters; trust fractures. |
| 7 | Betrayal | Chapter 7 | Insider leaks locations → Hana's past revealed, Kai furious, allies divided. |
| 8 | Escalation / Festival | Chapter 8 | Corporate events manipulate temporal stress points → festival chaos. (Festival-of-Lanterns comedic multi-romance event can trigger here.) |
| 9 | Darkest Hour | Chapter 9 | Mass anomaly spawns from citywide despair → Kai captured, memory erosion begins. |
| 10 | Rescue & Plan | Chapter 11 | Team coordinates ritual+tech plan to stabilize mass anchor. |
| 11 | Exposure | Chapter 12 | Mira/Emi leak evidence publicly → Chronos Division's crimes exposed. |
| 12 | Epilogue | Chapter 13 | TARB reformed; Hunters recognized; Aki celebrates with partner. |

---

## 4) Payoffs (3–5 must-land moments)
| ID | Payoff (one-line) | Emotion aim | Canonical chapter |
|---:|---|---|---:|
| P01 | Chronos Division is a front—Sable Group's board is secretly manipulating anomalies for profit. | Shock / vindication | Ch 12 |
| P02 | An old shrine charm Aki received early (from Hana’s shrine) becomes the key to dispelling a locked anomaly barrier. | Aha / relief | Ch 7 |
| P03 | Priestess Ayaka’s kindness masks guilt — her past choice doomed early Hunters, creating today’s anomaly outbreak. | Bittersweet | Ch 6 |
| P04 | Emi, torn between duty and family, secretly leaks evidence that exposes Chronos Division’s crimes. | Surprise / hope | Ch 12 |
| P05 | (optional) Aki nearly sacrifices himself to erase a colossal anomaly, but the team unites to save him, proving bonds can outlast frozen time. | Catharsis / triumph | Ch 11–13 |
| P06 | (placeholder) Kai learns to trust Aki with her family's painful past, choosing personal connection over solitary duty. | Hope / intimacy | Ch 9 |
| P07 | (placeholder) Hana accepts the team's help, realizing atonement doesn't have to be a lonely path. | Relief / belonging | Ch 7 |
| P08 | (placeholder) Mira's blog post, once a source of sensationalism, becomes the key to the public exposure of Chronos. | Vindication | Ch 12 |

- **Canonical vs adaptive note:** P01 and P02 are intended to be canonical (happen on the primary path). P03 and P04 can adapt by path (confession vs exposure) — see Branching notes. P05 is path-dependent and can resolve as heroics or sacrifice based on player choices.
- **Validation notes for payoffs:** 
  - P02: Requires S05 or fallback S06; block payoff until mirrored. <!-- EDIT -->
  - P01: Requires at least one of S01, S03, or S22 mirrored; block payoff until mirrored. <!-- EDIT -->
  - P05: Requires S16 or S23 (Engine Memory Core) mirrored; block payoff until mirrored. <!-- EDIT -->

---

## 5) Seed → Payoff Tracker (add 2–4 seeds per payoff)
_Copy one row per seed. Keep descriptions short._

| Seed ID | Payoff ID | Seed description | Seed type (item/dialogue/env/sidequest/motif) | Location | Chapter planted | Discover method (examine/talk/pickup) | Main/Optional | Fallback | date (YYYY-MM-DD or "Y years before") | essential_for_payoff (true/false) |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| S01 |	P01 |	Branded crate with corporate crest on containment gear | Env / prop |	Abandoned containment site | Ch2 | Examine crate | Main | If missed, later exposure includes security footage or an inventory manifest showing the same corporate crest on Chronos gear (fallback revealed at Ch5 public hearing). | 2016 (Ch2) | false |
| S02	| P01	| Mayor’s charity pamphlet lists Sable Group as sponsor	| Env / prop | City Hall lobby | Ch1 | Pickup / examine | Optional | If missed, Mira’s archived press release (S03) or a leaked internal email (S04) will still establish Sable’s sponsorship (fallback available by Ch4). **Fallback enforcement:** ensure fallback appears by Ch5 at the latest. <!-- EDIT --> | 2016 (Ch1) | false |
| S03	| P01	| Mira finds archived press release linking Sable to Chronos funding | Sidequest / dialogue	| Online archive | Ch4	| Talk / read	| Main | If missed, a later public hearing or the leaked board email (S04) supplies the same funding link (fallback public at Ch12). | 2016 (Ch4) | false |
| S04	| P01	| Board member named in a leaked email about “Temporal Assets” | Item / doc | Hidden Chronos file	| Ch5	| Examine document | Optional | If missed, the mayor’s bank records or an anonymous tip (S11) revealed at payoff will name the board member (fallback manifest at Ch12). **Fallback enforcement:** ensure fallback appears by Ch5. <!-- EDIT --> | 2016 (Ch5) | false |
| S05	| P02	| Small shrine charm Hana gives Aki at the festival	| Item | School festival	| Ch1	| Pickup (given) | Main | If missed, the carving in the shrine (S06) or Ayaka’s explanation (S07/S08) will tie the charm to the shrine’s seal (fallback occurs at shrine scene Ch3–Ch4). | 2016 (Ch1) | true |
| S06	| P02	| Carving on charm matches seal pattern in shrine inner chamber | Env / prop | Shrine inner room | Ch3	| Examine	| Optional | If missed, the charm given at the festival (S05) or the prayer slip (S07) will provide the same seal-match evidence. | 2016 (Ch3) | false |
| S07	| P02	| Old prayer slip references “charm to unlock closed time” | Item / dialogue	| Ayaka’s archive | Ch4	| Talk / examine | Optional | If missed, player can still learn the ritual link from Ayaka’s archive or shrine elder dialogue later. | 2016 (Ch4) | false |
| S08	| P03	| Ayaka flinches at a question about a past containment failure	| Dialogue | Shrine grounds | Ch2	| Talk | Main | If missed, the faded photo (S09) or ledger entry (S10) will reveal Ayaka’s family connection to the containment failure (fallback shown at Ch3 archive dig). | 2016 (Ch2) | false |
| S09 | P03 | Black-and-white photograph dated 15 years prior, showing shrine elders at the Higashimori Seal site; family crest visible and a handwritten note referencing "Kuro Family - guardians." The photo implies family involvement but not Ayaka herself, as she was a child. | env/item | Takashima Archive - Photo Album | Chapter 2 | examine (photo) | Optional | Fallback: If missed, ledger (S10) or Ayaka dialog will confirm family involvement (fallback at Ch4). | 2001 (15 years before present) | false |
| S10 | P03 | Small bound ledger of ritual notes with entries from multiple generations. Contains dated instructions (e.g., "teach when child turns 12," "preserve the second node") and practical ritual diagrams, demonstrating the transmission of inherited knowledge to Ayaka. | item/dialogue | Ayaka's Shrine - Hidden Box | Chapter 3 | pickup/examine | Main/Optional | If withheld because player protects shrine privacy, ledger can be revealed later via trust arc (fallback at Ch7 once Ayaka trusts player more). Decision: A partial photograph is allowed, capturing key ritual diagrams but obscuring personal entries. This provides a fallback for the main plot while rewarding the high-trust path with the full, unredacted lore. | 2006–2011 (10–5 years before present) | true |
| S11	| P04	| Anonymous tip email appears in Mira’s blog inbox | Dialogue / env | Mira’s blog / inbox | Ch5	| Read / talk	| Main | If missed, the USB (S12) or a gala photo (S13) or later investigative reporting will surface the same lead (fallback published by Ch12). | 2016 (Ch5) | false |
| S12	| P04	| USB labeled “For Kai” hidden in Emi’s desk drawer | Item	| Emi’s office | Ch6	| Pickup / examine | Optional | If missed, Mira’s inbox tip (S11) or the gala photo (S13) or later testimony during the exposure will implicate Emi (fallback during Ch12 exposure). **Fallback enforcement:** ensure fallback appears by Ch12. <!-- EDIT --> | 2016 (Ch6) | false |
| S13	| P04	| Photo of Emi meeting a Chronos official at gala event	| Env / prop	| City gala	| Ch3	| Examine photo	| Optional | If missed, the USB (S12) or Mira’s tip (S11) or later testimony during the exposure will show the meeting (fallback at public hearing Ch12). | 2016 (Ch3) | false |
| S14	| P05	| Kenta’s notebook sketch of an improvised temporal anchor device	| Item | Kenta’s locker	| Ch2	| Pickup / examine | Main | If missed, the training clip (S15) or after-action report (S16) or leaked note (S17) will document the anchor design (fallback available Ch5). | 2016 (Ch2) | false |
| S15	| P05	| Training clip showing ritual + tech synergy used on small nest | Env / prop (video) | TARB training room	| Ch5	| View / examine	| Optional | If missed, Kenta’s notebook (S14) or the rescue report (S16) or Emi’s leaked note (S17) will demonstrate the ritual+tech synergy (fallback at Ch11 planning). | 2016 (Ch5) | false |
| S16	| P05	| After-action report describing multi-team rescue procedure | Item / doc | Hunters’ Circle records	| Ch3	| Read | Main | If missed, the notebook (S14), training clip (S15), or leaked protocol note (S17) will describe the multi-team procedure (fallback at Ch11). | 2016 (Ch3) | false |
| S17	| P05	| Emi’s leaked note: “Stabilization protocol — combine charm & pulse” | Item / doc | Leaked TARB file	| Ch7	| Examine	| Optional | If missed, the after-action report (S16) or training footage (S15) or Kenta’s notes (S14) will still show the charm+pulse protocol (fallback at Ch11). | 2016 (Ch7) | false |
| S18 | P06 | Locker note from Emi mentioning "look after her" | dialogue/item | East High - Locker row 12 | Chapter 2 | examine (locker) | Optional | Fallback: short letter fragment found later in family box (Ch9). | 2014-09-11 | false |
| S19 | P07 | Small shrine token with a scratched name and date, hinting at Hana's past | item/env | Festival Shrine - vendor stall | Chapter 1 | pickup/examine | Optional | Fallback: vendor ledger or shrine elder testimony (Ch4). | 2010 (approx.) | false |
| S20 | P08 | Mira posts a short, sensational teaser calling the protagonist by a nickname | dialogue/motif | Mira's blog (public) | Chapter 1 | talk/read (public post) | Optional | Fallback: archived social post screenshot (Ch4). | 2016-03-15 | false |
| S21 | P_RomancePunish | Festival-of-Lanterns multi-romance convergence / Kenta rescue gag (triggers downgrade) | env / dialogue / event | Festival Plaza | Ch8 | event/cutscene | Optional (comedy easter egg) | None (scene-only) | 2016 (Ch8) | false |
| S22 | P01 | Reliquary core fragment with partial board signatures — links Sable to Chronos | item/doc | Reliquary Vault / Penultimate chest or mid-boss drop | Ch12 (primary) / Ch11 (fallback mid-boss) | pickup/examine | Main | Fallback: dropped by mid-boss in Ch11 if missed (mid-boss drop). **Mirroring:** mirror to Chronicle on pickup, `protected:true`. | 2016 (Ch11/Ch12) | true <!-- EDIT -->
| S23 | P05 | Engine Memory Core — fragment of the Engine Heart that links ritual tech outcomes to Aki’s sacrifice choice | item/doc | Engine Heart chamber (Climax - Ch11 default; optional Ch13 post-credits) | Ch11 | pickup/examine | Main | No fallback recommended; if missed, P05 may resolve via cinematic alternative (design fallback required). **Mirroring:** mirror to Chronicle on pickup, `protected:true`. | 2016 (Ch11) | true <!-- EDIT -->

**Seed fallback enforcement note:** For any optional seed whose fallback is weak (e.g., S02, S04, S12), ensure the fallback appears no later than the Midpoint (Ch5) or Exposure (Ch12) so payoffs remain understandable. Specific fallback enforcement lines were added above. <!-- EDIT -->

---

## 6) Scene / Chapter Checklist (copy per scene)
**Scene name:** Festival Awakening — Chapter 1
- Pillars/rules invoked: Chrono Stasis pockets form from human regret; Chronosense perceives freezes.
- Seeds present (IDs): S05, S02, S19, S20 - Seed placement natural? (yes/no): yes — charm gifted, pamphlet on table, token at stall, blog post online. - Guaranteed vs optional: S05 (shrine charm) should be guaranteed within Ch1 or guaranteed fallback must be available by Ch3. <!-- EDIT -->
- Guaranteed fallback: If player skips the festival side stroll, NPC will hand charm later in Shinto stall scene (guaranteed fallback by Ch3). <!-- EDIT -->
- New rules/facts introduced: Aki awakens chronosense; nestling can latch onto sensitive person.
- NPC knowledge level (list NPCs and level): Aki — newly awakened (full for moment); Hana — fragmentary; Mira — none/curious; Kenta — none.
- Optional lore rewards: Codex: “First Contact — Nestlings and Attachment”; acquire Shrine Charm (S05).
- Player choices that alter seed discoverability: If player skips the festival side stroll, S05 may not be collected immediately; guaranteed fallback ensures shrine carving will later confirm charm importance.
- Player load (recommended): 1 new mechanic (chronosense) + 1 small inventory item introduction; keep exposition light.

**Scene name:** Investigation & Recruitment — Chapter 2
- Pillars/rules invoked: Secrecy; Hunters’ Circle forms as unofficial response unit.
- Seeds present (IDs): S01, S14, S08, S18 - Seed placement natural? (yes/no): yes — abandoned gear, Kenta’s notebook, Ayaka’s guarded comment, locker note. - New rules/facts introduced: Hunters’ Circle establishes covert protocol; TARB existence hinted.
- NPC knowledge level: Kai — partial (knows Hunter contacts); Ayaka — fragmentary (warns against exposure); Mira — investigative (fragmentary).
- Optional lore rewards: Hunters’ Circle manifest: “Safe houses & comms protocol.”
- Player choices that alter seed discoverability: If the player avoids the abandoned containment site, S01 can still be revealed via later inspection of TARB trailers.
- Player load (recommended): Introduce 1 social beat and 1 exploration objective; do not introduce multiple new mechanics.

**Scene name:** First Containment — Chapter 3
- Pillars/rules invoked: Anomalies can be contained with combined ritual/tech; anchors localize pockets.
- Seeds present (IDs): S06, S16, S13 - Seed placement natural? (yes/no): yes — shrine carving found, training file glimpsed, Mira’s archive notes.
- New rules/facts introduced: Small nestlings subdued; team learns basic hampering technique.
- NPC knowledge level: Kai — skilled Hunter (full); Mira — technical knowledge grows (partial); Kenta — supportive novice (none→partial).
- Optional lore rewards: Codex entry: "Containment basics — charm + pulse."
- Player load (recommended): 1–2 new mechanics (anchor mini-game + stabilization concept); brief tutorial recommended.
- Combat/triggers:
  - (A Shrine Guardian patrols this chamber.) <!-- EDIT -->
  - Corruption breaches the shrine's safety—hostiles manifest. <!-- EDIT -->

### Monsters (Chapter 3 - Shrine Inner Room)
- M01 Shrine Guardian (Predator) — Type: Predator; Difficulty: Easy. Guards inner chamber; drop: S05 (Small shrine charm). On pickup: mirror to Chronicle (protected). <!-- EDIT -->
- Notes: Designed as a low-difficulty guardian that teaches players monster patterns and seed pickups. Mark seed S05 `essential_for_payoff: true` (already flagged). <!-- EDIT -->

**Scene name:** Sidequests & Echoes — Chapter 4
- Pillars/rules invoked: Temporal echoes leave forensic traces (timestamps, server glitches).
- Seeds present (IDs): S03, S07, S09 - Seed placement natural? (yes/no): yes — archival research, shrine carvings, photograph in shrine archive.
- New rules/facts introduced: Digital timestamps occasionally record impossible times; echoes can be tracked.
- NPC knowledge level: Mira — finds archives (full for doc); Ayaka — archive custodian (partial→full); Aki — learning (partial).
- Optional lore rewards: Sidequest: “Archive Dig” unlocks Ayaka’s flash fragment.
- Player load (recommended): 1 research sidequest + small dialogue beats; keep pace steady.

**Scene name:** Midpoint Reveal — Chapter 5
- Pillars/rules invoked: Government factions split; anomalies tied to human regret.
- Seeds present (IDs): S04, S11, S15
- Seed placement natural? (yes/no): yes — leaked doc fragments, anonymous tip, training clip glimpsed.
- New rules/facts introduced: Evidence points to corporate ties with Chronos; mass-scale exploitation possible.
- NPC knowledge level: Emi — conflicted (partial→full of evidence later); Kai — defensive (partial); Mira — investigative (partial→full).
- Optional lore rewards: Codex: “Chronos Division procurement chain."
- Player load (recommended): Avoid introducing new mechanics; focus on investigation & emotional beats.

**Scene name:** Complication / Pressure — Chapter 6
- Pillars/rules invoked: Secrecy enforced; exploiters escalate covert ops.
- Seeds present (IDs): S12, S10
- Seed placement natural? (yes/no): yes — hidden USB, shrine ledger, shrine charm appears again.
- New rules/facts introduced: Chronos Division begins covert abductions/experiments; TARB pressured to respond.
- NPC knowledge level: Emi — internal tension (full of bureaucracy); Ayaka — guilt deepens (partial→full emotionally); Hana — on edge (full about shrine past).
- Optional lore rewards: Sidequest: “Recover USB” reveals Chronos asset lists.
- Player choices that alter seed discoverability: If player intervenes to protect shrine privacy, S10's ledger may be withheld until trust is earned.
- Player load (recommended): Emotional pressure + 1 stealth/investigation objective; keep mechanical complexity low.

**Scene name:** Betrayal Revealed — Chapter 7
- Pillars/rules invoked: Actions inside stasis have moral cost; some Hunters keep secrets.
- Seeds present (IDs): S17
- Seed placement natural? (yes/no): yes — pamphlet cross-ref, prayer slip, Emi’s leaked note appear coherent.
- New rules/facts introduced: Cognitive locks can be dispelled using shrine charm + stabilization protocol.
- NPC knowledge level: Kai — betrayed/angry (full); Emi — compromised but sympathetic (partial→full); Ayaka — reveals ledger (full).
- Optional lore rewards: Codex unlock: “Stabilization protocol (charm + pulse).”
- Player load (recommended): High emotion + 1 new ritual detail, keep puzzles short.

**Scene name:** Escalation — Chapter 8
- Pillars/rules invoked: Natural anomalies amplify if human despair concentrates.
- Seeds present (IDs): S21
- Seed placement natural? (yes/no): yes — abandoned containment crate, gala photo, Kenta’s notes.
- New rules/facts introduced: Corporate or civic events can be manipulated to increase temporal stress points.
- NPC knowledge level: Mira — tracking sponsor ties (partial); Kenta — frightened but helpful (partial); Aki — aware of stakes (full).
- Optional lore rewards: Codex: “Temporal Stress Maps—city hotspots.”
- Player load (recommended): 1 tactical encounter + exposé beats.
- Player choices that alter seed discoverability: If the player has 2+ active romance flags, the Festival Punishment Scene (S21) will trigger automatically and play the comedic Kenta rescue gag.
- New UI feedback: show system toast and journal entry after the scene.

### Comedy Punishment Scene — Festival of Lanterns

**Trigger condition:** Player has active romance flags with 2 or more romanceable characters (Kai, Hana, Mira, Ayaka) at Chapter 8 Festival.

**Cutscene script (plug-and-play):**

```
### Comedy Punishment Scene — Festival of Lanterns

**Trigger condition:** Player has active romance flags with 2 or more romanceable characters (Kai, Hana, Mira, Ayaka) at Chapter 8 Festival.

**Cutscene script (plug-and-play):**

[Festival Plaza — Lantern Release about to start]
- SFX: distant festival music, lantern whispers, crowd murmurs.
- Visual: Lanterns float; camera centers on Aki, standing between four expecting partners.

**Kai (arms crossed, eyebrow raised):** "So… this is your idea of a date? With *all of us*?"
**Mira (smirking, arms folded):** "Bold move, Sato. Did you think no one would compare notes?"
**Hana (quiet, hurt):** "…You promised."
**Ayaka (sighing, composed):** "Deception, even in matters of the heart, leaves scars deeper than memory."

[Aki stammers; the tension rises. The lantern glow flickers—awkward silence.]

**Kenta (off-camera, cheerfully):** "Yo, Aki! I saved you some prime skewers before the stall ran out!"
[Kenta arrives holding two steaming yakitori skewers. He pauses, takes in the scene.]

**Kenta (cheerful, oblivious):** "…Uh. Did I walk into a boss fight?"
[Kenta notices the atmosphere, grins wide, and grabs Aki's sleeve.]

**Kenta (grinning, tugging Aki away):** "C’mon, bro. Let’s leave the battlefield behind. Guess you’re stuck with me tonight!"
[Kenta drags Aki toward the food stalls. Fade to a short gag montage of Aki and Kenta consuming skewers awkwardly under the lantern glow.]

**Kenta (mouth full, jokey sage):** "You know, dating’s like stasis hunting — you only focus on *one* target, or the whole thing blows up."
[Cut back briefly to the four standing in a row — glaring, sighing, pouting.]

**System Message (comedic):** *You lost 1 Memory Fragment: [Romantic Credibility].*

**After-scene caption:** "Romances downgraded to friendship. Rebuilding trust requires extra affinity."
```

**Aftermath / mechanical effects (implement):**
- Show system toast: `You lost 1 Memory Fragment: [Romantic Credibility].` (UI must be localizable and shown before autosave). <!-- EDIT -->
- Downgrade all current romance flags to **friendship** (clear romance-exclusive flags but preserve relationship progress as friendship).
- Set save flags: `flag_romance_multi_punishment_triggered = true` and `flag_romance_locked_until_rebuild = true`.
- Re-romancing requirement: `romance_rebuild_cost = 2` extra affinity ranks above normal romance threshold to regain full romance.
- Journal note added: `Festival Fiasco — Trust reset with romanceable partners. Rebuild required.`
- UX reminder: ensure this action never removes Chronicle or essential seeds; the toast/journal must not make or imply permanent loss of protected evidence. <!-- EDIT -->

**Scene name:** Darkest Hour — Chapter 9
- Pillars/rules invoked: Mass anomalies threaten memory integrity; sacrifice seems inevitable.
- Seeds present (IDs): S04
- Seed placement natural? (yes/no): yes — tip triggers action, USB provides evidence, doc ties Chronos to corporate backers.
- New rules/facts introduced: Large-scale anomaly can spawn from collective despair; memory erosion begins.
- NPC knowledge level: Kai — captured/limited; Emi — leaks evidence (full risk); Hana — frantic (full).
- Optional lore rewards: Urgent codex entry: “Mass Anomaly Protocols.”
- Player load (recommended): Allow players to roleplay rescue planning; avoid adding new mechanics.

**Scene name:** Final Showdown — Chapter 11
- Pillars/rules invoked: Ritual + tech synergy can neutralize anchors non-destructively.
- Seeds present (IDs): S16, S17, S15
- Seed placement natural? (yes/no): yes — training clip, containment crate, Emi’s note, TARB video used in plan.
- New rules/facts introduced: Team’s combined method stabilizes anchor without erasing people (if properly executed).
- NPC knowledge level: All main cast — full (Kai, Emi, Hana, Mira, Kenta, Aki).
- Optional lore rewards: High-value codex: “Anchor Stabilization Procedure — finalized.”
- Player load (recommended): Complex multi-step encounter allowed; provide clear UI checklist for players.
- Combat/triggers:
  - (A Stasis Wisp swarm harasses the back alleys during the plan.) <!-- EDIT -->
- Design note: Engine Heart default placement moved here (Ch11) to preserve epilogue tone; if the team prefers Engine Heart in Ch13, make the Ch13 version optional/post-credits. <!-- EDIT -->

### Monsters (Chapter 11 - Archive Vault / Back alleys / Mid-boss fallback)
- M_Wisps Stasis Wisps — Type: Minion swarm / Optional encounter; Difficulty: Easy/Medium. Purpose: pacing encounters and limited memory-fragment drops (non-essential). Drops: small memory fragments (non-essential). On pickup: non-essential fragments do NOT mirror to Chronicle. <!-- EDIT -->
- M_MidReliquary (Mid-boss) — Type: Predator; Difficulty: Medium. Drops: S22 (Reliquary core fragment) as fallback if earlier evidence missed. On pickup: mirror to Chronicle (protected). `essential_for_payoff: true`. <!-- EDIT -->

**Scene name:** Exposure & Reckoning — Chapter 12
- Pillars/rules invoked: Secrecy vs truth; corruption publicly challenged.
- Seeds present (IDs): S03, S04, S11
- Seed placement natural? (yes/no): yes — archives, documents, and Mira’s leak converge publicly.
- New rules/facts introduced: Chronos Division exposed; legal/moral frameworks for stasis begin forming.
- NPC knowledge level: Public figures — partial→public suspicion; TARB leadership — pressured; Hunters — acknowledged.
- Optional lore rewards: Public codex update: “Chronos Division exposed” entry.
- Player load (recommended): Exposition + legal fallout; split into scenes to avoid pacing crash.
- Pacing suggestion: Split Chapter 12 into two scenes—12A (Public Hearing / Legal Testimony) and 12B (Media Release / Public Protests and Prosecution) — this spaces exposition and provides clearer consequences. <!-- EDIT -->
- Combat/triggers:
  - (A Reliquary Warden guards the penultimate vault.) <!-- EDIT -->

### Monsters (Chapter 12 - Reliquary Vault / Penultimate)
- M_Penultimate Reliquary Warden — Type: Predator; Difficulty: Hard. Mandatory penultimate fight that guards key evidence. Drops: S22 (Reliquary core fragment with signatures). On pickup: mirror to Chronicle (protected). `essential_for_payoff: true`. <!-- EDIT -->
- Notes: This is an apex fight meant to be a story crescendo. Ensure pacing supports a mandatory combat here; if it breaks tone, consider moving to optional or shifting other beats. <!-- EDIT -->

**Scene name:** Epilogue — Chapter 13
- Pillars/rules invoked: Time, healing, and the cost of saving people.
- Seeds present (IDs): S05, S16, S17
- Seed placement natural? (yes/no): yes — shrine charm returned, training docs archived, Emi’s note set public.
- New rules/facts introduced: Reformed TARB & Hunters’ Circle recognized as guardians; rituals restored with transparency.
- NPC knowledge level: Aki & party — full closure; Ayaka — reconciled (full); Emi — professional consequences but moral victory (full).
- Optional lore rewards: Epilogue codex: “New Guardians’ Charter”; romance epilogues unlocked.
- Combat/triggers:
  - (The Engine Heart awakens as the final multi-phase predator.) — Default: Engine Heart fight occurs as climax in Ch11; if Engine Heart is kept in Ch13, mark as optional/post-credits to preserve epilogue tone. <!-- EDIT -->
- Tone note: Adding a required battle in the epilogue risks undermining resolution. Recommend making the Engine Heart fight the climax (Ch11/Ch12) or implementing it as an optional late-game boss or post-credits encounter to preserve epilogic tone. Default applied above. <!-- EDIT -->

### Monsters (Final Chapter / Climax - Engine Heart)
- M_Final Engine Heart  
  - Type: Predator  
  - Difficulty: Very Hard  
  - Location: Engine Heart chamber (default climax in Ch11; optional post-credits in Ch13). <!-- EDIT -->
  - Behavior: Multi-phase—time pulse arena shifts, anchor-corruption spawns, core volleys cause memory-drain AOE. Tie each phase to story beats (e.g., memory-fragment risk increases during Phase 3). <!-- EDIT -->
  - Drops: S23 (Engine Memory Core). On pickup: mirror to Chronicle (protected). `essential_for_payoff: true`. <!-- EDIT -->
- Multi-phase notes: Phase 1: Time pulses that shift arena; Phase 2: Anchor corruption spawns minions; Phase 3: Focused core attacks with memory-drain AOE. Tie each phase to story beats (e.g., memory-fragment risk increases during Phase 3). <!-- EDIT -->
- Design suggestion: consider making Phase 3 a scripted set-piece when Aki faces the sacrifice choice to ensure narrative clarity across player outcomes. <!-- EDIT -->

---

## 7) Branching notes (if applicable)
- Is the payoff canonical (Yes/No)? See per-payoff canonical notes below (P01 and P02 canonical on primary path; others adaptive).
- **P01 — Yes.** The method of revelation changes. It can be a public exposé (if Mira's arc is followed), a leaked set of board minutes (if Emi's arc is followed), or a press dump from an internal whistleblower. If the player fails to protect key evidence, the board is only partially exposed and prosecution stalls.
  - Validation: Requires at least one of S01, S03, or S22 mirrored to Chronicle; block canonical P01 reveal until evidence is mirrored. <!-- EDIT -->
- **P02 — Yes.** The specific item can vary. If player choices prevent Hana from gifting the charm, an equivalent item like Kai’s pendant or a family watch fragment can substitute. The alternative solution might require a more complex ritual+tech mini-game rather than a single-item unlock.
  - Validation: Requires S05 or fallback S06 mirrored to Chronicle; block payoff until mirrored. <!-- EDIT -->
- **P03 — Adaptive.** Ayaka either confesses willingly (if Aki builds a high-trust relationship with her) or is exposed by the team's investigation (if pressured). The consequences vary: a private atonement ritual versus a public scandal for the shrine, depending on whether the player chooses to protect her secret.
- **P04 — Adaptive.** This payoff only occurs if the player builds trust with Emi or forces her hand. Otherwise, the leak is performed by Mira or another insider. The emotional framing changes dramatically—is Emi a willing hero sacrificing her career for family, or a cornered bureaucrat forced to act?
- **P05 — Adaptive.** The finale can resolve in multiple ways based on team cohesion and previous choices. It can be a heroic survival (team rescue → hopeful ending), a partial sacrifice (Aki survives but loses key memories), or a true sacrifice (Aki perishes to contain the anomaly → tragic ending).
  - Validation: P05 requires S16 or S23 mirrored to Chronicle for the canonical mechanics that allow the "non-destructive stabilization" to be executed. If S23 is absent, provide a cinematic alternative to resolve P05. <!-- EDIT -->
- **Gameplay note:** When a payoff is adaptive, the delivery should change tone, but the core factual outcome should be preserved (e.g., the corporate corruption is still exposed, but who leaks it and their motivation differs).

---

## 8) QA tests (per payoff)
**Guidance:** Copy these tests for each payoff (replace `<PAYOFF_ID>` with P01, P02, etc.) and run them per build. Confirm seed dates, Chronicle immunity, and that memory-cost actions do not remove essential flags.

**Payoff ID:** P01
- Test A (all seeds found) — expected player reaction: “The corporate crest and donations all pointed here — I knew it.”
- Test B (no seeds found) — should still make sense? Yes — explained directly in leaked documents/news at reveal. Must ensure S22 fallback exists (Ch11 mid-boss or Ch12 Warden). <!-- EDIT -->
- Test C (some seeds found) — expected reaction: Suspicious connections finally confirmed; satisfaction at connecting partial hints.
- Timeline contradiction risks: Make donation dates, leaked files, and mayor’s charity timeline consistent.

**Payoff ID:** P02
- Test A (all seeds found) — expected player reaction: “The charm and carvings always looked special — it’s the seal key!”
- Test B (no seeds found) — should still make sense? Yes — Emi/Ayaka explains the charm’s sealing function at reveal.
- Test C (some seeds found) — expected reaction: Charm felt important; payoff validates earlier curiosity.
- Timeline contradiction risks: Ensure Hana gifts charm before its use; alternative paths provide equivalent item.

**Payoff ID:** P03
- Test A (all seeds found) — expected player reaction: “Her flinching, the old photo, the ledger… I pieced her secret together before she admitted it.”
- Test B (no seeds found) — should still make sense? Yes — Ayaka confesses or is exposed in-scene.
- Test C (some seeds found) — expected reaction: Suspicion confirmed; surprise about full depth of guilt.
- Timeline contradiction risks: Keep shrine history consistent; don’t contradict earlier statements about prior Hunters.

**Payoff ID:** P04
- Test A (all seeds found) — expected player reaction: “The email, USB, photo hinted she was conflicted — now it pays off.”
- Test B (no seeds found) — should still make sense? Yes — evidence can also arrive via alternate source (Mira/insider).
- Test C (some seeds found) — expected reaction: Player rewards Emi’s trust, feels twisty relief that she chose to act.
- Timeline contradiction risks: Ensure Emi’s actions don’t contradict her TARB duties unless leak timing matches story.

**Payoff ID:** P05
- Test A (all seeds found) — expected player reaction: “The anchor sketches and rituals all built to this moment — of course teamwork saves him.”
- Test B (no seeds found) — should still make sense? Yes — Emi explains protocol on the fly / deus ex training. If S23 is required for some variants, ensure fallback cinematic delivers similar exposition. <!-- EDIT -->
- Test C (some seeds found) — expected reaction: Feels partially foreshadowed, but still emotional shock at sacrifice risk.
- Timeline contradiction risks: Keep anchor tech consistent across Kenta’s notes, TARB records, and shrine rituals.

**Payoff ID:** P_RomancePunish
- Test A (2+ romances) — Setup: player has active romance flags for 2 or more partners by Ch8. Expected: Cutscene plays verbatim; system toast `You lost 1 Memory Fragment: [Romantic Credibility].`; all active romance flags are downgraded to friendship; `flag_romance_multi_punishment_triggered` set to true; `flag_romance_locked_until_rebuild` set to true; journal note added.
- Test B (1 or 0 romances) — Setup: player has 0 or 1 active romance flags. Expected: Standard single-romance festival scene (no downgrade), S21 does not trigger.
- Checklist items: Confirm `romance_rebuild_cost` is enforced when re-romancing; confirm journal entry is added; confirm no essential seeds/Chronicle entries are affected.
- Additional QA check: Confirm that the toast and journal entry are localizable and that the save occurs after the toast is displayed. <!-- EDIT -->

**Additional QA Tests (added):**
- S22/S23 mirroring tests:
  - Test: Acquire S22 via mid-boss drop or vault pickup. Expected: `chronicle_entries` receives S22, `flag_seed_S22_mirrored_to_chronicle = true`, UI shows "Protected in Chronicle". Payoff P01 should now be allowed if other conditions met. <!-- EDIT -->
  - Test: Acquire S23 via Engine Heart drop. Expected: `chronicle_entries` receives S23, `flag_seed_S23_mirrored_to_chronicle = true`. Payoff P05 can now use canonical mechanic. <!-- EDIT -->
- Engine Heart placement tests:
  - Test A: Engine Heart as Ch11 mandatory boss. Expected: Emotional climax occurs in Ch11; Ch13 is epilogue with no mandatory boss. Validate pacing and that epilogue tone is preserved. <!-- EDIT -->
  - Test B: Engine Heart as optional post-credits boss (Ch13). Expected: Players can experience resolution in Ch13 without forced combat; optional boss accessible after credits. Validate player expectation messaging and menu access. <!-- EDIT -->

**QA checklist (recommended):**
- Confirm each seed document has a `date` field consistent with the established timeline (Origin Event = 2001, Present = 2016).
- Verify that all seeds marked `essential_for_payoff: true` are correctly mirrored as Chronicle entries and cannot be removed by memory-cost actions.
- Test the memory-cost UI to ensure it clearly displays what optional fragments will be removed while also listing which Chronicle items are protected.
- Flag any mismatches between seed dates and the Origin Event as a TODO for writer review.
- Confirm no seed uses 2025 or later as an in-world date (seed date audit). <!-- EDIT -->

---

## 9) Changelog / Decisions
- CANONICAL_CHAPTER_COUNT: 13
- Version: 1.4 - Date: 2025-10-02
- CHANGELOG: Added Monsters subsections (Shrine Guardian, Stasis Wisps, Mid Reliquary, Reliquary Warden, Engine Heart). Inserted in-world combat triggers. Added seeds S22 and S23 and set mirroring instructions. Added payoff validation notes and flagged epilogue tension with final predator. Confirmed S22/S23 as essential and moved Engine Heart default to Ch11. <!-- EDIT -->
- Decisions made this version:
  - Reconciled timeline with final-chapter mapping and added monster placements accordingly (N=13 mapping assumed). <!-- EDIT -->
  - Inserted fallback mid-boss S22 in Chapter 11 to prevent missed evidence blocking P01. Mirrored S22 to Chronicle on pickup. <!-- EDIT -->
  - Added Chronicle mirroring notes for all monster-dropped essential seeds. <!-- EDIT -->
  - Default: Engine Heart moved to Ch11 (climax). If narrative leads prefer epilogue boss, make it optional in Ch13. <!-- EDIT -->
- Open questions / risks:
  - Confirm whether S22 and S23 should be strictly essential or optional canonical evidence; I set both to `true` to avoid payoff blocking. Please confirm if either should be optional. <!-- EDIT -->
  - Playtest pacing for Chapter 12 if penultimate boss is mandatory; consider splitting Ch12 into 12A/12B (hearing then vault) to avoid pacing crashes. <!-- EDIT -->

---

## 10) Quick actions
- [x] Fill Pillars
- [x] Fill Timeline
- [x] Pick Payoffs
- [x] Add Seeds (2–4 per payoff)
- [x] Add Festival Punishment Scene (S21) + flags + romance rebuild rule
- [x] Insert Monsters subsections and trigger sentences for Ch3, Ch11, Ch12, and Final. <!-- EDIT -->
- [x] Add fallback mid-boss S22 in Ch11 and final seed S23 in Ch11 (Engine Heart) and set mirroring instructions. <!-- EDIT -->
- [ ] Implement MVP seeds in early areas
- [ ] Playtest and update tracker
- [x] Seeds date audit (ensure no stray 2025 dates) <!-- EDIT -->

---

## 11) Save flags & state (minimum)
- flag_seed_S01_found : boolean
- flag_seed_S02_found : boolean
- ...
- flag_seed_S22_found : boolean <!-- EDIT -->
- flag_seed_S22_mirrored_to_chronicle : boolean <!-- EDIT -->
- flag_seed_S23_found : boolean <!-- EDIT -->
- flag_seed_S23_mirrored_to_chronicle : boolean <!-- EDIT -->
- flag_payoff_P01_triggered : boolean
- player_memory_fragments : int
- charm_owned_by_player : item_id or null
- relationship_X_level : int   // for confidant/romance tracking
- choice_ending_variant : enum {heroic, partial_sacrifice, true_sacrifice}
- flag_Ayaka_memory_points : int   # 0..3
- flag_Ayaka_rel_points : int      # relationship score
- flag_Ayaka_ritual_cooldown : int # turns/chapters until usable
- flag_Ayaka_private_fragment_shared : boolean
- chronosense_uses_current : int  # resets per area or when explicitly refilled
- chronosense_upgrade_level : int  # affects max uses and effectiveness
- chronicle_entries : list  # persistent protected entries mirrored to save and UI.
- essential_seeds_found : map  # maps seed_id -> boolean for easy validation in QA.
- flag_romance_multi_punishment_triggered : boolean
- flag_romance_locked_until_rebuild : boolean
- romance_rebuild_cost : int (default 2)  ← represents extra affinity ranks required to re-romance after downgrade

---

## 12) Monster appendix (compact reference)
- M01 Shrine Guardian  
  - Type: Predator  
  - Difficulty: Easy  
  - Location: Shrine inner room (Ch3)  
  - Behavior: Patrol, slow heavy strike, loyalty to shrine anchors.  
  - Drops: S05 (small shrine charm). On pickup: mirror to Chronicle (protected). <!-- EDIT -->

- M_Wisps Stasis Wisps  
  - Type: Minion swarm (optional pacing)  
  - Difficulty: Easy/Medium  
  - Location: Back alleys / Archive Vault approach (Ch11)  
  - Behavior: swarm, slow corrupting ticks that drain minor memory fragments.  
  - Drops: small memory fragments (non-essential). On pickup: DO NOT mirror to Chronicle. <!-- EDIT -->

- M_MidReliquary (Mid-boss fallback)  
  - Type: Predator  
  - Difficulty: Medium  
  - Location: Archive Vault / back alleys mid-boss (Ch11)  
  - Behavior: Guardian patterns with shield phases; drop S22 as fallback.  
  - Drops: S22 (Reliquary core fragment). On pickup: mirror to Chronicle (protected). `essential_for_payoff: true`. <!-- EDIT -->

- M_Penultimate Reliquary Warden  
  - Type: Predator  
  - Difficulty: Hard  
  - Location: Reliquary Vault / Penultimate (Ch12)  
  - Behavior: Multi-phase with anchor-shield mechanics; summons wisps during second phase.  
  - Drops: S22 (Reliquary core fragment with signatures). On pickup: mirror to Chronicle (protected). `essential_for_payoff: true`. <!-- EDIT -->

- M_Final Engine Heart  
  - Type: Predator  
  - Difficulty: Very Hard  
  - Location: Engine Heart chamber (default Climax Ch11; optional post-credits Ch13)  
  - Behavior: Multi-phase—time pulse arena shifts, anchor-corruption spawns, core volleys cause memory-drain AOE. Tie-in: S23 drop affects P05 branching.  
  - Drops: S23 (Engine Memory Core). On pickup: mirror to Chronicle (protected). `essential_for_payoff: true`. <!-- EDIT -->

**Design notes:** For all monster-dropped seeds that are `essential_for_payoff: true`, the system must:
- Immediately mirror the seed to the Chronicle on pickup and mark `protected: true`. <!-- EDIT -->
- Block any Memory Cost action from removing these entries. <!-- EDIT -->

---

## 13) Final notes / next steps
- Confirm mapping of N -> 13 with narrative leads or adjust placements if final timeline differs. <!-- EDIT -->
- Confirm whether S22 and S23 should be strictly essential or optional canonical evidence; I set both to `true` to avoid payoff blocking. Please confirm. <!-- EDIT -->
- Decide whether the Engine Heart is the Ch11 climax (default applied) or the Ch13 epilogue boss; if kept in Ch13, consider making the boss optional or post-credits. <!-- EDIT -->
- Playtest Ch11–Ch13 pacing with mandatory mid-boss and penultimate fights to ensure emotional beats land without fatigue. <!-- EDIT -->
- Add QA task to verify Chronicle mirroring pseudocode and ensure UI lists protected items in Memory Cost dialog. <!-- EDIT -->

---

_End of document._ 
