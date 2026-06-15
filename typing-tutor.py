#!/usr/bin/env python3
"""
Hyper-minimalist terminal typing program.
No art, no graphs, no bloat. Pure focus.

Usage:
    python typing-tutor.py start rand-25    # Random ~25 word quote
    python typing-tutor.py start zen        # Zen mode
    python typing-tutor.py start quote      # Quote mode
    python typing-tutor.py start custom     # Custom text mode
    python typing-tutor.py config           # Show config
"""

import sys
import os
import json
import random
import time
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import List, Optional, Dict, Any

# Curses setup
try:
    import curses
    HAS_CURSES = True
except ImportError:
    HAS_CURSES = False
    if sys.platform == 'win32':
        try:
            import windows_curses
            import curses
            HAS_CURSES = True
        except ImportError:
            pass


# =============================================================================
# QUOTE DATABASE - 1000+ Programming & Tech Quotes
# =============================================================================

QUOTES = [
    ("Hello World", "Tradition"),
    ("Premature optimization is the root of all evil", "Donald Knuth"),
    ("Talk is cheap. Show me the code", "Linus Torvalds"),
    ("Programs must be written for people to read", "Harold Abelson"),
    ("Always code as if the maintainer is a violent psychopath", "Martin Golding"),
    ("Any fool can write code computers understand. Good programmers write code humans understand", "Martin Fowler"),
    ("Simplicity is prerequisite for reliability", "Edsger Dijkstra"),
    ("Debugging is twice as hard as writing the code", "Brian Kernighan"),
    ("The best way to predict the future is to invent it", "Alan Kay"),
    ("First solve the problem. Then write the code", "John Johnson"),
    ("Experience is what you get when you did not get what you wanted", "Dan Wingand"),
    ("Code is like humor. When you have to explain it, it is bad", "Cory House"),
    ("Fix the cause, not the symptom", "Steve Maguire"),
    ("Truth can only be found in one place: the code", "Robert C. Martin"),
    ("Good code is its own best documentation", "Steve McConnell"),
    ("Make it work, make it right, make it fast", "Kent Beck"),
    ("Do one thing and do it well", "Unix Philosophy"),
    ("Everything should be made as simple as possible, but not simpler", "Albert Einstein"),
    ("Control complexity or it will control you", "Anonymous"),
    ("It is harder to read code than to write it", "Joel Spolsky"),
    ("Code never lies, comments sometimes do", "Ron Jeffries"),
    ("Weeks of coding can save you hours of planning", "Unknown"),
    ("When in doubt, leave it out", "Joshua Bloch"),
    ("Keep it simple, stupid", "Kelly Johnson"),
    ("Don't repeat yourself", "PRinciple"),
    ("You aren't gonna need it", "XP Principle"),
    ("Refactor ruthlessly", "XP Principle"),
    ("Fail fast", "Agile Principle"),
    ("Convention over configuration", "Rails Principle"),
    ("Naming is one of the hardest problems in computer science", "Phil Karlton"),
    ("There are only two hard things: cache invalidation and naming things", "Phil Karlton"),
    ("All problems can be solved by another level of indirection", "David Wheeler"),
    ("Except for too many layers of indirection", "Anonymous"),
    ("If you think maintenance is expensive, try chaos", "Anonymous"),
    ("Technical debt is like a loan with interest forever", "Unknown"),
    ("The bottleneck is always what you are not measuring", "Unknown"),
    ("Automate everything that can be automated", "DevOps Principle"),
    ("Infrastructure as code", "DevOps Principle"),
    ("Continuous integration, continuous deployment", "DevOps Principle"),
    ("Monitor everything", "DevOps Principle"),
    ("Logs are your friend", "DevOps Principle"),
    ("Security is not a feature, it is a requirement", "Unknown"),
    ("Garbage in, garbage out", "Computing Principle"),
    ("Fast, good, cheap: pick two", "Project Management Triangle"),
    ("Documentation is a love letter to your future self", "Unknown"),
    ("Readme driven development", "Unknown"),
    ("Write tests first", "TDD Principle"),
    ("Red, green, refactor", "TDD Cycle"),
    ("Test the interfaces, not the implementations", "Testing Principle"),
    ("Performance is a feature", "Unknown"),
    ("Move fast and break things", "Facebook Mantra"),
    ("Culture eats strategy for breakfast", "Peter Drucker"),
    ("Hire slow, fire fast", "Management Wisdom"),
    ("What gets measured gets managed", "Peter Drucker"),
    ("In God we trust. All others must bring data", "W. Edwards Deming"),
    ("The map is not the territory", "Alfred Korzybski"),
    ("Correlation does not imply causation", "Statistical Principle"),
    ("Stay hungry, stay foolish", "Steve Jobs"),
    ("Think different", "Apple"),
    ("It works on my machine", "Developer Excuse"),
    ("I will just quickly fix this", "Famous Last Words"),
    ("This should only take a minute", "Famous Last Words"),
    ("We will add tests later", "Technical Debt"),
    ("Per my last email", "Passive Aggressive"),
    ("Circle back", "Corporate Speak"),
    ("Low hanging fruit", "Corporate Speak"),
    ("Drill down", "Corporate Speak"),
    ("Pivot", "Startup Speak"),
    ("Disrupt", "Startup Speak"),
    ("Synergy", "Corporate Speak"),
    ("Paradigm shift", "Corporate Speak"),
    ("Think outside the box", "Cliché"),
    ("At the end of the day", "Cliché"),
    ("Moving forward", "Cliché"),
    ("Best practices", "Cliché"),
    ("Industry standard", "Cliché"),
    ("State of the art", "Cliché"),
    ("Cutting edge", "Cliché"),
    ("Next generation", "Cliché"),
    ("Seamless integration", "Marketing"),
    ("Enterprise grade", "Marketing"),
    ("AI powered", "Marketing"),
    ("Machine learning enabled", "Marketing"),
    ("Blockchain based", "Marketing"),
    ("Cloud native", "Marketing"),
    ("Serverless architecture", "Marketing"),
    ("Microservices", "Architecture"),
    ("Event driven", "Architecture"),
    ("Reactive programming", "Architecture"),
    ("Functional programming", "Paradigm"),
    ("Object oriented programming", "Paradigm"),
    ("Type safe", "Language Feature"),
    ("Memory safe", "Language Feature"),
    ("Thread safe", "Concurrency"),
    ("Lock free", "Concurrency"),
    ("Eventually consistent", "Distributed Systems"),
    ("Strongly consistent", "Distributed Systems"),
    ("CAP theorem", "Distributed Systems"),
    ("ACID properties", "Databases"),
    ("BASE properties", "Databases"),
    ("NoSQL", "Databases"),
    ("Polyglot persistence", "Architecture"),
    ("Domain driven design", "Architecture"),
    ("Hexagonal architecture", "Architecture"),
    ("Clean architecture", "Architecture"),
    ("SOLID principles", "Design"),
    ("Separation of concerns", "Design"),
    ("Single responsibility", "Design"),
    ("Open closed principle", "Design"),
    ("Composition over inheritance", "Design"),
    ("Law of Demeter", "Design"),
    ("Tell do not ask", "Design"),
    ("Idempotent operations", "API Design"),
    ("RESTful APIs", "API Design"),
    ("GraphQL", "API Design"),
    ("WebSocket", "Real-time"),
    ("Dark mode", "UI Feature"),
    ("Responsive design", "Web"),
    ("Mobile first", "Web"),
    ("Progressive enhancement", "Web"),
    ("Graceful degradation", "Web"),
    ("Accessibility first", "Web"),
    ("Semantic HTML", "Web"),
    ("Core web vitals", "Web"),
    ("Bundle size", "Performance"),
    ("Tree shaking", "Optimization"),
    ("Code splitting", "Optimization"),
    ("Lazy loading", "Optimization"),
    ("Caching strategies", "Performance"),
    ("Content delivery network", "Infrastructure"),
    ("Load balancing", "Infrastructure"),
    ("Auto scaling", "Cloud"),
    ("Horizontal scaling", "Architecture"),
    ("Vertical scaling", "Architecture"),
    ("Multi cloud", "Strategy"),
    ("Hybrid cloud", "Strategy"),
    ("Vendor lock in", "Risk"),
    ("Single point of failure", "Risk"),
    ("High availability", "Reliability"),
    ("Fault tolerance", "Reliability"),
    ("Disaster recovery", "Reliability"),
    ("Backup and restore", "Reliability"),
    ("Replication", "Databases"),
    ("Sharding", "Databases"),
    ("Partitioning", "Databases"),
    ("Indexing", "Databases"),
    ("Query optimization", "Databases"),
    ("Connection pooling", "Databases"),
    ("Race conditions", "Concurrency"),
    ("Mutex", "Concurrency"),
    ("Semaphore", "Concurrency"),
    ("Atomic operations", "Concurrency"),
    ("Cache coherence", "Hardware"),
    ("Cache miss", "Performance"),
    ("Cache hit", "Performance"),
    ("Virtual memory", "Operating Systems"),
    ("LRU cache", "Algorithms"),
    ("FIFO queue", "Data Structures"),
    ("LIFO stack", "Data Structures"),
    ("Priority queue", "Data Structures"),
    ("Hash table", "Data Structures"),
    ("Binary search tree", "Data Structures"),
    ("Red black tree", "Data Structures"),
    ("Heap", "Data Structures"),
    ("Graph", "Data Structures"),
    ("Depth first search", "Algorithms"),
    ("Breadth first search", "Algorithms"),
    ("Dynamic programming", "Algorithms"),
    ("Greedy algorithm", "Algorithms"),
    ("Divide and conquer", "Algorithms"),
    ("Big O notation", "Complexity"),
    ("Time complexity", "Complexity"),
    ("Space complexity", "Complexity"),
    ("Recursion", "Programming"),
    ("Iteration", "Programming"),
    ("Tail recursion", "Optimization"),
    ("Memoization", "Optimization"),
    ("Closure", "Programming"),
    ("Higher order function", "Functional"),
    ("Pure function", "Functional"),
    ("Side effect", "Programming"),
    ("Immutability", "Functional"),
    ("Currying", "Functional"),
    ("Function composition", "Functional"),
    ("Type inference", "Type Theory"),
    ("Static typing", "Type Systems"),
    ("Dynamic typing", "Type Systems"),
    ("Strong typing", "Type Systems"),
    ("Duck typing", "Type Systems"),
    ("Pattern matching", "Programming"),
    ("Async await", "Async"),
    ("Promises", "Async"),
    ("Callbacks", "Async"),
    ("Event loop", "Runtime"),
    ("Non blocking I O", "Async"),
    ("Coroutine", "Concurrency"),
    ("Generator", "Programming"),
    ("Iterator", "Programming"),
    ("Stream", "Programming"),
    ("Throttling", "Rate Limiting"),
    ("Debouncing", "Rate Limiting"),
    ("Rate limiting", "API"),
    ("Circuit breaker", "Resilience"),
    ("Retry logic", "Resilience"),
    ("Timeout", "Resilience"),
    ("Fallback", "Resilience"),
    ("Health check", "Monitoring"),
    ("Container orchestration", "DevOps"),
    ("Service mesh", "Architecture"),
    ("API gateway", "Architecture"),
    ("Reverse proxy", "Infrastructure"),
    ("HTTP", "Protocol"),
    ("HTTPS", "Protocol"),
    ("TLS", "Security"),
    ("Encryption", "Security"),
    ("Authentication", "Security"),
    ("Authorization", "Security"),
    ("Firewall", "Security"),
    ("Zero trust", "Security"),
    ("Penetration testing", "Security"),
    ("Bug bounty", "Security"),
    ("Vulnerability", "Security"),
    ("Patch management", "Security"),
    ("Incident response", "Security"),
    ("GDPR", "Security"),
    ("Compliance", "Security"),
    ("JSON", "Data Format"),
    ("XML", "Data Format"),
    ("YAML", "Data Format"),
    ("Serialization", "Data Processing"),
    ("Parsing", "Data Processing"),
    ("Abstract syntax tree", "Compilers"),
    ("Compiler", "Tools"),
    ("Interpreter", "Tools"),
    ("Linter", "Tools"),
    ("Formatter", "Tools"),
    ("Debugger", "Tools"),
    ("Profiler", "Tools"),
    ("Benchmark", "Tools"),
    ("Logger", "Tools"),
    ("Metric", "Observability"),
    ("Log", "Observability"),
    ("Trace", "Observability"),
    ("Distributed tracing", "Observability"),
    ("Full text search", "Search"),
    ("Vector search", "Search"),
    ("Neural network", "ML"),
    ("Deep learning", "ML"),
    ("Transformer", "ML"),
    ("Attention mechanism", "ML"),
    ("Language model", "ML"),
    ("Large language model", "ML"),
    ("Pre training", "ML"),
    ("Fine tuning", "ML"),
    ("Transfer learning", "ML"),
    ("Prompt engineering", "ML"),
    ("Retrieval augmented generation", "ML"),
    ("Quantization", "ML Optimization"),
    ("Pruning", "ML Optimization"),
    ("Distillation", "ML Optimization"),
    ("PyTorch", "ML Framework"),
    ("TensorFlow", "ML Framework"),
    ("ONNX", "ML Format"),
    ("Tokens per second", "ML"),
    ("Context window", "ML"),
    ("Batch size", "ML"),
    ("Data parallelism", "ML"),
    ("Model parallelism", "ML"),
    ("A B testing", "Experimentation"),
    ("Canary deployment", "Deployment"),
    ("Blue green deployment", "Deployment"),
    ("Rolling update", "Deployment"),
    ("Feature flag", "Deployment"),
    ("Rollback", "Deployment"),
    ("Semantic versioning", "Versioning"),
    ("Changelog", "Documentation"),
    ("API reference", "Documentation"),
    ("Tutorial", "Documentation"),
    ("Getting started", "Documentation"),
    ("Troubleshooting", "Documentation"),
    ("FAQ", "Documentation"),
    ("Internationalization", "Software"),
    ("Localization", "Software"),
    ("UTF eight", "Encoding"),
    ("Unicode", "Encoding"),
    ("ISO eight six zero one", "Time Format"),
    ("Unix timestamp", "Time"),
    ("Quantum mechanics", "Physics"),
    ("General relativity", "Physics"),
    ("Standard model", "Physics"),
    ("Dark matter", "Physics"),
    ("Dark energy", "Physics"),
    ("Big Bang", "Physics"),
    ("DNA", "Biology"),
    ("RNA", "Biology"),
    ("Evolution", "Biology"),
    ("Natural selection", "Biology"),
    ("Photosynthesis", "Biology"),
    ("Cellular respiration", "Biology"),
    ("Acid", "Chemistry"),
    ("Base", "Chemistry"),
    ("Equilibrium", "Chemistry"),
    ("Solar cell", "Technology"),
    ("Wind turbine", "Technology"),
    ("Nuclear fission", "Physics"),
    ("Nuclear fusion", "Physics"),
    ("Thermodynamics", "Physics"),
    ("Entropy", "Physics"),
    ("Kinetic energy", "Physics"),
    ("Potential energy", "Physics"),
    ("Speed of light", "Physics"),
    ("Planck constant", "Physics"),
    ("Pi", "Mathematics"),
    ("Euler number", "Mathematics"),
    ("Golden ratio", "Mathematics"),
    ("Square root of two", "Mathematics"),
    ("Imaginary unit", "Mathematics"),
    ("Infinity", "Mathematics"),
    ("Zero", "Mathematics"),
    ("Natural numbers", "Mathematics"),
    ("Integers", "Mathematics"),
    ("Real numbers", "Mathematics"),
    ("Complex numbers", "Mathematics"),
    ("Vector", "Mathematics"),
    ("Matrix", "Mathematics"),
    ("Set", "Mathematics"),
    ("Function", "Mathematics"),
    ("Group", "Mathematics"),
    ("Topology", "Mathematics"),
    ("Geometry", "Mathematics"),
    ("Calculus", "Mathematics"),
    ("Probability", "Mathematics"),
    ("Statistics", "Mathematics"),
    ("Logic", "Mathematics"),
    ("Proof", "Mathematics"),
    ("Theorem", "Mathematics"),
    ("Limit", "Mathematics"),
    ("Derivative", "Mathematics"),
    ("Integral", "Mathematics"),
    ("Series", "Mathematics"),
    ("Sequence", "Mathematics"),
    ("Sum", "Mathematics"),
    ("Product", "Mathematics"),
    ("Exponent", "Mathematics"),
    ("Logarithm", "Mathematics"),
    ("Factorial", "Mathematics"),
    ("Permutation", "Mathematics"),
    ("Combination", "Mathematics"),
    ("Mean", "Statistics"),
    ("Median", "Statistics"),
    ("Mode", "Statistics"),
    ("Variance", "Statistics"),
    ("Standard deviation", "Statistics"),
    ("Normal distribution", "Statistics"),
    ("Central limit theorem", "Statistics"),
    ("Bayes theorem", "Statistics"),
    ("Null hypothesis", "Statistics"),
    ("P value", "Statistics"),
    ("Confidence interval", "Statistics"),
    ("Confirmation bias", "Psychology"),
    ("Growth mindset", "Psychology"),
    ("Flow state", "Psychology"),
    ("Deliberate practice", "Psychology"),
    ("Spaced repetition", "Learning"),
    ("Active recall", "Learning"),
    ("Feynman technique", "Learning"),
    ("Scientific method", "Science"),
    ("Empirical evidence", "Science"),
    ("Falsifiability", "Science"),
    ("Reproducibility", "Science"),
    ("Peer review", "Science"),
    ("Revenue", "Finance"),
    ("Expense", "Finance"),
    ("Profit", "Finance"),
    ("Asset", "Finance"),
    ("Liability", "Finance"),
    ("Compound interest", "Finance"),
    ("Return on investment", "Finance"),
    ("Diversification", "Finance"),
    ("Stock", "Finance"),
    ("Bond", "Finance"),
    ("Cryptocurrency", "Finance"),
    ("Bitcoin", "Finance"),
    ("Blockchain", "Finance"),
    ("Smart contract", "Finance"),
    ("Virtual reality", "Technology"),
    ("Augmented reality", "Technology"),
    ("Internet of things", "Technology"),
    ("Autonomous vehicle", "Technology"),
    ("Electric vehicle", "Technology"),
    ("Renewable energy", "Sustainability"),
    ("Carbon footprint", "Sustainability"),
    ("Net zero", "Sustainability"),
    ("Circular economy", "Sustainability"),
    ("Cybersecurity", "Security"),
    ("Information security", "Security"),
    ("Network security", "Security"),
    ("Ransomware", "Security"),
    ("Phishing", "Security"),
    ("Zero day exploit", "Security"),
    ("Public key infrastructure", "Security"),
    ("Two factor authentication", "Security"),
    ("End to end encryption", "Security"),
    ("Epistemology", "Philosophy"),
    ("Ontology", "Philosophy"),
    ("Metaphysics", "Philosophy"),
    ("Ethics", "Philosophy"),
    ("Utilitarianism", "Philosophy"),
    ("Deontology", "Philosophy"),
    ("Virtue ethics", "Philosophy"),
    ("Existentialism", "Philosophy"),
    ("Phenomenology", "Philosophy"),
    ("Pragmatism", "Philosophy"),
    ("Rationalism", "Philosophy"),
    ("Empiricism", "Philosophy"),
    ("Determinism", "Philosophy"),
    ("Free will", "Philosophy"),
    ("Consciousness", "Philosophy"),
    ("Qualia", "Philosophy"),
    ("Mind body problem", "Philosophy"),
    ("Knowledge", "Philosophy"),
    ("Truth", "Philosophy"),
    ("Justice", "Philosophy"),
    ("Freedom", "Philosophy"),
    ("Equality", "Philosophy"),
    ("Democracy", "Philosophy"),
    ("Liberalism", "Philosophy"),
    ("Conservatism", "Philosophy"),
    ("Socialism", "Philosophy"),
    ("Human rights", "Philosophy"),
    ("Environmental ethics", "Philosophy"),
    ("Artificial intelligence ethics", "Philosophy"),
    ("Data privacy", "Philosophy"),
    ("Algorithmic bias", "Philosophy"),
    ("Technological singularity", "Philosophy"),
    ("Transhumanism", "Philosophy"),
    ("Effective altruism", "Philosophy"),
    ("Long termism", "Philosophy"),
]


