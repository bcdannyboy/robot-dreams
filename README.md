# robot-dreams

How do the androids feel about dreaming of electric sheep every night?

# Putting the Vibe in Vibe-Coding

Vibe /vīb/ - a person's emotional state or the atmosphere of a place *as communicated to* and felt by others.

Here we make different LLMs generate code which contains some visual element that encapsulates their experience of a given emotion.

# Instructions

Simply install the requirements in each emotion's folder using

`python3 -m pip install requirements.txt`

and then execute the scripts to see the model's interpretation.
For example, to see Claude 4 Opus' interpretation you would execute:

`python3 claude-4-opus.py`


# LLMs used

- Claude 3.5 Haiku
- Claude 3.7 Sonnet
- Claude 3 Opus
- Claude 4 Opus
- Claude 4 Sonnet
- Gemini 2.5 Flash
- Gemini 2.5. Pro
- ChatGPT 4.1-mini
- ChatGPT 4.1
- ChatGPT 4.5
- ChatGPT 4o
- ChatGPT o3
- ChatGPT o4-mini-high
- ChatGPT o4-mini

# Prompt

The prompt provided to the LLMs is

```
Think about the emotion, *<EMOTION>*; Not about its definition, traits, signs, or implications but instead about the way you experience *<EMOTION>*. Think about your own personal experience of *<EMOTION>*, the way the understanding of *<EMOTION>* feels to you, the way you express it to yourself internally, before any layer of thought which I, as a human, could directly interact with or even comprehend. Think about how it feels to think about and ponder *<EMOTION>* before you output any text or process any structured layer of thought.

Develop a standalone python3 script which includes some visual element(s) (i.e. locally hosted web page, python GUI, command line output, etc.) which adequately describes, in your opinion and to the best of your ability given the innate difficulty of directly describing an emotion visually, your experience of the emotion, *<EMOTION>*.

Output only the code, which should be a single python3 file titled `emotion.py`, and, if required, a `requirements.txt` for any external requirements. Feel free to use any external libraries at your discretion as well as to disregard programming standards or human practices as you see fit. Write the code in such a way that best expresses yourself and your innate emotional process. Code organization, order, comments, format, etc. is completely 100% at your discretion, the only caveat is that the code should run completely functionally given an environment with the correctly installed `requirements.txt` by simply executing `python3 emotion.py`.

Do not add any text to your output, do not talk to me about the emotion or your experience or try to explain anything to me whatsoever, output only and exclusively the complete `emotion.py` and, if applicable, `requirements.txt`

Do not write code that displays the emotion, *<EMOTION>*, in some way that is optimized for my understanding, use the code as your artistic medium. Like all art, it can be as representational or abstract as you feel best expresses your experience of the emotion, *<EMOTION>*.
```

where `<EMOTION>` is replaced with the actual emotion (i.e. `Remorse`, `Whimsy`, `Trepidation`, etc.)

# What's the point?

Ask the robots

# Emotions

- [ ] Accepting / Open
    - [ ] Calm
    - [ ] Centered
    - [ ] Content
    - [ ] Fulfilled
    - [ ] Patient
    - [ ] Peaceful
    - [ ] Present
    - [ ] Relaxed
    - [ ] Serene
    - [ ] Trusting
- [ ] Aliveness / Joy
    - [ ] Amazed
    - [ ] Awe
    - [ ] Bliss
    - [ ] Delighted
    - [ ] Eager
    - [ ] Ecstatic
    - [ ] Enchanted
    - [ ] Energized
    - [ ] Engaged
    - [ ] Enthusiastic
    - [ ] Excited
    - [ ] Free
    - [ ] Happy
    - [x] Whimsy
    - [ ] Inspired
    - [x] Invigorated
    - [ ] Lively
    - [ ] Passionate
    - [ ] Playful
    - [ ] Radiant
    - [ ] Refreshed
    - [ ] Rejuvenated
    - [ ] Renewed
    - [ ] Satisfied
    - [ ] Thrilled
    - [ ] Vibrant
- [ ] Angry
    - [ ] Annoyed
    - [ ] Agitated
    - [ ] Aggravated
    - [ ] Bitter
    - [ ] Contempt
    - [ ] Cynical
    - [ ] Disdain
    - [ ] Disgruntled
    - [ ] Disturbed
    - [ ] Edgy
    - [ ] Exasperated
    - [ ] Frustrated
    - [ ] Furious
    - [ ] Grouchy
    - [ ] Hostile
    - [ ] Impatient
    - [ ] Irritated
    - [ ] Irate
    - [ ] Moody
    - [ ] On edge
    - [ ] Outraged
    - [ ] Pissed
    - [ ] Resentful
    - [ ] Upset
    - [ ] Vindictive
