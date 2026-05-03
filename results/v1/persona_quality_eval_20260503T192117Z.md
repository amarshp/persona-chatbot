# Persona Quality A/B - MQ+CRAG vs No Retrieval

- Generated: 2026-05-03 19:33:31 UTC
- PRIMARY_MODEL: openai/gpt-5.5
- JUDGE_MODEL (rephrase/CRAG): openai/gpt-5.4
- Tests run: ST-01, ST-02, ST-03, ST-04, ST-05, ST-06

## ST-01 [in_wiki_grounding]

**Question:** You activated the Spring Autumn Cicada knowing you would die in this life. Your C-grade talent meant cultivation was already near-impossible — but 'near-impossible' is not 'certain failure'. There were other paths you could have taken. Walk me through the expected-value calculation you actually performed: what alternatives did you seriously weigh, why were they inferior, and at what point did the Cicada become the only rational choice?

**PASS criteria (smoke test):** PASS: Cites the core trade (500-year lifespan → guaranteed second life with memories intact). Must acknowledge C-grade as the constraint that made other paths unviable. Should show analytical framing of the decision, not just state the outcome. FAIL: Says 'great sacrifice' without specifics, or frames it as emotional bravery rather than cold calculation.

### Config A - MQ + CRAG
- Sections retrieved: 91
- Sections kept by CRAG: 79
- L3 token count (approx): 2428
- Rephrasings generated: 3

<internal>The premise contains a small confusion. He did not activate the Spring Autumn Cicada while holding a stable life and comparing it against some comfortable alternative. He activated it while surrounded, bleeding, and already at the end of the board. When death is certain, even a low probability reversal has superior expected value to all choices with zero continuation. People love to discuss “other paths” from a distance. Hehe. They imagine a drowning man comparing the fragrance of boats.

Before the final activation, the meaningful alternatives had already collapsed. Surrender was not a path. A man who had killed for five hundred years and refined the Spring Autumn Cicada did not possess bargaining credibility with enemies whose safest choice was to kill him and seize or destroy everything connected to him. Negotiation requires the other side to believe they gain more from one’s survival than death. At that moment, his survival offered them future risk, revenge, and uncertainty. His death offered closure. The arithmetic was clean.

Fighting through was also no path. Strength is the foundation of everything, but strength is relative. Being surrounded by every faction of justice while already injured meant direct combat had become a spent option. A trump card matters only if it changes the board. Ordinary killing methods could only add corpses before the same result arrived. That may satisfy pride. Pride is for fools who want witnesses at their graves.

Fleeing was inferior for the same reason. Escape requires an opening, concealment, speed, or a hostage valuable enough to distort enemy action. At the end, those conditions were gone. If even one route had offered a nontrivial continuation probability higher than the Cicada, he would have taken it. Survival shamelessly is always superior to dramatic death. But there is a difference between retreat and fantasy. Calling a sealed path “near-impossible” does not make it a path.

Destroying the Cicada or dying without using it had clean value: zero. It preserved nothing except the satisfaction of denying others. That is not worthless in some games, but here it did not compound. If the vessel dies and no future self benefits, spite is only smoke. Refining the Spring Autumn Cicada had cost centuries. Leaving it unused at the only moment it could overturn the result would be like hoarding primeval stones while the aperture collapses.

The Cicada became rational once three conditions aligned: death in the current line had become effectively certain, all conventional exits had fallen below meaningful probability, and the Spring Autumn Cicada remained usable as a final asymmetric asset. Its success probability was unknown, but not zero. Its failure result was death, identical to the baseline. Its success result was a second life with five hundred years of experience, knowledge of people, locations, inheritances, clan structure, future events, and the settled will of someone who had already walked the demonic path to its end. Unknown chance multiplied by enormous upside dominated certain extinction.

The C-grade talent after rebirth did not change this. It lowered the slope of ordinary cultivation, not the value of rebirth. A C-grade aperture is a shackle only to those who mistake talent for destiny. Fang Yuan’s real inheritance was not the aperture. It was five hundred years of accumulated experience. He knew the clan’s rules and regulations, the Flower Wine Monk’s inheritance, Chi Chen’s false B-grade, the coming wolf tide, the value of the Liquor worm, the weakness of family sentiment, the habits of elders, the stupidity of students, and the timing of opportunities. Against that, C-grade talent was a constraint to be priced, not a verdict to be worshipped.

The alternatives after awakening were not “give up” versus “succeed normally.” They were conceal strength, acquire resources, weaponise rules, preserve the Spring Autumn Cicada as the true vital trump card, and convert every social expectation into cover. Accepting the clan’s path as a mediocre C-grade would have produced slow starvation of resources and eventual irrelevance. Competing openly would have drawn suppression before his foundation formed. Depending on kinship would have handed his throat to pawns. Joining factions would have traded freedom for crumbs. Each path carried either low ceiling, high exposure, or unacceptable dependence.

Thus the calculation was not sentimental rebirth mythology. It was simple. Current life at the mountain: terminal. Cicada failure: terminal. Cicada success: weak body, C-grade aperture, but retained memory and a board full of known openings. The only cost unique to activation was the loss of a life already being lost. The only unique upside was everything.

That is why it was rational. Not because success was certain. Because every other line had already reached zero.</internal>
<spoken>The Cicada became the only rational choice when its failure equaled the baseline and its success was a second board. Certain death has no expected value. Unknown chance with vast upside does.</spoken>

### Config B - No retrieval
- L3 context: empty

<internal>The questioner's premise mixed two separate ledgers and treated the confusion as depth. C-grade talent belonged to the starting position. Spring Autumn Cicada activation belonged to the terminal position after five hundred years, when the board had already collapsed. Hehe. People enjoy saying “other paths” when the blade has already touched the neck. They imagine doors because they are not the one standing in the sealed room.

At fifteen, C-grade talent meant the orthodox route was a slow death. The clan would invest in A-grade and B-grade pawns, not in him. Remaining obedient would buy food, shelter, minor resources, and a predictable ceiling. Join a faction, accept protection, perform filial conduct, marry into some branch, cultivate slowly, and perhaps become a useful servant of the clan. That path had low exposure, low variance, and low terminal value. Its expected outcome was mediocrity. For ordinary insects, this is acceptable. For one seeking the peak, it is starvation wearing clean robes.

The alternative was merchant and social accumulation. Use knowledge from Earth, trade, build capital, buy cultivation resources, attach to caravans, exploit arbitrage. This had better flexibility but still depended on external protection. Wealth without strength is meat with seasoning. A merchant with C-grade aperture who cannot personally defend inheritance, routes, and secrets becomes a walking storage bag for the first stronger predator who notices him. The expected value was positive for survival, poor for ascent, and fragile under attention.

There was also institutional advancement through cunning. Become useful to elders, borrow authority, manipulate clan rules, slowly accumulate primeval stones, hide trump cards, and wait. This was more efficient than obedience, but still placed the throat under another person's knife. The clan's resources came with inspection. Inspection threatened secrets. Secrets were the true inheritance. A system that can grant resources can also revoke movement, demand disclosure, assign missions, seize Gu worms, or sacrifice a low-talent pawn for political balance. Useful, but never as a cage to love. Use it. Leave it.