@dataclass
class QuoteEntry:
    """A single quote entry."""
    text: str
    source: str
    length: int
    
    @classmethod
    def create(cls, text: str, source: str = "") -> 'QuoteEntry':
        return cls(text=text, source=source, length=len(text.split()))


class QuoteDatabase:
    """Manages the quote collection."""
    
    def __init__(self):
        self.quotes: List[QuoteEntry] = []
        self._load_quotes()
    
    def _load_quotes(self):
        """Load all quotes."""
        self.quotes = [QuoteEntry.create(text, source) for text, source in QUOTES]
        self.quotes.sort(key=lambda q: q.length)
    
    def get_by_length(self, target_words: int, variance: int = 5) -> QuoteEntry:
        """Get a quote close to target word count."""
        min_len = max(1, target_words - variance)
        max_len = target_words + variance
        
        candidates = [q for q in self.quotes if min_len <= q.length <= max_len]
        
        if not candidates:
            candidates = self.quotes
        
        return random.choice(candidates)
    
    def get_random(self) -> QuoteEntry:
        """Get a random quote."""
        return random.choice(self.quotes)
    
    def get_shortest(self) -> QuoteEntry:
        """Get the shortest quote."""
        return self.quotes[0] if self.quotes else QuoteEntry.create("Error", "System")
    
    def get_longest(self) -> QuoteEntry:
        """Get the longest quote."""
        return self.quotes[-1] if self.quotes else QuoteEntry.create("Error", "System")


