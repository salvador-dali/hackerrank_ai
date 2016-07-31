"""
https://www.hackerrank.com/challenges/punctuation-corrector-its
Detect whether it is correct to write "its" or "it's"

- create two lists (for each case). Each list will consist of sentences with one of two candidates.
  Note that "it's" is the same as "it is" and "it has"
- having these list, get information about a previous an next word after the "it's" or "its"
- here it would be nice to have part of speech to tell whether the word is a verb, etc. I use
  a stupid way of checking for verbs
- normalize these frequencies
- now for each query, get the previous, next word and based on them - get the probability of "its" / "it's"
"""

import string
from collections import Counter, defaultdict

verbs = {"accept", "add", "admire", "admit", "advise", "afford", "agree", "alert", "allow", "amuse", "analyse", "analyze", "announce", "annoy", "answer", "apologise", "appear", "applaud", "appreciate", "approve", "argue", "arrange", "arrest", "arrive", "ask", "attach", "attack", "attempt", "attend", "attract", "avoid", "back", "bake", "balance", "ban", "bang", "bare", "bat", "bathe", "battle", "beam", "beg", "behave", "belong", "bleach", "bless", "blind", "blink", "blot", "blush", "boast", "boil", "bolt", "bomb", "book", "bore", "borrow", "bounce", "bow", "box", "brake", "branch", "breathe", "bruise", "brush", "bubble", "bump", "burn", "bury", "buzz", "calculate", "call", "camp", "care", "carry", "carve", "cause", "challenge", "change", "charge", "chase", "cheat", "check", "cheer", "chew", "choke", "chop", "claim", "clap", "clean", "clear", "clip", "close", "coach", "coil", "collect", "colour", "comb", "command", "communicate", "compare", "compete", "complain", "complete", "concentrate", "concern", "confess", "confuse", "connect", "consider", "consist", "contain", "continue", "copy", "correct", "cough", "count", "cover", "crack", "crash", "crawl", "cross", "crush", "cry", "cure", "curl", "curve", "cycle", "dam", "damage", "dance", "dare", "decay", "deceive", "decide", "decorate", "delay", "delight", "deliver", "depend", "describe", "desert", "deserve", "destroy", "detect", "develop", "disagree", "disappear", "disapprove", "disarm", "discover", "dislike", "divide", "double", "doubt", "drag", "drain", "dream", "dress", "drip", "drop", "drown", "drum", "dry", "dust", "earn", "educate", "embarrass", "employ", "empty", "encourage", "end", "enjoy", "enter", "entertain", "escape", "examine", "excite", "excuse", "exercise", "exist", "expand", "expect", "explain", "explode", "extend", "face", "fade", "fail", "fancy", "fasten", "fax", "fear", "fence", "fetch", "file", "fill", "film", "fire", "fit", "fix", "flap", "flash", "float", "flood", "flow", "flower", "fold", "follow", "fool", "force", "form", "found", "frame", "frighten", "fry", "gather", "gaze", "glow", "glue", "grab", "grate", "grease", "greet", "grin", "grip", "groan", "guarantee", "guard", "guess", "guide", "hammer", "hand", "handle", "hang", "happen", "harass", "harm", "hate", "haunt", "head", "heal", "heap", "heat", "help", "hook", "hop", "hope", "hover", "hug", "hum", "hunt", "hurry", "identify", "ignore", "imagine", "impress", "improve", "include", "increase", "influence", "inform", "inject", "injure", "instruct", "intend", "interest", "interfere", "interrupt", "introduce", "invent", "invite", "irritate", "itch", "jail", "jam", "jog", "join", "joke", "judge", "juggle", "jump", "kick", "kill", "kiss", "kneel", "knit", "knock", "knot", "label", "land", "last", "laugh", "launch", "learn", "level", "license", "lick", "lie", "lighten", "like", "list", "listen", "live", "load", "lock", "long", "look", "love", "man", "manage", "march", "mark", "marry", "match", "mate", "matter", "measure", "meddle", "melt", "memorise", "mend", "mess", "up", "milk", "mine", "miss", "mix", "moan", "moor", "mourn", "move", "muddle", "mug", "multiply", "murder", "nail", "name", "need", "nest", "nod", "note", "notice", "number", "obey", "object", "observe", "obtain", "occur", "offend", "offer", "open", "order", "overflow", "owe", "own", "pack", "paddle", "paint", "park", "part", "pass", "paste", "pat", "pause", "peck", "pedal", "peel", "peep", "perform", "permit", "phone", "pick", "pinch", "pine", "place", "plan", "plant", "play", "please", "plug", "point", "poke", "polish", "pop", "possess", "post", "pour", "practise", "practice", "pray", "preach", "precede", "prefer", "prepare", "present", "preserve", "press", "pretend", "prevent", "prick", "print", "produce", "program", "promise", "protect", "provide", "pull", "pump", "punch", "puncture", "punish", "push", "question", "queue", "race", "radiate", "rain", "raise", "reach", "realise", "receive", "recognise", "record", "reduce", "reflect", "refuse", "regret", "reign", "reject", "rejoice", "relax", "release", "rely", "remain", "remember", "remind", "remove", "repair", "repeat", "replace", "reply", "report", "reproduce", "request", "rescue", "retire", "return", "rhyme", "rinse", "risk", "rob", "rock", "roll", "rot", "rub", "ruin", "rule", "rush", "sack", "sail", "satisfy", "save", "saw", "scare", "scatter", "scold", "scorch", "scrape", "scratch", "scream", "screw", "scribble", "scrub", "seal", "search", "separate", "serve", "settle", "shade", "share", "shave", "shelter", "shiver", "shock", "shop", "shrug", "sigh", "sign", "signal", "sin", "sip", "ski", "skip", "slap", "slip", "slow", "smash", "smell", "smile", "smoke", "snatch", "sneeze", "sniff", "snore", "snow", "soak", "soothe", "sound", "spare", "spark", "sparkle", "spell", "spill", "spoil", "spot", "spray", "sprout", "squash", "squeak", "squeal", "squeeze", "stain", "stamp", "stare", "start", "stay", "steer", "step", "stir", "stitch", "stop", "store", "strap", "strengthen", "stretch", "strip", "stroke", "stuff", "subtract", "succeed", "suck", "suffer", "suggest", "suit", "supply", "support", "suppose", "surprise", "surround", "suspect", "suspend", "switch", "talk", "tame", "tap", "taste", "tease", "telephone", "tempt", "terrify", "test", "thank", "thaw", "tick", "tickle", "tie", "time", "tip", "tire", "touch", "tour", "tow", "trace", "trade", "train", "transport", "trap", "travel", "treat", "tremble", "trick", "trip", "trot", "trouble", "trust", "try", "tug", "tumble", "turn", "twist", "type", "undress", "unfasten", "unite", "unlock", "unpack", "untidy", "use", "vanish", "visit", "wail", "wait", "walk", "wander", "want", "warm", "warn", "wash", "waste", "watch", "water", "wave", "weigh", "welcome", "whine", "whip", "whirl", "whisper", "whistle", "wink", "wipe", "wish", "wobble", "wonder", "work", "worry", "wrap", "wreck", "wrestle", "wriggle", "x-ray", "yawn", "yell", "zip", "zoom", "awake", "awoke", "awoken", "be", "was,", "were", "been", "beat", "beat", "beaten", "become", "became", "become", "begin", "began", "begun", "bend", "bent", "bent", "bet", "bet", "bet", "bid", "bid", "bid", "bite", "bit", "bitten", "blow", "blew", "blown", "break", "broke", "broken", "bring", "brought", "brought", "broadcast", "broadcast", "broadcast", "build", "built", "built", "burn", "burned", "burnt", "burned", "burnt", "buy", "bought", "bought", "catch", "caught", "caught", "choose", "chose", "chosen", "come", "came", "come", "cost", "cost", "cost", "cut", "cut", "cut", "dig", "dug", "dug", "do", "did", "done", "draw", "drew", "drawn", "dream", "dreamed", "dreamt", "dreamed", "dreamt", "drive", "drove", "driven", "drink", "drank", "drunk", "eat", "ate", "eaten", "fall", "fell", "fallen", "feel", "felt", "felt", "fight", "fought", "fought", "find", "found", "found", "fly", "flew", "flown", "forget", "forgot", "forgotten", "forgive", "forgave", "forgiven", "freeze", "froze", "frozen", "get", "got", "gotten", "give", "gave", "given", "go", "went", "gone", "grow", "grew", "grown", "hang", "hung", "hung", "have", "had", "had", "hear", "heard", "heard", "hide", "hid", "hidden", "hit", "hit", "hit", "hold", "held", "held", "hurt", "hurt", "hurt", "keep", "kept", "kept", "know", "knew", "known", "lay", "laid", "laid", "lead", "led", "led", "learn", "learned", "learnt", "learned", "learnt", "leave", "left", "left", "lend", "lent", "lent", "let", "let", "let", "lie", "lay", "lain", "lose", "lost", "lost", "make", "made", "made", "mean", "meant", "meant", "meet", "met", "met", "pay", "paid", "paid", "put", "put", "put", "read", "read", "read", "ride", "rode", "ridden", "ring", "rang", "rung", "rise", "rose", "risen", "run", "ran", "run", "say", "said", "said", "see", "saw", "seen", "sell", "sold", "sold", "send", "sent", "sent", "show", "showed", "showed", "shown", "shut", "shut", "shut", "sing", "sang", "sung", "sit", "sat", "sat", "sleep", "slept", "slept", "speak", "spoke", "spoken", "spend", "spent", "spent", "stand", "stood", "stood", "swim", "swam", "swum", "take", "took", "taken", "teach", "taught", "taught", "tear", "tore", "torn", "tell", "told", "told", "think", "thought", "thought", "throw", "threw", "thrown", "understand", "understood", "understood", "wake", "woke", "woken", "wear", "wore", "worn", "win", "won", "won", "write", "wrote", "written"}