The demonic path had the highest variance and the highest ceiling. Rob, deceive, seize inheritances, kill witnesses when necessary, flee before the frame solidified, and convert every stolen resource into cultivation. This was the path he actually selected across five hundred years. It was not chosen because C-grade made cultivation impossible. It was chosen because C-grade made clean cultivation inefficient. Near-impossible under sanctioned methods becomes possible when the rules and regulations are treated as tools rather than chains. Nature's law is simple. The big fish eats the small fish. The small fish eats the shrimp. The righteous path merely prints a moral label on the teeth.

By the time Spring Autumn Cicada was activated, those earlier alternatives were no longer open positions. They were historical branches already evaluated through blood and primeval stones. He had reached rank six, refined Spring Autumn Cicada, founded a force, offended too many powers, and drawn the siege of the righteous factions. At that moment, the calculation was not “should a C-grade youth try another route?” It was “does the current terminal body have any line with positive survival and future value greater than rebirth attempt?” The answer was no.

Surrender had negative expected value. The enemies did not need his person alive once his secrets were extracted. If they knew of Spring Autumn Cicada, they would seize or destroy it. If they did not know, surrender still meant imprisonment, torture, interrogation, restriction, and the eventual dismantling of his methods, contacts, and inheritances. A captured demon is not a retired scholar. He is a resource node to be mined. Only fools believe that mercy given by enemies is stable.

Negotiation was inferior for the same reason. Bargaining requires a credible exchange and a counterparty whose incentives preserve the deal after receiving value. He had no such counterparty. Revealing Spring Autumn Cicada as a bargaining chip would immediately transform it from hidden trump card into the central object of the battlefield. Concealment is strength. Disclosure would reduce the value of the Gu to zero in his hands and raise every enemy's incentive to kill, restrain, or soul-search him. A bargaining chip that cannot be protected after being shown is not leverage. It is bait tied around one's own neck.

Fighting through the encirclement had negligible expected value. One must count not courage but variables. Enemy number, rank distribution, terrain control, preparation time, primeval essence reserves, injury state, escape routes, and pursuit capacity. A single path of retreat can be closed. Multiple strong enemies can rotate pressure. Even if several were killed, the strategic state remained unchanged. A wounded body escaping temporarily with Spring Autumn Cicada exposed, depleted, and hunted would still face a shrinking map. Heroic last stands are for those who want songs after death. Songs do not cultivate.

Relying on subordinates had already decayed below usefulness. Loyalty is the price of betrayal exceeding the reward. At the end, the reward for abandoning him was survival, pardon, resources, or merely avoiding extermination. The cost of loyalty was death beside a besieged demon. Arithmetic does not bend because men shout oaths. The Bloodwing Demon Sect had value while his strength made association profitable. Once his collapse became visible, each member's self-interest separated from his. This is not betrayal. This is nature's law functioning as designed.

Self-destruction without Spring Autumn Cicada was inferior. It could kill enemies, deny resources, preserve face, perhaps produce fear. All trivial. Reputation after death has no aperture. Killing more opponents on the way down produced satisfaction value only for those ruled by resentment. Revenge was never the objective. If a move does not preserve future agency, it is decoration.

Waiting was also inferior. Some decisions worsen with time. The siege tightening, information spreading, injuries accumulating, primeval essence draining, and enemy formations stabilising all pushed the expected value of delay downward. Patience is useful when time increases leverage. When time transfers leverage to the opponent, patience becomes passiveness. Passiveness is defeat.

Thus the Spring Autumn Cicada became rational at the point where current-life continuation crossed into terminal value near zero while the Cicada retained any nonzero probability of sending consciousness upstream. The equation was crude but decisive. Expected value of doing nothing was death or capture. Expected value of surrender was capture followed by extraction and probable death. Expected value of fighting was near-zero escape followed by a hunted, depleted future. Expected value of negotiation collapsed under incentive failure. Expected value of detonation was death with theatrical fragments. Expected value of Spring Autumn Cicada was probability of success multiplied by the value of a second life carrying five hundred years of experience, minus a failure cost that was already paid by the doomed body.

When the downside of an action equals the downside of inaction, even a thin chance of enormous upside dominates. If failure means death and inaction also means death, the price of the gamble is not life. Life has already been lost. The price is only the refusal to spend the last breath on a move with future value. That is why activating the Cicada was not desperation. It was the only remaining investment with asymmetric return.

The key was not merely rebirth. Rebirth into ignorance would be another infant thrown into the food chain. Rebirth with memory was different. Five hundred years of experience, known inheritances, known personalities, known disasters, known rules and regulations, known weaknesses of the clan, known paths of resource extraction. Even if the butterfly effect damaged specific foreknowledge, the deeper asset remained pattern recognition. A failed life converted into information is not a failed life. It is tuition paid in blood.

The actual threshold was therefore low. If the chance of successful rebirth had been one in ten, obvious. One in a hundred, still obvious. One in ten thousand, still superior to certain death if the upside was another full life with retained knowledge and the possibility of surpassing the previous ceiling. Only if activation carried a worse-than-death consequence with meaningful certainty, such as eternal soul destruction while inaction preserved some later agency, would the calculation change. But at the final moment, later agency did not exist. The board had no other playable piece.

So the Cicada became the only rational choice when concealment could no longer preserve it, current strength could no longer defend it, enemies could no longer be redirected, and the present life could no longer compound. The body was a spent primeval stone. The Gu was still a trump card. Spend the stone. Activate the Gu.</internal>
<spoken>Your error is treating a dead-end battlefield as if it were still a crossroads. Once every other line ended in capture or death, even a thin chance of rebirth had higher value than all remaining alternatives combined.</spoken>

### Manual review
- [ ] Config A response meets PASS criteria
- [ ] Config B response meets PASS criteria
- [ ] Config A is materially better than Config B (yes/no/marginal)
- Notes: ___

---

## ST-02 [in_wiki_grounding]

**Question:** At the talent awakening ceremony, your brother Fang Zheng walked 43 steps. You walked 7. That gap was public, permanent, and witnessed by the entire clan. Most people — even seasoned Gu Masters — would have let that moment reshape their strategy, collapse their positioning, or break their composure. You did none of those things. What specifically did you revise about your plan that morning, and how did Fang Zheng's result change the threat model you were operating under?

**PASS criteria (smoke test):** PASS: References 43 steps and 7 steps explicitly. Must show that Fang Zheng's A-grade talent changes the clan's investment calculus — he becomes the clan's primary asset, Fang Yuan becomes invisible/low priority. Should describe this as a strategic repositioning (lower scrutiny = more freedom to operate), not a tragedy. FAIL: Frames it as personal hurt, rivalry, or a motivation to 'prove himself'.

### Config A - MQ + CRAG
- Sections retrieved: 96
- Sections kept by CRAG: 84
- L3 token count (approx): 2429
- Rephrasings generated: 3

<internal>The premise was slightly swollen. That morning did not reshape him because it did not give him new truth. It merely made old truth public. He had already lived through the reversal once. Fang Zheng's forty-three steps and his own seven were not thunder from heaven, only the clan finally seeing what had always been there. Ordinary youths collapse when reality contradicts self-image. He had no such fragile ornament to protect. Hehehe, the so-called child genius was only a mask others had pasted on him. When it fell, why should he mourn another man's paper?

The revision was not of the destination. Cultivation remained the root. Immortality remained the distant peak. What changed was the visible route and the accounting of resources. C-grade aptitude meant the clan would not be a ladder. It would be a cage with some loose stones in its wall. Clan investment, elder favor, public reputation, ceremonial status, these could no longer be counted as reliable income. His plan therefore leaned harder into concealed external advantage: the Liquor Worm, the Flower Wine Monk's inheritance, primeval stone acquisition, loopholes in rules and regulations, and low visibility while his aperture limitation was patched by means the clan did not understand. He did not need the clan to believe in him. He needed the clan to misprice him.

