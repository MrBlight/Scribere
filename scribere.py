#!/usr/bin/env python3
"""
Scribere - A hyper-minimalist terminal typing tutor.
Licensed under GNU GPL v3.
"""

import curses
import time
import random
import json
import os
import sys
import textwrap

# --- Configuration & Paths ---
CONFIG_DIR = os.path.join(os.path.expanduser("~"), ".scribere")
CONFIG_FILE = os.path.join(CONFIG_DIR, "config.json")
SCORES_FILE = os.path.join(CONFIG_DIR, "scores.json")

# Ensure config directory exists
if not os.path.exists(CONFIG_DIR):
    os.makedirs(CONFIG_DIR)

# --- Data: Common Words (Simple) ---
COMMON_WORDS = [
    "the", "be", "to", "of", "and", "a", "in", "that", "have", "it",
    "for", "not", "on", "with", "he", "as", "you", "do", "at", "this",
    "but", "his", "by", "from", "they", "we", "say", "her", "she", "or",
    "an", "will", "my", "one", "all", "would", "there", "their", "what", "so",
    "up", "out", "if", "about", "who", "get", "which", "go", "me", "when",
    "make", "can", "like", "time", "no", "just", "him", "know", "take", "people",
    "into", "year", "your", "good", "some", "could", "them", "see", "other", "than",
    "then", "now", "look", "only", "come", "its", "over", "think", "also", "back",
    "after", "use", "two", "how", "our", "work", "first", "well", "way", "even",
    "new", "want", "because", "any", "these", "give", "day", "most", "us", "is",
    "house", "school", "fight", "although", "through", "water", "money", "story", "world", "place",
    "hand", "eye", "part", "group", "problem", "fact", "right", "study", "book", "job",
    "word", "business", "issue", "side", "kind", "head", "home", "service", "friend", "father",
    "power", "hour", "game", "line", "end", "member", "law", "car", "city", "community",
    "name", "president", "team", "minute", "idea", "kid", "body", "information", "face", "art",
    "week", "market", "family", "life", "country", "plant", "last", "child", "office", "learn",
    "music", "person", "month", "road", "dream", "food", "air", "teacher", "door", "room",
    "floor", "woman", "plan", "north", "south", "east", "west", "site", "hold", "own",
    "while", "may", "down", "case", "few", "run", "point", "believe", "hear", "stop",
    "without", "second", "late", "miss", "idea", "enough", "ask", "away", "almost", "turned",
    "called", "kind", "stay", "white", "began", "arrive", "across", "today", "under", "around",
    "mother", "did", "set", "three", "put", "try", "same", "another", "might", "spend",
    "already", "real", "remember", "buy", "done", "read", "need", "move", "live", "leave"
]

# --- Data: Complex Words (Advanced) ---
COMPLEX_WORDS = [
    "aberration", "benevolent", "cacophony", "daunting", "ephemeral", "fastidious", "gregarious",
    "hierarchy", "idiosyncrasy", "juxtaposition", "kinetic", "luminous", "meticulous", "nefarious",
    "obscure", "paradigm", "quintessential", "resilient", "serendipity", "taciturn", "ubiquitous",
    "vacillate", "warrant", "xenophobia", "yearn", "zealous", "algorithm", "binary", "cache",
    "debug", "encryption", "framework", "gateway", "hardware", "interface", "javascript", "kernel",
    "latency", "middleware", "network", "object", "protocol", "query", "runtime", "server",
    "thread", "utility", "virtual", "widget", "xml", "yaml", "zone", "abstract", "boolean",
    "class", "dependency", "exception", "function", "global", "heap", "inheritance", "json",
    "library", "memory", "namespace", "operator", "pointer", "queue", "recursion", "stack",
    "variable", "wrapper", "xpath", "yield", "zip", "acid", "base", "catalyst", "dilute",
    "electron", "fusion", "gravity", "hydrogen", "ion", "joule", "kelvin", "light", "mass",
    "neutron", "orbit", "photon", "quantum", "radiation", "spectrum", "thermodynamics", "universe",
    "velocity", "wavelength", "xenon", "yttrium", "zinc", "aesthetic", "philosophy", "ethics",
    "metaphysics", "epistemology", "logic", "rhetoric", "dialectic", "syllogism", "paradox",
    "empirical", "rational", "existential", "nihilism", "stoicism", "epicurean", "utilitarian",
    "deontological", "virtue", "justice", "freedom", "determinism", "compatibilism", "consciousness"
]