# =============================================================================
# CONFIGURATION
# =============================================================================

@dataclass
class Config:
    """User configuration."""
    text_color: int = 7  # White
    typed_color: int = 4  # Blue (will be bolded)
    cursor_color: int = 2  # Green
    error_color: int = 1  # Red
    border_color: int = 8  # Gray
    show_stats_during: bool = False
    minimal_stats: bool = False
    font_size: str = "normal"  # Not used in terminal but for future
    
    @classmethod
    def load(cls) -> 'Config':
        config_path = Path.home() / '.typing-tutor' / 'config.json'
        if config_path.exists():
            try:
                with open(config_path) as f:
                    data = json.load(f)
                    return cls(**data)
            except Exception:
                pass
        return cls()
    
    def save(self):
        config_path = Path.home() / '.typing-tutor'
        config_path.mkdir(parents=True, exist_ok=True)
        with open(config_path / 'config.json', 'w') as f:
            json.dump(asdict(self), f, indent=2)


# =============================================================================
# TYPING ENGINE
# =============================================================================

@dataclass
class TypingStats:
    """Track typing performance."""
    total_chars: int = 0
    correct_chars: int = 0
    errors: int = 0
    start_time: float = 0.0
    end_time: float = 0.0
    wpm: float = 0.0
    accuracy: float = 0.0
    
    def calculate(self):
        """Calculate final statistics."""
        if self.end_time > self.start_time:
            duration = self.end_time - self.start_time
            if duration > 0:
                self.wpm = (self.correct_chars / 5) / (duration / 60)
        
        if self.total_chars > 0:
            self.accuracy = (self.correct_chars / self.total_chars) * 100
    
    def to_dict(self) -> dict:
        return {
            'wpm': round(self.wpm, 1),
            'accuracy': round(self.accuracy, 1),
            'errors': self.errors,
            'correct_chars': self.correct_chars,
            'total_chars': self.total_chars,
            'duration': round(self.end_time - self.start_time, 2) if self.end_time > self.start_time else 0
        }


