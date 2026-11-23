"""Narration for 'I Accidentally Stole the Mona Lisa!' (first person, young narrator).
Each entry: (shot_id, narration_text, pause_after_seconds). Comments = scene numbers from the brief."""

SHOTS = [
    # Scene 1 - hook
    ("hook", "Okay. I know how this looks. I'm running through Paris, in nineteen eleven, "
             "with the most famous painting in the world under my arm. "
             "Behind me: three policemen, one very excited dog, and a whistle that will not stop. "
             "And in front of me... a cart full of baguettes.", 0.2),
    ("crash", "Crunch! So how did a regular guy in a red cap end up stealing the Mona Lisa? "
              "Funny story. I didn't steal it. I was trying to save it.", 0.3),
    ("rewind", "Let me back up.", 0.4),
    # Scene 2 - the ticket
    ("ticket", "It all started in my bedroom. I was looking for my phone charger in a box of my grandpa's old stuff. "
               "And at the very bottom, I found a ticket. An old, yellow, paper ticket. "
               "Musée du Louvre. Paris. August twenty first, nineteen eleven. Weird. "
               "Then my thumb touched the date, and the ticket started to glow.", 0.3),
    ("portal", "The light swallowed my whole room. My lamp went one way, my socks went the other, "
               "and I went spinning through a tunnel of gold and blue light. Backwards. More than a hundred years backwards.", 0.5),
    # Scene 3 - Paris 1911
    ("paris", "I landed on a cobblestone street with a very loud bonk. Horses. Carriages. Gentlemen in top hats. "
              "Ladies with hats the size of umbrellas. And in the distance, the Eiffel Tower. "
              "Only twenty two years old, and already the most famous thing in Paris.", 0.4),
    ("newspaper", "A newsboy was shouting the headlines, so I grabbed a paper. Monday, August twenty first, nineteen eleven. "
                  "My brain did the math. That was the day somebody walked into the Louvre, and walked out with the Mona Lisa. "
                  "And it would take two whole years to get her back.", 0.5),
    # Scene 4 - disguise
    ("plan", "Normal people would panic. I panicked too. Then I made a plan. Stop the thief. Save the painting. "
             "Be home in time for dinner. Easy.", 0.4),
    ("disguise", "One problem. On Mondays, the Louvre was closed to visitors. Staff only. "
                 "So I borrowed a white cleaner's coat from a laundry line, grabbed a broom, and tried to look extremely professional. "
                 "I whistled. I swept. I nodded at the guard. He nodded back. I was in!", 0.4),
    ("louvre", "And wow. The Louvre is huge. Long golden galleries, painted ceilings, marble statues everywhere. "
               "Fun fact: before it was a museum, it was a royal palace.", 0.4),
    # Scene 5 - the missing painting
    ("empty", "I swept my way to a famous room called the Salon Carré, where the Mona Lisa hung. And I froze. "
              "On the wall, between the other paintings, there were just four iron hooks. And an empty space. "
              "I was too late!", 0.5),
    ("suspect", "Then, at the far end of the gallery, I saw him. A man in a white workman's smock, just like mine, "
                "walking very fast, and holding something flat, wrapped in a cloth. Hmm. Suspicious.", 0.4),
    # Scene 6 - museum chase
    ("chase", "I followed him. Very sneakily. I hid behind a Roman statue. Then behind a Greek statue. "
              "Then behind a guard, who was not a statue. The man turned around. "
              "I froze, and pretended to be art. It worked! Then he started running. So did I. "
              "And that's when I discovered that freshly waxed museum floors are extremely slippery.", 0.3),
    ("stairs", "I slid across the gallery like a hockey puck, bounced off a suit of armor, "
               "and tumbled down an entire marble staircase. Bump. Bump. Bump. Bump. "
               "Right past the Winged Victory of Samothrace, who did not help at all. "
               "And I landed right in front of the thief.", 0.3),
    # Scene 7 - accidental theft
    ("catch", "We crashed into each other. The painting flew into the air. Time slowed down. I dove. I stretched. "
              "And I caught it! I peeked under the cloth. A wooden panel. A mysterious smile. It was really her! "
              "Fun fact: the Mona Lisa is painted on poplar wood, not canvas. And she's tiny. About the size of a school poster.", 0.4),
    ("guard", "I looked up to thank the universe, and the universe sent me a museum guard. "
              "He looked at me. He looked at the painting. He looked at the empty wall. The real thief had vanished. "
              "And the guard blew his whistle. Thief! Stop, thief!", 0.3),
    # Scene 8 - Paris chase
    ("escape", "So I ran. Out of the Louvre, across the courtyard, and into the busy streets of Paris. "
               "Policemen blowing whistles. A carriage driver yelling in French. "
               "And a little dog who decided this was the best day of his life.", 0.3),
    ("streetchase", "I jumped over a flower stand, ducked under a horse, and dodged a man on a bicycle. "
                    "Then I turned the corner, and there it was. The baguette cart. Yes. That baguette cart. "
                    "Crunch! Bread everywhere. The dog was thrilled. The baker was not.", 0.4),
    ("hide", "I hid under a pile of bread until the whistles faded away. My heart was pounding. "
             "I was holding the most famous painting in the world, and every cop in Paris was looking for a short guy in a red cap. "
             "I needed a new plan.", 0.5),
    # Scene 9 - returning the painting
    ("note", "So I found a pencil, and wrote a note. Dear police. Here is the Mona Lisa. I did not steal it. "
             "I found it. Please give it back to the Louvre. Sincerely, a friend. P.S. Sorry about the baguettes.", 0.4),
    ("station", "That night, I tiptoed to the police station, placed the wrapped painting on the steps, "
                "rang the bell, and ran. From behind a lamppost, I watched a sleepy officer open the door, look down, "
                "and scream so loudly that the whole street woke up.", 0.5),
    # Scene 10 - changing history
    ("history", "And that's when it hit me. In real history, the Mona Lisa disappeared for more than two years. "
                "The thief, a man named Vincenzo Peruggia, hid her in a trunk in his tiny Paris apartment, "
                "until he was caught in Florence in December, nineteen thirteen. "
                "Meanwhile, crowds lined up at the Louvre just to stare at the empty wall. "
                "That's how she became the most famous painting on Earth.", 0.4),
    ("glow", "And I had just brought her back on the very first night. Two years early. "
             "Then my ticket started glowing again.", 0.5),
    # Scene 11 - final twist
    ("home", "Whoosh. Back in my bedroom. Same messy floor. Still no charger. I grabbed my laptop and searched: Mona Lisa theft. "
             "And my jaw dropped. Stolen August twenty first, nineteen eleven. Returned the very same night, by an unknown hero, "
             "described by witnesses as short, very fast, and wearing a strange red cap.", 0.5),
    ("next", "I was famous! Kind of. Then the ticket glowed one more time, and new words appeared. "
             "Next destination: Titanic. Nineteen twelve. Uh oh. No. No, no, no, no. Not the Titanic! "
             "Can I get a refund on this thing?", 0.6),
    ("outro", "If you enjoyed my disaster, subscribe to History World! And maybe pack me a life jacket.", 0.6),
]
