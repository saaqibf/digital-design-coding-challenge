#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Byte: helper module for the MindFuel Digital Design Coding Challenge,
Codebreaker track (cybersecurity).

Same architecture as the analyst tracks (adapted from Callysto's hackathon
mini-challenge templates, CC-BY, rebuilt by MindFuel), but a different
mechanic: instead of analyzing a dataset, students crack ciphers.
"""

import random
from collections import Counter
import matplotlib.pyplot as plt

# ---------------------------------------------------------------- voices

def byte(text):
    print("\033[1;37;40m 🔐 Byte: \033[1;0m" + text)

def task(text):
    print("\033[1;36m✅ " + text + "\033[1;0m")

def cheer():
    lines = [
        "Cracked it!", "Access granted!", "The firewall salutes you!",
        "Agent-level work!", "Cipher shattered!", "You're a natural codebreaker!",
        "Security clearance upgraded!", "Even Byte couldn't do it faster!",
    ]
    print("\033[1;35m" + random.choice(["✨ ", "🔓 ", "🎉 ", "🕵️ ", "🚀 "]) + random.choice(lines) + "\033[1;0m")

def hint(text):
    print("\033[1;31m❗️ " + text + "\033[1;0m")

# ---------------------------------------------------------- cipher tools

def encode(message, shift):
    """Caesar-shift a message. Students call this directly in later challenges."""
    out = ""
    for ch in message.upper():
        if ch.isalpha():
            out += chr((ord(ch) - 65 + shift) % 26 + 65)
        else:
            out += ch
    return out

def decode(message, shift):
    """Undo a Caesar shift. Students call and modify this."""
    return encode(message, -shift)


def reverse(text):
    """Flip a message back to front. One of the unit's standard tools."""
    return text[::-1]

def crack(text):
    """Brute force ANY message: print all 26 possible decodings."""
    for s in range(26):
        print(f"   shift {s:2d}: {decode(text, s)}")

# The intercepted messages
_M1 = encode("MEET AT THE OLD CLOCK TOWER AT NOON", 3)
_M2 = encode("THE PASSWORD IS STARDUST", 7)
_M3 = encode("WELL DONE AGENT YOU FOUND THE SIGNAL", 19)
_LONG = encode(
    "THE QUICK BROWN FOX JUMPS OVER THE LAZY DOG AGAIN AND AGAIN WHILE THE "
    "EAGER TEAM WATCHES EVERY MESSAGE THAT ENTERS THE NETWORK EVERY EVENING", 11)
_FINAL = encode("TRUST NO ONE THE VAULT OPENS AT MIDNIGHT", 15)[::-1]

# ------------------------------------------------------- answer checking

def _ask_mc(question, options, correct_index, why):
    print()
    task(question)
    for n, opt in enumerate(options, start=1):
        print(f"   {n}. {opt}")
    while True:
        ans = input("Type the number of your answer: ").strip().rstrip(".")
        if ans == str(correct_index):
            cheer()
            byte(why)
            return True
        hint("Not that one. Look again!")

def _ask_contains(question, keyword, why):
    """Pass if the student's answer contains the keyword, any case, any punctuation."""
    print()
    task(question)
    while True:
        ans = input("Your answer: ").strip().lower()
        if keyword.lower() in ans:
            cheer()
            byte(why)
            return True
        hint("Not quite. Decode carefully and look for the key word.")

def _ask_value(question, correct, why):
    print()
    task(question)
    while True:
        ans = input("Your answer: ").strip().strip('"').strip("'")
        if ans.lower() == str(correct).lower():
            cheer()
            byte(why)
            return True
        hint("Check again. You've got this.")

# ------------------------------------------------------------ points bar

_points = {"total": 0}

def _award(pts):
    _points["total"] += pts
    print(f"\033[1;33m +{pts} points! Session total so far: {_points['total']} \033[1;0m")

# =================================================== CHALLENGE FUNCTIONS

def join_the_team():
    """Challenge 0, worth 1 point."""
    name = input(" 🔐 Byte: Psst. I'm Byte, cyber defence unit. Codename? ").strip() or "Agent"
    byte(f"Welcome to the unit, Agent {name}. Someone calling themselves "
         "the Cipher Ring has been sending scrambled messages across the "
         "school network. Your mission: crack them.")
    scrambled = encode(name, 5)
    byte(f"First, watch what a cipher does. Your codename, scrambled: {scrambled}")
    byte(f"And unscrambled again: {decode(scrambled, 5)}")
    byte("Every letter slid 5 places down the alphabet, then slid back. "
         "That's called a Caesar cipher. Julius Caesar really used it for "
         "military orders two thousand years ago.")
    _award(1)

def first_intercept():
    """Challenge 0b, worth 1 point."""
    byte("Here's the first intercepted message:")
    print(f"\n   {_M1}\n")
    byte("Unreadable, right? By the end of this hour you'll crack messages "
         "like this in seconds. Run the next cell to see the decoder do it.")
    _award(1)

def crack_101():
    """Challenge 1, worth 3 points. How ciphers work, multiple choice."""
    byte("Codebreaking 101. The alphabet slides. A becomes B, B becomes C, "
         "and so on. Slide amount = the 'shift'.")
    _ask_mc(
        "If the shift is 1, what does the word CAB become?",
        ["DBC", "BZA", "CAB", "DCA"],
        1,
        "C slides to D, A slides to B, B slides to C. Every letter moves the same amount. That's the whole trick.",
    )
    _ask_mc(
        "To UNDO a shift of 3, you slide every letter:",
        ["3 more forward", "3 back", "26 forward", "You can't undo it"],
        2,
        "Encoding slides forward, decoding slides back. Same key, opposite direction. That's why the sender and receiver both need to know the shift.",
    )
    _award(3)