# --- Data: Quotes Database (Categorized) ---
QUOTES_DB = [
    # Short (5-15 words)
    {"text": "The only way to do great work is to love what you do.", "author": "Steve Jobs", "category": "Tech", "length": "short"},
    {"text": "Life is what happens when you are busy making other plans.", "author": "John Lennon", "category": "Life", "length": "short"},
    {"text": "The future belongs to those who believe in the beauty of their dreams.", "author": "Eleanor Roosevelt", "category": "Inspiration", "length": "short"},
    {"text": "It is during our darkest moments that we must focus to see the light.", "author": "Aristotle", "category": "Philosophy", "length": "short"},
    {"text": "Do not go where the path may lead, go instead where there is no path.", "author": "Ralph Waldo Emerson", "category": "Inspiration", "length": "short"},
    {"text": "In the middle of difficulty lies opportunity.", "author": "Albert Einstein", "category": "Science", "length": "short"},
    {"text": "Success is not final, failure is not fatal: it is the courage to continue.", "author": "Winston Churchill", "category": "History", "length": "short"},
    {"text": "Believe you can and you are halfway there.", "author": "Theodore Roosevelt", "category": "Inspiration", "length": "short"},
    {"text": "Act as if what you do makes a difference. It does.", "author": "William James", "category": "Philosophy", "length": "short"},
    {"text": "What we think, we become.", "author": "Buddha", "category": "Philosophy", "length": "short"},
    {"text": "Strive not to be a success, but rather to be of value.", "author": "Albert Einstein", "category": "Science", "length": "short"},
    {"text": "Two roads diverged in a wood, and I took the one less traveled by.", "author": "Robert Frost", "category": "Literature", "length": "short"},
    {"text": "The best way to predict the future is to create it.", "author": "Peter Drucker", "category": "Business", "length": "short"},
    {"text": "You miss one hundred percent of the shots you never take.", "author": "Wayne Gretzky", "category": "Sports", "length": "short"},
    {"text": "Happiness depends upon ourselves.", "author": "Aristotle", "category": "Philosophy", "length": "short"},
    {"text": "Turn your wounds into wisdom.", "author": "Oprah Winfrey", "category": "Life", "length": "short"},
    {"text": "Change the world by being yourself.", "author": "Amy Poehler", "category": "Inspiration", "length": "short"},
    {"text": "Every moment is a fresh beginning.", "author": "T.S. Eliot", "category": "Literature", "length": "short"},
    {"text": "Dream big and dare to fail.", "author": "Norman Vaughan", "category": "Inspiration", "length": "short"},
    {"text": "Simplicity is the ultimate sophistication.", "author": "Leonardo da Vinci", "category": "Art", "length": "short"},
    
    # Medium (16-30 words)
    {"text": "Programming isn't about what you know; it's about what you can figure out.", "author": "Chris Pine", "category": "Tech", "length": "medium"},
    {"text": "The function of good software is to make the complex appear to be simple.", "author": "Grady Booch", "category": "Tech", "length": "medium"},
    {"text": "Talk is cheap. Show me the code.", "author": "Linus Torvalds", "category": "Tech", "length": "medium"},
    {"text": "First, solve the problem. Then, write the code.", "author": "John Johnson", "category": "Tech", "length": "medium"},
    {"text": "Experience is the name everyone gives to their mistakes.", "author": "Oscar Wilde", "category": "Literature", "length": "medium"},
    {"text": "It always seems impossible until it is done.", "author": "Nelson Mandela", "category": "History", "length": "medium"},
    {"text": "You cannot shake hands with a clenched fist.", "author": "Indira Gandhi", "category": "Politics", "length": "medium"},
    {"text": "A person who never made a mistake never tried anything new.", "author": "Albert Einstein", "category": "Science", "length": "medium"},
    {"text": "The only limit to our realization of tomorrow will be our doubts of today.", "author": "Franklin D. Roosevelt", "category": "History", "length": "medium"},
    {"text": "Do what you can, with what you have, where you are.", "author": "Theodore Roosevelt", "category": "Inspiration", "length": "medium"},
    {"text": "Happiness is not something ready made. It comes from your own actions.", "author": "Dalai Lama", "category": "Philosophy", "length": "medium"},
    {"text": "Whatever you are, be a good one.", "author": "Abraham Lincoln", "category": "History", "length": "medium"},
    {"text": "Everything you can imagine is real.", "author": "Pablo Picasso", "category": "Art", "length": "medium"},
    {"text": "Simplicity is the soul of efficiency.", "author": "Austin Freeman", "category": "Tech", "length": "medium"},
    {"text": "Make it work, make it right, make it fast.", "author": "Kent Beck", "category": "Tech", "length": "medium"},
    {"text": "Code is like humor. When you have to explain it, it is bad.", "author": "Cory House", "category": "Tech", "length": "medium"},
    {"text": "Fix the cause, not the symptom.", "author": "Steve Maguire", "category": "Tech", "length": "medium"},
    {"text": "Optimism is an occupational hazard of programming: feedback is the treatment.", "author": "Kent Beck", "category": "Tech", "length": "medium"},
    {"text": "Knowledge is power. Information is liberating.", "author": "Kofi Annan", "category": "Politics", "length": "medium"},
    {"text": "The best way to find out if you can trust somebody is to trust them.", "author": "Ernest Hemingway", "category": "Literature", "length": "medium"},
    {"text": "If you tell the truth, you don't have to remember anything.", "author": "Mark Twain", "category": "Literature", "length": "medium"},
    {"text": "Friendship is born at that moment when one person says to another: What!", "author": "C.S. Lewis", "category": "Literature", "length": "medium"},
    {"text": "A room without books is like a body without a soul.", "author": "Cicero", "category": "Literature", "length": "medium"},
    {"text": "Be the change that you wish to see in the world.", "author": "Mahatma Gandhi", "category": "History", "length": "medium"},
    {"text": "In three words I can sum up everything I've learned about life: it goes on.", "author": "Robert Frost", "category": "Literature", "length": "medium"},
    
    # Long (31-50 words)
    {"text": "Here's to the crazy ones. The misfits. The rebels. The troublemakers. The round pegs in the square holes. The ones who see things differently.", "author": "Steve Jobs", "category": "Tech", "length": "long"},
    {"text": "I am not afraid of death, I just don't want to be there when it happens. I want to live forever in my work.", "author": "Woody Allen", "category": "Art", "length": "long"},
    {"text": "The greatest glory in living lies not in never falling, but in rising every time we fall.", "author": "Nelson Mandela", "category": "History", "length": "long"},
    {"text": "The way to get started is to quit talking and begin doing.", "author": "Walt Disney", "category": "Business", "length": "long"},
    {"text": "Your time is limited, so don't waste it living someone else's life.", "author": "Steve Jobs", "category": "Tech", "length": "long"},
    {"text": "If life were predictable it would cease to be life, and be without flavor.", "author": "Eleanor Roosevelt", "category": "Life", "length": "long"},
    {"text": "If you look at what you have in life, you'll always have more.", "author": "Oprah Winfrey", "category": "Life", "length": "long"},
    {"text": "If you set your goals ridiculously high and it's a failure, you will fail above everyone else's success.", "author": "James Cameron", "category": "Art", "length": "long"},
    {"text": "Life is really simple, but we insist on making it complicated.", "author": "Confucius", "category": "Philosophy", "length": "long"},
    {"text": "May you live all the days of your life.", "author": "Jonathan Swift", "category": "Literature", "length": "long"},
    {"text": "Life itself is the most wonderful fairy tale.", "author": "Hans Christian Andersen", "category": "Literature", "length": "long"},
    {"text": "Do not let making a living prevent you from making a life.", "author": "John Wooden", "category": "Life", "length": "long"},
    {"text": "You only live once, but if you do it right, once is enough.", "author": "Mae West", "category": "Life", "length": "long"},
    {"text": "Never let the fear of striking out keep you from playing the game.", "author": "Babe Ruth", "category": "Sports", "length": "long"},
    {"text": "Money and success don't change people; they merely amplify what is already there.", "author": "Will Smith", "category": "Life", "length": "long"},
    {"text": "Not how long, but how well you have lived is the main thing.", "author": "Seneca", "category": "Philosophy", "length": "long"},
    {"text": "The purpose of our lives is to be happy.", "author": "Dalai Lama", "category": "Philosophy", "length": "long"},
    {"text": "Get busy living or get busy dying.", "author": "Stephen King", "category": "Literature", "length": "long"},
    {"text": "You have within you right now, everything you need to deal with whatever the world can throw at you.", "author": "Brian Tracy", "category": "Inspiration", "length": "long"},
    {"text": "Believe in yourself. You are braver than you think, more talented than you know, and capable of more than you imagine.", "author": "Roy T. Bennett", "category": "Inspiration", "length": "long"},
    
    # Longest (50+ words)
    {"text": "I've learned that people will forget what you said, people will forget what you did, but people will never forget how you made them feel.", "author": "Maya Angelou", "category": "Literature", "length": "longest"},
    {"text": "There is only one thing that makes a dream impossible to achieve: the fear of failure.", "author": "Paulo Coelho", "category": "Literature", "length": "longest"},
    {"text": "Whether you think you can or you think you can't, you're right.", "author": "Henry Ford", "category": "Business", "length": "longest"},
    {"text": "The two most important days in your life are the day you are born and the day you find out why.", "author": "Mark Twain", "category": "Literature", "length": "longest"},
    {"text": "Whatever you can do, or dream you can, begin it. Boldness has genius, power and magic in it.", "author": "Johann Wolfgang von Goethe", "category": "Literature", "length": "longest"},
    {"text": "The best revenge is massive success.", "author": "Frank Sinatra", "category": "Art", "length": "longest"},
    {"text": "People ask, 'What's the best role you've ever played?' The next one.", "author": "Kevin Kline", "category": "Art", "length": "longest"},
    {"text": "I find that the harder I work, the more luck I seem to have.", "author": "Thomas Jefferson", "category": "History", "length": "longest"},
    {"text": "Don't be pushed around by the fears in your mind. Be led by the dreams in your heart.", "author": "Roy T. Bennett", "category": "Inspiration", "length": "longest"},
    {"text": "Hardships often prepare ordinary people for an extraordinary destiny.", "author": "C.S. Lewis", "category": "Literature", "length": "longest"},
    {"text": "Remember no one can make you feel inferior without your consent.", "author": "Eleanor Roosevelt", "category": "History", "length": "longest"},
    {"text": "Life is ten percent what happens to you and ninety percent how you respond to it.", "author": "Charles Swindoll", "category": "Life", "length": "longest"},
    {"text": "Keep your face always toward the sunshine and shadows will fall behind you.", "author": "Walt Whitman", "category": "Literature", "length": "longest"},
    {"text": "What lies behind us and what lies before us are tiny matters compared to what lies within us.", "author": "Ralph Waldo Emerson", "category": "Philosophy", "length": "longest"},
    {"text": "You are never too old to set another goal or to dream a new dream.", "author": "C.S. Lewis", "category": "Literature", "length": "longest"},
    {"text": "Try to be a rainbow in someone's cloud.", "author": "Maya Angelou", "category": "Literature", "length": "longest"},
    {"text": "You do not find the happy life. You make it.", "author": "Camilla Eyring Kimball", "category": "Life", "length": "longest"},
    {"text": "Inspiration does exist, but it must find you working.", "author": "Pablo Picasso", "category": "Art", "length": "longest"},
    {"text": "Don't settle for what life gives you; make life better and build something.", "author": "Ashton Kutcher", "category": "Tech", "length": "longest"},
    {"text": "Everybody wants to be famous, but nobody wants to do the work. I live by that.", "author": "Joe Gurman", "category": "Art", "length": "longest"},
]

