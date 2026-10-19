"""Hand-written demo content (own words). Run: python3 content_src.py -> content/*.json"""
import json, os
def S(title, visual, beats, example, sayback, quiz, tieback=None):
    d = dict(title=title, visual=visual, beats=beats, example=example, sayback=sayback, quiz=[dict(q=q, a=a) for q, a in quiz])
    if tieback: d["tieback"] = tieback
    return d
L = {}
def lesson(id, track, title, subtitle, sections, source=None): L[id] = dict(id=id, track=track, title=title, subtitle=subtitle, source=source, sections=sections)

# ---------------- PAPERS ----------------
lesson("dkh", "papers", "Deep Kernel Hedging", "arXiv 2609.34474 · options hedging with a learned similarity score", [
 S("The big idea", "kernel", [
   "Goal: protect a position in an option by trading the stock underneath it. That protection is called hedging.",
   "The paper learns a hedging rule from example price paths instead of a textbook formula.",
   "Key tool: a kernel (a score for how similar two situations are). Similar market moments should get similar hedges.",
   "Twist: a tiny neural net first squeezes the market data into a better summary. Then a bell-curve kernel compares those summaries. Together that's a deep kernel.",
   "Result: it hedges better than plain kernels and than deep hedging, mostly when data is scarce."],
   "A weather app that says 'today looks like these 5 past days, so bring an umbrella' is using similarity the same way.",
   "Explain to a friend why 'similar situations get similar hedges' is a useful rule.",
   [("What does a kernel measure?", "How similar two inputs are."), ("What does the neural net add?", "It learns a better summary of the market before the similarity is scored.")],
   "Liquid Bot tie-in: theme weights are a crude 'similar setups behave alike' rule. A kernel is the math version."),
 S("The setup: hedging error", "flow", [
   "You owe an option payoff Y at the end. You start with some cash and trade the stock on fixed dates.",
   "At each date the rule looks only at what you can see now (price, volatility) and says how many shares to hold.",
   "Self-financing means no money comes in or out. Profit only comes from what you already hold.",
   "Hedging error = what you owe, minus what your cash grew to, minus your trading gains. Zero means perfect cover.",
   "Training goal: make the average error small, plus a penalty that keeps the rule smooth."],
   "Like budgeting for a bill due in a month: each week you adjust savings so you land right on the amount.",
   "Say in one sentence what the hedging error measures.",
   [("What does a hedging error of zero mean?", "Your trades exactly covered the payoff you owe."), ("Why add a smoothness penalty?", "So the rule doesn't memorize noise in the training paths.")]),
 S("The shortcut: one weight per path", "gram", [
   "Searching over every possible rule is impossible. There are infinitely many.",
   "A theorem (the representer theorem) proves the best rule is a weighted mix of one building block per training path.",
   "So you only solve for N numbers, one weight per path.",
   "The weights come from a table Q: entry (i, j) scores how alike path i's trading is to path j's.",
   "With squared error there's a one-line formula for the weights."],
   "Instead of writing a new recipe from scratch, you blend your 50 tested recipes in the right amounts.",
   "Why does turning 'infinite choices' into 'N weights' matter?",
   [("What is one entry of Q?", "How similar two training paths' trading patterns are.")]),
 S("Making it fast: random waves", "waves", [
   "Problem: Q has N×N entries. With many paths it gets huge and slow.",
   "Fix: random Fourier features. Approximate the bell-curve kernel with D random cosine waves (D = 100 here).",
   "Each path becomes a list of 100 numbers. Now you solve for 100 weights, no matter how many paths you have.",
   "The waves are drawn once and frozen. More waves = closer to the exact answer.",
   "Training uses mini-batches and the Adam optimizer, like any neural net."],
   "Describing a song by the strength of 100 notes instead of comparing it to every other song.",
   "Explain why cost stops exploding as you add more paths.",
   [("What is D in this paper?", "100 random features."), ("Weights solved for after the swap?", "D (100), not N.")],
   "Liquid Bot tie-in: same trick lets a similarity model stay fast as your trade log grows."),
], source="https://arxiv.org/abs/2609.34474")