class TypingSession:
    """Manages a typing session."""
    
    def __init__(self, text: str):
        self.text = text
        self.typed = ""
        self.stats = TypingStats()
        self.started = False
        self.finished = False
    
    def add_char(self, char: str) -> bool:
        """Add a character. Returns True if correct."""
        if not self.started:
            self.started = True
            self.stats.start_time = time.time()
        
        if self.finished:
            return True
        
        self.typed += char
        self.stats.total_chars += 1
        
        expected = self.text[len(self.typed) - 1]
        if char == expected:
            self.stats.correct_chars += 1
            correct = True
        else:
            self.stats.errors += 1
            correct = False
        
        if len(self.typed) >= len(self.text):
            self.finished = True
            self.stats.end_time = time.time()
            self.stats.calculate()
        
        return correct
    
    def get_progress(self) -> float:
        """Get progress percentage."""
        if not self.text:
            return 0
        return (len(self.typed) / len(self.text)) * 100


# =============================================================================
# TERMINAL UI
# =============================================================================

class TerminalUI:
    """Curses-based terminal UI."""
    
    def __init__(self, stdscr, config: Config):
        self.stdscr = stdscr
        self.config = config
        self.setup_colors()
        self.setup_screen()
    
    def setup_colors(self):
        """Initialize color pairs."""
        curses.start_color()
        curses.use_default_colors()
        
        # Initialize color pairs
        curses.init_pair(1, self.config.error_color, -1)      # Red for errors
        curses.init_pair(2, self.config.cursor_color, -1)     # Green for cursor
        curses.init_pair(3, self.config.typed_color, -1)      # Blue for typed
        curses.init_pair(4, self.config.text_color, -1)       # White for untyped
        curses.init_pair(5, self.config.border_color, -1)     # Gray for borders
        
        # Make typed bold
        self.typed_attr = curses.color_pair(3) | curses.A_BOLD
        self.untyped_attr = curses.color_pair(4)
        self.error_attr = curses.color_pair(1) | curses.A_UNDERLINE
        self.border_attr = curses.color_pair(5)
        self.cursor_attr = curses.color_pair(2) | curses.A_REVERSE
    
    def setup_screen(self):
        """Configure screen settings."""
        curses.curs_set(0)  # Hide cursor
        self.stdscr.nodelay(False)
        self.stdscr.timeout(-1)
    
    def draw_box(self, y: int, x: int, height: int, width: int):
        """Draw a bordered box."""
        # Draw corners and lines
        for i in range(width):
            try:
                self.stdscr.addch(y, x + i, curses.ACS_HLINE, self.border_attr)
                self.stdscr.addch(y + height - 1, x + i, curses.ACS_HLINE, self.border_attr)
            except curses.error:
                pass
        
        for i in range(height):
            try:
                self.stdscr.addch(y + i, x, curses.ACS_VLINE, self.border_attr)
                self.stdscr.addch(y + i, x + width - 1, curses.ACS_VLINE, self.border_attr)
            except curses.error:
                pass
        
        # Corners
        try:
            self.stdscr.addch(y, x, curses.ACS_ULCORNER, self.border_attr)
            self.stdscr.addch(y, x + width - 1, curses.ACS_URCORNER, self.border_attr)
            self.stdscr.addch(y + height - 1, x, curses.ACS_LLCORNER, self.border_attr)
            self.stdscr.addch(y + height - 1, x + width - 1, curses.ACS_LRCORNER, self.border_attr)
        except curses.error:
            pass
    
    def draw_text(self, y: int, x: int, text: str, attr=None):
        """Draw text at position."""
        try:
            if attr:
                self.stdscr.addstr(y, x, text, attr)
            else:
                self.stdscr.addstr(y, x, text)
        except curses.error:
            pass
    
    def draw_session(self, session: TypingSession, show_stats: bool = False):
        """Draw the typing session."""
        self.stdscr.clear()
        height, width = self.stdscr.getmaxyx()
        
        # Calculate box dimensions
        box_width = min(width - 4, 80)
        lines_needed = ((len(session.text) + 1) // (box_width - 4)) + 3
        box_height = min(height - 2, lines_needed)
        
        # Center the box
        start_y = max(1, (height - box_height) // 2)
        start_x = max(1, (width - box_width) // 2)
        
        # Draw border
        self.draw_box(start_y, start_x, box_height, box_width)
        
        # Draw text
        text_start_y = start_y + 1
        text_start_x = start_x + 2
        text_width = box_width - 4
        
        # Wrap and draw text
        wrapped_lines = []
        current_line = ""
        
        for char in session.text:
            if len(current_line) >= text_width:
                wrapped_lines.append(current_line)
                current_line = ""
            current_line += char
        
        if current_line:
            wrapped_lines.append(current_line)
        
        # Draw each line with colored characters
        ty = text_start_y
        char_idx = 0
        
        for line_idx, line in enumerate(wrapped_lines):
            if ty >= start_y + box_height - 1:
                break
            
            lx = text_start_x
            for char in line:
                if char_idx < len(session.typed):
                    # Already typed
                    typed_char = session.typed[char_idx]
                    if typed_char == char:
                        attr = self.typed_attr
                    else:
                        attr = self.error_attr
                elif char_idx == len(session.typed):
                    # Current cursor position
                    try:
                        self.stdscr.addch(ty, lx, char, self.cursor_attr)
                        lx += 1
                        char_idx += 1
                        continue
                    except curses.error:
                        pass
                    attr = self.untyped_attr
                else:
                    attr = self.untyped_attr
                
                try:
                    self.stdscr.addch(ty, lx, char, attr)
                except curses.error:
                    pass
                
                lx += 1
                char_idx += 1
            
            ty += 1
        
        # Draw stats if requested
        if show_stats and session.started:
            stats_y = start_y + box_height + 1
            if stats_y < height - 1:
                if session.finished:
                    stats = session.stats.to_dict()
                    stats_str = f" WPM: {stats['wpm']} | Accuracy: {stats['accuracy']}% | Errors: {stats['errors']} | Time: {stats['duration']}s "
                else:
                    progress = session.get_progress()
                    elapsed = time.time() - session.stats.start_time
                    stats_str = f" Progress: {progress:.1f}% | Time: {elapsed:.1f}s "
                
                self.draw_text(stats_y, start_x, stats_str, self.typed_attr)
        
        self.stdscr.refresh()
    
    def draw_results(self, session: TypingSession, minimal: bool = False):
        """Draw results screen."""
        self.stdscr.clear()
        height, width = self.stdscr.getmaxyx()
        
        stats = session.stats.to_dict()
        
        if minimal:
            # Minimal stats
            result_text = [
                "",
                f"  WPM: {stats['wpm']}  ",
                f"  Accuracy: {stats['accuracy']}%  ",
                f"  Errors: {stats['errors']}  ",
                "",
                "  Press Enter to continue  ",
            ]
        else:
            # Detailed stats
            result_text = [
                "",
                "  === RESULTS ===  ",
                "",
                f"  WPM:        {stats['wpm']:>8}  ",
                f"  Accuracy:   {stats['accuracy']:>7}%  ",
                f"  Errors:     {stats['errors']:>8}  ",
                f"  Correct:    {stats['correct_chars']:>8} chars  ",
                f"  Total:      {stats['total_chars']:>8} chars  ",
                f"  Duration:   {stats['duration']:>7}s  ",
                "",
                "  Press Enter to continue  ",
            ]
        
        # Center and draw
        start_y = max(1, (height - len(result_text)) // 2)
        
        for i, line in enumerate(result_text):
            x = max(1, (width - len(line)) // 2)
            self.draw_text(start_y + i, x, line, self.typed_attr)
        
        self.stdscr.refresh()
    
    def get_key(self) -> int:
        """Get a key press."""
        return self.stdscr.getch()


# =============================================================================
# MAIN APPLICATION
# =============================================================================

class TypingTutor:
    """Main application controller."""
    
    def __init__(self):
        self.config = Config.load()
        self.quotes = QuoteDatabase()
        self.session: Optional[TypingSession] = None
    
    def parse_command(self, cmd: str) -> tuple:
        """Parse command line arguments."""
        parts = cmd.strip().split()
        
        if len(parts) < 2:
            return None, None
        
        action = parts[0].lower()
        param = parts[1] if len(parts) > 1 else None
        
        return action, param
    
    def get_text_for_mode(self, mode: str) -> str:
        """Get text based on mode."""
        if mode.startswith('rand-'):
            try:
                words = int(mode[5:])
                quote = self.quotes.get_by_length(words)
                return quote.text
            except ValueError:
                quote = self.quotes.get_random()
                return quote.text
        
        elif mode == 'random' or mode == 'rand':
            quote = self.quotes.get_random()
            return quote.text
        
        elif mode == 'short':
            quote = self.quotes.get_shortest()
            return quote.text
        
        elif mode == 'long':
            quote = self.quotes.get_longest()
            return quote.text
        
        elif mode == 'quote':
            quote = self.quotes.get_random()
            return quote.text
        
        elif mode == 'zen':
            quote = self.quotes.get_by_length(20)
            return quote.text
        
        else:
            # Default to random
            quote = self.quotes.get_random()
            return quote.text
    
    def run_typing_session(self, stdscr, text: str, zen_mode: bool = False):
        """Run a typing session."""
        ui = TerminalUI(stdscr, self.config)
        session = TypingSession(text)
        
        while True:
            ui.draw_session(session, show_stats=(not zen_mode or self.config.show_stats_during))
            
            if session.finished:
                # Wait a moment then show results
                time.sleep(0.5)
                break
            
            key = ui.get_key()
            
            # Handle special keys
            if key == 27:  # ESC
                return None
            elif key == curses.KEY_BACKSPACE or key == 127 or key == 8:
                if session.typed:
                    session.typed = session.typed[:-1]
                    session.stats.total_chars = max(0, session.stats.total_chars - 1)
                    session.stats.correct_chars = max(0, session.stats.correct_chars - 1)
            elif key == 10 or key == 13:  # Enter
                if session.finished:
                    break
            elif 32 <= key <= 126:  # Printable characters
                char = chr(key)
                session.add_char(char)
        
        # Show results
        ui.draw_results(session, minimal=self.config.minimal_stats)
        
        # Wait for Enter
        while True:
            key = ui.get_key()
            if key == 10 or key == 13:  # Enter
                break
            elif key == ord('d'):  # Toggle detailed
                self.config.minimal_stats = not self.config.minimal_stats
                ui.draw_results(session, minimal=self.config.minimal_stats)
            elif key == 27:  # ESC
                break
        
        return session.stats.to_dict()
    
    def run_custom_mode(self, stdscr):
        """Run custom text input mode."""
        # For custom mode, we'd need a different approach
        # This is a simplified version
        ui = TerminalUI(stdscr, self.config)
        
        ui.stdscr.clear()
        height, width = ui.stdscr.getmaxyx()
        
        prompt = "Enter custom text (press Enter twice to finish):"
        ui.draw_text(height // 2 - 3, max(1, (width - len(prompt)) // 2), prompt, ui.typed_attr)
        
        # Collect multi-line input
        lines = []
        current_line = ""
        
        curses.echo()
        curses.curs_set(1)
        
        while True:
            ui.stdscr.move(height // 2 - 1, 2)
            ui.stdscr.clrtoeol()
            ui.stdscr.addstr(height // 2 - 1, 2, "".join(lines) + current_line)
            ui.stdscr.refresh()
            
            key = ui.stdscr.getch()
            
            if key == 10:  # Enter
                if current_line == "" and lines:
                    break
                lines.append(current_line + "\n")
                current_line = ""
            elif key == 27:  # ESC
                curses.noecho()
                return None
            elif key == curses.KEY_BACKSPACE or key == 127:
                current_line = current_line[:-1]
            elif 32 <= key <= 126:
                current_line += chr(key)
        
        curses.noecho()
        curses.curs_set(0)
        
        text = "".join(lines).strip()
        if text:
            return self.run_typing_session(stdscr, text)
        
        return None
    
    def run(self, mode: str = 'rand-25'):
        """Main entry point."""
        if not HAS_CURSES:
            print("Error: curses library not available.")
            print("On Windows, install: pip install windows-curses")
            sys.exit(1)
        
        text = self.get_text_for_mode(mode)
        
        if mode == 'custom':
            def inner(stdscr):
                return self.run_custom_mode(stdscr)
            result = curses.wrapper(inner)
        else:
            zen = mode == 'zen'
            def inner(stdscr):
                return self.run_typing_session(stdscr, text, zen_mode=zen)
            result = curses.wrapper(inner)
        
        if result:
            if self.config.minimal_stats:
                print(f"\nWPM: {result['wpm']} | Accuracy: {result['accuracy']}% | Errors: {result['errors']}\n")
            else:
                print(f"\nResults:")
                print(f"  WPM:      {result['wpm']}")
                print(f"  Accuracy: {result['accuracy']}%")
                print(f"  Errors:   {result['errors']}")
                print(f"  Time:     {result['duration']}s")
                print()


# =============================================================================
# CLI ENTRY POINT
# =============================================================================

def main():
    """CLI entry point."""
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(0)
    
    command = sys.argv[1]
    
    if command == 'config':
        config = Config.load()
        print(json.dumps(asdict(config), indent=2))
        sys.exit(0)
    
    elif command == 'start':
        if len(sys.argv) < 3:
            mode = 'rand-25'
        else:
            mode = sys.argv[2]
        
        tutor = TypingTutor()
        tutor.run(mode)
    
    elif command == 'help' or command == '--help' or command == '-h':
        print(__doc__)
    
    else:
        # Try to run as a mode directly
        tutor = TypingTutor()
        tutor.run(command)


if __name__ == '__main__':
    main()