def the_decoder():
    """Challenge 2, worth 3 points. Run the decoder, then change the shift."""
    byte("Time to crack message one. Our informant says the Ring used shift 3.")
    result = decode(_M1, 3)
    print(f"\n   decode(message_1, 3)  →  {result}\n")
    _ask_contains(
        "Where is the meeting? (type the decoded location)",
        "clock",
        "Cracked in one line. When you know the shift, a Caesar cipher falls instantly.",
    )
    byte("Message two just arrived. The informant says shift 7 this time. "
         "The code cell below this one decodes with shift 3. Change the 3 "
         "to a 7 and run it on message_2.")
    _award(3)

def message_2():
    return _M2

def message_3():
    return _M3

def brute_force():
    """Challenge 3, worth 5 points. Try all 26 shifts."""
    byte("Message three. No informant this time, the shift is unknown. "
         "But here's the codebreaker's secret: there are only 26 possible "
         "shifts. So we try ALL of them.")
    for s in range(26):
        print(f"   shift {s:2d}: {decode(_M3, s)}")
    byte("Only one line above is English. Scan for it.")
    _ask_value(
        "Which shift number cracks message three?",
        "19",
        "That technique is called brute force: when you can't be clever, try everything. Computers try millions of password guesses a second the exact same way, which is why long passwords beat short ones.",
    )
    _ask_contains(
        "What did the message call you? (the two-word title, type it)",
        "agent",
        "Brute force plus a human eye for real words. That combination cracked codes at Bletchley Park and it still works today.",
    )
    _award(5)

def frequency_lab():
    """Challenge 4, worth 5 points. Frequency analysis with a chart."""
    byte("The Ring got smarter: their next message is LONG, and scanning 26 "
         "decodes of it would hurt. Time for the elegant weapon: frequency "
         "analysis.")
    byte("In English, the most common letter is E, by a mile. So in a "
         "Caesar-encoded English message, the most common letter is "
         "probably E in disguise.")
    letters = [c for c in _LONG if c.isalpha()]
    counts = Counter(letters)
    top = counts.most_common(1)[0][0]
    plt.figure(figsize=(9, 4))
    common = counts.most_common()
    plt.bar([c[0] for c in common], [c[1] for c in common], color="#4B258C")
    plt.title("Letter frequency in the intercepted message")
    plt.xlabel("Letter"); plt.ylabel("Count")
    plt.show()
    _ask_value(
        "Which letter appears MOST in the encoded message? (read the chart)",
        top,
        "Now the magic: if that letter is E in disguise, the shift is the distance from E to it.",
    )
    shift = (ord(top) - ord("E")) % 26
    byte(f"Distance from E to {top}: {shift}. Let's test that shift on the message:")
    print(f"\n   {decode(_LONG, shift)[:80]}...\n")
    _ask_value(
        "Did frequency analysis find the right shift? What is it?",
        str(shift),
        "One chart, one guess, instant crack. This is real cryptanalysis: the same idea, scaled up, broke the Enigma machine in World War Two.",
    )
    _award(5)

def make_your_own():
    """Challenge 5, worth 7 points. Students design their own cipher message."""
    byte("You've cracked their codes. Now build your own. Pick a secret "
         "shift (1 to 25) and a short message.")
    while True:
        try:
            shift = int(input("Your secret shift (1-25): ").strip())
            if 1 <= shift <= 25:
                break
        except ValueError:
            pass
        hint("A whole number between 1 and 25.")
    msg = input("Your secret message: ").strip() or "MINDFUEL RULES"
    coded = encode(msg, shift)
    byte(f"Encoded: {coded}")
    byte("Write that down and hand it to a neighbour WITHOUT the shift. "
         "See if they can brute-force it like you did in Challenge 3. "
         "While they work, try the open cells below: encode longer messages, "
         "chain two shifts, or find out why shift 13 is special (encode "
         "something with 13, then encode the RESULT with 13 again).")
    _award(7)

def final_mission():
    """Challenge 6, worth 10 points. Layered cipher."""
    byte("FINAL MISSION. The Ring's last message resisted everything. "
         "Brute force produced garbage on all 26 shifts:")
    print(f"\n   {_FINAL}\n")
    byte("When all 26 fail, the message has MORE than one layer. Hint: "
         "the Ring wrote this one backwards BEFORE encoding it.")
    byte("Your toolkit, agent: b.reverse(text) flips a message, "
         "b.crack(text) brute-forces anything. Use the tool cell below. "
         "Peel one layer, then attack the next.")
    _ask_contains(
        "Crack it. What opens at midnight? (decode and type the key word)",
        "vault",
        "Reversed, then shift 15. Layered defences beat single tricks, and "
        "peeling layers one at a time beats layered defences. That is "
        "modern cybersecurity in one sentence.",
    )
    reason = ""
    while len(reason) < 15:
        reason = input("Debrief: in one sentence, how did you crack it? ").strip()
        if len(reason) < 15:
            hint("Give the full debrief, at least a sentence. Future agents will read this.")
    cheer()
    byte("Mission complete. You brute-forced, frequency-analyzed, and "
         "peeled a layered cipher. Cybersecurity analysts, cryptographers, "
         "and penetration testers get paid to do exactly this, every day, "
         "against codes a little harder than the Ring's.")
    _award(10)

def scoreboard():
    byte(f"Your point total: {_points['total']}")
    byte("1-3 point missions taught the tools. 5s made you a codebreaker. "
         "7s and 10s made you the agent the unit calls first.")