def checkVerb(word):
    if not word:
        return word

    if word in verbs or word[-3:] == 'ing':
        return 'verb'

    return word

def generateLists():
    arr = ' '.join([i.strip().lower() for i in open("corpus.txt", "r") if i.strip()]).translate(string.maketrans("!?;-", '... ')).translate(None, '"_,*)(:1234567890')
    arr = arr.replace(" its ", ' XXX ').replace(" it is ", ' YYY ').replace(" it has ", ' YYY ').replace(" it's ", ' YYY ').replace("'", " ").split('.')
    its_list, it_s_list = [], []
    for i in arr:
        i = i.split()
        if "XXX" in i:
            its_list.append(i)

        if "YYY" in i:
            it_s_list.append(i)

    return its_list, it_s_list

def stats(el_list, el):
    word_prev, word_next = [], []
    for i in el_list:
        a = i.index(el)
        word_prev.append(checkVerb(None if a == 0 else i[a - 1]))
        word_next.append(checkVerb(None if a == len(i) else i[a + 1]))

    prev, next = Counter(word_prev), Counter(word_next)
    prev_sum = float(sum(v for k, v in prev.iteritems()))
    next_sum = float(sum(v for k, v in next.iteritems()))
    prev_dict = {k: v / prev_sum for k, v in prev.iteritems()}
    next_dict = {k: v / next_sum for k, v in next.iteritems()}
    return defaultdict(float, prev_dict), defaultdict(float, next_dict)

def extractWords(s):
    s = s.lower().replace('???', 'XXXX').translate(None, '".!;?:_,*)(:1234567890').split()
    a = s.index('XXXX')

    word_prev = None if a == 0 else s[a - 1]
    word_next = None if a == len(s) else s[a + 1]

    return checkVerb(word_prev), checkVerb(word_next)

def analyse(prev, next):
    # XXX   - its
    # YYY   - it's
    XXX = XXX_prev[prev] + XXX_next[next]
    YYY = YYY_prev[prev] + YYY_next[next]
    if XXX >= YYY:
        return 'its'

    return "it's"

XXX_list, YYY_list = generateLists()
XXX_prev, XXX_next = stats(XXX_list, 'XXX')
YYY_prev, YYY_next = stats(YYY_list, 'YYY')

for i in xrange(input()):
    s = raw_input()
    if '???' in s:
        prev, next = extractWords(s)
        correct = analyse(prev, next)
        print s.replace('???', correct)
    else:
        print s