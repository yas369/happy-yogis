# -*- coding: utf-8 -*-
"""Ten posts for people searching for yoga near them.

Written for what a person types when they are choosing a class - near me,
near Perungalathur, a yoga instructor, online - and each one answers a
different question so no two cover the same ground. Every fact (hours,
batches, centres, phone numbers) is the one on the rest of the site; nothing
is promised that the cited health authorities do not support, and there are
no prices, qualifications, distances or reviews.

The same three photographs are used on every post, on purpose: tree pose as
the lead, then the seated meditation and the breathing practice inline.
"""

LINK = 'class="text-blue font-medium hover:underline"'


def a(slug, text):
    return f'<a href="{slug}" {LINK}>{text}</a>'


PERU = a("yoga-classes-perungalathur.html", "yoga classes in Perungalathur")
TAMB = a("yoga-classes-tambaram.html", "Tambaram")
FIRST = a("what-happens-in-your-first-yoga-class.html", "what happens in a first class")
OFTEN = a("how-often-should-you-do-yoga.html", "how many days a week")
PARK = a("new-yoga-centre-park-63-perungalathur.html", "Park 63 centre")
EARLY = a("early-morning-yoga-batch-park-63.html", "5:30 am batch at Park 63")
GOOD = a("yoga-for-good-health.html", "yoga for good health")
MEN = a("yoga-classes-for-men-perungalathur.html", "men's batches")
KIDS = a("yoga-classes-for-children-perungalathur.html", "children")
TIME = a("morning-or-evening-yoga-class.html", "morning or evening")

TRIAL = ("The 2-day trial on WhatsApp is the easiest way to find out: "
         "message us, pick a batch, and come along.")

CAP1 = "Adults and children seated in meditation facing their teacher at Happy Yogis."
CAP5 = "The teacher leading a seated breathing practice for a mixed-age group."