# ---------------- FOUNDATIONS ----------------
lesson("f-ev-variance", "foundations", "Expected value & variance", "The two numbers behind every trading decision", [
 S("Expected value", "bars", [
   "Expected value (EV) is the long-run average result if you repeat a bet many times.",
   "Recipe: multiply each outcome by its chance, then add them up.",
   "Positive EV means you win over time, even if you lose often.",
   "Worked: 40% chance to win $30, 60% chance to lose $10. EV = 0.4×30 − 0.6×10 = $6 per bet."],
   "A carnival game that costs $2 and pays $10 one time in 10 has EV = $1 − $2 = −$1. The house wins.",
   "Tell someone why a strategy that loses 60% of the time can still make money.",
   [("Win $20 at 50%, lose $15 at 50%. EV?", "0.5×20 − 0.5×15 = $2.50"), ("EV = 0 means?", "Break even over the long run.")],
   "Liquid Bot: 'expectancy' on your scorecard is exactly EV per trade."),
 S("Variance & standard deviation", "dice", [
   "Variance measures how spread out results are around the average.",
   "Recipe: for each result, take (result − average) squared. Average those.",
   "Standard deviation is the square root of variance. It's back in dollars, so it's easier to read.",
   "Worked: results 2, 4, 6. Average 4. Squared gaps 4, 0, 4. Variance = 8/3 ≈ 2.67. SD ≈ 1.63."],
   "Two drivers both average 30 min to work. One is always 29–31, one swings 10–50. Same EV, very different variance.",
   "Why can two strategies with the same EV feel totally different?",
   [("Results 1, 1, 7: average and variance?", "Average 3; gaps² 4, 4, 16; variance 8.")],
   "Liquid Bot: high variance = deeper drawdowns. That's why you start with small size."),
])

# ---------------- LIQUID BOT LAB ----------------
lesson("lb-expectancy", "liquidbot", "Expectancy, R and position size", "Read a trading scorecard like a quant", [
 S("R-multiples", "stop", [
   "R is the amount you risk on a trade: entry to stop.",
   "Measure every result in R. Made 2× what you risked = +2R. Got stopped = −1R.",
   "Using R lets you compare a $5 trade to a $50 trade fairly."],
   "Risk $10 (stop $1 away, 10 units). Close $2.50 in profit per unit = +$25 = +2.5R.",
   "Explain why measuring in R beats measuring in dollars.",
   [("Risk $8, make $20. R?", "+2.5R")],
   "A sensible go-live gate: positive average R over a decent sample of real trades."),
 S("Expectancy & profit factor", "bars", [
   "Expectancy = win rate × average win − loss rate × average loss. That's EV per trade.",
   "Profit factor = total won ÷ total lost. Above 1 means you're net up.",
   "Worked: 45% wins averaging +2R, 55% losses at −1R. Expectancy = 0.9 − 0.55 = +0.35R per trade."],
   "20 trades at +0.35R with $5 risk ≈ +$35 expected.",
   "Say back: why can a 45% win rate be good?",
   [("Wins total $300, losses total $200. Profit factor?", "1.5")]),
 S("Position size from the stop", "flow", [
   "Pick dollars at risk first. Then size = dollars at risk ÷ distance to stop.",
   "A wider stop means a smaller position, so the dollar risk stays the same.",
   "ATR stops: ATR (average true range, typical daily move) sets how far the stop sits. A good risk check rejects stops tighter than some multiple of ATR."],
   "Risk $2, ATR $0.40, mult 1.5 → stop $0.60 away → size ≈ 3.3 units.",
   "Explain why the stop decides size, not the other way round.",
   [("Risk $3, stop $0.50 away. Units?", "6")]),
])
lesson("lb-overfitting", "liquidbot", "Overfitting checks: holdout & walk-forward", "Who checks what, in plain words", [
 S("What overfitting is", "holdout", [
   "Overfitting = a model memorizes the past instead of learning a real pattern.",
   "It looks great on old data and falls apart on new data.",
   "The cure: always judge it on data it never saw while tuning."],
   "Memorizing last year's test answers vs actually learning the subject.",
   "Say why a perfect backtest is a warning sign.",
   [("Main symptom of overfitting?", "Great on training data, bad on new data.")]),
 S("Holdout & walk-forward", "holdout", [
   "Holdout: hide the last chunk of data (say 30%). Tune on the rest. Test once on the hidden part.",
   "Walk-forward: tune on months 1–3, test on 4. Slide: tune 2–4, test 5. Repeat.",
   "Walk-forward fits trading because markets change over time."],
   "A paper-trading phase is a forward test: trades settled on real prices the bot never tuned on.",
   "Explain walk-forward with a calendar.",
   [("Why test only once on the holdout?", "Each extra peek leaks it into tuning, so it stops being unseen.")],
   "Idea only: a script could replay closed trades and report scorecard per walk-forward window."),
 S("The calibration haircut", "sigmoid", [
   "Calibration = when the model says 70%, does it win about 70%?",
   "A haircut = stated confidence − real hit rate, kept inside safe bounds (e.g., 0 to 0.3).",
   "Overconfident models get marked down automatically.",
   "Small samples are noisy. 10 trades can't prove much, so the bounds and 1-step limits matter."],
   "Says 80%, wins 60% → haircut 0.2 → future 80% calls treated as 60%.",
   "Why clamp the haircut instead of letting it go anywhere?",
   [("Says 65%, wins 55%. Haircut?", "0.10")]),
])