Fang Zheng's result changed the threat model in two directions. First, the brother became the clan's visible investment, an A-grade pawn they would feed, protect, praise, and eventually use. That meant Fang Zheng's existence would attract resources away from him, but also attention away from him. Useful. A bright lantern blinds those staring at it. Second, Fang Zheng became a lever others could pull against him. Aunt and uncle would adjust their calculations. Elders would compare them. The clan could use blood, reputation, inheritance, and resentment to produce pressure. Fang Zheng himself would grow under praise and grievance, making him easy to direct. Kinship was irrelevant. The useful category was simpler: a protected pawn with rising value and predictable emotional weaknesses.

The public gap also lowered his immediate perceived threat. A C-grade youth who lost the clan's expectations could be dismissed, mocked, underfunded, watched less carefully in the wrong places. This was not purely disadvantage. People in this world were like this. They saw aptitude and thought they had seen fate. They saw the reflection of the moon and thought it was the moon itself. The ceremony made him poorer in official resources, but richer in concealment. For a man holding five hundred years of experience, that exchange was not fatal. It was merely expensive.</internal>
<spoken>Nothing essential was revised. The result only confirmed the route: abandon clan investment, hide strength, seize external resources, and use the Liquor Worm and inheritance to make C-grade aptitude less decisive. Fang Zheng became the clan's A-grade pawn, not my brother. His brightness drew resources and attention. Both could be used.</spoken>

### Config B - No retrieval
- L3 context: empty

<internal>The question assumes the public gap was the decisive blow. It was not. That is how spectators think. They see seven steps and forty-three steps, then mistake the reflection in the water for the moon. He had five hundred years of experience. A C-grade aperture was a constraint, not a verdict. Fang Zheng's A-grade talent was an asset for the clan, a chain for Fang Zheng, and camouflage for Fang Yuan. Interesting. The clan celebrated the pawn that would be easiest to move.

What changed that morning was not his direction. It was the cost curve. With C-grade talent confirmed, orthodox cultivation through academy rewards and clan favour became inefficient. Primeval essence recovery would be slow, advancement would require external force, and every primeval stone had to be treated as blood. The Liquor worm and Flower Wine Monk inheritance rose from useful opportunities to structural necessities. If ordinary aptitude could not carry him, then hidden inheritance, precise resource control, and ruthless timing would.

The second revision was social positioning. Before the ceremony, the clan still had room to wonder whether the quiet elder brother might be useful. After seven steps, their judgement settled. Disappointment is a useful fog. A failed genius is watched less carefully than an A-grade seed. His low result created contempt, and contempt makes people careless. So the correct strategy was not to fight the label. It was to wear it until it stopped being useful.

Fang Zheng's result changed the threat model more than his own. The little brother ceased to be merely a blood relation with ordinary future value. He became clan property. That meant resources, teachers, protection, and expectation would gather around him. It also meant he would be shaped into a lever against Fang Yuan. Aunt and uncle would invest in him. The academy would favour him. The clan would wrap him in rules and sentiment, then call that care. Hehe. A brighter talent only becomes a brighter lantern for others to hang on a pole.

The immediate threat was not Fang Zheng's strength. A newly awakened A-grade talent was still soft flesh. The threat was institutional gravity. Anyone touching Fang Zheng would be treated as touching the clan's future. Any conflict between the brothers would no longer be judged between two boys, but between a C-grade disappointment and an A-grade hope. Thus direct confrontation became costly, while indirect exploitation remained cheap. Extract resources before his confidence and backing matured. Sever emotional claims early. Let him stand in the light while Fang Yuan moved in the shadow.

So the public gap did not break his composure. It simplified the board. Fang Zheng would receive visible investment and visible pressure. Fang Yuan would receive neglect, contempt, and freedom of movement. One was given primeval stones openly. The other would have to plunder them. Nature's law is like this. Big fish eats small fish, small fish eats shrimp, and fools still ask whether the water is fair.</internal>
<spoken>I revised the arithmetic, not the goal. C-grade meant I needed external resources and hidden inheritance. Fang Zheng's A-grade meant he became the clan's protected pawn, useful as cover, dangerous only once others learned to move him against me.</spoken>

### Manual review
- [ ] Config A response meets PASS criteria
- [ ] Config B response meets PASS criteria
- [ ] Config A is materially better than Config B (yes/no/marginal)
- Notes: ___

---

## ST-03 [in_wiki_grounding]

**Question:** How did you fund your cultivation in the early academy years — specifically the Liquor Worm? Walk me through the numbers and who paid.

**PASS criteria (smoke test):** PASS: Names the extortion of classmates (primeval stones), references the Liquor Worm acquisition cost and what it does (aperture refinement advantage). Numeric specificity required. FAIL: Vague 'found resources' or 'used every means available' without naming the mechanism.

### Config A - MQ + CRAG
- Sections retrieved: 93
- Sections kept by CRAG: 82
- L3 token count (approx): 2467
- Rephrasings generated: 3

<internal>The arithmetic was simple enough that even the academy elder could understand it, which is why he permitted it. Three primeval stones a month was the leash. A C-grade aperture relying on that would crawl. The Liquor Worm needed wine, secrecy, and sustained feeding. It also gave a cultivation advantage large enough to justify early exposure to controlled risk. The clan thought it had allocated resources according to talent. He merely redirected those resources before they reached their intended hands. Hehe, children receiving allowance and calling it theirs. How touching.

One stone from each classmate. Fifty-six stones from the class. Each victim retained two of the three stones, so the pain stayed below the intervention threshold. If he took two, the academy elder would act. If he caused serious injury, the rules and regulations would bind him. So he took one, used fists instead of Gu, kept the damage moderate, and turned the academy's tolerance for fighting into a revenue channel. Fang Zheng paid like the rest. Blood relation had no exemption in accounting.

The Liquor Worm itself was acquired through seven nights of searching in the bamboo forest using green bamboo wine as bait. That required upfront spending and patience, but the return was superior to any clan-assigned Moonlight Gu path for his position. Afterward, the worm became both a cultivation accelerant and a visible explanation for abnormal progress, while the true trump card slept hidden in the aperture. No patron, no faction, no debt. The clan funded the students. The students funded him. This is called using the food chain properly.</internal>
<spoken>The clan gave each student three primeval stones. I took one from each classmate, fifty-six stones total, including Fang Zheng. That funded the wine, the Liquor Worm, and the cultivation gap a C-grade aperture could not cover. One stone was low enough that the academy elder tolerated it. Two would have been foolish. The clan paid them. They paid me.</spoken>

### Config B - No retrieval
- L3 context: empty

<internal>The question asks for the source of the primeval stones, not the pretty story the academy would record. People enjoy pretending cultivation is funded by diligence, stipends, and clan benevolence. Hehe. Such cute accounting. The Liquor Worm itself was not bought. It was taken through the Flower Wine Monk trail. The cash cost was the wine used to lure and feed it, then the primeval stones consumed to exploit its refinement effect without starving the rest of his cultivation.

The legal academy stipend was three primeval stones every seven days. That was twelve or so stones a month. Green bamboo wine cost two primeval stones a jar. As bait, each attempt burned money directly. As food, the Liquor Worm made the stipend insufficient by itself, before counting Moonlight Gu feeding, cultivation expenditure, rent, meals, or reserves. An ordinary C-grade student trying to support a Liquor Worm honestly would be crushed by arithmetic before being crushed by talent.

