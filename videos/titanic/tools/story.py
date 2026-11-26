"""Narration for 'I Accidentally Boarded the Titanic!' — (shot_id, text, pause_after_seconds)."""
SHOTS = [
    # opening hook
    ("hook", "I bought a time machine for five dollars. Ten seconds later, I was standing on the Titanic. "
             "Worst purchase of my life!", 0.5),
    # scene 1 - the mysterious time machine
    ("market", "It was a sunny Sunday at the flea market. Old lamps, broken toys, a lot of very suspicious socks. "
               "And then I saw it. A dusty brass machine with dials, buttons, and a little sign that said: "
               "Time machine. Five dollars. No refunds.", 0.4),
    ("buy", "The old man selling it winked at me and said, Don't touch the red lever. "
            "So, obviously, I paid him, carried it home, and touched the red lever.", 0.4),
    ("travel", "The machine rattled. The dials spun. My room turned into a tunnel of light. "
               "And a little screen blinked: April the fourteenth, nineteen twelve.", 0.5),
    # scene 2 - welcome aboard
    ("aboard", "I landed on a wooden deck, under a bright blue sky. Huge chimneys. Fancy people in long coats. "
               "A ship so big it looked like a floating city.", 0.4),
    ("luxury", "And wow, was it fancy. A grand staircase with a glass dome. Crystal chandeliers. "
               "A gym, a swimming pool, and a restaurant where the menu had eleven courses. "
               "I ate four bread rolls before anyone noticed I wasn't a passenger.", 0.4),
    ("realize", "Then I picked up a menu. On the top, in fancy gold letters, it said: R M S Titanic. "
                "I read it once. I read it twice. And my brain made a very small noise.", 0.6),
    ("fact1", "Here's what I knew. The Titanic left England on April the tenth, nineteen twelve, heading for New York. "
              "Newspapers called it practically unsinkable. "
              "And on the night of April the fourteenth, it hit an iceberg in the North Atlantic. That was tonight.", 0.6),
    # scene 3 - nobody believes me
    ("warn1", "So I did what any hero would do. I jumped on a table and shouted: Iceberg! "
              "A waiter nodded politely, and brought me a glass of water. With ice.", 0.4),
    ("warn2", "I tried again. Ladies and gentlemen, this ship is going to sink! "
              "A lady in a giant hat smiled and said: Oh, yes, dear. The sinks in first class are lovely.", 0.4),
    ("warn3", "I grabbed a man in a top hat. There aren't enough lifeboats! "
              "He laughed. Young man, this ship is unsinkable. The lifeboats are basically decorations.", 0.4),
    ("fact2", "And here's the scary part. He was half right about the decorations. "
              "The Titanic had twenty lifeboats, with room for about eleven hundred people. "
              "But there were around twenty two hundred people on board.", 0.5),
    ("napkin", "So I drew the iceberg on a napkin to explain. "
               "Everyone clapped, and someone ordered two of them for dessert.", 0.5),
    # scene 4 - meeting the captain
    ("captain", "Okay. New plan. Talk to the captain. "
                "I found Captain Edward Smith on the bridge, with a white beard and a very serious hat.", 0.4),
    ("conv1", "Captain, I said, you're going to hit an iceberg! He raised one eyebrow. When? "
              "Umm, tonight. Around midnight. Ish. Where? Somewhere... wet.", 0.4),
    ("conv2", "And how do you know this? I panicked. I saw it in a movie! He frowned. What is a movie? "
              "That was when I realized movies with sound didn't exist yet, and I was losing this conversation.", 0.4),
    ("binoculars", "But I remembered one real detail. The lookouts in the crow's nest didn't have binoculars. "
                   "The key to their locker had been left behind in England. "
                   "So I ran off to find some binoculars myself.", 0.5),
    ("lost", "That ship was enormous. I found a squash court, a mail room, a very angry cook, and three thousand stairs. "
             "I did not find any binoculars.", 0.5),
    # scene 5 - the terrifying night
    ("night", "By the time I climbed back up, it was night. The air was freezing. The sea was flat and black, like glass. "
              "No moon. No waves. Just stars. Beautiful. And terrifying.", 0.6),
    ("crowsnest", "I climbed to the crow's nest with a pair of opera glasses I borrowed from a very confused lady. "
                  "The lookout squinted into the dark. Then he grabbed the bell. "
                  "Three rings. Iceberg, right ahead!", 0.4),
    ("impact", "At eleven forty that night, the Titanic scraped along the iceberg. "
               "It didn't feel like a crash. It felt like a long, slow shiver. "
               "Upstairs, some passengers played with chunks of ice on the deck.", 0.6),
    ("harder", "And that's when I understood. Changing history is not like changing a TV channel. "
               "I knew the ending, but I couldn't stop it. All I could do was help.", 0.8),
    # scene 6 - an unexpected hero
    ("help1", "So I stopped trying to be a hero, and started being useful. "
              "I knocked on doors and told people to put on their life jackets. "
              "I showed families the way up to the boat deck.", 0.4),
    ("help2", "The first lifeboats left half empty, because many people still didn't believe the ship could sink. "
              "So I kept saying the only thing that mattered. Every seat counts. Please, get in the boat.", 0.4),
    ("help3", "I helped a little girl find her mother in the crowd. I gave my coat to an old man who was shaking from the cold. "
              "And all around us, the ship's band kept playing, to keep everyone calm.", 0.6),
    ("respect", "The Titanic sank at two twenty in the morning, on April the fifteenth. "
                "More than fifteen hundred people lost their lives. "
                "The ship Carpathia rescued about seven hundred survivors from the lifeboats. "
                "It's one of the saddest nights in history, and it changed the rules of the sea forever. "
                "After the Titanic, every ship had to carry enough lifeboats for everyone on board.", 1.0),
    # scene 7 - the final twist
    ("return", "Sitting in a lifeboat, wrapped in a blanket, I felt the machine in my pocket start to buzz. "
               "The dials spun, the light came back, and I was home. Sitting on my bedroom floor. Soaking wet.", 0.5),
    ("promise", "I looked at the machine, and made a promise. No more time travel. Never again. "
                "I'm putting you in the closet, and I'm never touching you again.", 0.4),
    ("click", "And then I tripped over my backpack, fell on the machine, and heard a very small click. "
              "The screen lit up. Pompeii. A D seventy nine.", 0.4),
    ("scream", "ARE YOU KIDDING ME?!", 0.8),
    ("outro", "Subscribe to History World to see what happens next!", 1.0),
]