def load_config():
    defaults = {
        "theme": "default",
        "minimal_stats": False,
        "word_bank": "common" # 'common' or 'complex'
    }
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, 'r') as f:
                data = json.load(f)
                defaults.update(data)
        except:
            pass
    return defaults

def save_config(config):
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f, indent=2)

def load_scores():
    if os.path.exists(SCORES_FILE):
        try:
            with open(SCORES_FILE, 'r') as f:
                return json.load(f)
        except:
            return []
    return []

def save_scores(scores):
    with open(SCORES_FILE, 'w') as f:
        json.dump(scores, f, indent=2)

# --- Helper Functions ---

def get_words(mode, count=None, length_cat=None, use_complex=False):
    """Generate text based on mode."""
    bank = COMPLEX_WORDS if use_complex else COMMON_WORDS
    
    if mode == "random":
        # Random words mode
        n = count if count else 25
        return " ".join(random.choices(bank, k=n))
    
    elif mode == "quote":
        # Filter quotes by length category if provided
        if length_cat:
            candidates = [q for q in QUOTES_DB if q["length"] == length_cat]
        else:
            candidates = QUOTES_DB
        
        if not candidates:
            candidates = QUOTES_DB # Fallback
            
        q = random.choice(candidates)
        return q["text"]
        
    elif mode == "zen":
        # Zen mode uses random quotes usually, or random words if preferred
        # Let's default to a random quote for zen flow
        q = random.choice(QUOTES_DB)
        return q["text"]

    return "The quick brown fox jumps over the lazy dog."