# ---------------- SCHOOL ----------------
lesson("bis102-l13", "school", "BIS 102 · Lesson 13: ANNs in Action", "AI for Business · how a network spots a dog breed", [
 S("Feeding data in", "network", [
   "A photo is a grid of pixels. A 25×25 gray photo has 625 of them.",
   "Each pixel becomes one input node, holding a brightness from 0 (black) to 1 (white).",
   "Sigmoid neurons can output anything between 0 and 1, not just yes/no.",
   "Output: one node per breed. A value near 1 means 'very likely this breed'."],
   "625 inputs → two hidden layers of 20 → 10 breed outputs.",
   "Explain how a picture turns into numbers.",
   [("Pixels in a 25×25 image?", "625")]),
 S("Hidden layers & weights", "network", [
   "Every node links to every node in the next layer. 625×20 = 12,500 links in the first jump alone.",
   "A weight is how strong one link is. Training turns weights up or down.",
   "Early layers catch simple bits like edges and spots. Later layers combine them into ears, fur, shape.",
   "Total here: 12,500 + 400 + 200 = 13,100 tiny dials."],
   "Like focusing on a dalmatian's spots and ignoring the background.",
   "Why are there far more connections than neurons?",
   [("Links from 20 nodes to 10 nodes?", "200")],
   "Quant link: a weight is just a coefficient, same idea as a regression slope."),
 S("Activation functions & bias", "sigmoid", [
   "Each node: add up weighted inputs, add a bias, run an activation function.",
   "Step function: on or off. Too jumpy to learn from.",
   "Sigmoid: smooth S-curve squeezed between 0 and 1.",
   "ReLU: negative → 0, positive → passes through.",
   "Bias slides the curve left or right. Weights change how steep it is."],
   "Bias is like a thermostat offset: same heater, different trigger point.",
   "Explain the difference between a weight and a bias.",
   [("ReLU of −3? Of 2?", "0 and 2"), ("Which shifts the S-curve sideways?", "Bias")],
   "Quant link: sigmoid output ≈ a probability, the same thing Liquid Bot calibrates."),
], source="Lesson notes, own words")