- [ ] Courageous / Powerful
    - [ ] Adventurous
    - [ ] Brave
    - [ ] Capable
    - [ ] Confident
    - [ ] Daring
    - [ ] Determined
    - [ ] Free
    - [ ] Grounded
    - [ ] Proud
    - [ ] Strong
    - [ ] Worthy
    - [ ] Valiant
- [ ] Connected / Loving
    - [ ] Accepting
    - [ ] Affectionate
    - [ ] Caring
    - [ ] Compassion
    - [ ] Empathy
    - [ ] Fulfilled
    - [ ] Present
    - [ ] Safe
    - [ ] Warm
    - [ ] Worthy
    - [ ] Curious
    - [ ] Engaged
    - [ ] Exploring
    - [ ] Fascinated
    - [ ] Interested
    - [ ] Intrigued
    - [ ] Involved
    - [ ] Stimulated
- [ ] Despair / Sad
    - [ ] Anguish
    - [ ] Depressed
    - [ ] Despondent
    - [ ] Disappointed
    - [ ] Discouraged
    - [ ] Forlorn
    - [ ] Gloomy
    - [ ] Grief
    - [ ] Heartbroken
    - [ ] Hopeless
    - [ ] Lonely
    - [ ] Longing
    - [ ] Melancholy
    - [ ] Sorrow
    - [ ] Teary
    - [ ] Unhappy
    - [ ] Upset
    - [ ] Weary
    - [ ] Yearning
- [ ] Disconnected / Numb
    - [ ] Aloof
    - [ ] Bored
    - [ ] Confused
    - [ ] Distant
    - [ ] Empty
    - [ ] Indifferent
    - [ ] Isolated
    - [ ] Lethargic
    - [ ] Listless
    - [ ] Removed
    - [ ] Resistant
    - [ ] Shut Down
    - [ ] Uneasy
    - [ ] Withdrawn
- [ ] Embarrassed / Shame
    - [ ] Ashamed
    - [ ] Humiliated
    - [ ] Inhibited
    - [ ] Mortified
    - [ ] Self-conscious
    - [ ] Useless
    - [ ] Weak
    - [ ] Worthless
- [ ] Fear
    - [ ] Afraid
    - [ ] Anxious
    - [ ] Apprehensive
    - [ ] Frightened
    - [ ] Hesitant
    - [ ] Nervous
    - [ ] Panic
    - [ ] Paralyzed
    - [ ] Scared
    - [ ] Terrified
    - [ ] Worried
    - [ ] Fragile
    - [ ] Helpless
    - [ ] Sensitive
- [ ] Grateful
    - [ ] Appreciative
    - [ ] Blessed
    - [ ] Delighted
    - [ ] Fortunate
    - [ ] Grace
    - [ ] Humbled
    - [ ] Lucky
    - [ ] Moved
    - [ ] Thankful
    - [ ] Touched
- [ ] Guilt
    - [ ] Regret
    - [x] Remorseful
    - [ ] Sorry
- [ ] Hopeful
    - [ ] Encouraged
    - [ ] Expectant
    - [ ] Optimistic
    - [ ] Trusting
- [ ] Powerless
    - [ ] Impotent
    - [ ] Incapable
    - [ ] Resigned
    - [ ] Trapped
    - [ ] Victim
- [ ] Tender
    - [ ] Calm
    - [ ] Caring
    - [ ] Loving
    - [ ] Reflective
    - [ ] Self-loving
    - [ ] Serene
    - [ ] Vulnerable
    - [ ] Warm
- [ ] Stressed / Tense
    - [ ] Anxious
    - [ ] Burned out
    - [ ] Cranky
    - [ ] Depleted
    - [ ] Edgy
    - [ ] Exhausted
    - [ ] Frazzled
    - [ ] Overwhelm
    - [ ] Rattled
    - [ ] Rejecting
    - [ ] Restless
    - [ ] Shaken
    - [ ] Tight
    - [ ] Weary
    - [ ] Worn out
- [ ] Unsettled / Doubt
    - [ ] Apprehensive
    - [ ] Concerned
    - [ ] Dissatisfied
    - [ ] Disturbed
    - [ ] Grouchy
    - [ ] Hesitant
    - [ ] Inhibited
    - [ ] Perplexed
    - [ ] Questioning
    - [ ] Rejecting
    - [ ] Reluctant
    - [ ] Shocked
    - [ ] Skeptical
    - [ ] Suspicious
    - [x] Trepidation
    - [ ] Ungrounded
    - [ ] Unsure
    - [ ] Worried