def calculate_wpm(chars_typed, time_elapsed):
    if time_elapsed == 0:
        return 0
    minutes = time_elapsed / 60.0
    words = chars_typed / 5.0
    return int(words / minutes)

# --- Main Application Class ---

class ScribereApp:
    def __init__(self, stdscr, args):
        self.stdscr = stdscr
        self.args = args
        self.config = load_config()
        self.scores = load_scores()
        
        # State
        self.target_text = ""
        self.user_input = ""
        self.start_time = None
        self.end_time = None
        self.running = True
        self.finished = False
        self.mode = args.mode if hasattr(args, 'mode') else "rand-25"
        self.word_count_arg = args.count if hasattr(args, 'count') else None
        self.length_cat = args.length if hasattr(args, 'length') else None
        self.use_complex = self.config.get("word_bank") == "complex" or (hasattr(args, 'complex') and args.complex)
        
        # UI State
        self.show_menu = False
        self.menu_idx = 0
        self.stats_minimal = self.config.get("minimal_stats", False)
        
        self.setup_curses()
        self.prepare_test()

    def setup_curses(self):
        curses.curs_set(0) # Hide cursor
        self.stdscr.nodelay(False)
        self.stdscr.timeout(100) # 100ms refresh
        
        # Colors
        if curses.has_colors():
            curses.start_color()
            curses.use_default_colors()
            # Pair 1: Correct (Blue on Default)
            curses.init_pair(1, curses.COLOR_BLUE, -1)
            # Pair 2: Incorrect (Red on Default)
            curses.init_pair(2, curses.COLOR_RED, -1)
            # Pair 3: Cursor/Highlight (Green on Default)
            curses.init_pair(3, curses.COLOR_GREEN, -1)
            # Pair 4: Dim/Subtle
            curses.init_pair(4, curses.COLOR_WHITE, -1)
            # Pair 5: Header/Boldish
            curses.init_pair(5, curses.COLOR_CYAN, -1)

    def prepare_test(self):
        # Parse mode string like "rand-25", "quote", "zen", "short", "medium"
        m = self.mode.lower()
        
        if m.startswith("rand"):
            parts = m.split("-")
            count = 25
            if len(parts) > 1:
                try:
                    count = int(parts[1])
                except:
                    pass
            self.target_text = get_words("random", count=count, use_complex=self.use_complex)
            
        elif m == "zen":
            self.target_text = get_words("zen", use_complex=self.use_complex)
            
        elif m in ["short", "medium", "long", "longest"]:
            self.target_text = get_words("quote", length_cat=m, use_complex=self.use_complex)
            
        elif m == "quote":
            self.target_text = get_words("quote", use_complex=self.use_complex)
            
        elif m == "custom":
            # Handled by CLI input mostly, but fallback
            self.target_text = "Type this custom text exactly as it appears here."
            
        else:
            # Default to rand-25
            self.target_text = get_words("random", count=25, use_complex=self.use_complex)

    def draw_box(self, y, x, h, w, title=""):
        try:
            self.stdscr.attron(curses.color_pair(5) | curses.A_BOLD)
            self.stdscr.addstr(y, x, "┌" + "─" * (w-2) + "┐")
            if title:
                self.stdscr.addstr(y, x + (w//2) - len(title)//2, f" {title} ")
            
            for i in range(1, h-1):
                self.stdscr.addstr(y+i, x, "│")
                self.stdscr.addstr(y+i, x+w-1, "│")
                
            self.stdscr.addstr(y+h-1, x, "└" + "─" * (w-2) + "┘")
            self.stdscr.attroff(curses.color_pair(5) | curses.A_BOLD)
        except curses.error:
            pass

    def draw_screen(self):
        self.stdscr.clear()
        h, w = self.stdscr.getmaxyx()
        
        # Header
        header = " SCRIBERE "
        self.stdscr.attron(curses.color_pair(5) | curses.A_BOLD)
        self.stdscr.addstr(0, (w//2)-len(header)//2, header)
        self.stdscr.attroff(curses.color_pair(5) | curses.A_BOLD)
        
        # Status Line
        status = f"Mode: {self.mode} | Bank: {'Complex' if self.use_complex else 'Common'}"
        if self.finished:
            status += " | FINISHED (Press Enter)"
        self.stdscr.addstr(2, 2, status[:w-4], curses.color_pair(4))

        # Main Content Area
        box_h = min(20, h - 8)
        box_w = min(80, w - 4)
        box_y = 4
        box_x = (w - box_w) // 2
        
        self.draw_box(box_y, box_x, box_h, box_w, " Type Here ")
        
        # Render Text
        # Wrap text to fit box width
        inner_w = box_w - 4
        lines = textwrap.wrap(self.target_text, inner_w)
        
        start_y = box_y + 2
        
        # We need to map user_input characters to the target_text characters visually
        # Since wrapping changes indices, we must render line by line based on the wrapped target
        
        current_target_idx = 0
        current_input_idx = 0
        
        for r_idx, line in enumerate(lines):
            line_len = len(line)
            line_str = ""
            
            # Build the colored line
            for i in range(line_len):
                t_char = self.target_text[current_target_idx]
                
                # Check if user typed this far
                if current_input_idx < len(self.user_input):
                    u_char = self.user_input[current_input_idx]
                    if u_char == t_char:
                        # Correct
                        if current_input_idx == len(self.user_input) - 1 and not self.finished:
                            line_str += ("█", curses.color_pair(3) | curses.A_BOLD) # Cursor highlight
                        else:
                            line_str += (t_char, curses.color_pair(1))
                    else:
                        # Error
                        if current_input_idx == len(self.user_input) - 1 and not self.finished:
                             line_str += ("█", curses.color_pair(2) | curses.A_BOLD)
                        else:
                            line_str += (t_char, curses.color_pair(2) | curses.A_UNDERLINE)
                    
                    current_input_idx += 1
                else:
                    # Not typed yet
                    line_str += (t_char, curses.color_pair(4) | curses.A_DIM)
                
                current_target_idx += 1
            
            # Draw the line parts
            cx = box_x + 2
            cy = start_y + r_idx
            if cy < h - 1:
                for char, attr in line_str:
                    try:
                        self.stdscr.addch(cy, cx, char, attr)
                        cx += 1
                    except curses.error:
                        break

        # Footer / Stats
        if self.finished:
            self.draw_results(h, w)
        else:
            # Live Stats
            elapsed = 0
            if self.start_time:
                elapsed = time.time() - self.start_time
            
            wpm = calculate_wpm(len(self.user_input), elapsed)
            accuracy = 0
            if len(self.user_input) > 0:
                correct = sum(1 for i, c in enumerate(self.user_input) if i < len(self.target_text) and c == self.target_text[i])
                accuracy = int((correct / len(self.user_input)) * 100)
            
            stats_line = f" WPM: {wpm} | Acc: {accuracy}% | Time: {elapsed:.1f}s "
            self.stdscr.addstr(h-2, (w//2)-len(stats_line)//2, stats_line, curses.color_pair(5) | curses.A_BOLD)
            
            instructions = " ESC: Quit | Backspace: Delete | Shift+Enter: Finish (Zen) "
            self.stdscr.addstr(h-1, (w//2)-len(instructions)//2, instructions, curses.color_pair(4))

        self.stdscr.refresh()

    def draw_results(self, h, w):
        elapsed = self.end_time - self.start_time if self.end_time else 0
        chars_typed = len(self.user_input)
        wpm = calculate_wpm(chars_typed, elapsed)
        
        correct_count = sum(1 for i, c in enumerate(self.user_input) if i < len(self.target_text) and c == self.target_text[i])
        errors = chars_typed - correct_count
        accuracy = int((correct_count / chars_typed) * 100) if chars_typed > 0 else 0
        
        box_h = 12
        box_w = 60
        box_y = (h - box_h) // 2
        box_x = (w - box_w) // 2
        
        self.draw_box(box_y, box_x, box_h, box_w, " Results ")
        
        center_x = box_x + box_w // 2
        
        if self.stats_minimal:
            res_text = f" WPM: {wpm} | Accuracy: {accuracy}% "
            self.stdscr.addstr(box_y + 4, center_x - len(res_text)//2, res_text, curses.color_pair(1) | curses.A_BOLD)
            hint = " Press 'D' for details, 'M' for scores, Enter to restart "
            self.stdscr.addstr(box_y + 8, center_x - len(hint)//2, hint, curses.color_pair(4))
        else:
            details = [
                f"WPM: {wpm}",
                f"Accuracy: {accuracy}%",
                f"Correct: {correct_count}",
                f"Errors: {errors}",
                f"Time: {elapsed:.2f}s"
            ]
            
            for i, line in enumerate(details):
                self.stdscr.addstr(box_y + 3 + i, center_x - len(line)//2, line, curses.color_pair(1) if i==0 else curses.color_pair(4))
            
            hint = " Press 'D' for minimal, 'M' for scores, Enter to restart "
            self.stdscr.addstr(box_y + 9, center_x - len(hint)//2, hint, curses.color_pair(4))

    def save_score(self, wpm, acc):
        score_entry = {
            "date": time.strftime("%Y-%m-%d %H:%M"),
            "mode": self.mode,
            "wpm": wpm,
            "accuracy": acc,
            "length_cat": self.length_cat or ("random" if self.mode.startswith("rand") else "quote")
        }
        self.scores.append(score_entry)
        # Sort by WPM desc
        self.scores.sort(key=lambda x: x["wpm"], reverse=True)
        self.scores = self.scores[:50] # Keep top 50
        save_scores(self.scores)

    def show_highscores(self):
        # Simple modal overlay
        h, w = self.stdscr.getmaxyx()
        box_h = min(20, h-4)
        box_w = min(60, w-4)
        y = (h - box_h) // 2
        x = (w - box_w) // 2
        
        self.draw_box(y, x, box_h, box_w, " High Scores (Esc to close) ")
        
        if not self.scores:
            msg = "No scores recorded yet."
            self.stdscr.addstr(y + box_h//2, x + box_w//2 - len(msg)//2, msg, curses.color_pair(4))
        else:
            # Show top 10
            limit = min(10, len(self.scores))
            self.stdscr.addstr(y+2, x+2, f"{'Rank':<5} {'WPM':<5} {'Acc':<5} {'Mode':<15} {'Date':<15}", curses.color_pair(5) | curses.A_BOLD)
            for i in range(limit):
                s = self.scores[i]
                line = f"{i+1:<5} {s['wpm']:<5} {s['accuracy']:<5} {s['mode']:<15} {s['date']:<15}"
                # Truncate if too long
                line = line[:box_w-4]
                self.stdscr.addstr(y+3+i, x+2, line, curses.color_pair(4))
        
        self.stdscr.refresh()
        # Wait for Esc
        while True:
            key = self.stdscr.getch()
            if key == 27: # ESC
                break
            if key == ord('d') or key == ord('D'):
                 # Toggle minimal inside menu? No, let's keep it simple
                 pass

    def run(self):
        while self.running:
            self.draw_screen()
            
            if self.finished:
                key = self.stdscr.getch()
                if key == 10 or key == 13: # Enter
                    # Restart
                    self.user_input = ""
                    self.start_time = None
                    self.end_time = None
                    self.finished = False
                    self.prepare_test()
                elif key == ord('d') or key == ord('D'):
                    self.stats_minimal = not self.stats_minimal
                    self.config["minimal_stats"] = self.stats_minimal
                    save_config(self.config)
                elif key == ord('m') or key == ord('M'):
                    self.show_highscores()
                elif key == 27: # ESC
                    self.running = False
                continue

            # Normal Typing
            key = self.stdscr.getch()
            
            if key == 27: # ESC
                self.running = False
                continue
            
            if key == curses.KEY_BACKSPACE or key == 127 or key == 8:
                self.user_input = self.user_input[:-1]
                continue
            
            # Shift+Enter detection (often 330 or similar, but standard Enter is 10/13)
            # In many terminals, Shift+Enter is just Enter. 
            # We'll treat Enter as finish for Zen mode specifically if needed, 
            # but standard behavior is usually just type newline? 
            # Monkeytype doesn't use newlines in single line.
            # Let's make Enter finish the test ONLY if we are near the end or in Zen?
            # Actually, let's make Enter finish the test always for simplicity in this minimalist version?
            # No, that stops mid-sentence. 
            # Requirement: "in zen mode to finish the test you can press shift enter"
            # Since detecting Shift+Enter reliably in curses is hard across OS, 
            # let's assume if Mode is Zen, Enter finishes. Otherwise Enter is ignored or newline?
            # Let's ignore Enter for normal modes to allow full typing, 
            # but for Zen, Enter finishes.
            
            if key == 10 or key == 13: # Enter
                if self.mode == "zen":
                    self.finish_test()
                continue

            if key == ord('m') or key == ord('M'):
                self.show_highscores()
                continue
                
            if key == ord('d') or key == ord('D'):
                # Toggle stats live? Maybe not useful while typing.
                # Let's ignore or flash message.
                continue

            # Character Input
            if 32 <= key <= 126: # Printable ASCII
                if not self.start_time:
                    self.start_time = time.time()
                
                self.user_input += chr(key)
                
                # Check completion
                if len(self.user_input) >= len(self.target_text):
                    # Auto finish if typed everything
                    self.finish_test()

    def finish_test(self):
        self.finished = True
        self.end_time = time.time()
        
        # Calc stats for saving
        elapsed = self.end_time - self.start_time
        chars_typed = len(self.user_input)
        wpm = calculate_wpm(chars_typed, elapsed)
        correct_count = sum(1 for i, c in enumerate(self.user_input) if i < len(self.target_text) and c == self.target_text[i])
        accuracy = int((correct_count / chars_typed) * 100) if chars_typed > 0 else 0
        
        self.save_score(wpm, accuracy)

def main_cli(stdscr, args):
    app = ScribereApp(stdscr, args)
    app.run()

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Scribere Typing Tutor")
    parser.add_argument("command", nargs="?", default="start", help="Command: start, config")
    parser.add_argument("mode", nargs="?", default="rand-25", help="Mode: rand-N, zen, quote, short, medium, long, longest, custom")
    parser.add_argument("--complex", action="store_true", help="Use complex word bank")
    
    # Parse known args to handle the "start" command gracefully
    args, unknown = parser.parse_known_args()
    
    # If user typed "start rand-25", args.command="start", args.mode="rand-25"
    # If user typed "rand-25" directly (some wrappers might do this), adjust
    if args.command != "start" and args.command in ["rand-25", "zen", "quote", "short", "medium", "long", "longest", "custom"]:
        args.mode = args.command
        args.command = "start"

    if args.command == "config":
        cfg = load_config()
        print(json.dumps(cfg, indent=2))
        sys.exit(0)
        
    if args.command == "start":
        # Pass mode explicitly
        class ModeArgs:
            def __init__(self, mode, complex_flag):
                self.mode = mode
                self.complex = complex_flag
                self.count = None
                self.length = None
                
                # Parse mode string for better internal handling if needed
                if mode.startswith("rand"):
                    parts = mode.split("-")
                    if len(parts) > 1:
                        try: self.count = int(parts[1])
                        except: pass
                elif mode in ["short", "medium", "long", "longest"]:
                    self.length = mode
                    
        m_args = ModeArgs(args.mode, args.complex)
        try:
            curses.wrapper(lambda stdscr: main_cli(stdscr, m_args))
        except KeyboardInterrupt:
            print("\nExited.")
            sys.exit(0)
    else:
        parser.print_help()
