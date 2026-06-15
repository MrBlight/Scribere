#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Scribere - A hyper-minimalist terminal typing tutor.
License: GNU GPL v3
Author: MrBlight
"""

import curses
import time
import random
import sys
import os
import json
import platform

# --- CONFIGURATION & DATA ---

CONFIG_DIR = os.path.expanduser("~/.scribere")
CONFIG_FILE = os.path.join(CONFIG_DIR, "config.json")
SCORES_FILE = os.path.join(CONFIG_DIR, "scores.json")

# Built-in Random Word List (500 common words) to ensure 'rand' mode works without external files
RANDOM_WORDS = [
    "the", "be", "of", "and", "a", "to", "in", "he", "have", "it", "that", "for", "they", "i", "with", "as", "not", "on", "she", "at", "by", "this", "we", "you", "do", "but", "from", "or", "which", "one", "would", "all", "will", "there", "say", "who", "make", "when", "can", "more", "if", "no", "man", "out", "other", "so", "what", "time", "up", "go", "about", "than", "into", "could", "state", "only", "new", "year", "some", "take", "come", "these", "know", "see", "use", "get", "like", "then", "first", "any", "work", "now", "may", "such", "give", "over", "think", "most", "even", "find", "day", "also", "after", "way", "many", "must", "look", "before", "great", "back", "through", "long", "where", "much", "should", "well", "people", "down", "own", "just", "because", "good", "each", "those", "feel", "seem", "how", "high", "too", "place", "little", "world", "very", "still", "nation", "hand", "old", "life", "tell", "write", "become", "here", "show", "house", "both", "between", "need", "mean", "call", "develop", "under", "last", "right", "move", "thing", "general", "school", "never", "same", "another", "begin", "while", "number", "part", "turn", "real", "leave", "might", "want", "point", "form", "off", "child", "few", "small", "since", "against", "ask", "late", "home", "interest", "large", "person", "end", "open", "public", "follow", "during", "present", "without", "again", "hold", "govern", "around", "possible", "head", "consider", "word", "program", "problem", "however", "lead", "system", "set", "order", "eye", "plan", "run", "keep", "face", "fact", "group", "play", "stand", "increase", "early", "course", "change", "help", "line", "city", "put", "close", "case", "force", "meet", "once", "water", "upon", "war", "build", "hear", "light", "unite", "live", "every", "country", "bring", "center", "let", "side", "try", "provide", "continue", "name", "certain", "power", "pay", "result", "question", "study", "woman", "member", "until", "far", "night", "always", "service", "away", "report", "something", "company", "week", "church", "toward", "start", "social", "room", "figure", "nature", "though", "young", "less", "enough", "almost", "read", "include", "president", "nothing", "yet", "better", "big", "boy", "cost", "business", "value", "second", "why", "clear", "expect", "family", "complete", "act", "sense", "mind", "experience", "art", "next", "near", "direct", "car", "law", "industry", "important", "girl", "god", "several", "matter", "usual", "rather", "per", "often", "kind", "among", "white", "reason", "action", "return", "foot", "care", "simple", "within", "love", "human", "along", "appear", "doctor", "believe", "speak", "active", "student", "month", "drive", "concern", "best", "door", "hope", "example", "inform", "body", "ever", "least", "probable", "understand", "reach", "effect", "different", "idea", "whole", "control", "condition", "field", "pass", "fall", "note", "special", "talk", "particular", "today", "measure", "walk", "teach", "low", "hour", "type", "carry", "rate", "remain", "full", "street", "easy", "although", "record", "sit", "determine", "level", "local", "sure", "receive", "thus", "moment", "spirit", "train", "college", "religion", "perhaps", "music", "grow", "free", "cause", "serve", "age", "book", "board", "recent", "sound", "office", "cut", "step", "class", "true", "history", "position", "above", "strong", "friend", "necessary", "add", "court", "deal", "tax", "support", "party", "whether", "earth", "union", "appear", "leader", "voice", "unit", "product", "black", "magic", "silver", "gold", "bronze", "victory", "success", "failure", "courage", "fear", "joy", "sadness", "anger", "peace", "war", "light", "dark", "sun", "moon", "star", "sky", "cloud", "rain", "snow", "wind", "fire", "water", "earth", "stone", "wood", "metal", "glass", "paper", "ink", "pen", "book", "page", "word", "letter", "sentence", "paragraph", "chapter", "story", "tale", "myth", "legend", "hero", "villain", "king", "queen", "prince", "princess", "knight", "dragon", "castle", "tower", "bridge", "road", "path", "street", "avenue", "lane", "alley", "park", "garden", "forest", "mountain", "hill", "valley", "river", "lake", "ocean", "sea", "beach", "island", "continent", "country", "city", "town", "village", "house", "home", "room", "door", "window", "wall", "floor", "ceiling", "roof", "stairs", "step", "ladder", "chair", "table", "desk", "bed", "sofa", "lamp", "light", "switch", "wire", "battery", "engine", "motor", "wheel", "tire", "car", "truck", "bus", "train", "plane", "ship", "boat", "bike", "cycle", "road", "track", "rail", "station", "airport", "port", "dock", "pier", "wharf", "market", "shop", "store", "mall", "bank", "office", "factory", "farm", "field", "barn", "stable", "zoo", "museum", "library", "school", "college", "university", "hospital", "clinic", "pharmacy", "church", "temple", "mosque", "synagogue", "shrine", "grave", "tomb", "monument", "statue", "fountain", "pool", "well", "spring", "stream", "brook", "creek", "pond", "swamp", "marsh", "desert", "jungle", "plain", "plateau", "cliff", "cave", "hole", "pit", "tunnel", "mine", "quarry", "dam", "dyke", "levee", "embankment", "fence", "gate", "hedge", "bush", "shrub", "tree", "leaf", "branch", "trunk", "root", "flower", "fruit", "seed", "nut", "berry", "grain", "corn", "wheat", "rice", "oat", "barley", "rye", "bean", "pea", "potato", "tomato", "onion", "garlic", "carrot", "cabbage", "lettuce", "spinach", "broccoli", "cauliflower", "cucumber", "pepper", "chili", "ginger", "turmeric", "cinnamon", "nutmeg", "clove", "vanilla", "sugar", "salt", "pepper", "vinegar", "oil", "butter", "cheese", "milk", "cream", "yogurt", "egg", "meat", "beef", "pork", "lamb", "chicken", "duck", "goose", "turkey", "fish", "salmon", "tuna", "cod", "shrimp", "crab", "lobster", "oyster", "clam", "mussel", "squid", "octopus", "jellyfish", "starfish", "seahorse", "whale", "dolphin", "shark", "ray", "eel", "snake", "lizard", "turtle", "frog", "toad", "newt", "salamander", "crocodile", "alligator", "hippo", "rhino", "elephant", "giraffe", "zebra", "lion", "tiger", "leopard", "cheetah", "jaguar", "panther", "bear", "wolf", "fox", "dog", "cat", "mouse", "rat", "rabbit", "hare", "squirrel", "chipmunk", "beaver", "otter", "seal", "walrus", "penguin", "ostrich", "eagle", "hawk", "owl", "raven", "crow", "pigeon", "dove", "sparrow", "robin", "bluebird", "cardinal", "parrot", "canary", "finch", "peacock", "flamingo", "swan", "goose", "duck", "pelican", "stork", "heron", "crane", "ibis", "spoonbill", "hummingbird", "woodpecker", "kingfisher", "bee", "wasp", "hornet", "ant", "termite", "fly", "mosquito", "gnat", "midge", "butterfly", "moth", "dragonfly", "damselfly", "beetle", "ladybug", "grasshopper", "cricket", "cockroach", "termite", "ant", "bee", "wasp", "spider", "scorpion", "centipede", "millipede", "worm", "leech", "snail", "slug", "shell", "coral", "sponge", "jellyfish", "anemone", "starfish", "urchin", "cucumber", "worm", "mollusk", "crustacean", "insect", "arachnid", "myriapod", "vertebrate", "invertebrate", "mammal", "bird", "reptile", "amphibian", "fish", "animal", "plant", "fungus", "bacteria", "virus", "cell", "tissue", "organ", "system", "organism", "species", "genus", "family", "order", "class", "phylum", "kingdom", "domain", "life", "death", "birth", "growth", "decay", "evolution", "adaptation", "mutation", "selection", "survival", "extinction", "fossil", "rock", "mineral", "crystal", "gem", "metal", "alloy", "compound", "mixture", "solution", "suspension", "colloid", "element", "atom", "molecule", "ion", "electron", "proton", "neutron", "nucleus", "shell", "orbital", "bond", "reaction", "equation", "formula", "structure", "property", "state", "phase", "change", "energy", "heat", "work", "power", "force", "motion", "speed", "velocity", "acceleration", "momentum", "impulse", "friction", "gravity", "mass", "weight", "density", "volume", "pressure", "temperature", "entropy", "enthalpy", "kinetic", "potential", "thermal", "chemical", "electrical", "magnetic", "nuclear", "radiation", "wave", "particle", "light", "sound", "color", "spectrum", "frequency", "wavelength", "amplitude", "phase", "interference", "diffraction", "refraction", "reflection", "absorption", "emission", "transmission", "conduction", "convection", "radiation", "insulation", "resistance", "conductance", "capacitance", "inductance", "impedance", "voltage", "current", "power", "energy", "charge", "field", "flux", "potential", "gradient", "divergence", "curl", "laplacian", "vector", "scalar", "tensor", "matrix", "determinant", "eigenvalue", "eigenvector", "space", "time", "dimension", "coordinate", "axis", "origin", "point", "line", "plane", "curve", "surface", "solid", "shape", "form", "size", "scale", "ratio", "proportion", "fraction", "decimal", "percent", "integer", "rational", "irrational", "real", "complex", "imaginary", "number", "digit", "numeral", "symbol", "sign", "operator", "function", "relation", "set", "subset", "union", "intersection", "complement", "difference", "product", "sum", "difference", "quotient", "remainder", "factor", "multiple", "prime", "composite", "even", "odd", "positive", "negative", "zero", "one", "infinity", "limit", "derivative", "integral", "series", "sequence", "progression", "pattern", "rule", "law", "theorem", "proof", "axiom", "postulate", "definition", "conjecture", "hypothesis", "theory", "model", "simulation", "experiment", "observation", "measurement", "data", "information", "knowledge", "wisdom", "truth", "falsehood", "belief", "opinion", "fact", "fiction", "reality", "illusion", "dream", "nightmare", "vision", "hallucination", "memory", "forgetfulness", "learning", "teaching", "education", "school", "university", "college", "academy", "institute", "laboratory", "library", "museum", "gallery", "theater", "cinema", "studio", "stage", "screen", "film", "movie", "video", "audio", "sound", "music", "song", "melody", "harmony", "rhythm", "beat", "tempo", "pitch", "tone", "timbre", "noise", "silence", "quiet", "loud", "soft", "hard", "smooth", "rough", "sharp", "dull", "bright", "dim", "clear", "cloudy", "transparent", "opaque", "translucent", "color", "red", "orange", "yellow", "green", "blue", "indigo", "violet", "purple", "pink", "brown", "black", "white", "gray", "gold", "silver", "bronze", "copper", "iron", "steel", "aluminum", "lead", "tin", "zinc", "nickel", "chromium", "titanium", "platinum", "mercury", "uranium", "plutonium", "radium", "carbon", "hydrogen", "oxygen", "nitrogen", "sulfur", "phosphorus", "chlorine", "fluorine", "bromine", "iodine", "helium", "neon", "argon", "krypton", "xenon", "radon", "lithium", "sodium", "potassium", "rubidium", "cesium", "francium", "beryllium", "magnesium", "calcium", "strontium", "barium", "radium", "boron", "aluminum", "gallium", "indium", "thallium", "silicon", "germanium", "tin", "lead", "arsenic", "antimony", "bismuth", "polonium", "astatine", "tennessine", "oganesson"
]

# Curated Quotes Database (Categorized by length)
QUOTES_DB = [
    # Short (5-15 words)
    {"text": "Simplicity is the ultimate sophistication.", "author": "Leonardo da Vinci", "topic": "Design"},
    {"text": "Less is more.", "author": "Ludwig Mies van der Rohe", "topic": "Design"},
    {"text": "Knowledge is power.", "author": "Francis Bacon", "topic": "Philosophy"},
    {"text": "Time is money.", "author": "Benjamin Franklin", "topic": "Business"},
    {"text": "Actions speak louder than words.", "author": "Proverb", "topic": "Wisdom"},
    {"text": "Practice makes perfect.", "author": "Proverb", "topic": "Skill"},
    {"text": "The early bird catches the worm.", "author": "Proverb", "topic": "Wisdom"},
    {"text": "Beauty is in the eye of the beholder.", "author": "Proverb", "topic": "Art"},
    {"text": "Necessity is the mother of invention.", "author": "Proverb", "topic": "Innovation"},
    {"text": "A journey of a thousand miles begins with a single step.", "author": "Lao Tzu", "topic": "Philosophy"},
    {"text": "To be or not to be.", "author": "William Shakespeare", "topic": "Literature"},
    {"text": "All that glitters is not gold.", "author": "William Shakespeare", "topic": "Literature"},
    {"text": "The truth will set you free.", "author": "Bible", "topic": "Religion"},
    {"text": "Love thy neighbor as thyself.", "author": "Bible", "topic": "Religion"},
    {"text": "I think therefore I am.", "author": "René Descartes", "topic": "Philosophy"},
    {"text": "God is dead.", "author": "Friedrich Nietzsche", "topic": "Philosophy"},
    {"text": "Life is suffering.", "author": "Buddha", "topic": "Philosophy"},
    {"text": "Be the change you wish to see in the world.", "author": "Mahatma Gandhi", "topic": "Activism"},
    {"text": "An eye for an eye leaves the whole world blind.", "author": "Mahatma Gandhi", "topic": "Peace"},
    {"text": "In the middle of difficulty lies opportunity.", "author": "Albert Einstein", "topic": "Science"},
    {"text": "Imagination is more important than knowledge.", "author": "Albert Einstein", "topic": "Science"},
    {"text": "The unexamined life is not worth living.", "author": "Socrates", "topic": "Philosophy"},
    {"text": "Know thyself.", "author": "Socrates", "topic": "Philosophy"},
    {"text": "One cannot step twice in the same river.", "author": "Heraclitus", "topic": "Philosophy"},
    {"text": "Man is the measure of all things.", "author": "Protagoras", "topic": "Philosophy"},
    {"text": "The only thing I know is that I know nothing.", "author": "Socrates", "topic": "Philosophy"},
    {"text": "We are what we repeatedly do.", "author": "Aristotle", "topic": "Philosophy"},
    {"text": "Happiness depends upon ourselves.", "author": "Aristotle", "topic": "Philosophy"},
    {"text": "The whole is greater than the sum of its parts.", "author": "Aristotle", "topic": "Philosophy"},
    {"text": "Fortune favors the bold.", "author": "Virgil", "topic": "Literature"},
    
    # Medium (16-30 words)
    {"text": "It does not matter how slowly you go as long as you do not stop.", "author": "Confucius", "topic": "Wisdom"},
    {"text": "Our lives begin to end the day we become silent about things that matter.", "author": "Martin Luther King Jr.", "topic": "Activism"},
    {"text": "Do not dwell in the past, do not dream of the future, concentrate the mind on the present moment.", "author": "Buddha", "topic": "Mindfulness"},
    {"text": "The best way to predict the future is to create it.", "author": "Peter Drucker", "topic": "Business"},
    {"text": "Success is not final, failure is not fatal: it is the courage to continue that counts.", "author": "Winston Churchill", "topic": "Leadership"},
    {"text": "Believe you can and you're halfway there.", "author": "Theodore Roosevelt", "topic": "Motivation"},
    {"text": "The only limit to our realization of tomorrow will be our doubts of today.", "author": "Franklin D. Roosevelt", "topic": "Motivation"},
    {"text": "It always seems impossible until it's done.", "author": "Nelson Mandela", "topic": "Perseverance"},
    {"text": "Education is the most powerful weapon which you can use to change the world.", "author": "Nelson Mandela", "topic": "Education"},
    {"text": "First they ignore you, then they laugh at you, then they fight you, then you win.", "author": "Mahatma Gandhi", "topic": "Activism"},
    {"text": "Live as if you were to die tomorrow. Learn as if you were to live forever.", "author": "Mahatma Gandhi", "topic": "Life"},
    {"text": "Happiness is not something ready made. It comes from your own actions.", "author": "Dalai Lama", "topic": "Happiness"},
    {"text": "If you want to lift yourself up, lift up someone else.", "author": "Booker T. Washington", "topic": "Kindness"},
    {"text": "I have not failed. I've just found 10,000 ways that won't work.", "author": "Thomas Edison", "topic": "Innovation"},
    {"text": "Genius is one percent inspiration and ninety-nine percent perspiration.", "author": "Thomas Edison", "topic": "Work"},
    {"text": "Logic will get you from A to B. Imagination will take you everywhere.", "author": "Albert Einstein", "topic": "Creativity"},
    {"text": "Try not to become a man of success. Rather become a man of value.", "author": "Albert Einstein", "topic": "Values"},
    {"text": "Look deep into nature, and then you will understand everything better.", "author": "Albert Einstein", "topic": "Nature"},
    {"text": "The important thing is not to stop questioning. Curiosity has its own reason for existing.", "author": "Albert Einstein", "topic": "Curiosity"},
    {"text": "Anyone who has never made a mistake has never tried anything new.", "author": "Albert Einstein", "topic": "Learning"},
    {"text": "Two things are infinite: the universe and human stupidity; and I'm not sure about the universe.", "author": "Albert Einstein", "topic": "Humor"},
    {"text": "Life is like riding a bicycle. To keep your balance, you must keep moving.", "author": "Albert Einstein", "topic": "Life"},
    {"text": "The measure of intelligence is the ability to change.", "author": "Albert Einstein", "topic": "Intelligence"},
    {"text": "Weakness of attitude becomes weakness of character.", "author": "Albert Einstein", "topic": "Character"},
    {"text": "A person who never made a mistake never tried anything new.", "author": "Albert Einstein", "topic": "Growth"},
    {"text": "Strive not to be a success, but rather to be of value.", "author": "Albert Einstein", "topic": "Purpose"},
    {"text": "Great spirits have always encountered violent opposition from mediocre minds.", "author": "Albert Einstein", "topic": "Excellence"},
    {"text": "Peace cannot be kept by force; it can only be achieved by understanding.", "author": "Albert Einstein", "topic": "Peace"},
    {"text": "In the midst of winter, I found there was, within me, an invincible summer.", "author": "Albert Camus", "topic": "Resilience"},
    {"text": "The only way to deal with an unfree world is to become so absolutely free that your very existence is an act of rebellion.", "author": "Albert Camus", "topic": "Freedom"},

    # Long (31-50 words)
    {"text": "Three passions, simple but overwhelmingly strong, have governed my life: the longing for love, the search for knowledge, and unbearable pity for the suffering of mankind.", "author": "Bertrand Russell", "topic": "Life"},
    {"text": "I am enough of an artist to draw freely upon my imagination. Imagination is more important than knowledge. Knowledge is limited. Imagination encircles the world.", "author": "Albert Einstein", "topic": "Creativity"},
    {"text": "It is our attitude at the beginning of a difficult task which, more than anything else, will affect its successful outcome.", "author": "William James", "topic": "Psychology"},
    {"text": "The greatest glory in living lies not in never falling, but in rising every time we fall.", "author": "Nelson Mandela", "topic": "Resilience"},
    {"text": "In three words I can sum up everything I've learned about life: it goes on.", "author": "Robert Frost", "topic": "Life"},
    {"text": "If you judge people, you have no time to love them.", "author": "Mother Teresa", "topic": "Love"},
    {"text": "Not all those who wander are lost.", "author": "J.R.R. Tolkien", "topic": "Literature"},
    {"text": "There is some good in this world, and it's worth fighting for.", "author": "J.R.R. Tolkien", "topic": "Hope"},
    {"text": "All we have to decide is what to do with the time that is given us.", "author": "J.R.R. Tolkien", "topic": "Time"},
    {"text": "Even the darkest night will end and the sun will rise.", "author": "Victor Hugo", "topic": "Hope"},
    {"text": "To love another person is to see the face of God.", "author": "Victor Hugo", "topic": "Love"},
    {"text": "Life is the flower for which love is the honey.", "author": "Victor Hugo", "topic": "Love"},
    {"text": "Whatever you are, be a good one.", "author": "Abraham Lincoln", "topic": "Character"},
    {"text": "A house divided against itself cannot stand.", "author": "Abraham Lincoln", "topic": "Unity"},
    {"text": "Government of the people, by the people, for the people, shall not perish from the earth.", "author": "Abraham Lincoln", "topic": "Democracy"},
    {"text": "Four score and seven years ago our fathers brought forth on this continent, a new nation, conceived in Liberty, and dedicated to the proposition that all men are created equal.", "author": "Abraham Lincoln", "topic": "History"},
    {"text": "The best revenge is massive success.", "author": "Frank Sinatra", "topic": "Success"},
    {"text": "I have a dream that one day this nation will rise up and live out the true meaning of its creed.", "author": "Martin Luther King Jr.", "topic": "Dreams"},
    {"text": "Darkness cannot drive out darkness: only light can do that. Hate cannot drive out hate: only love can do that.", "author": "Martin Luther King Jr.", "topic": "Love"},
    {"text": "Injustice anywhere is a threat to justice everywhere.", "author": "Martin Luther King Jr.", "topic": "Justice"},
    {"text": "The time is always right to do what is right.", "author": "Martin Luther King Jr.", "topic": "Morality"},
    {"text": "Faith is taking the first step even when you don't see the whole staircase.", "author": "Martin Luther King Jr.", "topic": "Faith"},
    {"text": "We must accept finite disappointment, but never lose infinite hope.", "author": "Martin Luther King Jr.", "topic": "Hope"},
    {"text": "Intelligence plus character—that is the goal of true education.", "author": "Martin Luther King Jr.", "topic": "Education"},
    {"text": "Life's most persistent and urgent question is, 'What are you doing for others?'", "author": "Martin Luther King Jr.", "topic": "Service"},
    {"text": "The function of education is to teach one to think intensively and to think critically. Intelligence plus character – that is the goal of true education.", "author": "Martin Luther King Jr.", "topic": "Education"},
    {"text": "We must learn to live together as brothers or perish together as fools.", "author": "Martin Luther King Jr.", "topic": "Unity"},
    {"text": "Human progress is neither automatic nor inevitable... Every step toward the goal of justice requires sacrifice, suffering, and struggle; the tireless exertions and passionate concern of dedicated individuals.", "author": "Martin Luther King Jr.", "topic": "Progress"},
    {"text": "Everything that is done in this world is done by hope.", "author": "Martin Luther", "topic": "Hope"},
    {"text": "Peace is not merely a distant goal that we seek, but a means by which we arrive at that goal.", "author": "Martin Luther King Jr.", "topic": "Peace"},

    # Longest (50+ words)
    {"text": "Here's to the crazy ones. The misfits. The rebels. The troublemakers. The round pegs in the square holes. The ones who see things differently. They're not fond of rules. And they have no respect for the status quo. You can quote them, disagree with them, glorify or vilify them. About the only thing you can't do is ignore them. Because they change things. They push the human race forward. And while some may see them as the crazy ones, we see genius. Because the people who are crazy enough to think they can change the world, are the ones who do.", "author": "Steve Jobs", "topic": "Innovation"},
    {"text": "Your time is limited, so don't waste it living someone else's life. Don't be trapped by dogma – which is living with the results of other people's thinking. Don't let the noise of others' opinions drown out your own inner voice. And most important, have the courage to follow your heart and intuition. They somehow already know what you truly want to become. Everything else is secondary.", "author": "Steve Jobs", "topic": "Life"},
    {"text": "Stay hungry, stay foolish. Have the courage to follow your heart and intuition. They somehow already know what you truly want to become. Everything else is secondary. Your time is limited, so don't waste it living someone else's life. Don't be trapped by dogma – which is living with the results of other people's thinking.", "author": "Steve Jobs", "topic": "Wisdom"},
    {"text": "The reasonable man adapts himself to the world; the unreasonable one persists in trying to adapt the world to himself. Therefore all progress depends on the unreasonable man.", "author": "George Bernard Shaw", "topic": "Progress"},
    {"text": "We are all in the gutter, but some of us are looking at the stars.", "author": "Oscar Wilde", "topic": "Hope"},
    {"text": "Be yourself; everyone else is already taken.", "author": "Oscar Wilde", "topic": "Identity"},
    {"text": "To live is the rarest thing in the world. Most people exist, that is all.", "author": "Oscar Wilde", "topic": "Life"},
    {"text": "Always forgive your enemies; nothing annoys them so much.", "author": "Oscar Wilde", "topic": "Humor"},
    {"text": "Experience is simply the name we give our mistakes.", "author": "Oscar Wilde", "topic": "Learning"},
    {"text": "I can resist everything except temptation.", "author": "Oscar Wilde", "topic": "Humor"},
    {"text": "We are all born mad. Some remain so.", "author": "Samuel Beckett", "topic": "Absurdism"},
    {"text": "Ever tried. Ever failed. No matter. Try Again. Fail again. Fail better.", "author": "Samuel Beckett", "topic": "Perseverance"},
    {"text": "Hell is other people.", "author": "Jean-Paul Sartre", "topic": "Existentialism"},
    {"text": "Man is condemned to be free; because once thrown into the world, he is responsible for everything he does.", "author": "Jean-Paul Sartre", "topic": "Freedom"},
    {"text": "Existence precedes essence. We act, and in acting, we define ourselves.", "author": "Jean-Paul Sartre", "topic": "Existentialism"},
    {"text": "The absurd is the essential concept and the first truth.", "author": "Albert Camus", "topic": "Absurdism"},
    {"text": "One must imagine Sisyphus happy.", "author": "Albert Camus", "topic": "Absurdism"},
    {"text": "Real generosity toward the future lies in giving all to the present.", "author": "Albert Camus", "topic": "Time"},
    {"text": "Don't walk behind me; I may not lead. Don't walk in front of me; I may not follow. Just walk beside me and be my friend.", "author": "Albert Camus", "topic": "Friendship"},
    {"text": "The only way to deal with an unfree world is to become so absolutely free that your very existence is an act of rebellion.", "author": "Albert Camus", "topic": "Rebellion"},
    {"text": "In the depth of winter, I finally learned that within me there lay an invincible summer.", "author": "Albert Camus", "topic": "Resilience"},
    {"text": "Freedom is nothing but a chance to be better.", "author": "Albert Camus", "topic": "Freedom"},
    {"text": "You will never be happy if you continue to search for what happiness consists of. You will never live if you are looking for the meaning of life.", "author": "Albert Camus", "topic": "Happiness"},
    {"text": "Should I kill myself, or have a cup of coffee?", "author": "Albert Camus", "topic": "Absurdism"},
    {"text": "There is but one truly serious philosophical problem, and that is suicide. Judging whether life is or is not worth living amounts to answering the fundamental question of philosophy.", "author": "Albert Camus", "topic": "Philosophy"},
    {"text": "The struggle itself toward the heights is enough to fill a man's heart.", "author": "Albert Camus", "topic": "Struggle"},
    {"text": "What is a rebel? A man who says no.", "author": "Albert Camus", "topic": "Rebellion"},
    {"text": "I rebel; therefore I exist.", "author": "Albert Camus", "topic": "Existence"},
    {"text": "Without freedom, no art; art lives only on the restraints it imposes on itself, and dies of all others.", "author": "Albert Camus", "topic": "Art"},
    {"text": "Fiction is the lie through which we tell the truth.", "author": "Albert Camus", "topic": "Literature"}
]

def get_config():
    if not os.path.exists(CONFIG_DIR):
        os.makedirs(CONFIG_DIR)
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r') as f:
            return json.load(f)
    return {"theme": "default", "minimal_stats": False}

def save_config(config):
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f)

def get_scores():
    if os.path.exists(SCORES_FILE):
        with open(SCORES_FILE, 'r') as f:
            return json.load(f)
    return []

def save_score(score_entry):
    scores = get_scores()
    scores.append(score_entry)
    # Keep top 100
    scores.sort(key=lambda x: x['wpm'], reverse=True)
    with open(SCORES_FILE, 'w') as f:
        json.dump(scores[:100], f)

# --- LOGIC HELPERS ---

def get_text_for_mode(mode_arg):
    """Returns (text, mode_name) based on user argument."""
    if mode_arg == "custom":
        print("Enter custom text (press Enter twice to finish):")
        lines = []
        while True:
            line = input()
            if line == "" and lines and lines[-1] == "":
                break
            lines.append(line)
            if line == "" and len(lines) > 0:
                # Allow single empty line to finish if previous was not empty? 
                # Simpler: double enter.
                pass 
        return "\n".join(lines).strip(), "custom"

    if mode_arg == "zen":
        # Zen uses a random medium quote by default or specific logic
        quote = random.choice([q for q in QUOTES_DB if 15 < len(q['text'].split()) <= 30])
        return quote['text'], "zen"

    if mode_arg.startswith("rand"):
        try:
            count = int(mode_arg.split('-')[1])
            words = random.sample(RANDOM_WORDS, min(count, len(RANDOM_WORDS)))
            return " ".join(words), f"rand-{count}"
        except (IndexError, ValueError):
            # Default to 25 if parsing fails
            words = random.sample(RANDOM_WORDS, 25)
            return " ".join(words), "rand-25"

    if mode_arg in ["short", "medium", "long", "longest"]:
        filtered = []
        if mode_arg == "short":
            filtered = [q for q in QUOTES_DB if 5 <= len(q['text'].split()) <= 15]
        elif mode_arg == "medium":
            filtered = [q for q in QUOTES_DB if 16 <= len(q['text'].split()) <= 30]
        elif mode_arg == "long":
            filtered = [q for q in QUOTES_DB if 31 <= len(q['text'].split()) <= 50]
        elif mode_arg == "longest":
            filtered = [q for q in QUOTES_DB if len(q['text'].split()) > 50]
        
        if not filtered:
            return "No quotes found for this category.", "error"
        q = random.choice(filtered)
        return q['text'], f"quote-{mode_arg}"

    if mode_arg == "quote":
        q = random.choice(QUOTES_DB)
        return q['text'], "quote-random"

    # Fallback
    q = random.choice(QUOTES_DB)
    return q['text'], "random"

# --- CURSES UI ---

def draw_box(stdscr, y, x, h, w, title=""):
    try:
        stdscr.attron(curses.color_pair(4)) # Box color
        for i in range(h):
            stdscr.addstr(y + i, x, " " * w)
        
        # Corners and lines
        stdscr.addch(y, x, curses.ACS_ULCORNER)
        stdscr.addch(y, x + w - 1, curses.ACS_URCORNER)
        stdscr.addch(y + h - 1, x, curses.ACS_LLCORNER)
        stdscr.addch(y + h - 1, x + w - 1, curses.ACS_LRCORNER)
        for i in range(1, w - 1):
            stdscr.addch(y, x + i, curses.ACS_HLINE)
            stdscr.addch(y + h - 1, x + i, curses.ACS_HLINE)
        for i in range(1, h - 1):
            stdscr.addch(y + i, x, curses.ACS_VLINE)
            stdscr.addch(y + i, x + w - 1, curses.ACS_VLINE)
        
        if title:
            stdscr.addstr(y, x + 2, f" {title} ", curses.A_BOLD)
        stdscr.attroff(curses.color_pair(4))
    except curses.error:
        pass

def main_ui(stdscr):
    curses.curs_set(0)
    curses.start_color()
    curses.use_default_colors()
    
    # Colors: 1=Correct(Blue), 2=Error(Red), 3=Cursor(Green BG), 4=Box(Cyan), 5=Dim
    curses.init_pair(1, curses.COLOR_BLUE, -1)
    curses.init_pair(2, curses.COLOR_RED, -1)
    curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_GREEN)
    curses.init_pair(4, curses.COLOR_CYAN, -1)
    curses.init_pair(5, curses.COLOR_WHITE, -1)

    config = get_config()
    
    # Get Mode from Args if needed, here we assume called via wrapper or direct
    # For simplicity in this single-file version, we rely on env var or default
    mode_arg = os.environ.get("SCRIBERE_MODE", "rand-25")
    
    target_text, mode_name = get_text_for_mode(mode_arg)
    
    # State
    user_input = ""
    start_time = None
    finished = False
    show_results = False
    show_scores = False
    minimal_stats = config.get("minimal_stats", False)
    
    # Scroll offset for long texts
    scroll_offset = 0
    
    while True:
        h, w = stdscr.getmaxyx()
        stdscr.clear()
        
        # Header
        stdscr.addstr(0, 2, f" SCRIBERE | Mode: {mode_name} ", curses.A_BOLD | curses.color_pair(4))
        stdscr.addstr(0, w - 10, " ESC:Quit ", curses.A_DIM)
        
        if show_scores:
            # High Scores View
            scores = get_scores()
            draw_box(stdscr, 2, 2, h-4, w-4, " HIGH SCORES (M to Close) ")
            stdscr.addstr(3, 5, f"{'Rank':<5} {'WPM':<6} {'Acc':<6} {'Mode':<15} {'Date'}", curses.A_UNDERLINE)
            for i, s in enumerate(scores[:15]): # Show top 15
                date = s.get('date', 'N/A')[:10]
                stdscr.addstr(4+i, 5, f"{i+1:<5} {s['wpm']:<6.1f} {s['acc']:<6.1f}% {s['mode']:<15} {date}")
            stdscr.refresh()
            key = stdscr.getch()
            if key == ord('m') or key == curses.KEY_ENTER or key == 10 or key == 13:
                show_scores = False
            continue

        if show_results:
            # Results Screen
            elapsed = time.time() - start_time if start_time else 0
            wpm = (len(user_input.split()) / 5) / (elapsed / 60) if elapsed > 0 else 0
            
            # Calculate accuracy
            errors = sum(1 for i, c in enumerate(user_input) if i < len(target_text) and c != target_text[i])
            accuracy = (1 - (errors / len(user_input))) * 100 if len(user_input) > 0 else 0
            
            draw_box(stdscr, 2, 2, 10, 60, " RESULTS ")
            
            stats_y = 4
            stdscr.addstr(stats_y, 5, f"WPM: {wpm:.1f}", curses.A_BOLD | curses.color_pair(1))
            stdscr.addstr(stats_y, 25, f"Accuracy: {accuracy:.1f}%", curses.A_BOLD | curses.color_pair(2 if accuracy < 90 else 1))
            
            if not minimal_stats:
                stdscr.addstr(stats_y+2, 5, f"Chars: {len(user_input)}", curses.A_DIM)
                stdscr.addstr(stats_y+2, 25, f"Errors: {errors}", curses.A_DIM)
                stdscr.addstr(stats_y+2, 45, f"Time: {elapsed:.1f}s", curses.A_DIM)
            
            stdscr.addstr(stats_y+5, 5, " Press Enter to Restart | M: Scores | D: Toggle Stats ", curses.A_REVERSE)
            stdscr.refresh()
            
            key = stdscr.getch()
            if key == ord('m'):
                show_scores = True
            elif key == ord('d'):
                minimal_stats = not minimal_stats
                config["minimal_stats"] = minimal_stats
                save_config(config)
            elif key == 10 or key == 13: # Enter
                # Restart
                target_text, mode_name = get_text_for_mode(mode_arg)
                user_input = ""
                start_time = None
                finished = False
                show_results = False
                scroll_offset = 0

            continue

        # Typing Area
        box_h = min(15, h - 6)
        draw_box(stdscr, 2, 2, box_h, w - 4, " TYPE HERE ")
        
        # Render Text
        # Simple wrapping logic
        content_x = 4
        content_y = 4
        max_w = w - 8
        
        current_word = ""
        char_idx = 0
        
        # Adjust scroll if cursor goes out of view
        # Calculate cursor position roughly
        # This is a simplified renderer. For perfect scrolling, we'd map chars to coords.
        
        for i, char in enumerate(target_text):
            if content_y >= 2 + box_h - 1:
                break # Stop drawing if box full
            
            # Determine color
            color = curses.color_pair(5) # Default white
            if i < len(user_input):
                if user_input[i] == char:
                    color = curses.color_pair(1) # Blue correct
                else:
                    color = curses.color_pair(2) # Red error
            
            # Cursor highlight
            if i == len(user_input):
                stdscr.addstr(content_y, content_x, char, curses.color_pair(3) | curses.A_BOLD)
            else:
                try:
                    stdscr.addstr(content_y, content_x, char, color)
                except curses.error:
                    pass
            
            # Move cursor
            content_x += 1
            if content_x >= w - 6:
                content_x = 4
                content_y += 1
                
        # Draw User Input Progress (Visual feedback below or overlay)
        # In this minimalist design, the colored text IS the feedback.
        
        # Status bar
        status = f"Typed: {len(user_input)}/{len(target_text)}"
        if mode_name == "zen":
            status += " | Shift+Enter to Finish"
        stdscr.addstr(h-2, 2, status, curses.A_DIM)
        
        stdscr.refresh()
        
        # Input Handling
        key = stdscr.getch()
        
        if key == 27: # ESC
            break
        
        if finished:
            continue
            
        if start_time is None and key != curses.KEY_ENTER:
            start_time = time.time()
            
        if key == curses.KEY_BACKSPACE or key == 127 or key == 8:
            if len(user_input) > 0:
                user_input = user_input[:-1]
        elif key == 10 or key == 13: # Enter
            if mode_name == "zen":
                finished = True
                show_results = True
                # Save Score
                elapsed = time.time() - start_time
                wpm = (len(user_input.split()) / 5) / (elapsed / 60) if elapsed > 0 else 0
                errors = sum(1 for i, c in enumerate(user_input) if i < len(target_text) and c != target_text[i])
                acc = (1 - (errors / len(user_input))) * 100 if len(user_input) > 0 else 0
                save_score({"wpm": wpm, "acc": acc, "mode": mode_name, "date": time.strftime("%Y-%m-%d")})
            else:
                # In normal mode, Enter might just add a newline if in custom, 
                # but for quotes/words, usually space is enough. 
                # Let's treat Enter as finish for non-zen too if desired, or ignore.
                # Monkeytype: Space advances. Enter finishes test? 
                # Let's make Enter finish test for all modes for simplicity.
                finished = True
                show_results = True
                elapsed = time.time() - start_time
                wpm = (len(user_input.split()) / 5) / (elapsed / 60) if elapsed > 0 else 0
                errors = sum(1 for i, c in enumerate(user_input) if i < len(target_text) and c != target_text[i])
                acc = (1 - (errors / len(user_input))) * 100 if len(user_input) > 0 else 0
                save_score({"wpm": wpm, "acc": acc, "mode": mode_name, "date": time.strftime("%Y-%m-%d")})
                
        elif 32 <= key <= 126: # Printable
            if len(user_input) < len(target_text):
                user_input += chr(key)
            elif len(user_input) == len(target_text):
                # Auto finish if typed exactly to end
                finished = True
                show_results = True
                elapsed = time.time() - start_time
                wpm = (len(user_input.split()) / 5) / (elapsed / 60) if elapsed > 0 else 0
                errors = sum(1 for i, c in enumerate(user_input) if i < len(target_text) and c != target_text[i])
                acc = (1 - (errors / len(user_input))) * 100 if len(user_input) > 0 else 0
                save_score({"wpm": wpm, "acc": acc, "mode": mode_name, "date": time.strftime("%Y-%m-%d")})

if __name__ == "__main__":
    # Check args for mode
    if len(sys.argv) > 1:
        # Pass mode to env for the curses app to pick up
        # Or refactor to pass directly. Env is easiest for this structure.
        os.environ["SCRIBERE_MODE"] = sys.argv[1]
    else:
        os.environ["SCRIBERE_MODE"] = "rand-25"
        
    try:
        curses.wrapper(main_ui)
    except KeyboardInterrupt:
        pass
