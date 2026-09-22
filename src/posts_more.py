# -*- coding: utf-8 -*-
"""Four posts answering what people actually type into Google before joining.

Same rules as the rest of the journal: nothing claimed that the cited health
authorities do not support, no promised outcomes, no invented numbers, and
every batch time taken from content.BATCHES rather than retyped.
"""

def make(para, bullets, photo, qa, cite, DISCLAIMER):
    """Called by blog.py once its helpers exist."""
    return [

    # ------------------------------------------------------------------ 1
    {
     "slug": "how-often-should-you-do-yoga.html",
     "date": "2026-09-06", "date_text": "6 September 2026",
     "title": "How many days a week should you do yoga?",
     "standfirst": ("The honest answer is not the one that sounds most impressive. "
                    "Four ordinary mornings beat two heroic ones, and the number "
                    "you can keep is worth more than the number you can manage."),
     "meta": ("How often should you practise yoga? What a realistic week looks "
              "like, and why consistency beats intensity."),
     "photo": "ima24",
     "short": [
       "Three to four times a week is where most people see change.",
       "Twice a week still works. Once a week maintains, it does not build.",
       "Pick the number you can keep on a bad week, not a good one.",
     ],
     "body": [
      ("The number most people land on",
       para("Almost everyone who walks in asks some version of this, usually "
            "phrased as <em>how much is enough</em>. Three to four sessions a "
            "week is where most of our students settle, and it is where most of "
            "them start noticing something &mdash; sleeping better, standing "
            "straighter, getting out of a chair without thinking about it.",
            "Twice a week is not wasted. It is slower, and it holds ground rather "
            "than gaining much, but it is a real practice. Once a week is "
            "maintenance: pleasant, better than nothing, and unlikely to change "
            "how your back feels in March.")),

      ("Why the answer is not seven",
       para("Practising every single day sounds like the committed choice. In "
            "our experience it is the one most likely to end by week three. A "
            "schedule with no slack in it breaks the first time a child is ill "
            "or a deadline moves, and people rarely restart at five days &mdash; "
            "they restart at zero.",
            "The World Health Organization's guidance for adults is 150 to 300 "
            "minutes of moderate activity a week. Four hour-long batches sits "
            "inside that comfortably, without needing a perfect week to reach it. "
            + cite("who_pa", "WHO physical activity guidance")),
       ),

      ("Pick for your worst week, not your best",
       para("This is the only planning advice we give that reliably works. Do "
            "not choose the schedule you could keep in a calm month. Choose the "
            "one that survives a bad week &mdash; and then anything above it is "
            "a bonus rather than a failure.",
            "In practice that usually means committing to three, turning up four "
            "or five times when the week allows, and not treating a missed "
            "Tuesday as the end of the thing.")),

      ("What a realistic week looks like here",
       bullets("<strong>Three mornings.</strong> The most common pattern. Enough "
               "to build, easy enough to protect.",
               "<strong>Four or five.</strong> What people move to once the habit "
               "is set, usually without deciding to.",
               "<strong>Two, plus something at home.</strong> Works if the two "
               "are consistent. Ten minutes of breathing on the other days does "
               "more than an occasional long session.")
       + para("Batches run Monday to Friday, four times a day, so there is no "
              "single slot you have to defend. If you miss the 6:15 am, the "
              "5:00 pm exists.")),

      ("Does it have to be a class?",
       para("No, but a class is what most people actually turn up to. Practising "
            "alone asks you to supply the time, the sequence and the motivation; "
            "a batch at a fixed hour supplies two of the three. That is most of "
            "why attendance beats intention.",
            "It also means someone is watching your form. Doing the wrong thing "
            "three times a week is worse than doing the right thing twice.")),

      ("Common questions",
       qa([("Is 20 minutes a day better than an hour three times a week?",
            "For building a habit, yes. For building strength and mobility, the "
            "longer sessions do more, because a full hour has room for warm-up, "
            "asanas, pranayama and relaxation rather than a rushed version of "
            "each."),
           ("How soon will I feel a difference?",
            "Most of our students say they sleep better and feel less stiff "
            "within two or three weeks of practising regularly. That is our "
            "students talking, not a study. Physical changes take longer."),
           ("Should I practise if I am sore?",
            "Mild stiffness, yes &mdash; it usually eases within the warm-up. "
            "Sharp or joint pain, no. Tell the teacher instead and the practice "
            "gets adjusted."),
           ("Can I come every day if I want to?",
            "Yes. Batches run five days a week and plenty of members come to all "
            "five. We would rather you built up to it than started there.")])),
     ],
     "related": ("what-happens-in-your-first-yoga-class.html",
                 "What happens in your first yoga class",
                 "What to wear, what to bring, and what the hour actually involves."),
    },

    # ------------------------------------------------------------------ 2
    {
     "slug": "yoga-or-gym-which-should-you-pick.html",
     "date": "2026-09-06", "date_text": "6 September 2026",
     "title": "Yoga or the gym? An honest comparison",
     "standfirst": ("We teach yoga, so treat this with the suspicion it deserves "
                    "&mdash; and then read the part where the gym wins, because "
                    "there is one."),
     "meta": ("Yoga or gym, compared honestly by a Chennai yoga centre. Where "
              "each genuinely wins, and why the question is usually wrong."),
     "photo": "ima3",
     "short": [
       "For maximum strength or muscle size, the gym wins. Plainly.",
       "For mobility, breathing, sleep and joints, yoga does more.",
       "The real question is which one you will still be doing in month six.",
     ],
     "body": [
      ("Where the gym genuinely wins",
       para("If your goal is maximum strength or visible muscle, go to a gym. "
            "Progressive loading with weights does that better than yoga does, "
            "and no amount of loyalty to our own practice changes it. The same "
            "goes for training a specific sport, or rehabilitating under a "
            "physiotherapist who has given you a barbell programme.",
            "Anyone at a yoga centre who tells you otherwise is selling "
            "something.")),

      ("Where yoga does more",
       bullets("<strong>Mobility.</strong> Hips, spine and shoulders through "
               "their full range, rather than through the range one machine allows.",
               "<strong>Breathing.</strong> Pranayama is part of the hour, not "
               "something you are told to do later at home.",
               "<strong>Joints.</strong> Nothing in the practice pounds the "
               "knees, which matters if you are carrying extra weight right now.",
               "<strong>Sleep and stress.</strong> The closing relaxation is the "
               "part our students most often say changed something.")),

      ("The comparison that actually decides it",
       para("Not calories per hour. Attendance in month six.",
            "A gym membership taken in January and abandoned by April is a "
            "Chennai institution. The reasons are rarely about the exercise: it "
            "is far away, the equipment is occupied, nobody notices whether you "
            "came, and there is no fixed hour that expects you.",
            "A small batch ten minutes from home, at a set time, where the "
            "teacher knows your name and notices your absence, is a different "
            "proposition. Not a better workout on paper &mdash; a better bet on "
            "actually being done a year from now.")),

      ("The heat, which nobody accounts for",
       para("Outdoor running or walking is unpleasant for a good part of the "
            "year here, and the months you give it up are the months the habit "
            "dies. An indoor hall at half past five in the morning works in "
            "April as well as it works in December.")),

      ("You do not have to choose",
       para("Plenty of our students lift weights twice a week and practise here "
            "three times. That combination is better than either alone: the gym "
            "loads the muscle, the practice keeps the joints and the breath "
            "working, and the two do not compete for the same recovery.",
            "If you can only do one, pick the one you will keep.")),

      ("Common questions",
       qa([("Is yoga enough exercise on its own?",
            "For mobility, posture, breathing and general health, yes &mdash; a "
            "regular practice sits comfortably inside the WHO's activity "
            "guidance. For maximum strength, no. " + cite("who_pa", "WHO physical activity guidance")),
           ("Will yoga build muscle?",
            "It builds usable strength, particularly in the shoulders, core and "
            "legs, and the faster sun-salutation practice is genuinely "
            "demanding. It will not build size the way progressive weight "
            "training does."),
           ("Which burns more calories?",
            "The gym, for most sessions. We have never thought that was the "
            "interesting question."),
           ("Can I do both in the same week?",
            "Yes, and many do. Tell the teacher what else you are training so "
            "the practice complements it rather than duplicating it.")])),
     ],
     "related": ("yoga-for-weight-loss-in-chennai.html",
                 "Yoga for weight loss in Chennai, honestly",
                 "What the practice changes, how long it takes, and the half of the problem yoga cannot solve."),
    },

    # ------------------------------------------------------------------ 3
    {
     "slug": "morning-or-evening-yoga-class.html",
     "date": "2026-09-06", "date_text": "6 September 2026",
     "title": "Morning or evening? Choosing your batch",
     "standfirst": ("Four times a day, five days a week. Which one suits you has "
                    "less to do with yoga than with your commute, your sleep and "
                    "who else is in the room."),
     "meta": ("Morning or evening yoga class? Choosing between our 5:30 am, "
              "6:15 am, 10:00 am and 5:00 pm batches in New Perungalathur."),
     "photo": "ima20",
     "short": [
       "Morning suits people who want it done before the day starts.",
       "The 10:00 am batch is women only. The other three are for everyone.",
       "The best batch is the one you can reach on a bad week.",
     ],
     "body": [
      ("There is no better time, only a better fit",
       para("People expect this answer to be <em>morning</em>, and plenty of "
            "traditions say so. In practice the batch that works is the one you "
            "can reach without rearranging your life, and the difference between "
            "a 5:30 am practice and a 5:00 pm practice matters far less than the "
            "difference between practising and not.",
            "So the useful question is not when yoga works best. It is when "
            "<em>you</em> work best, and what your week actually allows.")),

      ("The early batch, 5:30 am",
       para("Forty-five minutes, and mostly people who want it finished before "
            "the day starts. It is the quietest hour in the hall and the "
            "coolest part of the day, which in Chennai is not a small thing.",
            "It suits you if you already wake early, or if your day becomes "
            "unpredictable after eight. It does not suit you if you are "
            "regularly getting five hours of sleep &mdash; borrowing from sleep "
            "to practise is a poor trade.")),

      ("The busiest hour, 6:15 am",
       para("An hour, and our most mixed batch: school children, people fitting "
            "a session in before the commute, homemakers, retired members. If "
            "you are nervous about being the least flexible person in the room, "
            "this is the batch where that stops mattering fastest, because "
            "everyone is visibly doing a different version of the same pose.",
            "It is the one most beginners choose, and the one we suggest if you "
            "have no particular constraint.")),

      ("Mid-morning, 10:00 am, women only",
       para("An hour, and the one exception to our mixed batches. It is popular "
            "with homemakers and with anyone on a shift pattern, and for a "
            "number of our students the fact that it is women only is the "
            "difference between attending and not.",
            "Practice here is adapted around PCOD, thyroid and hormonal health "
            "the same way it is in every other batch &mdash; the difference is "
            "the room, not the syllabus.")),

      ("Evening, 5:00 pm",
       para("An hour, and the batch a lot of school and college students come "
            "to, along with people whose mornings are simply not negotiable. "
            "The room is warmer and bodies are looser than at 5:30 am, which "
            "makes some postures easier.",
            "If you sleep badly, this is often the batch worth trying: the "
            "closing relaxation lands a few hours before bed rather than at "
            "the start of the day.")),

      ("A practical way to decide",
       bullets("Which time could you reach on a <em>bad</em> week? Start there.",
               "Do you need the practice to be done before work, or to unwind "
               "after it?",
               "Are you sleeping enough to get up for 5:30 am without cutting "
               "sleep short?",
               "Would a women-only room make you more likely to come?")
       + para("The 3-day trial exists for exactly this. Come three times, at "
              "whichever hour you could keep to, and see how the fourth morning "
              "feels before deciding.")),

      ("Common questions",
       qa([("Can I switch batches later?",
            "Yes. Students move between them as work and school terms change. "
            "Tell us and we will make sure there is room."),
           ("Is it bad to practise on a full stomach?",
            "Come on a reasonably empty stomach, ideally two hours after a "
            "meal. This is the main practical argument for a morning batch."),
           ("Which batch is best for beginners?",
            "Any of them &mdash; every batch is mixed ability. Most beginners "
            "pick the 6:15 am or the 5:00 pm."),
           ("Do you teach at weekends?",
            "No. Batches run Monday to Friday, and the centre is closed "
            "Saturday, Sunday and public holidays.")])),
     ],
     "related": ("what-happens-in-your-first-yoga-class.html",
                 "What happens in your first yoga class",
                 "What to wear, what to bring, and what the hour actually involves."),
    },

    # ------------------------------------------------------------------ 4
    {
     "slug": "yoga-for-back-pain-chennai.html",
     "date": "2026-09-06", "date_text": "6 September 2026",
     "title": "Yoga for back pain, carefully",
     "standfirst": ("A desk, a commute up the GST Road and years of no "
                    "stretching is the most common back in our hall. Here is "
                    "what a practice can do about it, and where it stops."),
     "meta": ("Yoga for back pain in Chennai. What the evidence supports, how "
              "we adapt practice for a bad back, and when to see a doctor."),
     "photo": "ima7",
     "short": [
       "Evidence supports yoga for chronic low-back pain, modestly.",
       "Tell the teacher before your first class so it can be adapted.",
       "Sudden, severe or radiating pain is a doctor's question, not ours.",
     ],
     "body": [
      ("Read this part first",
       para("Back pain has many causes and some of them need a doctor rather "
            "than a yoga mat. If your pain came on suddenly, is severe, follows "
            "an injury, runs down a leg, or comes with numbness, weakness or "
            "any change in bladder or bowel control, see a doctor before you do "
            "anything else. None of that is something a class should be working "
            "around unassessed.",
            "What follows is about the ordinary, grumbling, long-standing back "
            "&mdash; the kind that has been there for months and gets worse "
            "after a long day sitting.")),

      ("What the evidence actually says",
       para("Reviews of yoga for chronic low-back pain are cautiously positive: "
            "modest improvements in pain and function, with the honest caveat "
            "that the quality of the studies varies and the effect is not "
            "dramatic. That is a real result, and it is also a smaller claim "
            "than most pages selling this will make. "
            + cite("nccih_pain", "NCCIH on yoga for pain")),
       ),

      ("The Chennai back",
       para("The most common back we see is not injured. It is a desk, an hour "
            "on a two-wheeler or standing in a suburban train carriage, and "
            "years of no stretching. That combination shortens the hip flexors, "
            "locks the lower back and rounds the upper back until the head "
            "carries forward.",
            "That pattern responds well to practice, because the practice works "
            "on the cause rather than the ache: hip openers to release what the "
            "commute tightens, spinal movement in every direction, and standing "
            "postures that rebuild the support the chair removed.")),

      ("How we adapt it",
       bullets("Forward folds are done with bent knees and a long spine, never "
               "rounded and forced.",
               "Twists are led from the upper back, kept gentle, and never "
               "pushed to a maximum.",
               "Back-bending shapes such as cobra are kept low and short at "
               "first, and built up over weeks.",
               "Props and wall support are used wherever they help, which is "
               "more often than people expect.")
       + para("Tell the teacher before your first class. It changes what you "
              "will be asked to do, and it is the whole reason a small batch "
              "can adapt at all.")),

      ("What it will not do",
       para("It will not fix a structural problem, replace physiotherapy, or "
            "work in a fortnight. Yoga supports treatment; it does not replace "
            "it. If you are under medical care for your back, stay under it and "
            "keep your doctor in the loop.",
            "What a regular practice can realistically offer is a back that is "
            "stiff less often, hips that give more, and a stronger set of "
            "muscles holding the whole thing up.")),

      ("Common questions",
       qa([("Should I practise while my back hurts?",
            "Mild, familiar stiffness, usually yes, with the practice adapted. "
            "New, sharp or radiating pain, no &mdash; get it looked at first."),
           ("Is a slipped disc a reason not to come?",
            "It is a reason to talk to your doctor first and to tell the "
            "teacher exactly what you have been told. Some movements will be "
            "left out."),
           ("How long before it helps?",
            "Most of our students report feeling less stiff within a few weeks "
            "of practising regularly. Pain that has been there for years does "
            "not resolve on that timescale."),
           ("Which batch should I join?",
            "Any of them. Every batch is mixed ability and the practice is "
            "adjusted person by person &mdash; a bad back is one of the most "
            "common things we adapt around.")])),
     ],
     "related": ("hatha-yoga-in-chennai.html",
                 "Hatha yoga in Chennai for a working week",
                 "What the practice is, why it suits desk work and long commutes."),
    },
    ]