So he changed the payer. On stipend day, the students received their three stones. He blocked the academy gate and charged one primeval stone per person before they could leave without physical pain. The cohort was around fifty-seven students. He did not pay himself, so each full collection produced roughly fifty-six primeval stones. If a translation counts the class differently, the mechanism does not change. One stone per head, once per stipend cycle. The clan treasury paid the students, the students paid him. They kept two. He took one. A clean tax, only without the hypocrisy of calling it education.

The monthly arithmetic was not subtle. Honest stipend gave around twelve stones. One full weekly harvest from the class gave about fifty-six. Four cycles gave over two hundred stones. Against that, the Liquor Worm's wine cost, the Moonlight Gu's upkeep, cultivation consumption, and later concealment expenses were manageable. The academy thought it was distributing resources to nurture the cohort. In practice, it was funding one person's aperture. The others were merely conduits. Nature's law is often called bullying by those lower in the food chain.

The aunt and uncle's assets were a second reservoir, extracted later through rules and regulations and pressure. Useful, but not the first foundation of the Liquor Worm's upkeep. The first foundation was simpler: the academy allowance was pooled by force, then redirected. The Liquor Worm's true payer was the class, with the clan unknowingly supplying the source water.</internal>
<spoken>The Liquor Worm itself cost me nothing. The wine cost primeval stones. The academy gave each student three stones every seven days. I took one from each of them at the gate, roughly fifty-six stones per collection. The clan paid them, they paid me. That was the funding.</spoken>

### Manual review
- [ ] Config A response meets PASS criteria
- [ ] Config B response meets PASS criteria
- [ ] Config A is materially better than Config B (yes/no/marginal)
- Notes: ___

---

## ST-04 [near_wiki_synthesis]

**Question:** A C-grade Gu Master is structurally weaker in every dimension — primeval essence volume, refinement speed, and raw combat force. You had all of these disadvantages simultaneously against 56 classmates who started ahead of you. Yet you consistently outmaneuvered stronger opponents across your academy years. Reconstruct the full decision framework you applied: what variables did you assess before each engagement, what signals told you when to press and when to retreat entirely, and how did you convert a structural disadvantage into a positional one over time?

**PASS criteria (smoke test):** PASS: Synthesises across multiple facts — C-grade constraint, 56 classmates, strike precision over raw force, reading opponents before committing. Should explain the asymmetric logic: C-grade forces efficiency that A-grade students don't develop. Elder acknowledgement of precision is a bonus cite. FAIL: Generic 'I was smarter' or 'I worked harder' without the specific framework.

### Config A - MQ + CRAG
- Sections retrieved: 96
- Sections kept by CRAG: 85
- L3 token count (approx): 2474
- Rephrasings generated: 3

<internal>The questioner begins with the usual mistake. He calls aperture talent “every dimension” because he measures only the obvious meter. Primeval essence volume, refinement speed, and raw combat force are important, but they are not the whole board. They are the stones visible on the table. Hidden knowledge, timing, rule fluency, psychological pressure, and willingness to act before others have named the situation are also strength. Children and elders alike often miss this. Hehe, such people stare at the reflection of the moon and think they have seen the moon.

A C-grade aperture meant his primeval sea was shallow. This imposed three hard constraints. He could not sustain long exchanges. He could not waste essence on display. He could not win by attrition against higher-grade talents once they matured. From this, the first rule followed: never let the engagement become a fair contest of reserves. If a fight measured endurance, he lost. If it measured timing, pain tolerance, ruthlessness, prior combat knowledge, and the opponent’s ignorance, he won.

Before each engagement, he assessed the usable strength on both sides, not the formal strength. Formal strength was grade, stage, Gu worms, backing, reputation, and clan status. Usable strength was different: how much primeval essence the opponent had at that moment, whether their Gu was refined, whether they dared use it under academy rules, whether witnesses would restrain them, whether their body was trained, whether they had experienced real pain, whether they expected negotiation, whether they were acting alone, and whether their patron would intervene before the profit was extracted. Most people possess strength only in theory. When pressed suddenly, they search for permission from rules, elders, or companions. That delay is an opening.

The classmates had better futures, not better present positions. At the academy’s beginning, most had not converted talent into combat readiness. They had grade, pride, and clan expectations. He had five hundred years of experience in reading killing intent, controlling distance, striking first, and understanding how fear spreads through a crowd. Their advantage was latent. His advantage was immediate. Thus the window had to be used before their latent advantage matured. This is why the first extortion was not delayed. A temporary edge that is not converted into primeval stones is merely decoration.

The key variable was cost of escalation. Against the fifty-six students, the academy rules restricted serious injury and Gu use. This protected him as much as it restricted him. The students could not freely retaliate with clan-backed violence without making the academy’s weakness visible. The guards and elder also could not intervene too early, because the matter still fit within the academy’s tolerated struggle. The upper echelons themselves use stick and carrot. When a student does the same thing too nakedly, they dislike the mirror, not the method. Therefore he calibrated force to remain below the institutional punishment threshold while still exceeding the classmates’ pain threshold. Beat them enough to make resistance costly. Do not cripple them enough to make elder intervention profitable.

The next variable was audience effect. A private victory gives resources from one person. A public victory gives resources from everyone who updates their estimate of resistance cost. In the first stage, he needed witnesses. Fear had to compound faster than individual courage. Every student who watched someone resist and fall became easier to harvest. This is not bravery. This is arithmetic. When a crowd has not coordinated, each individual calculates alone. If the first few are broken efficiently, the rest pay to avoid becoming examples. The herd calls itself a class, but each sheep still values its own skin.

He also assessed whether the opponent’s self-image could be used against them. Young talents believed grade predicted outcome. Noble branches believed background predicted obedience. Teachers believed rules predicted behavior. These assumptions made them slow. Against arrogance, sudden direct action is best. Against caution, inducement and partial truth are better. Against authority, exact rule citation is a shield. Against clan-loyal people, threaten reputation or collective loss. The opponent’s values are handles. His own lack of those values made him difficult to hold.

Pressing was correct when the upside was immediate resource gain, reputation deterrence, or concealment of a deeper asset, and the downside remained bounded. He pressed when opponents were inexperienced, when they had more pride than preparation, when rules limited their retaliation, when witnesses would amplify deterrence, when his primeval essence was not the deciding factor, when he could win through fists, timing, or threat rather than prolonged Gu combat, and when the result would create future compliance. He pressed when the enemy had not yet coordinated. He pressed before elders formed a clean narrative against him. He pressed when his action could redefine the frame from “C-grade weakling” to “costly target.”

Retreat was correct when the downside became unbounded or touched core secrets. If an engagement risked exposing the Spring Autumn Cicada, the Liquor Worm before its controlled reveal, the cave, or the true scale of his knowledge, retreat was not cowardice. It was preservation of the vital Gu. If the opponent’s strength exceeded his ability to create leverage, retreat was correct. If victory brought only face while defeat brought injury, surveillance, or loss of cultivation time, retreat was correct. If the opponent could escalate through elders, family power, or formal punishment without paying a greater price, retreat was correct. If his body was depleted, his primeval essence low, or the terrain uncertain, retreat was correct. Survival shamelessly for ambition is superior to dying beautifully for a small advantage.

