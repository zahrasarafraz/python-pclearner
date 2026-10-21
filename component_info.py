# component_info.py
# This file only holds DATA (text about PC parts). No fancy logic here.
# A dictionary looks like:  {"key": value}  - we use it to store info by name.

COMPONENTS = {
    "CPU": {
        "emoji": "🧠",
        "title": "CPU (Processor)",
        "short": "The brain of the computer.",
        "analogy": "Think of the CPU as a chef in a kitchen. It reads the recipe "
                   "(your program) and does the steps one by one, very fast.",
        "look_for": [
            "Cores: more cores = more tasks at the same time",
            "Clock speed (GHz): how fast each core works",
            "Socket: it must match your motherboard",
        ],
        "fun_fact": "A 4 GHz CPU ticks about 4 billion times every second!",
    },
    "GPU": {
        "emoji": "🎮",
        "title": "GPU (Graphics Card)",
        "short": "Draws everything you see in games and videos.",
        "analogy": "If the CPU is one super chef, the GPU is a huge team of cooks "
                   "who each make a tiny part of the meal at the same time.",
        "look_for": [
            "VRAM: memory on the card (more helps with high resolution)",
            "Performance tier: check game benchmarks on YouTube",
            "Size and power: make sure it fits your case and PSU",
        ],
        "fun_fact": "GPUs were made for graphics, but today they also train AI models!",
    },
    "RAM": {
        "emoji": "⚡",
        "title": "RAM (Memory)",
        "short": "Short-term memory for programs that are open right now.",
        "analogy": "RAM is your desk. A bigger desk lets you keep more books "
                   "open at once, but it gets cleared when you leave (power off).",
        "look_for": [
            "Size: 16GB is a good start, 32GB is comfortable",
            "Type: DDR5 or DDR4 - must match your motherboard",
            "Speed: higher MHz is a bit faster",
        ],
        "fun_fact": "RAM forgets everything when the power is off. That's why you must save your work!",
    },
    "Motherboard": {
        "emoji": "🧩",
        "title": "Motherboard",
        "short": "The main board that connects every part together.",
        "analogy": "The motherboard is the city road map. Every part is a "
                   "building and the motherboard is the roads between them.",
        "look_for": [
            "Socket: must match your CPU",
            "RAM type: DDR4 or DDR5",
            "Extras: Wi-Fi, USB ports, extra SSD slots",
        ],
        "fun_fact": "Tiny copper lines called traces carry signals across the board.",
    },
    "Storage": {
        "emoji": "💾",
        "title": "Storage (SSD / HDD)",
        "short": "Where your files, games and Windows live permanently.",
        "analogy": "Storage is your bookshelf. Things stay there even when you "
                   "turn everything off.",
        "look_for": [
            "SSD is much faster than HDD (no moving parts)",
            "NVMe SSDs are the fastest type",
            "Size: 1TB is a good starting point for games",
        ],
        "fun_fact": "The first hard drives were the size of a fridge and stored only a few megabytes!",
    },
    "PSU": {
        "emoji": "🔌",
        "title": "PSU (Power Supply)",
        "short": "Turns wall power into the power your parts can use.",
        "analogy": "The PSU is the heart pumping energy (blood) to every part of the body.",
        "look_for": [
            "Watts: enough for your CPU and GPU with some extra room",
            "80+ rating (Bronze, Gold...): higher means less wasted energy",
            "Cables: make sure it has the connectors your GPU needs",
        ],
        "fun_fact": "A cheap, bad PSU can damage other parts. Never save money here!",
    },
    "Case": {
        "emoji": "🏠",
        "title": "Case",
        "short": "The box that holds and protects everything.",
        "analogy": "The case is the house. It needs windows (airflow) so the "
                   "parts inside don't get too hot.",
        "look_for": [
            "Airflow: mesh front panels keep parts cool",
            "Size: check that your GPU and motherboard fit",
            "Looks: glass side panels, RGB lights, colors",
        ],
        "fun_fact": "When parts get too hot they slow themselves down. This is called thermal throttling.",
    },
}


# Quiz questions: a LIST of dictionaries.
QUIZ = [
    {
        "question": "Which part is the 'brain' of the computer?",
        "options": ["GPU", "CPU", "PSU"],
        "answer": "CPU",
    },
    {
        "question": "What happens to data in RAM when you turn the PC off?",
        "options": ["It is saved forever", "It moves to the GPU", "It is erased"],
        "answer": "It is erased",
    },
    {
        "question": "Which part connects all the other parts together?",
        "options": ["Motherboard", "Case", "Storage"],
        "answer": "Motherboard",
    },
    {
        "question": "Which storage type is usually faster?",
        "options": ["HDD", "SSD", "They are the same"],
        "answer": "SSD",
    },
    {
        "question": "Which part gives power to the whole PC?",
        "options": ["RAM", "PSU", "CPU"],
        "answer": "PSU",
    },
]