# ---------------- DAYS 1-7 (study plan) ----------------
def day(n, title, sections): lesson(f"day-{n:03d}", "today", title, f"Study plan · Day {n}", sections)
day(1, "Vectors: what are they?", [
 S("An arrow and a list", "vectors", [
   "A vector is an arrow with a length and a direction.",
   "It's also just a list of numbers. [3, 2] means 3 right, 2 up.",
   "Physics sees arrows, computer science sees lists, math says both are the same thing."],
   "Your portfolio is a vector: [BTC units, ETH units, SOL units].", "Explain a vector two ways.",
   [("What does [−1, 4] mean as an arrow?", "1 left, 4 up.")]),
 S("Adding & scaling", "vectors", [
   "Add vectors tip to tail: [1,2] + [3,1] = [4,3].",
   "Scaling multiplies every number: 2×[1,2] = [2,4]. Same direction, twice as long.",
   "A negative scale flips the direction."],
   "Two trades' position changes add up into your net position change.", "Show adding two arrows on paper.",
   [("3×[2,−1]?", "[6, −3]"), ("[1,1]+[2,−3]?", "[3, −2]")],
   "Liquid Bot: exposure across assets is a vector. A cap on open positions is a limit on it."),
])
day(2, "Combos, span and basis", [
 S("Linear combinations", "span", [
   "A linear combination means scale some vectors, then add them.",
   "With î = [1,0] and ĵ = [0,1], any point is a·î + b·ĵ.",
   "The span is every point you can reach that way."],
   "Two ingredients in different amounts make a whole range of drinks.", "Define span in your own words.",
   [("Span of [1,0] and [0,1]?", "The whole flat plane.")]),
 S("Basis", "span", [
   "A basis is a minimum set of vectors whose span covers the space.",
   "If one vector is just a stretch of another, it adds nothing new. That's linear dependence.",
   "Two independent arrows span a plane. Three can span 3D space."],
   "BTC and 'BTC ×2 leverage' are dependent. They point the same way.", "Why does a dependent vector add nothing?",
   [("Are [1,2] and [2,4] independent?", "No. One is 2× the other.")],
   "Quant link: highly correlated assets ≈ dependent vectors, so they give little diversification."),
])
day(3, "Matrices as transformations", [
 S("A matrix moves space", "transform", [
   "A linear transformation stretches, rotates or shears space. Grid lines stay straight and evenly spaced.",
   "You only need to know where î and ĵ land.",
   "Write those landing spots as columns. That grid of numbers is the matrix."],
   "Photo-editing 'rotate' and 'skew' are matrices.", "Why do just two landing spots describe the whole move?",
   [("Matrix [[0,−1],[1,0]] does what?", "Rotates 90° counter-clockwise.")]),
 S("Matrix × vector", "transform", [
   "To move [x, y]: take x of column 1 plus y of column 2.",
   "Worked: [[2,0],[0,3]] · [1,1] = 1·[2,0] + 1·[0,3] = [2,3]."],
   "Scaling width ×2 and height ×3.", "Do one by hand and explain each step.",
   [("[[1,1],[0,1]] · [2,3]?", "2·[1,0] + 3·[1,1] = [5,3]")],
   "Neural nets: each layer is a matrix times a vector, then an activation."),
])
day(4, "Matrix multiplication = doing two moves", [
 S("Composition", "compose", [
   "Multiplying two matrices = doing one move, then the other.",
   "Read right to left: in AB, B happens first.",
   "Order matters. Rotate-then-shear ≠ shear-then-rotate."],
   "Putting on socks then shoes is not the same as shoes then socks.", "Explain why AB ≠ BA in general.",
   [("In ABv, which acts on v first?", "B")]),
 S("Computing it", "compose", [
   "Column 1 of AB = A times column 1 of B. Same for column 2.",
   "Worked: A=[[0,−1],[1,0]] (rotate), B=[[2,0],[0,1]] (stretch x). AB's columns: A·[2,0]=[0,2], A·[0,1]=[−1,0]."],
   "A 2-layer network without activations collapses into one matrix. That's why activations matter.", "Say back the column rule.",
   [("Why do deep nets need nonlinear activations?", "Without them, stacked layers multiply into one single matrix.")]),
])
day(5, "Probability basics: counting outcomes", [
 S("Sample space & naive probability", "dice", [
   "Sample space = every possible outcome.",
   "Event = the outcomes you care about.",
   "Naive probability = favorable ÷ total. It only works when every outcome is equally likely.",
   "Worked: one die, P(even) = 3/6 = 1/2."],
   "Not every outcome is equally likely: 'will BTC go up tomorrow' isn't 50/50 just because there are two outcomes.",
   "When does favorable ÷ total fail?", [("Two coins: P(both heads)?", "1/4")]),
 S("Counting", "dice", [
   "Multiplication rule: 3 shirts × 4 pants = 12 outfits.",
   "Order matters (arrangements): n × (n−1) × …",
   "Order doesn't matter (groups): 'n choose k'.",
   "Worked: pick 2 of 5 assets to watch: 5×4/2 = 10 pairs."],
   "Number of asset pairs to check for correlation grows fast: 20 assets → 190 pairs.", "Explain why we divide by 2 for pairs.",
   [("Choose 3 from 6?", "20")],
   "Liquid Bot: more setups tested = more chance one looks great by luck. That's overfitting again."),
])
day(6, "Probability rules & the birthday problem", [
 S("The rules", "dice", [
   "Probabilities run from 0 to 1. Something certain is 1.",
   "P(not A) = 1 − P(A). Often the easy way in.",
   "Inclusion-exclusion: P(A or B) = P(A) + P(B) − P(A and B), so overlap isn't counted twice."],
   "P(draw heart or king) = 13/52 + 4/52 − 1/52 = 16/52.", "Why subtract the overlap?",
   [("P(A)=0.5, P(B)=0.4, P(both)=0.2. P(A or B)?", "0.7")]),
 S("The birthday problem", "birthday", [
   "How many people before two likely share a birthday? Only 23 for a 50% chance.",
   "Trick: find P(nobody shares), then subtract from 1.",
   "It's small because there are so many pairs: 23 people make 253 pairs."],
   "Test 50 random strategies and a couple will 'match' the market by pure luck.", "Explain why 23 is enough.",
   [("Pairs among 23 people?", "253")],
   "Liquid Bot: coincidences are common. Need a real sample of trades before trusting a pattern."),
])
day(7, "Sunday review + one Liquid Bot idea", [
 S("Review the week", "review", [
   "Vectors = arrows = lists. Add tip to tail, scale to stretch.",
   "Span and basis: what a set of vectors can reach.",
   "Matrices move space. Multiplying = doing moves in order.",
   "Probability: count outcomes, use the complement, don't double count."],
   "Redo two counting problems by hand without notes.", "Teach the whole week in 60 seconds.",
   [("What does a matrix's first column tell you?", "Where î lands."), ("Fastest route to P(at least one)?", "1 − P(none)")]),
 S("Build one idea", "flow", [
   "Pick one idea: your open positions as a vector, or counting how many setups you tested.",
   "Write it in the tracker's 'Liquid Bot idea?' column.",
   "Ideas only for now. No code changes yet. Write it down first."],
   "Idea: log how many setups each scan considered, to estimate luck risk.", "Explain your idea in two sentences.",
   [("Why count setups tested?", "More tests = more lucky false winners.")]),
])

os.makedirs("content", exist_ok=True)
for k, v in L.items(): json.dump(v, open(f"content/{k}.json", "w"), indent=1, ensure_ascii=False)
print(len(L), "lessons")