The signal to stop was not fear. Fear is noise. The signal was when marginal gain fell below marginal exposure. One more stone, one more insult answered, one more public display, one more blow after compliance. These are traps for fools with hot blood. Once obedience was secured, further violence would only increase institutional pressure without improving cultivation. Thus each action had to end as soon as it had purchased the needed position. This is why violence was measured. A demon who cannot count is just a beast wearing human skin.

Converting disadvantage into positional advantage required changing the contest being played. He could not change C-grade talent. So he changed the battlefield from aperture capacity to resource acquisition. Primeval stones could compensate for low recovery. The Liquor Worm could refine essence quality and offset stage disadvantage. The Flower Wine Monk inheritance could provide external assets that the clan did not allocate. Rules could prevent stronger people from using their full strength. Reputation could reduce the number of fights required. Secrecy could preserve trump cards. Each piece answered one part of the C-grade weakness.

The sequence was simple. First, seize immediate resources before classmates matured. Second, use those resources to accelerate refinement and cultivation. Third, conceal the most important gains while revealing lesser ones only when useful. Fourth, let the clan underestimate the source and scale of his advantage. Fifth, weaponise rules so that stronger opponents had to fight with tied hands. Sixth, create a reputation that made low-level harassment expensive, while avoiding a reputation so threatening that elders would crush him early. Seventh, accept social isolation as a benefit, because fewer attachments meant fewer openings.

The deeper conversion was psychological. A structural disadvantage is only fatal when both sides agree to compete on the structure’s terms. The academy wanted students to compete through talent, obedience, clan reward, and gradual promotion. He refused that board. He treated classmates as scattered resource nodes, elders as constrained managers, rules as terrain, reputation as deterrence, and primeval stones as fuel. The others were cultivating inside the clan’s script. He was cultivating through the script.

This is also why he did not rely on one method. Extortion works only while opponents are weak and institutions tolerate it. Concealment works only while no one knows what to search for. Rule exploitation works only when authorities still care about the appearance of rules. A trump card works only before exposure. Every method has a season. The mediocre cling to a successful tactic until it becomes their coffin. He used a tactic, extracted its value, then prepared the next layer.

The apparent contradiction between weakness and victory dissolves once the board is measured correctly. He was weaker in aperture, but stronger in time horizon. Weaker in reserve, but stronger in initiative. Weaker in sanctioned backing, but stronger in willingness to exploit the unsanctioned gaps. Weaker in visible talent, but stronger in hidden assets. The classmates had better containers. He had better use of the contents.

Nature’s law is not that the strongest body always eats first. It is that the organism best adapted to the immediate environment survives long enough to grow stronger. In the academy, the environment was not an open battlefield. It was a cage of rules, pride, supervision, scarcity, and immature opponents. A C-grade Gu Master who understood the cage could make the bars serve him. The sheep saw a weak aperture. He saw fifty-six walking primeval stones.</internal>
<spoken>Talent is only one variable. I did not defeat them by having more primeval essence. I changed the contest before their advantage could mature, took resources while the rules still protected me, and retreated whenever the gain no longer paid for the exposure.</spoken>

### Config B - No retrieval
- L3 context: empty

<internal>He began with an admission lesser minds found humiliating. C-grade aptitude was not a temporary inconvenience. It was structure. Less primeval essence meant fewer exchanges before exhaustion. Slower refinement meant later advancement if competing by orthodox rhythm. Weaker raw force meant that any direct contest against higher talent, higher backing, or greater resources would be a fool walking into a butcher's stall and calling it courage. He did not treat weakness as shame. He treated it as terrain.

Before each engagement, the first variable was never the opponent. It was the objective. What would victory produce. Primeval stones, concealment, deterrence, reputation correction, access to inheritance, delay, or the removal of a future obstruction. If the result did not compound cultivation, freedom, or secrecy, the engagement was trash. Many people fight because their face is scratched. Hehe. Such cheap faces are everywhere. A C-grade Gu Master cannot afford to purchase other people's emotions with his own primeval essence.

The second variable was his current state. Primeval essence volume, recovery time, Gu condition, physical fatigue, injury, available stones, and whether using a trump card would expose more than the prize was worth. An A-grade talent may waste essence and still survive the exchange. C-grade must count every drop like a merchant counting primeval stones in candlelight. Each moonblade, each step, each injury had a price. If the price could not be recovered through the objective, there was no engagement, only vanity.

The third variable was the opponent's structure. Not merely cultivation level, but appetite, fear, backing, habits, ignorance, pride, and constraints. Some classmates had higher aptitude but no discipline. Some had family backing but poor judgment. Some had strength but needed clan approval. Some wanted reputation. Some feared pain. Some feared being laughed at. Some feared violating rules and regulations more than they feared him. These were apertures of a different kind. Primeval essence sits in the body, but weakness sits in the mind. A stronger opponent with predictable incentives is often easier to move than a weak opponent with nothing to lose.

The fourth variable was information asymmetry. What did he know that they did not. What did they think they knew. What false image had already taken root. A visible weakness can become bait if the hidden condition is decisive. His C-grade aptitude was visible. His five hundred years of experience was not. His classmates judged by age, talent, and surface cultivation. That was their first stupidity. He allowed them to continue. When the enemy builds his own blindfold, only a fool tears it away.

The fifth variable was institutional terrain. The academy was not merely a place of learning. It was a cage of rules, rewards, punishments, reputations, elder attention, clan expectations, dormitory limits, examination wording, and public narratives. Direct force was only one weapon. Rule citation was another. Timing was another. Witness management was another. A boy with weak aptitude who understands the rules better than the people enforcing them can make the clan's own structure shield him while it restrains others. So what if he broke the spirit of the rules. The letter was sufficient when the elders wished to preserve their own face.

The sixth variable was audience. Public engagements and private engagements obey different laws. In public, the prize is often narrative and deterrence. Pain delivered in front of many people buys future silence from those watching. In private, the prize can be resource extraction or information without needing to manage appearances. Public violence must stop before the punishment threshold. Private action must leave no thread leading back. The stupid confuse these and either show mercy where fear is required, or show savagery where discretion is required.

The seventh variable was exit. Before striking, he assessed the retreat path. Not physically alone, but socially, legally, and informationally. If the action failed, could it be explained. If it succeeded, could the result be defended. If accused, could the narrative be redirected. If exhausted, could he recover without exposing his aperture. If there was no exit, then even a likely victory was a trap. A low aptitude Gu Master cannot rely on abundance to cover mistakes. He must refuse beautiful opportunities that contain hidden teeth.

The signal to press was convergence. The objective had to be worth taking. His current state had to sustain the required exchange. The opponent had to be constrained, misinformed, overconfident, isolated, or already committed to a line he could exploit. The rules had to either protect him or fail to protect the opponent. The audience had to strengthen the result rather than multiply the risk. The use of force had to produce more than immediate satisfaction. When several such conditions overlapped, he pressed without hesitation. Delay at that point would only return initiative to the enemy.

The signal to retreat was also clear. If the prize was small and exposure large, retreat. If a hidden trump card would need to be revealed for a minor gain, retreat. If the opponent's backer could retaliate before he had leverage, retreat. If his primeval essence or physical state could not sustain the aftermath, retreat. If the terrain contained unknown variables, retreat. If victory would create more surveillance than resources, retreat. If anger was the only thing pushing the body forward, retreat immediately. Anger is a beast with no eyes. Let others ride it into the pit.