def make(para, bullets, photo, qa, cite, DISCLAIMER):
    base = {"date": "2026-11-10", "date_text": "10 November 2026",
            "photo": "ima6"}
    posts = [

    # ------------------------------------------------------------------ 1
    {**base,
     "slug": "yoga-classes-near-me-questions-to-ask.html",
     "title": "Yoga classes near me: 8 questions to ask",
     "standfirst": ("Searching for yoga classes near you gives you a list. "
                    "Eight questions turn the list into a decision, and here "
                    "is how we answer each of them."),
     "meta": ("Choosing yoga classes near you in Chennai? Eight questions to "
              "ask any studio first, with straight answers for Happy Yogis."),
     "short": [
        "Ask who teaches, how big the batch is and whether you can try first.",
        "Check the timing against your commute, not just the map pin.",
        "Tell the teacher about injuries before the first class.",
     ],
     "body": [
      ("Near on the map is not the same as near in practice",
       para("A class two kilometres away that you reach through GST Road "
            "traffic is further than one ten minutes on foot. So the first "
            "thing to check is not the pin, it is the route at the hour you "
            "would actually travel. Our two centres are both in New "
            "Perungalathur, close to the railway station area just off GST "
            "Road, between Tambaram and Vandalur.")
       + photo("ima1", CAP1)),

      ("The eight questions",
       para("Ask these of any studio, ours included.")
       + qa([
        ("1. Who teaches, and for how long?",
         "Karthika has practised and taught for more than ten years and takes "
         "every batch at SSM Nagar. Surekha teaches the 5:30 am batch at Park 63."),
        ("2. What times are there?",
         "Monday to Friday, 5:30 am to 7:00 pm. At SSM Nagar the batches are "
         "5:30&ndash;6:15 am, 6:15&ndash;7:15 am, 10:00&ndash;11:00 am (ladies "
         "only) and 5:00&ndash;6:00 pm. Park 63 runs 5:30&ndash;6:30 am. We are "
         "closed on Saturdays, Sundays and public holidays."),
        ("3. Can I try before I commit?",
         "Yes. " + TRIAL),
        ("4. Is it a class for beginners?",
         "Most people who join have never done yoga before. See "
         + FIRST + "."),
        ("5. What language is it taught in?", "Tamil and English."),
        ("6. What if I have an injury or a health condition?",
         "Tell the teacher before the class so the practice can be adjusted, "
         "and check with your doctor. That is also the advice of "
         + cite("nccih_safe", "NCCIH") + "."),
        ("7. Is there an online option?",
         "Yes. Online classes run at all four times, from either centre, and "
         "you can switch between online and in person."),
        ("8. What do I need to bring?",
         "A mat for the trial. Once you join you can leave it at the centre, "
         "and every student gets a Happy Yogis t-shirt."),
       ])),

      ("Why the teacher matters most",
       para("The " + cite("nccih_safe", "National Center for Complementary and "
            "Integrative Health") + " says yoga is generally safe when "
            "practised properly under a qualified instructor, and that "
            "learning on your own is linked with a higher risk of injury. A "
            "good studio is mostly a good teacher paying attention to a small "
            "group.")
       + photo("ima5", CAP5)),

      ("Where to go from here",
       para("If you are in Perungalathur, our page on " + PERU + " has both "
            "centres, directions and phone numbers. " + TRIAL)),
     ],
     "related": ("yoga-classes-near-me-for-women-chennai.html",
                 "Yoga classes near me for women in Chennai",
                 "The ladies-only batch, and what to tell your teacher.")},

    # ------------------------------------------------------------------ 2
    {**base,
     "slug": "yoga-classes-near-me-for-women-chennai.html",
     "title": "Yoga classes near me for women in Chennai",
     "standfirst": ("A ladies-only morning batch, mixed batches at other times, "
                    "and a teacher who needs to know what you are working with."),
     "meta": ("Yoga classes for women in New Perungalathur, Chennai: a ladies-only "
              "10 am batch, mixed batches, and what to tell your teacher."),
     "short": [
        "The 10:00&ndash;11:00 am batch at SSM Nagar is for ladies only.",
        "Mixed batches at 5:30, 6:15 and 5:00 pm are open to women too.",
        "Tell the teacher about PCOD, thyroid, knees or pregnancy first.",
     ],
     "body": [
      ("A batch for ladies, and others that are mixed",
       para("The 10:00&ndash;11:00 am batch at SSM Nagar is for ladies only. "
            "It is popular with homemakers and with anyone on a shift "
            "pattern, because mid-morning is free for them when early "
            "mornings are not. Women also join the early and evening "
            "batches, which are open to everyone, and the 5:30 am batch at "
            "Park 63 is taught by Surekha.")
       + photo("ima1", CAP1)),

      ("Choosing between them",
       para("If privacy and a quieter pace in the day suit you, take the "
            "10 am. If you work or have school-age children, the 5:30 or "
            "6:15 am batches get the practice done before the day starts, "
            "and 5:00 pm suits students and people finishing work. Our "
            "post on " + TIME + " goes through the trade-off.")),

      ("Tell your teacher what you are working with",
       para("PCOD, a thyroid condition, a bad knee, a recent delivery, "
            "pregnancy: say so before the first class, and the practice is "
            "adjusted. Check with your doctor as well. Yoga sits alongside "
            "medical care and does not replace it. "
            "See " + GOOD + " for what the evidence does and does not "
            "support.")
       + photo("ima5", CAP5)),

      ("If you have never done yoga",
       para("Most people who join have never done yoga before. Nobody is "
            "expected to be flexible on day one. Read " + FIRST + ", then "
            + TRIAL)),
     ],
     "related": ("yoga-classes-near-me-questions-to-ask.html",
                 "Yoga classes near me: 8 questions to ask",
                 "What to check before joining any studio.")},

    # ------------------------------------------------------------------ 3
    {**base,
     "slug": "yoga-near-perungalathur-station-before-work.html",
     "title": "Yoga near Perungalathur station, before work",
     "standfirst": ("Early batches for people who catch the train or drive up "
                    "GST Road, finished in time to get to work."),
     "meta": ("Early morning yoga near Perungalathur station: 5:30 am batches at "
              "SSM Nagar and Park 63, Monday to Friday, in New Perungalathur."),
     "short": [
        "Three early batches: 5:30 and 6:15 am at SSM Nagar, 5:30 am at Park 63.",
        "Both centres are close to the railway station area.",
        "Online is there for the mornings you cannot get out.",
     ],
     "body": [
      ("The early batches",
       para("At SSM Nagar the first batch runs 5:30&ndash;6:15 am, 45 minutes, "
            "which suits anyone who needs to be out of the door by seven. The "
            "6:15&ndash;7:15 am batch is our busiest hour, with a mix of "
            "ages and abilities. At Park 63, Surekha teaches 5:30&ndash;6:30 "
            "am. All of this runs Monday to Friday.")
       + photo("ima6", "Students holding tree pose together.")),

      ("Where we are",
       para("Both centres are in New Perungalathur, close to the Perungalathur "
            "railway station area and just off GST Road, between Tambaram and "
            "Vandalur. The Chengalpattu line is one stop from Tambaram. The "
            "page on " + PERU + " has the address of each centre and a "
            "directions link.")),

      ("Making an early start stick",
       para("The first week is the hard one. Lay out your clothes and keep "
            "the mat by the door. Our post on " + OFTEN + " has a realistic target.")
       + photo("ima5", CAP5)),

      ("For the mornings you cannot come",
       para("Online classes run at all four times, so a wet morning or an "
            "early meeting does not have to mean a missed practice. " + TRIAL)),
     ],
     "related": ("early-morning-yoga-batch-park-63.html",
                 "The 5:30 am batch at Park 63",
                 "What the early hour at the second centre is like.")},

    # ------------------------------------------------------------------ 4
    {**base,
     "slug": "yoga-in-perungalathur-neighbourhood-guide.html",
     "title": "Yoga in Perungalathur: a neighbourhood guide",
     "standfirst": ("Where students come from, how they get here, and when "
                    "the online class is the better call."),
     "meta": ("Yoga in Perungalathur: a local guide to our two New Perungalathur "
              "centres, who comes from where, languages and online classes."),
     "short": [
        "Students come from Perungalathur, Tambaram, Selaiyur, Chromepet and beyond.",
        "Classes are in Tamil and English.",
        "When GST Road is not worth the drive, join online.",
     ],
     "body": [
      ("Two centres in New Perungalathur",
       para("We teach from SSM Nagar and from Park 63, both in New "
            "Perungalathur and close to the station area. For the full "
            "picture, including hours, see our page on " + PERU + ".")
       + photo("ima1", CAP1)),

      ("Where our students come from",
       para("Students travel from New Perungalathur and Old Perungalathur, "
            "SSM Nagar, East and West Tambaram, Selaiyur, Chromepet, "
            "Vandalur, Urapakkam, Guduvanchery and Medavakkam. If you are in "
            "Tambaram, our " + TAMB + " page has the route.")),

      ("Language and who is in the room",
       para("Classes are taught in Tamil and English, so either is fine. The "
            "batches mix ages: adults and children practise together in the "
            "regular batches, and there is a ladies-only batch at 10 am. "
            "See also our pages for " + MEN + " and for " + KIDS + ".")
       + photo("ima5", CAP5)),

      ("When not to drive",
       para("GST Road at peak hour is a real cost. Some students come in "
            "person most days and join online on the days the traffic is "
            "not worth it. Same teacher, same batch structure. " + TRIAL)),
     ],
     "related": ("yoga-new-perungalathur-ssm-nagar-or-park-63.html",
                 "New Perungalathur yoga: SSM Nagar or Park 63?",
                 "Two centres in one neighbourhood, compared.")},

    # ------------------------------------------------------------------ 5
    {**base,
     "slug": "yoga-new-perungalathur-ssm-nagar-or-park-63.html",
     "title": "New Perungalathur yoga: SSM Nagar or Park 63?",
     "standfirst": ("Two centres in the same neighbourhood. Here is how they "
                    "differ, so you can pick the one that fits your morning."),
     "meta": ("Yoga in New Perungalathur: SSM Nagar or Park 63? Batches, "
              "teachers, addresses and phone numbers for both centres."),
     "short": [
        "SSM Nagar has four batches; Park 63 has one, at 5:30 am.",
        "Karthika teaches at SSM Nagar; Surekha teaches at Park 63.",
        "Both are in New Perungalathur and close to the station area.",
     ],
     "body": [
      ("SSM Nagar",
       para("Address: SSM Nagar, New Perungalathur. Karthika, who has "
            "practised and taught for more than ten years, takes every batch: "
            "5:30&ndash;6:15 am, 6:15&ndash;7:15 am, 10:00&ndash;11:00 am "
            "(ladies only) and 5:00&ndash;6:00 pm, Monday to Friday. Phone "
            "<a href=\"tel:+919994247450\" " + LINK + ">+91 99942 47450</a>. "
            "<a href=\"https://www.google.com/maps/search/?api=1&amp;"
            "query=SSM+Nagar+New+Perungalathur+Chennai\" "
            "target=\"_blank\" rel=\"noopener\" " + LINK + ">Directions</a>.")
       + photo("ima1", CAP1)),

      ("Park 63",
       para("Address: Yoga Room, Tower 20, Park 63, Sriram Apartments, New "
            "Perungalathur. Surekha teaches 5:30&ndash;6:30 am, Monday to "
            "Friday. Phone "
            "<a href=\"tel:+919025629706\" " + LINK + ">+91 90256 29706</a>. "
            "<a href=\"https://maps.app.goo.gl/rk2vP6Sfuvw3FS347\" "
            "target=\"_blank\" rel=\"noopener\" " + LINK + ">Directions</a>. "
            "More in our " + PARK + " post.")),

      ("How to choose",
       para("If you live in Park 63 or nearby, the 5:30 am batch there saves "
            "you the journey. If you need a mid-morning, evening or ladies-only "
            "hour, SSM Nagar is where those run. If you are unsure, message "
            "us on WhatsApp and we will help you pick a batch.")
       + photo("ima5", CAP5)),

      ("Try it first",
       para(TRIAL + " Read " + FIRST + " beforehand. Online classes are also "
            "there if you want to begin from home.")),
     ],
     "related": ("beginner-yoga-new-perungalathur-first-month.html",
                 "Beginner yoga in New Perungalathur: month one",
                 "What the first month looks like.")},

    # ------------------------------------------------------------------ 6
    {**base,
     "slug": "beginner-yoga-new-perungalathur-first-month.html",
     "title": "Beginner yoga in New Perungalathur: month one",
     "standfirst": ("What to expect from before day one to the end of the "
                    "first month, without promises about outcomes."),
     "meta": ("Beginner yoga in New Perungalathur: how the first month usually "
              "goes, from the 2-day trial to settling into a weekly rhythm."),
     "short": [
        "Start with the 2-day trial, then choose a batch.",
        "Three to four sessions a week is a realistic rhythm.",
        "Most people who join have never done yoga before.",
     ],
     "body": [
      ("Before day one",
       para("Nothing to prepare except a mat for the trial and clothes you "
            "can move in. If you have an injury or a health condition, tell "
            "the teacher and check with your doctor. For the hour itself, see "
            + FIRST + ".")
       + photo("ima1", CAP1)),

      ("The trial",
       para(TRIAL + " Two days is enough to see the room, meet the teacher "
            "and know whether the pace suits you.")),

      ("Weeks one to four",
       para("Most people who join have never done yoga before, so the early "
            "weeks are about the basics: getting comfortable on the mat, "
            "learning the breathing, and building a habit. A realistic rhythm "
            "is three to four sessions a week &mdash; see " + OFTEN + ". "
            "Missing a day is normal. Come back the next one.")
       + photo("ima5", CAP5)),

      ("At the end of the month",
       para("Take stock. Is the batch time right? Is the commute worth it, "
            "or would online on some days help? Did you tell the teacher "
            "everything relevant? Nothing here promises a particular result "
            "&mdash; yoga does different things for different people &mdash; "
            "but a month is long enough to know whether you want to carry on. "
            "See " + GOOD + " for what research does and does not say.")),
     ],
     "related": ("yoga-new-perungalathur-ssm-nagar-or-park-63.html",
                 "New Perungalathur yoga: SSM Nagar or Park 63?",
                 "Pick the centre that fits your morning.")},

    # ------------------------------------------------------------------ 7
    {**base,
     "slug": "how-to-choose-a-yoga-instructor.html",
     "title": "How to choose a yoga instructor near you",
     "standfirst": ("A good instructor matters more than a good room. Here "
                    "is what to look for and what to ask."),
     "meta": ("How to choose a yoga instructor near you: what to ask about "
              "experience, safety and class size, and why trying a class first helps."),
     "short": [
        "Ask about experience and how they handle injuries.",
        "Check how many people are in the room.",
        "Try a class before you commit.",
     ],
     "body": [
      ("Why the instructor matters",
       para("The " + cite("nccih_safe", "US National Center for Complementary and "
            "Integrative Health") + " says yoga is generally safe when "
            "practised properly under a qualified instructor, and that "
            "learning alone is linked with a higher risk of injury. In "
            "practice, the instructor decides whether the class suits you.")
       + photo("ima1", CAP1)),

      ("What to ask",
       bullets([
        "How long have you taught, and what do you teach?",
        "How do you handle a student with an injury or a health condition?",
        "How many people will be in the room?",
        "Will I be corrected, or left to copy?",
        "Can I try a class before paying?",
       ])),

      ("Certification",
       para("In India, the Ministry of AYUSH runs the Yoga Certification "
            "Board, which sets standards for instructors. Its level names "
            "have changed over time, so check the "
            "<a href=\"https://yogacertificationboard.nic.in/\" "
            "target=\"_blank\" rel=\"noopener\" " + LINK + ">board's own "
            "site</a> for the current ones. Ask any instructor about "
            "training, and whether they teach beginners.")
       + photo("ima5", CAP5)),

      ("Our own answer",
       para("Karthika has practised and taught for more than ten years and "
            "takes every batch at SSM Nagar; Surekha teaches the 5:30 am "
            "batch at Park 63. " + TRIAL)),
     ],
     "related": ("private-yoga-instructor-or-group-class.html",
                 "Private yoga instructor or a small group class?",
                 "Which format suits you.")},

    # ------------------------------------------------------------------ 8
    {**base,
     "slug": "private-yoga-instructor-or-group-class.html",
     "title": "Private yoga instructor or group class?",
     "standfirst": ("One-to-one attention against the energy of a group: "
                    "a plain comparison to help you decide."),
     "meta": ("Private yoga instructor or a small group class? A fair comparison "
              "of attention, routine, cost of time and motivation."),
     "short": [
        "A private instructor gives attention; a group gives routine.",
        "Small groups let a teacher still correct each person.",
        "Ask us what is available before you decide.",
     ],
     "body": [
      ("What a private instructor gives you",
       para("Full attention, a plan built around you, and flexible timing. "
            "That helps if you have a specific injury, a tight schedule or "
            "you feel self-conscious in a room. The trade-offs: it is harder "
            "to keep going when it is only you, and you miss the pace that "
            "other people set.")
       + photo("ima1", CAP1)),

      ("What a small group gives you",
       para("A fixed time that turns into a habit, other people to practise "
            "alongside, and a teacher who can still see everyone when the "
            "batch is small. Most people who join Happy Yogis have never "
            "done yoga before, and find the group easier than expected. "
            "The teacher can adjust the practice for each person as long as "
            "they know what you are working with.")),

      ("How to decide",
       para("Ask yourself three things: do I need to work around an injury, "
            "do I need a time nobody else offers, and do I tend to skip "
            "things I do alone? If you need individual attention, say so "
            "when you message us, and ask what we can arrange. We would "
            "rather tell you honestly than promise something.")
       + photo("ima5", CAP5)),

      ("Try the group first",
       para(TRIAL + " It costs you two sessions of your time and tells you "
            "most of what you need. For the questions to ask any teacher, see "
            + a("how-to-choose-a-yoga-instructor.html", "how to choose a yoga instructor")
            + ".")),
     ],
     "related": ("how-to-choose-a-yoga-instructor.html",
                 "How to choose a yoga instructor near you",
                 "What to ask and what to look for.")},

    # ------------------------------------------------------------------ 9
    {**base,
     "slug": "online-yoga-classes-near-me-how-to-choose.html",
     "title": "Online yoga classes near me: how to choose",
     "standfirst": ("Live or recorded, solo or with a teacher watching: how "
                    "to pick an online yoga class that works for you."),
     "meta": ("Online yoga classes near me in Chennai: how to choose between "
              "live and recorded, what to check, and our Tamil and English classes."),
     "short": [
        "Live classes let a teacher see and correct you; recordings do not.",
        "Learning alone is linked with a higher risk of injury.",
        "Our online classes run at all four times, in Tamil and English.",
     ],
     "body": [
      ("Live or recorded",
       para("A recording is flexible and cheap to run, but nobody is watching "
            "you. A live class costs you a fixed time, but the teacher can "
            "see your posture and tell you what to change. The "
            + cite("nccih_safe", "NCCIH") + " notes that learning yoga on "
            "your own is linked with a higher risk of injury, which is a "
            "reason to prefer a teacher who can see you, especially at the "
            "start.")
       + photo("ima1", CAP1)),

      ("What to check",
       bullets([
        "Is the class live, and can the teacher see you?",
        "Is it taught in a language you follow?",
        "Is there a trial before you commit?",
        "What happens if you are injured or unsure of a pose?",
        "Can you move to in-person classes later?",
       ])),

      ("How ours work",
       para("Online classes run at all four times, from either centre, "
            "taught in Tamil and English by the same teachers and following "
            "the same batch structure as the room. You can switch between "
            "online and in person. For the full list of times see "
            + PERU + ".")
       + photo("ima5", CAP5)),

      ("Start here",
       para(TRIAL + " Mention that you want to start online and we will "
            "tell you which batch to join. Tell the teacher about any "
            "injury first, and check with your doctor.")),
     ],
     "related": ("online-or-in-person-yoga-how-to-decide.html",
                 "Online or in person yoga? How to decide",
                 "Which format fits your week.")},

    # ------------------------------------------------------------------ 10
    {**base,
     "slug": "online-or-in-person-yoga-how-to-decide.html",
     "title": "Online or in person yoga? How to decide",
     "standfirst": ("Both formats work. Which is better depends on your "
                    "week, your commute and how you learn."),
     "meta": ("Online or in-person yoga? How to decide, when each fits best, "
              "and how to switch between them at Happy Yogis in Chennai."),
     "short": [
        "In person suits beginners and anyone with an injury.",
        "Online suits bad-traffic days, travel and tight mornings.",
        "You can switch between them.",
     ],
     "body": [
      ("When in person works best",
       para("The first weeks, an injury or health condition, or any time you "
            "want hands-on adjustment. The teacher can see your whole body "
            "and the room keeps you consistent.")
       + photo("ima1", CAP1)),

      ("When online works best",
       para("A day when GST Road is not worth the drive, a week away, an "
            "early meeting, a long commute. Online classes run at all four "
            "times from either centre, so you do not have to change your "
            "batch.")),

      ("A mix is common",
       para("Many students combine the two: in person on most days, online "
            "on the days that do not work. Same teacher, same batch "
            "structure. If you have never done yoga before, spend your first "
            "weeks in the room if you can. See " + FIRST + ".")
       + photo("ima5", CAP5)),

      ("Switching",
       para("You can switch between online and in person. Tell the teacher "
            "so they know what to expect. " + TRIAL + " For a longer look at "
            "choosing online classes, read "
            + a("online-yoga-classes-near-me-how-to-choose.html",
                "online yoga classes near me: how to choose") + ".")),
     ],
     "related": ("online-yoga-classes-near-me-how-to-choose.html",
                 "Online yoga classes near me: how to choose",
                 "Live or recorded, and what to check.")},
    ]
    return posts
