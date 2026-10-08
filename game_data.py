LEVELS = {
    1: {
        "title": "Level 1: The Midnight Gallery Heist",
        "story": "A priceless diamond ring was stolen from the art gallery right around midnight.",
        "clues": [
            {
                "id": "c1",
                "name": "Footprints",
                "desc": "Size 9 muddy shoe prints found near the gallery window."
            },
            {
                "id": "c2",
                "name": "Torn Fabric",
                "desc": "A piece of torn black silk fabric snagged on the back door handle."
            },
            {
                "id": "c3",
                "name": "Security Log",
                "desc": "The security camera for the back entrance was turned off at 11:45 PM."
            }
        ],
        "suspects": {
            "vikram": {
                "name": "Vikram (Security Guard)",
                "role": "Night Security",
                "personality": "Nervous and jumpy, but completely honest about his rounds.",
                "secret": "He fell asleep on duty, but he did not steal anything."
            },
            "anita": {
                "name": "Anita (Curator)",
                "role": "Art Expert",
                "personality": "Calm, polite, and speaks in a very refined, professional tone.",
                "secret": "The true culprit. She was wearing a black silk dress and holds the key to the back door."
            },
            "rahul": {
                "name": "Rahul (Cleaner)",
                "role": "Cleaning Staff",
                "personality": "Short-tempered, defensive, and very anxious around authorities.",
                "secret": "He wears size 7 sneakers, which clearly do not match the size 9 muddy footprints."
            }
        },
        "culprit": "anita",
        "next_level": 2
    },
    2: {
        "title": "Level 2: The Cyber Syndicate Vault",
        "story": "A classified AI encrypted drive was wiped clean from the tech lab server room at 2:00 AM.",
        "clues": [
            {
                "id": "c4",
                "name": "USB Drive",
                "desc": "A burnt rubber USB stick with an engineering serial code left near Server #4."
            },
            {
                "id": "c5",
                "name": "Badge Access Log",
                "desc": "Admin badge #8809 was swiped into the vault at 01:58 AM."
            },
            {
                "id": "c6",
                "name": "Coffee Cup",
                "desc": "A hot hazelnut latte cup left on the console, freshly brewed before 2 AM."
            }
        ],
        "suspects": {
            "elena": {
                "name": "Dr. Elena (Lead Scientist)",
                "role": "Chief AI Researcher",
                "personality": "Arrogant, speaks fast with technical jargon, hates coffee.",
                "secret": "Her badge was stolen from her desk earlier that evening."
            },
            "marcus": {
                "name": "Marcus (DevOps Engineer)",
                "role": "System Administrator",
                "personality": "Chill, talks casually, addicted to sweet drinks like hazelnut coffee.",
                "secret": "True culprit. He cloned Elena's badge #8809 to inject malware and wipe the drive."
            },
            "priya": {
                "name": "Priya (Network Intern)",
                "role": "Junior Analyst",
                "personality": "Timid, constantly checks time, was studying for an exam late night.",
                "secret": "Was on the floor but only drinks green tea and had no server room clearance."
            }
        },
        "culprit": "marcus",
        "next_level": 3
    },
    3: {
        "title": "Level 3: The Grand Penthouse Poisoning",
        "story": "Billionaire Mr. Singhania was poisoned in his penthouse during a private dinner at 10:15 PM.",
        "clues": [
            {
                "id": "c7",
                "name": "Bitter Almond Aroma",
                "desc": "A faint scent of bitter almonds lingering around the vintage wine glass on the table."
            },
            {
                "id": "c8",
                "name": "Torn Chemical Receipt",
                "desc": "A pharmacy receipt for cyanide compound found crumpled near the kitchen trash."
            },
            {
                "id": "c9",
                "name": "Smart Lock Log",
                "desc": "The kitchen service door keypad was unlocked using personal staff PIN #4412 at 10:10 PM."
            }
        ],
        "suspects": {
            "meera": {
                "name": "Dr. Meera (Personal Physician)",
                "role": "Doctor",
                "personality": "Cool-headed, scientific, and blunt.",
                "secret": "She knows all about poisons, but she was performing an emergency surgery at City Hospital until 11 PM."
            },
            "arjun": {
                "name": "Arjun (Business Partner)",
                "role": "Co-founder",
                "personality": "Aggressive, anxious about financial audits, drinks only whisky.",
                "secret": "Argued with Singhania about company shares, but left through the main lobby at 9:30 PM."
            },
            "rohan": {
                "name": "Rohan (Private Butler)",
                "role": "Head Butler",
                "personality": "Excessively polite, speaks softly, hands visibly trembling.",
                "secret": "The true culprit. Holds staff PIN #4412, served the vintage wine, and forged the pharmacy signature."
            }
        },
        "culprit": "rohan",
        "next_level": None
    }
}