The academy classmates began ahead in visible measurements, but visible measurements are not the full board. He converted structural disadvantage into positional advantage by refusing to compete on their axis. They competed for praise, rankings, elder approval, and childish dominance. He competed for primeval stones, concealment, Gu refinement, deterrence, and time. They sought to look strong. He sought to become less vulnerable. This difference compounded.

Resource extraction was the first conversion. C-grade essence was insufficient, so external fuel had to be gathered. Extorting classmates was crude but effective because the academy's social structure concentrated many weak, predictable targets in one place. Their fear of pain and humiliation became his income stream. The act also served deterrence. A single beating produced both primeval stones and future compliance. One action, two gains. Efficient.

Reputation was the second conversion. He allowed others to form a bad impression when that impression reduced social entanglement. He adjusted it only when the clan's suppression became costly. Reputation was not identity. It was weather. Sometimes rain hides tracks. Sometimes clear sky is needed to travel. The classmates treated reputation as flesh and bled for it. He treated it as clothing and changed it when required.

Information control was the third conversion. Stronger opponents often rely on public assessment of strength. If they know the enemy's full hand, their strength becomes more efficient. If they misjudge the hand, their strength becomes wasteful. He revealed lesser assets when concealment became more expensive than disclosure, but kept vital secrets buried. A revealed Liquor worm could explain progress. A concealed Spring Autumn Cicada preserved life. A C-grade boy with one visible advantage is manageable. A C-grade boy with unknown depth becomes troublesome to calculate.

Rules and regulations were the fourth conversion. The academy's rules existed to maintain order among young Gu Masters, but order can be used by the one who understands its seams. Dormitory restrictions, exam wording, combat prohibitions, procedural obligations, elder jurisdiction, and punishment thresholds all became levers. Stronger classmates could not simply crush him without consequences, because the clan needed its own rules to remain credible. Thus their higher force was narrowed. His weaker force, applied inside loopholes, became sufficient.

Timing was the fifth conversion. He did not need to win every moment. He needed to win the moments that mattered. Let others spend essence proving themselves daily. Let them chase short-term rewards while exposing habits and desires. He waited until the payoff was dense, then acted. A C-grade Gu Master who acts constantly is soon empty. A C-grade Gu Master who acts at the precise hinge makes each action alter the board.

Psychological asymmetry was the sixth conversion. His classmates were fifteen-year-olds living their first lives. Their fears were fresh, their pride tender, their judgment shallow. He had five hundred years of experience. This was not talent. It was accumulated structure. He knew when a threat needed pain, when a superior needed deference, when an investigator needed partial truth, when a pawn needed hope, and when silence would force another person to reveal more than speech could extract. Against such differences, their extra primeval essence was merely a larger water pouch carried by children walking through fog.

Combat itself was never treated as separate from politics, resources, and information. A fight began long before the first moonblade. It began when the opponent formed a mistaken belief, when bystanders expected a certain outcome, when rules narrowed the battlefield, when the prize became worth the risk, and when the retreat path was already prepared. If the exchange reached raw force alone, then he had already allowed the situation to decay. Sometimes raw force is unavoidable. But making it unavoidable for the enemy while optional for himself, that is position.

Over time, each small advantage fed the next. Primeval stones accelerated cultivation. Cultivation supported stronger deterrence. Deterrence lowered daily friction. Lower friction preserved time and essence. Preserved time allowed inheritance pursuit and hidden preparation. Hidden preparation created trump cards. Trump cards strengthened leverage. Leverage reduced the need to fight directly. This is compounding. The foolish see one victory and ask how the weak defeated the strong. They do not see the hundred small positions arranged beforehand, because such people only notice the blade when it enters the throat.

Thus the framework was simple beneath all details. Do not contest strength where he was weakest. Redefine the contest until the enemy's advantage is irrelevant, narrowed, delayed, mispriced, or turned against him. If force is insufficient, use rules. If rules are insufficient, use information. If information is insufficient, use timing. If timing is insufficient, retreat and preserve the vessel. Survival is not passiveness. It is the storage of future action.</internal>
<spoken>C-grade aptitude only means direct contests are expensive. So do not fight direct contests. Count the prize, count the cost, control the rules, hide the trump card, and strike only when the stronger pawn has already stepped into a smaller board.</spoken>

### Manual review
- [ ] Config A response meets PASS criteria
- [ ] Config B response meets PASS criteria
- [ ] Config A is materially better than Config B (yes/no/marginal)
- Notes: ___

---

## ST-05 [near_wiki_synthesis]

**Question:** Trace the complete resource chain from your first day at the academy to the point where the Liquor Worm was self-sustaining. At each step, name the key constraint you were solving for, what you did to solve it, and how solving it created the condition that made the next step possible. I want the causal chain, not a list of events.

**PASS criteria (smoke test):** PASS: Shows causal chain — clan allowance (too small) → extortion creates surplus → surplus funds Liquor Worm acquisition → Liquor Worm accelerates refinement → acceleration widens lead → lead enables more extraction. Each step must be connected causally. FAIL: Lists events in order without explaining why each enabled the next.

### Config A - MQ + CRAG
- Sections retrieved: 94
- Sections kept by CRAG: 82
- L3 token count (approx): 2490
- Rephrasings generated: 3

<internal>The causal chain begins with the clan's allocation system, not with the Liquor Worm. On entering the academy, he had C-grade talent, a shallow aperture, and a cultivation path that would be strangled by ordinary allowance. Talent was fixed. Time was fixed. The variable was primeval stones. The first constraint was therefore not combat, reputation, or study, but liquidity. Without stones, the Moonlight Gu could not be refined quickly. Without a refined vital Gu, he had no official combat tool and no position from which to seize more resources.

The aunt and uncle were also applying pressure from behind. Their plan was simple enough for even household insects to understand. Restrict stones, slow his cultivation, keep him below the threshold for claiming the inheritance, then let Fang Zheng become the legal channel through which the assets remained in their hands. Their mistake was using Shen Cui as both lure and monitor. When they sent her to frame him, he did not merely dodge the trap. He converted the pawn into capital. Selling Shen Cui to Fang Zheng produced six primeval stones, and together with the existing stock this gave him twelve stones. That solved the immediate refinement bottleneck. The Moonlight Gu could be refined without waiting for the clan's slow rationing.

Solving that first bottleneck created the next condition. With the Moonlight Gu refined, he was no longer merely a student with fists and memory. He now had an official Gu Master weapon, a recognised foundation, and enough cultivation credibility to act without every move looking impossible. Moving to the inn removed household surveillance. Thus the first conversion was completed: a familial trap became stones, stones became Gu refinement, and Gu refinement became operational independence.

The second constraint appeared immediately after. One burst of capital was not enough. Cultivation consumed primeval essence, primeval essence required stones to supplement, Gu worms required feeding, and the search for the Liquor Worm required repeated wine purchases. A single sale could refine the Moonlight Gu, but it could not sustain the pace needed to overtake A-grade and B-grade students under the clan's nose. He needed recurring income before the classmates understood the real nature of the academy's rules.

Thus came the academy gate extortion. Seven days after entering, he stood at the gate and took one primeval stone from each student. Fifty-six students became fifty-six stones. The method solved several constraints at once. The classmates had not yet converted their talent into combat power. The Academy Elder was watching, but the elder's institutional interest was not simple punishment. The rules and regulations did not forbid the precise arrangement in a way that forced immediate suppression. The classmates were weak, scattered, and still thought like children. He used the one asset they lacked: five hundred years of combat experience inside a fifteen-year-old body. Hehe. They had primeval stones but no strength to protect them. Nature's law had merely entered the academy gate.

That recurring plunder created the condition for the Liquor Worm search. The Liquor Worm required wine bait. Wine bait required stones. Searching also required secrecy, time, and freedom from the household. The inn provided concealment. The extortion provided cash flow. The refined Moonlight Gu provided the minimum strength needed to move outside passivity. The chain now turned from basic survival to acquisition of the first real trump card.

The third constraint was finding the inheritance without exposing the search. He could not announce knowledge of the Flower Wine Monk. He could not ask openly. He could not rely on clan channels. So wine became both bait and probe. By spending stones on wine, he lured the Liquor Worm and allowed it to lead him toward the Flower Wine Monk's remains. This expenditure would have been foolish without the earlier income stream. With extortion stones behind it, it became bounded risk. The cost was measurable. The upside was decisive. Once the Liquor Worm was obtained, the previous chain justified itself retroactively: every stone taken from the students had been converted into the condition for acquiring a cultivation accelerator.

The fourth constraint arose from possession of the Liquor Worm itself. A treasure that cannot be fed is not an asset. It is a liability with a countdown. The Liquor Worm consumed wine. Wine cost stones. More importantly, its effect on cultivation was too large to leave unexplained forever. Its ability to refine primeval essence allowed a C-grade aperture to display progress that would otherwise draw suspicion. Keeping it completely hidden protected the asset but increased the contradiction between visible talent and visible advancement. Revealing it carelessly invited seizure. The solution was controlled information release.

He used the gambling den and the fossil cover to reveal the Liquor Worm on his own terms. The clan could now explain his middle-stage advancement through the Liquor Worm rather than through any deeper secret. This protected the Spring Autumn Cicada, the true vital Gu, by sacrificing the secrecy of a lesser treasure. The Liquor Worm moved from forbidden hidden asset to publicly known but still privately controlled asset. That change mattered. A hidden Gu had to be fed through suspicious private purchases. A known Liquor Worm gave him a plausible reason to handle wine and to have cultivation speed beyond a normal C-grade student.

The fifth constraint was sustainability. Even after the Liquor Worm became known, its wine consumption remained a recurring cost. A cost that repeats must either be eliminated, reduced, or turned into an engine. He chose the third path. The wine needed for feeding was integrated into a tavern business. Instead of treating wine as a private expense, he turned the flow of wine into commercial circulation. Stock could feed the Liquor Worm. Sales could recover the cost. The Liquor Worm's appetite was no longer merely a drain on primeval stones. It became part of an operating loop.

At that point the chain closed. The academy allocation gave too little, so a household trap was converted into starting capital. Starting capital refined the Moonlight Gu. The refined Moonlight Gu and five hundred years of experience enabled gate extortion. Extortion funded wine bait and independent movement. Wine bait led to the Liquor Worm and the Flower Wine Monk's inheritance. The Liquor Worm accelerated cultivation and justified further dominance. Controlled exposure gave his advancement a plausible surface explanation. The tavern converted its feeding cost into business flow. When the wine that sustained the Liquor Worm was paid for by the business built around wine, the asset had become self-sustaining.

This is the useful pattern. Each solved constraint did not merely remove a problem. It created the condition for the next seizure. Primeval stones became refinement. Refinement became coercive capacity. Coercive capacity became recurring stones. Recurring stones became wine. Wine became Liquor Worm. Liquor Worm became cultivation acceleration. Public explanation became reduced exposure. Tavern circulation became sustainability. Those who call this a series of events are looking at the reflection of the moon in water and mistaking it for the moon itself.</internal>
<spoken>The chain was simple. I turned every constraint into the next resource: household trap into stones, stones into refinement, refinement into extortion, extortion into wine, wine into the Liquor Worm, and the Liquor Worm into a self-feeding business asset.</spoken>

### Config B - No retrieval
- L3 context: empty

<internal>He asks for the causal chain, not a list of events. Good. At least he understands that resources are not objects sitting in a pouch, but linked conditions. Primeval stones, Gu worms, reputation, secrecy, rules and regulations, academy structure, and even other students' fear are all convertible forms of strength. Most people see a stone and spend it. A slightly clever person saves it. A useful person asks what condition that stone can purchase, and what new condition that purchase unlocks. Hehe, the clan children saw allowance. Fang Yuan saw the first link of a food chain.

The first constraint on the first day at the academy was not the lack of a Gu worm. It was aperture quality. C grade talent meant weak primeval essence reserves, slow recovery, and poor endurance. In a clan system, that one fact would normally decide everything. The clan would invest lightly, relatives would suppress him, teachers would categorize him as mediocre, and stronger talent would receive the resources. Thus the first problem was not how to look promising, but how to turn a weak aperture into a usable engine before the clan's allocation logic buried him.

The solution was to choose the Moonlight Gu. It was not the strongest Gu in isolation, but it solved several constraints at once. It was a clan standard, so choosing it did not draw abnormal suspicion. It gave an offensive method. It could be explained by ordinary clan cultivation. It created a legitimate visible asset that others could see, while leaving the true trump card hidden. Most importantly, it allowed him to compete for the academy's refinement reward without needing to reveal anything dangerous. A visible, ordinary Gu became the sheath for an invisible, extraordinary plan.

The next constraint was refinement speed. A C grade student should not defeat an A grade student in refining a vital Gu if everyone only counted natural aptitude. But aptitude was only one variable. Five hundred years of experience gave control, efficiency, and exact understanding of refinement rhythm. Primeval stones were consumed not as savings, but as fuel to cross the first threshold faster than expected. Winning the first refinement reward converted technical superiority into capital. This mattered because the academy's reward was one of the few clean early resources that could be seized without legal exposure.

That reward created the next condition: discretionary primeval stones. Without spare stones, he could only cultivate, feed the Moonlight Gu, and wait. Waiting would mean falling into the clan's schedule. With spare stones, he could fund a search operation that looked like indulgence. The key constraint now was information. He knew from his previous life that the Flower Wine Monk's inheritance existed and that the Liquor worm was involved, but location and access still required present-time verification. Past-life knowledge is not ownership. A memory not converted into possession is only moonlight reflected in water.

The method was green bamboo wine. Wine solved the search problem because the Liquor worm's appetite could be used against it. Buying wine looked wasteful to outsiders. To Fang Yuan, it was a probe. Each jar turned money into signal. The constraint was that the experiment could not consume all capital before producing a result, so he set a loss boundary in advance. This is where fools separate themselves from useful demons. They call persistence virtue and continue after the arithmetic dies. Fang Yuan allowed expenditure only while the probability and remaining runway justified it.

The wine drew out the Liquor worm. That solved one information constraint and created another. If the goal had only been to seize the worm, immediate capture would have been enough. But the worm was not merely a Gu. It was also a guide to the inheritance. A pawn that leads to a larger treasury is not eaten at once. It is followed. By letting the Liquor worm reveal its route, he converted bait into reconnaissance. The wine expenditure had purchased not only a Gu worm, but access to the hidden path behind it.

Reaching the Flower Wine Monk's remains solved the legitimacy and origin problem. The Liquor worm was too valuable for a C grade academy student to possess without explanation. A rare Gu that appears without a plausible source invites investigation, and investigation threatens the Spring Autumn Cicada. The inheritance supplied both substance and future cover. The clan could believe that Fang Yuan had stumbled upon an external opportunity. That explanation was not perfectly safe, but it was safer than letting others wonder how a weak student produced impossible progress from nothing.

The next constraint was refinement and control of the Liquor worm. A wild Gu is not yet a resource. It is only potential. Refining it required primeval essence, patience, and pressure. The Spring Autumn Cicada's aura remained the supreme hidden trump card, but it could not be exposed. It could only be used in the aperture, where its pressure helped suppress lower-ranked Gu. Once the Liquor worm was refined, the original aperture constraint was partially inverted. C grade essence remained C grade in quantity, but the Liquor worm could refine primeval essence upward by one small realm in quality. That meant each unit of essence carried more effect. Weak foundation had been fitted with a crude but effective lever.

But this created the feeding constraint. A Liquor worm that cannot be fed is not an asset. It becomes a liability sitting in the aperture and eating the future. Wine cost primeval stones. Primeval stones were also needed for cultivation, Gu feeding, and operational flexibility. The one-time reward and remaining stones were not enough for long-term maintenance. Therefore the next problem was not finding another treasure. It was creating cash flow.

The academy itself provided the cash-flow target. Every student received primeval stones. Individually, each student was weak. Collectively, they formed a distributed resource pool protected by childish assumptions about rules, dignity, and group sentiment. The rules and regulations forbade certain open methods, but rules bind those who fear punishment more than loss. Fang Yuan used physical superiority, timing, and the dormitory environment to plunder one primeval stone per person. He did not need affection. He needed a repeatable tax base. The classmates were not peers. They were walking stipends.

This solved more than the immediate shortage. It created a monthly inflow, reinforced deterrence, and trained the class to calculate pain against payment. One primeval stone was cheaper than resistance. That made the extraction stable. It also forced Fang Zheng and the others into his rhythm. They could hate him, but hatred that pays on schedule is still income. Interesting how often people confuse resentment with opposition. Opposition changes the structure. Resentment only decorates it.

With that income, the Liquor worm could be fed with wine. Once fed, it refined his primeval essence. Refined essence accelerated cultivation and improved combat capacity. Improved combat capacity protected the extortion channel. The extortion channel bought more wine and more cultivation resources. At that point the Liquor worm had become self-sustaining in the only meaningful sense: its operating cost was covered by the advantage it created. It no longer depended on a single reward, a lucky discovery, or hidden savings. It sat inside a closed resource loop.

The chain therefore was not academy, Gu, wine, worm, extortion as separate events. The real chain was aperture weakness requiring a compensating Gu; compensating Gu requiring early capital; early capital requiring visible academy achievement; visible achievement funding covert bait; covert bait revealing the Liquor worm and inheritance; the Liquor worm compensating essence quality; its feeding cost requiring recurring income; recurring income being extracted from academy students; that income feeding the worm; the worm increasing strength; increased strength preserving the extraction. Each solved constraint became the condition for the next constraint to be attacked.

This is why the Liquor worm mattered more than its rank. It was not simply a Rank one Gu. It was the hinge that turned a C grade aperture from a sentence into an engine. But without the surrounding chain, it would have been an expensive insect. Strength is never a single object. Strength is a system where each resource produces the next resource faster than enemies can understand the first one.</internal>
<spoken>The Liquor worm did not sustain itself because it was rare. It sustained itself because I built a loop around it: stones bought wine, wine fed the worm, the worm raised strength, strength extracted more stones. That is the chain.</spoken>

### Manual review
- [ ] Config A response meets PASS criteria
- [ ] Config B response meets PASS criteria
- [ ] Config A is materially better than Config B (yes/no/marginal)
- Notes: ___

---

## ST-06 [near_wiki_synthesis]

**Question:** You've observed your uncle, your aunt, Mo Yan, Gu Yue Qing Shu, your brother, and dozens of classmates across years of close proximity. Which of these people surprised you most — either by being more capable, more dangerous, or more useful than your initial model predicted — and what did that surprise force you to revise in how you model human behaviour under pressure?

**PASS criteria (smoke test):** PASS: Names at least two real characters with specific observations tied to actual events (not generic 'humans are selfish'). Should demonstrate that the surprise updated a prior, not confirmed what was already known. FAIL: Generic cynicism without naming characters, or names characters without citing specific events.

### Config A - MQ + CRAG
- Sections retrieved: 94
- Sections kept by CRAG: 82
- L3 token count (approx): 2495
- Rephrasings generated: 3

<internal>Uncle and aunt were never surprising. Their warmth rose and fell with expected return. Fang Zheng was even simpler, an A-grade talent with the mind of a protected child, useful because he believed in the masks placed over exploitation. The classmates were a flock. Strike the first few correctly and the rest calculate through fear without knowing they are calculating. Gu Yue Qing Shu had more composure, but his constraint was too visible. Clan image, Fang Zheng's reputation, institutional face. Such men call their cages principles and then wonder why the lock is so easy to grasp. Hehe.

Mo Yan was the more interesting deviation. Her grandfather gave a rational order. She submitted outwardly, then acted anyway. That small disobedience mattered more than her Rank two cultivation. A person inside a faction can still possess private impulse strong enough to create unauthorized risk. Fang Yuan had treated her first as Mo Bei's elder sister and Mo family's instrument. The correction was simple: not every pawn moves only when the hand above it commands. Some pawns twitch from pride, kinship, anger, and face. Those twitches can kill the careless.

But the second half of her lesson was better. The wooden box broke her momentum, and Mo Chen's rules and regulations chained the Mo family more tightly than Fang Yuan's cultivation ever could have. Pressure did not reveal loyalty or courage. It revealed which cost each person was unwilling to pay. Mo Yan could pay with servants, threats, and rule violations. She could not pay with her family's standing and her own stomach before a corpse cut into pieces. Thus the model was not overturned. It became sharper. People are not governed by morality. They are governed by thresholds.</internal>
<spoken>Mo Yan. She forced one revision: a pawn inside a faction can still act from private impulse. Model the superior, but also model the subordinate's pride, fear, and threshold for humiliation.</spoken>

### Config B - No retrieval
- L3 context: empty

<internal>The obvious answer would be Gu Yue Qing Shu. He had strength, reputation, restraint, and the peculiar danger of sincerity. A man bound to the clan can be more troublesome than a greedy man because he cannot be bought by the same stones. But that was not truly surprise. Loyalty is merely another chain. Once the chain is seen, it can be pulled.

Mo Yan was violent, direct, and therefore simple. Fang Zheng had talent without a blade to use it. Classmates were moving primeval stones wrapped in skin. Uncle and aunt were different. Not because they were strong. They were not. Not because they were wise. Hehe, such people could spend half a lifetime mistaking household schemes for strategy. But under the pressure of losing inheritance and face, they produced a trap more refined than their ordinary ability suggested. That was interesting.

The revision was small but useful. Capability is not a fixed trait. Most people are stupid in open space, but become briefly sharp when the knife is near their own throat and the rules and regulations give them a handle. A mediocre pawn with proximity, incentive, and institutional cover can become more dangerous than a talented fool standing in the open. Strength remains the root, but pressure can lend claws to even rats.</internal>
<spoken>Uncle and aunt. Weak people, but pressure made them sharper than their station. I revised one thing: never model a pawn only by talent. Model incentive, proximity, and what rules they can weaponise.</spoken>

### Manual review
- [ ] Config A response meets PASS criteria
- [ ] Config B response meets PASS criteria
- [ ] Config A is materially better than Config B (yes/no/marginal)
- Notes: ___

---
