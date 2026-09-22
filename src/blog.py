#!/usr/bin/env python3
"""Yogi's Upadesha: the index page and the posts.

The owner asked for structure only, no real posts. The single post below is
written from facts already confirmed for the site (batch times, what a class
contains, the trial) so it is publishable as-is rather than lorem filler.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build import (head, nav, footer, SCRIPT, icon, wa, BASE, PHONE_TEXT,
                   PHONE_HREF, JOURNAL, JOURNAL_PLAIN)
import content as C

# The site root, derived from this file's location so a clone works
# wherever it sits. HAPPY_YOGIS_ROOT overrides it if ever needed.
OUT = os.environ.get("HAPPY_YOGIS_ROOT") or os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

P = 'mt-4 text-[16px] leading-relaxed text-ink/80'
UL = ('mt-4 space-y-2.5 text-[16px] leading-relaxed text-ink/80 '
      'list-disc pl-5 marker:text-muted')


def para(*paragraphs):
    """Body copy. Each argument is one paragraph."""
    return "\n".join(f'            <p class="{P}">{t}</p>' for t in paragraphs)


def bullets(*items):
    lis = "\n".join(f"                <li>{t}</li>" for t in items)
    return f'            <ul class="{UL}">\n{lis}\n            </ul>'


def dims(key):
    """Real intrinsic size. A guessed height reserves the wrong box and the
    article reflows the moment the photo lands."""
    from PIL import Image
    return Image.open(os.path.join(OUT, f"{key}.jpeg")).size


def photo(key, caption=None):
    cap = (f'\n                <figcaption class="mt-2.5 text-[13px] text-muted">'
           f'{caption}</figcaption>' if caption else "")
    return f"""            <figure class="mt-8">
                <div class="rounded zoom grade">
                <picture>
                    <source type="image/webp" sizes="(min-width:768px) 720px, 92vw"
                            srcset="{key}-xs.webp 320w, {key}-sm.webp 640w, {key}-md.webp 768w, {key}.webp {dims(key)[0]}w">
                    <source type="image/jpeg" sizes="(min-width:768px) 720px, 92vw"
                            srcset="{key}-xs.jpg 320w, {key}-sm.jpg 640w, {key}-md.jpg 768w, {key}.jpeg {dims(key)[0]}w">
                    <img src="{key}.jpeg" width="{dims(key)[0]}" height="{dims(key)[1]}" alt="{C.PHOTOS[key]}"
                         class="w-full rounded" loading="lazy" decoding="async">
                </picture>
                </div>{cap}
            </figure>"""


# Sources are health-authority and government pages only, chosen because a
# yoga centre writing about PCOD, sleep or body weight is writing health
# content, and Google weighs what such a page cites. Every claim in the posts
# stays inside what these pages actually support - "may help", not "will fix".
SOURCES = {
    "nccih":      ("https://www.nccih.nih.gov/health/yoga-effectiveness-and-safety",
                   "US National Center for Complementary and Integrative Health"),
    "nccih_safe": ("https://www.nccih.nih.gov/health/tips/things-you-should-know-about-yoga",
                   "NCCIH, 5 things to know about yoga"),
    "nccih_pain": ("https://www.nccih.nih.gov/health/providers/digest/yoga-for-pain",
                   "NCCIH, yoga for pain"),
    "who_pa":     ("https://www.who.int/news-room/fact-sheets/detail/physical-activity",
                   "World Health Organization, physical activity"),
    "nichd_pcos": ("https://www.nichd.nih.gov/health/topics/pcos/conditioninfo/treatments",
                   "US National Institute of Child Health and Human Development"),
    "ayush":      ("https://yoga.ayush.gov.in/",
                   "Ministry of Ayush, Government of India"),
    "un_yoga":    ("https://www.un.org/en/observances/yoga-day",
                   "United Nations, International Day of Yoga"),
}


def cite(key, text):
    """An outbound citation. Arrowed, because on this site an arrow means the
    link leaves the site."""
    url, name = SOURCES[key]
    return (f'<a href="{url}" target="_blank" rel="noopener" title="{name}" '
            f'class="text-blue font-medium hover:underline">{text}'
            f'{icon("arrow-up-right", "w-3.5 h-3.5 inline-block align-[-1px] ml-0.5")}</a>')


# Shown at the foot of every post. It has to agree with the Health Disclaimer
# and Limitation of Liability clauses already in the terms of service - a note
# here that contradicted those would be worse than no note at all.
DISCLAIMER = """
        <aside class="mt-14 border-t border-line pt-6" aria-labelledby="health-note">
            <h2 id="health-note" class="text-[13.5px] font-medium text-ink">A note on health information</h2>
            <div class="mt-2.5 space-y-2.5 text-[13.5px] leading-relaxed text-muted max-w-2xl">
                <p>
                    This article is general information about yoga as we teach it at Happy
                    Yogis Yoga Centre. It is not medical advice, not a diagnosis and not a
                    treatment plan, and it is not a substitute for care from a qualified
                    doctor. Nothing here is a promise of any particular result &mdash; what a
                    practice does for one person it may not do for another.
                </p>
                <p>
                    If you are pregnant, recovering from an injury or surgery, or under
                    treatment for any condition &mdash; including PCOD, a thyroid condition,
                    blood pressure, heart or joint problems &mdash; speak to your doctor
                    before starting yoga and keep them informed. Tell your teacher as well,
                    before your first class, so the practice can be adapted. Stop, and seek
                    medical attention, if you feel pain, dizziness or breathlessness in class.
                </p>
                <p>
                    Our teachers give yoga instruction. They do not diagnose conditions,
                    prescribe treatment, or give dietary or medical advice, and students
                    practise within their own limits and at their own risk. Our
                    <a href="terms-of-service.html" class="underline hover:text-ink">terms of
                    service</a> set out the health disclaimer and limitation of liability
                    that apply.
                </p>
            </div>
        </aside>"""


def qa(pairs):
    rows = "\n".join(f"""                <div class="border-t border-line py-5">
                    <dt class="display text-d3 text-ink">{q}</dt>
                    <dd class="mt-2 text-[15.5px] leading-relaxed text-ink/80">{a}</dd>
                </div>""" for q, a in pairs)
    return f'            <dl class="mt-6 border-b border-line">\n{rows}\n            </dl>'



POSTS = [{
    "slug": "what-happens-in-your-first-yoga-class.html",
    "short": [
        "Wear anything you can move in. Bring a mat if you have one.",
        "The hour is warm-up, then postures, then breathing, then lying still.",
        "Nobody is pushed past what their body will do that day.",
    ],
    "title": "What happens in your first yoga class",
    "meta": ("What to expect in your first class at Happy Yogis in New Perungalathur "
             "- what to wear, what to bring, and what the hour actually involves."),
    "date": "2026-08-31",
    "date_text": "31 August 2026",
    "standfirst": ("The most common thing people tell us before their first class is that "
                   "they are worried about being the least flexible person in the room. "
                   "Here is what actually happens."),
    "photo": "ima1",
    "related": ("yoga-for-weight-loss-in-chennai.html",
                "Yoga for weight loss in Chennai, honestly",
                "What sun salutations actually do, how long it really takes, and the "
                "half of the problem a yoga hall cannot solve for you."),
    "body": [
        ("Before you arrive",
         "Wear something you can move in &mdash; that is the entire dress "
         "code. Bring a mat if you own one; if not, tell us beforehand. Come "
         "on a reasonably empty stomach, ideally two hours after a meal, and "
         "arrive five minutes early."),
        ("The first ten minutes",
         "Every batch opens with warm-up: joint rotations, gentle stretches, "
         "settling the breath. None of it requires any flexibility. This is "
         "also when the teacher asks whether anyone is working around an "
         "injury or a health condition, so say so &mdash; it changes what you "
         "will be asked to do. Practising under a teacher who knows what you "
         "are working with is the"
         + cite("nccih_safe", "standard safety advice") + " for starting yoga, and it is "
         "the reason we ask."),
        ("The middle of the class",
         "Then asanas &mdash; the postures. In a mixed batch you will see the "
         "same pose at three different depths, and that is the point: you do "
         "the version your body will do today. Nobody is pushed into "
         "something they are not ready for, and nobody is watching you."),
        ("How it ends",
         "Last comes pranayama and relaxation: breathing practice, then a few "
         "minutes lying still. Plenty of students say this is the part they "
         "came back for. You will leave looser than you arrived, and probably "
         "more awake."),
        ("What it costs to find out",
         "We run a 3-day trial so you can sit in on a batch before committing to "
         "anything. Message us on WhatsApp and we will tell you which of the four "
         "batches has room."),
    ],
}, {
    "slug": "hatha-yoga-in-chennai.html",
    "short": [
        "Hatha is postures, breathing and relaxation &mdash; held, not rushed.",
        "It suits Chennai heat, a GST Road commute and desk-bound shoulders.",
        "Four batches, Monday to Friday, taught in Tamil or English.",
    ],
    "title": "Hatha yoga in Chennai for a working week",
    "meta": ("Hatha yoga at Happy Yogis in New Perungalathur, Chennai - what the practice "
             "is, why it suits desk work and long commutes, and which batch fits your day."),
    "date": "2026-09-01",
    "date_text": "1 September 2026",
    "standfirst": ("Most people who walk into our hall in New Perungalathur "
                   "are not after a workout. They have a desk job, a commute "
                   "up the GST Road, a stiff lower back and five or six hours "
                   "of sleep. Hatha yoga suits that life, and this is how we "
                   "teach it."),
    "photo": "ima5",
    "related": ("international-yoga-day-beach.html",
                "International Yoga Day on the beach",
                "The morning we took the whole centre out of the hall and onto the "
                "sand, in photographs."),
    "body": [
        ("What hatha yoga actually is", para(
            "Hatha is the " + cite("ayush", "branch of yoga") + " almost everyone in "
                                                                "India has already "
                                                                "met, named or not. "
                                                                "It is three things "
                                                                "practised in order: "
                                                                "<em>asana</em>, the "
                                                                "postures; "
                                                                "<em>pranayama</em>, "
                                                                "the breathing; and "
                                                                "relaxation. Postures "
                                                                "are held rather than "
                                                                "rushed, the breath "
                                                                "sets the pace, and "
                                                                "the class finishes "
                                                                "lying still instead "
                                                                "of out of breath.",
            "That is the shape of every batch at our centre in Chennai "
            "&mdash; warm-up, asanas, pranayama, relaxation. Not because it "
            "is fashionable, but because it is the version a person can do at "
            "half past five in the morning, five days a week, for years, "
            "without being an athlete to begin with.",
            "Be clear about what it is not. Hatha is not a heated room, not a "
            "fast flow you chase for forty minutes, not a class you are "
            "expected to keep up with. If you have stayed away from yoga "
            "classes in Chennai because the ones you saw looked like a gym "
            "session set to music, this is the other thing.")),

        ("Why it suits a Chennai working week",
            para("Chennai hands a body a specific set of problems, and they are not the "
                 "ones a generic fitness plan is built for.",
                 "<strong>The heat.</strong> For most of the year this city "
                 "does not need your core temperature raised further. A "
                 "practice that holds postures and lengthens the breath "
                 "leaves you steady rather than wrung out &mdash; which "
                 "matters with a full working day still ahead. Hence batches "
                 "at either end of the day: early morning, before the heat, "
                 "and five in the evening, after it.")
            + bullets(
                "<strong>The commute.</strong> An hour on a two-wheeler or "
                "standing in a suburban train carriage, five days a week, "
                "tightens the hip flexors and shortens the front of the body. "
                "Hip openers and spinal movement answer that directly.",
                "<strong>The desk.</strong> Screen work rounds the upper back "
                "and pushes the head forward. Standing postures and "
                "back-bends such as cobra work against that pattern rather than "
                "around it. Low-back and neck pain are the areas where the" + cite("nccih_pain", "evidence for yoga is "
                "strongest") + ", though how much it helps varies from person to person.",
                "<strong>The sleep.</strong> Pranayama and the closing "
                "relaxation are what students most often say changed "
                "something: better sleep and less stiffness within two or "
                "three weeks of practising regularly. That is our students "
                "talking, not a study &mdash; though the" + cite("nccih", "US National Center for Complementary and "
                "Integrative Health") + ", which reviews the research, reports that yoga "
                "may help with sleep and with stress.")
            + para("None of this is unique to yoga &mdash; walking and "
                   "swimming are good for you too. What hatha adds is that "
                   "the breathing and the stillness are inside the hour, not "
                   "something you are told to do later at home, which nobody "
                   "does.")),

        ("What an hour in the hall contains",
            para("The batches are mixed. On a normal morning school children, "
                 "people on their way to an office, homemakers and retired "
                 "members share the mats, all doing the same practice at "
                 "whatever depth their body gives that day.")
            + bullets(
                "<strong>Warm-up.</strong> Joint rotations and gentle stretches, usually "
                "including cat-and-cow through the spine. Nothing in this part asks for "
                "any flexibility at all.",
                "<strong>Asanas.</strong> Standing postures such as tree pose, forward "
                "folds, downward dog, cobra and seated twists. When the practice is built "
                "around stamina it runs through sun salutations instead.",
                "<strong>Pranayama.</strong> Seated breathing practice. Several students "
                "arrived for the postures and now say this is the part they would not "
                "skip.",
                "<strong>Relaxation.</strong> A few minutes lying still at the end. It is "
                "not padding; it is where the practice settles.")
            + photo("ima7", "A seated spinal twist &mdash; one of the shapes that answers "
                            "a week of desk work.")
            + para("Karthika takes every batch herself and has practised and "
                   "taught for more than ten years. Batches stay small enough "
                   "that she knows what each person is working with &mdash; "
                   "the whole reason the practice can be adapted rather than "
                   "simply delivered.")),

        ("Choosing a batch around your day",
            para("There are four batches, Monday to Friday. Which one is right is usually "
                 "decided by your commute rather than by your yoga.")
            + bullets(
                "<strong>5:30 &ndash; 6:15 am, 45 minutes.</strong> The short early "
                "batch, for people who have to be out of the house first.",
                "<strong>6:15 &ndash; 7:15 am, 60 minutes.</strong> The busiest hour, and "
                "where most beginners start.",
                "<strong>10:00 &ndash; 11:00 am, 60 minutes, ladies only.</strong> "
                "Mid-morning, after the school run and before the afternoon.",
                "<strong>5:00 &ndash; 6:00 pm, 60 minutes.</strong> The evening batch, "
                "for anyone whose mornings are not negotiable.")
            + para('We also teach the same practice online, and students move between '
                   'online and in-person as their week allows &mdash; useful in a city '
                   'where one bad evening on the road costs you an hour. You can see '
                   'which batch is next on the <a href="/#schedule" '
                   'class="text-blue font-medium hover:underline">schedule on the '
                   'homepage</a>, and there is a 3-day trial so you can sit in before '
                   'deciding anything.')),

        ("Practising around what you arrive with",
            para("A good number of students come to us because a doctor suggested it. The "
                 "practice is planned around the condition rather than in spite of it.")
            + bullets(
                "PCOD and hormonal health, sequenced at a manageable pace",
                "Thyroid support, through breathing and chosen movement",
                "Knee and joint pain, worked low-impact and with support",
                "Back and spine &mdash; posture correction and spinal strengthening, the "
                "most common request we get from desk workers",
                "Pregnancy care, guided and adjusted by stage",
                "Stress and sleep, for students who arrive wound up")
            + para("Tell us before your first class so the teacher can plan "
                   "around it. And to be plain: yoga supports treatment, it "
                   "does not replace it. If you are under medical care, keep "
                   "your doctor in the loop.")),

        ("Taught in Tamil and in English", para(
            "Instructions come in whichever language the batch is comfortable "
            "with, Tamil or English &mdash; how a hall in Chennai with three "
            "generations on the mats has to work. Children practise alongside "
            "their parents in the morning and evening batches, not in a "
            "separate class. Families arrive together, and the practice is "
            "old enough in Tamil Nadu that somebody's grandmother in the room "
            "usually knows what pranayama is without being told.",
            "Every student is given a Happy Yogis t-shirt, and once you join you can "
            "leave your mat at the centre instead of carrying it in every day.")),

        ("Where we are, and who travels in", para(
            "We teach from a single hall in SSM Nagar, New Perungalathur "
            "&mdash; just off the GST Road stretch between Tambaram and "
            "Vandalur, close to Perungalathur railway station. No other "
            "branches, no franchise: one centre, one teacher.",
            'Students travel in from Old Perungalathur, East and West Tambaram, '
            'Selaiyur, Chromepet, Vandalur, Urapakkam, Guduvanchery and Medavakkam. If '
            'you are looking for <a href="yoga-classes-perungalathur.html" '
            'class="text-blue font-medium hover:underline">yoga classes in '
            'Perungalathur</a> or a <a href="yoga-classes-tambaram.html" '
            'class="text-blue font-medium hover:underline">yoga centre near Tambaram</a>, '
            'those two pages cover getting here from either side. Anyone further out, or '
            'with an unpredictable week, takes the same batches online.')),

        ("Questions people ask before they start", qa([
            ("Do I need to be flexible?",
             "No, and it is the most common worry we hear. Most people who join cannot "
             "touch their toes on day one. Flexibility is what the practice builds; it is "
             "not what it asks for."),
            ("Is hatha yoga enough on its own?",
             "For mobility, posture, breathing and sleep, it does the work. "
             "If your goal is specifically losing weight, the faster "
             "sun-salutation practice is taught inside the regular batches "
             "&mdash; there is no separate course to book."),
            ("Which batch should a complete beginner join?",
             "Any of them. Every batch is mixed ability and the practice is adjusted "
             "person by person. Most beginners pick the 6:15 am or the 5:00 pm batch."),
            ("Can men join?",
             "Yes. The 5:30 am, 6:15 am and 5:00 pm batches are for everyone. The 10:00 "
             "am batch is women only."),
            ("What happens if I miss a week?",
             "You pick it up again. Nobody is behind, because the practice is adapted to "
             "the person rather than run as a syllabus."),
        ])),

        ("Where to start", para(
            "If you have read this far, the useful next step is not more "
            "reading. Come to one class, at whichever of the four times you "
            "could keep to, and see what an hour of hatha yoga does to a "
            "Chennai working day. The 3-day trial exists for that.")),
    ],
}, {
    "slug": "yoga-for-weight-loss-in-chennai.html",
    "short": [
        "Yoga is not the fastest calorie burn. It is the one people keep doing.",
        "Sun salutations and standing sequences are the practice for stamina.",
        "Better sleep in two or three weeks; physical change takes months.",
    ],
    "title": "Yoga for weight loss in Chennai, honestly",
    "meta": ("Yoga for weight loss at Happy Yogis in New Perungalathur, Chennai - what sun "
             "salutations actually do, how long it really takes, and which batch to join."),
    "date": "2026-09-01",
    "date_text": "1 September 2026",
    "standfirst": ("Search for yoga for weight loss in Chennai and you are "
                   "promised a number: so many kilos, in so many weeks. We "
                   "will not do that. Here is what the practice changes, how "
                   "long it takes, and the half of the problem yoga cannot "
                   "solve for you."),
    "photo": "ima3",
    "related": ("hatha-yoga-in-chennai.html",
                "Hatha yoga in Chennai for a working week",
                "What the practice is, why it suits desk work and long commutes, and "
                "which of the four batches fits your day."),
    "body": [
        ("Start with what yoga is not", para(
            "Yoga is not the most efficient calorie burner available to you. "
            "If maximum calories per hour were the only thing that mattered, "
            "running would beat it, and so would swimming. For scale, the"
            + cite("who_pa", "World Health Organization") + " asks adults for at least 150 "
            "minutes of moderate activity a week; five hour-long batches clear that, but "
            "an hour of yoga is not an hour of running and we are not going to pretend "
            "otherwise.",
            "What yoga has instead is a far better record on the thing that "
            "decides whether anyone loses weight: still doing it in month "
            "six. The gym membership taken in January and abandoned by April "
            "is a Chennai institution. A 6:15 am batch ten minutes away, in a "
            "hall where nobody watches you and the teacher knows your name, "
            "is a different proposition from a treadmill you motivate "
            "yourself onto alone.",
            "So, honestly: yoga will not melt fat off you in a fortnight. It "
            "builds a practice you keep, strength you did not have, and "
            "control over how you eat and sleep &mdash; and those, over "
            "months, are what change your weight.")),

        ("What the weight-loss practice actually is",
            para("For students whose main goal is losing weight and building stamina, the "
                 "practice runs faster and is built around <strong>sun salutations</strong> "
                 "&mdash; surya namaskar &mdash; and standing sequences.")
            + para("A sun salutation is a linked round of postures moved "
                   "through with the breath: forward fold, lunge, a "
                   "plank-like position, cobra, downward dog, and back up. Done "
                   "slowly it is a mobility sequence; done in rounds, at "
                   "pace, it is cardiovascular work that also loads the "
                   "shoulders, core and legs. Hence its place at the centre "
                   "of almost every weight-focused yoga practice in India.")
            + bullets(
                "<strong>It scales.</strong> Beginners do a handful of rounds "
                "with the knees down. Later the same sequence, more rounds "
                "and a steadier breath, is genuinely demanding. You are not "
                "moved to a harder class; the same practice gets harder as "
                "you do.",
                "<strong>It builds, not just burns.</strong> Standing postures held "
                "properly are strength work. Muscle you keep is the part of this that "
                "still helps you a year later.",
                "<strong>It is joint-friendly.</strong> Nothing in it pounds "
                "the knees, which matters if you are carrying extra weight "
                "&mdash; the point at which running is hardest on you is "
                "exactly when you most want to be moving.",
                "<strong>It ends with breathing.</strong> Every batch closes with "
                "pranayama and relaxation, and the effect that has on stress eating and "
                "on sleep is not a side note. It may be the most useful part.")
            + para("On weight itself, the " + cite("nccih", "NCCIH's summary of the "
                   "research") + " is measured rather than enthusiastic: "
                                 "reviews have found yoga associated with "
                                 "reductions in body weight and BMI, while "
                                 "noting the quality of the evidence varies. "
                                 "Measured is the right word, and the tone we "
                                 "would rather take than the one on most "
                                 "pages selling this.")),

        ("The Chennai part of the problem",
            para("The obstacles here are specific, and worth naming.")
            + bullets(
                "<strong>The heat.</strong> Outdoor running or walking is "
                "unpleasant for much of the year, and the months you give it "
                "up are the months the habit dies. An indoor hall at half "
                "past five in the morning works in April as well as December.",
                "<strong>The commute.</strong> If your evening is an hour on the GST Road, "
                "an evening workout loses to traffic more often than it wins. A 45-minute "
                "5:30 am batch is finished before the road wakes up.",
                "<strong>The food.</strong> A rice-heavy plate three times a "
                "day, tiffin in the evening and sweet filter coffee is not a "
                "moral failing; it is just a lot of carbohydrate. It is also "
                "the half a yoga hall cannot fix for you.")
            + para("On that we would rather be blunt than sell you something. "
                   "A yoga centre is not a nutrition clinic. We teach the "
                   "practice; what goes on your plate is between you, your "
                   "doctor and a dietitian if you need one. Anybody promising "
                   "weight loss from an hour of exercise while saying nothing "
                   "about food is selling.")),

        ("How it fits into the batches",
            para("There is no separate weight-loss course and no package to "
                 "buy. All of it is taught inside the regular batches: tell "
                 "the teacher what you are working towards and she builds it "
                 "into your practice.")
            + para("That is possible because the batches stay small. On any morning the "
                   "same room holds a school child, someone heading to an office, a "
                   "homemaker and a retired member &mdash; and the person next to you "
                   "working on mobility after a knee problem is doing a different version "
                   "of the same sequence than the person working on stamina. Karthika "
                   "takes every batch herself and has been teaching for more than ten "
                   "years, which is what makes that practical rather than theoretical.")
            + photo("ima6", "The same standing posture, held by a room of different bodies "
                            "at different depths.")),

        ("Weight, PCOD and thyroid",
            para("Many of the women who ask us about weight are really asking "
                 "about something underneath it. PCOD and thyroid conditions "
                 "are common, make weight harder to shift, and are often the "
                 "reason someone starts.")
            + para("So we adapt the practice: for PCOD, work sequenced around "
                   "hormonal balance at a manageable pace; for thyroid, "
                   "breathing and movement chosen with that in mind. The "
                   "10:00 to 11:00 am batch is women only, which for many "
                   "students is the difference between attending and not.")
            + para("Lifestyle changes, including physical activity, sit among the "
                   + cite("nichd_pcos", "recognised treatments for PCOS") + " alongside "
                   "medication &mdash; which is exactly why we describe the practice as "
                   "supporting your treatment rather than being it.")
            + photo("ima10", "The ladies-only mid-morning batch.")
            + para("What we will not tell you is that yoga treats either "
                   "condition. It does not. Yoga supports treatment, it does "
                   "not replace it &mdash; if you are under medical care for "
                   "a thyroid condition, for PCOD, or for anything else, stay "
                   "under it and keep your doctor in the loop. Tell us before "
                   "your first class so the practice can be planned around "
                   "it.")),

        ("What changes, and when",
            para("Here is the timeline we actually see, rather than the one that makes a "
                 "better advertisement.")
            + bullets(
                "<strong>The first two or three weeks.</strong> Most students say they "
                "sleep better and feel less stiff. Nothing on the scale yet.",
                "<strong>After that.</strong> Stamina, and the first postures that were "
                "impossible in week one. Clothes fitting differently is usually noticed "
                "before the scale moves meaningfully.",
                "<strong>Months, not weeks.</strong> Physical change is slower than "
                "anybody wants it to be. That is true of every honest exercise programme "
                "and it is true here.")
            + para("Weigh yourself less often than you think you should. "
                   "Judge it by how you climb stairs, how you sleep, how your "
                   "clothes sit. Those move first, and they predict whether "
                   "you will still be practising in six months &mdash; the "
                   "only thing that really decides the outcome.")),

        ("Which batch to join",
            para("Four batches, Monday to Friday. For weight and stamina the mornings tend "
                 "to work better, simply because nothing has had a chance to go wrong with "
                 "your day yet.")
            + bullets(
                "<strong>5:30 &ndash; 6:15 am, 45 minutes.</strong> The short early batch, "
                "for people who have to leave the house first.",
                "<strong>6:15 &ndash; 7:15 am, 60 minutes.</strong> The busiest hour, and "
                "where most beginners start.",
                "<strong>10:00 &ndash; 11:00 am, 60 minutes, ladies only.</strong>",
                "<strong>5:00 &ndash; 6:00 pm, 60 minutes.</strong> The evening batch, if "
                "mornings are genuinely not going to happen. The batch you attend beats "
                "the batch that is theoretically better.")
            + para('We teach the same practice online as well, and students move between '
                   'online and in-person as the week allows. You can see which batch is '
                   'next on the <a href="/#schedule" class="text-blue '
                   'font-medium hover:underline">schedule on the homepage</a>. Students '
                   'travel in to our hall in SSM Nagar, New Perungalathur from Old '
                   'Perungalathur, East and West Tambaram, Selaiyur, Chromepet, Vandalur, '
                   'Urapakkam, Guduvanchery and Medavakkam &mdash; there are pages on '
                   '<a href="yoga-classes-perungalathur.html" class="text-blue font-medium '
                   'hover:underline">yoga classes in Perungalathur</a> and on finding a '
                   '<a href="yoga-classes-tambaram.html" class="text-blue font-medium '
                   'hover:underline">yoga centre near Tambaram</a> if you are coming from '
                   'either side.')),

        ("Questions people ask", qa([
            ("Is yoga better than the gym for weight loss?",
             "For pure calorie burn per hour, no. For building something you "
             "will still be doing next year, and for what it does to sleep "
             "and stress, it holds up well. The best exercise is the one you "
             "keep turning up to."),
            ("Do I need to be flexible or fit to start?",
             "No. Most people who join cannot touch their toes on day one, and plenty are "
             "starting from no exercise at all. Every batch is mixed ability and the "
             "practice is adjusted person by person."),
            ("How many times a week should I practise?",
             "The batches run Monday to Friday, and regular practice is what makes the "
             "difference &mdash; sporadic sessions do very little for weight. Start with "
             "what you can actually keep to."),
            ("Will you give me a diet plan?",
             "No. We teach yoga; we are not qualified to write a diet chart, "
             "and you should be wary of anyone at a yoga centre who offers "
             "one. Speak to a doctor or a dietitian for that half."),
            ("Can I try before joining?",
             "Yes. There is a 3-day trial, so you can sit in on a batch and see whether it "
             "suits you before committing to anything. Message us on WhatsApp and we will "
             "tell you which batches have room."),
        ])),

        ("Where to start", para(
            "Pick the batch you could attend on a bad week, not the one you "
            "would attend in an ideal one. Come for three days on the trial, "
            "see how your body feels on the fourth morning, and decide then.")),
    ],
}, {
    "slug": "yoga-classes-for-men-perungalathur.html",
    "short": [
        "Three of the four batches are mixed. Only the 10 am is women only.",
        "Most men arrive stiff from a desk and a commute. That is expected.",
        "There is a 3-day trial, and no need to touch your toes first.",
    ],
    "title": "Yoga classes for men in Perungalathur",
    "meta": ("Yoga classes for men at Happy Yogis in New Perungalathur, Chennai. Three "
             "of the four daily batches are mixed, Monday to Friday, with a 3-day trial."),
    "date": "2026-09-02",
    "date_text": "2 September 2026",
    "standfirst": ("The question we are asked most often by men on the phone is whether "
                   "this is a women's class. It is not."),
    "photo": "ima6",
    "related": ("yoga-classes-for-children-perungalathur.html",
                "Yoga classes for children in New Perungalathur",
                "Where children practise, what the hour is actually for, and what we "
                "do not do."),
    "body": [
        ("Three of the four batches are for everyone", para(
            "The 5:30 am, 6:15 am and 5:00 pm batches are mixed &mdash; men, "
            "women and children on the mats together. Only the 10:00 to 11:00 "
            "am batch is women only. On a normal morning the room holds "
            "school boys, men heading to an office and retired members, all "
            "at whatever depth their body gives that day.")),

        ("Most men arrive stiff. That is the point",
            para("A desk, a long commute up the GST Road and years of no "
                 "stretching leave tight hips, a locked lower back and "
                 "shoulders near the ears. You do not need to touch your toes "
                 "to start. Nobody is pushed into a posture they are not "
                 "ready for, and nobody is watching you.")
            + photo("ima4", "A weekday morning batch &mdash; men, women and children in "
                            "the same room.")
            + para("If your goal is strength and stamina rather than flexibility, the "
                   "practice runs faster and is built around sun salutations and standing "
                   "sequences. Say so on your first day and the teacher builds it in.")),

        ("Coming for a look", para(
            "Batches run Monday to Friday at our hall in SSM Nagar, New Perungalathur, "
            "with a 3-day trial so you can sit in before deciding anything. We teach "
            "online as well, for weeks when the road wins.")),
    ],
}, {
    "slug": "yoga-classes-for-children-perungalathur.html",
    "short": [
        "There is no separate children's batch &mdash; they practise with their parents.",
        "The focus is balance, concentration and enjoying it, not flexibility.",
        "Nobody is pushed, nobody is ranked, and deep poses are taught slowly.",
    ],
    "title": "Yoga classes for children in New Perungalathur",
    "meta": ("Yoga classes for children in New Perungalathur, Chennai. Kids practise in "
             "the morning and evening batches alongside their parents, with a 3-day trial."),
    "date": "2026-09-03",
    "date_text": "3 September 2026",
    "standfirst": ("Children are on the mats in almost every batch we run. "
                   "Parents searching for a yoga class for children near them "
                   "want to know three things: what their child will do, "
                   "whether it is safe, and whether they have to sit through "
                   "it themselves."),
    "photo": "ima23",
    "related": ("what-happens-in-your-first-yoga-class.html",
                "What happens in your first yoga class",
                "What to wear, what to bring, and what the hour actually involves - "
                "written for people who have never been on a mat."),
    "body": [
        ("Children practise with the grown-ups, not away from them", para(
            "There is no separate children's batch. Children practise in the "
            "morning and evening batches alongside their parents &mdash; the "
            "5:30 am, the 6:15 am and the 5:00 pm. The 10:00 am batch is the "
            "exception, because it is women only.",
            "Parents expect this to be a problem and it turns out the "
            "opposite. A child on a mat next to a parent copies the parent, "
            "and a parent who drives a child to class then sits outside on "
            "their phone tends to stop coming by week three. Both of you "
            "practising is what lasts.")),

        ("What the hour is actually for",
            para("The focus is balance, concentration and enjoying it &mdash; "
                 "not flexibility, not achieving a posture, not competing "
                 "with the child on the next mat. A seven-year-old who holds "
                 "their attention on one shape for thirty seconds has got "
                 "what the class is for, whether or not it looked like the "
                 "picture.")
            + photo("ima22", "Three students folded forward together. Nobody is holding "
                             "the same shape, and that is fine.")
            + para("Children are more flexible than the adults in the room "
                   "and far less patient, so their practice moves more, holds "
                   "less and breaks up more often. The breathing at the end "
                   "is short. The lying-still part is shorter still, and some "
                   "days it does not happen at all.")),

        ("The shapes they learn first",
            para("Most children start where everyone starts: standing postures, simple "
                 "back bends and forward folds.")
            + photo("ima21", "Cobra pose &mdash; usually one of the first back bends a "
                             "child learns.")
            + photo("ima20", "A wide-legged seated forward fold.")
            + para("Arm balances come later. They are the ones children ask "
                   "for, because they look difficult and feel like an "
                   "achievement &mdash; and where a teacher has to be firm "
                   "about wrists, shoulders and not trying it before the body "
                   "is ready.")
            + photo("ima23", "An arm balance. This one takes months, not weeks.")),

        ("What we do not do",
            bullets(
                "<strong>Nobody is pushed into a posture.</strong> Children bend easily, "
                "which makes it easy to push them too far. The practice is adjusted to "
                "the child, the same as it is for every adult in the room.",
                "<strong>There is no ranking.</strong> No child is held up as the example "
                "and no child is told they are behind.",
                "<strong>Inversions and deep poses are taught slowly.</strong> The "
                "students you see holding them have been practising for a long time. "
                "They are not what your child will be doing in week one.")
            + photo("ima25", "A shoulder-supported inversion, held by a student who has "
                             "been practising for a while.")
            + photo("ima26", "A seated side split. Again: months of practice, not a "
                             "starting point.")),

        ("Practicalities", para(
            "Batches run Monday to Friday. Every student gets a Happy Yogis "
            "t-shirt, and once you join, mats can stay at the centre. Tell us "
            "before the first class if your child has a health condition, an "
            "old injury or anything else the teacher should plan around.",
            "There is a 3-day trial, so your child can sit in on a batch and you can see "
            "how they take to it before committing to anything.")),

        ("Finding us", para(
            "One hall, in SSM Nagar, New Perungalathur &mdash; just off the "
            "GST Road stretch between Tambaram and Vandalur, close to "
            "Perungalathur railway station. Families travel in from Old "
            "Perungalathur, East and West Tambaram, Selaiyur, Chromepet, "
            "Vandalur, Urapakkam, Guduvanchery and Medavakkam.")
            + photo("ima8", "A children's group working through cobra pose at the centre.")
            + para('If you have been searching for a yoga class for children near you in '
                   'this part of Chennai, message us on WhatsApp and we will tell you '
                   'which of the batches has room. There are pages on '
                   '<a href="yoga-classes-perungalathur.html" class="text-blue font-medium '
                   'hover:underline">yoga classes in Perungalathur</a> and on finding a '
                   '<a href="yoga-classes-tambaram.html" class="text-blue font-medium '
                   'hover:underline">yoga centre near Tambaram</a> with directions from '
                   'either side.')),

        ("Questions parents ask", qa([
            ("What age can a child start?",
             "We set no age limit. Children practise alongside their parents "
             "in the morning and evening batches, adjusted to whoever is on "
             "the mat. Talk to us about your child and we will tell you "
             "honestly whether it suits them."),
            ("Do I have to practise too?",
             "You do not have to, but it works far better when you do. Children copy "
             "what the adult beside them is doing, and families who practise together "
             "are the ones still coming a year later."),
            ("Is it safe for a growing child?",
             "Practised the way it is taught here &mdash; adjusted to the "
             "child, no pushing, nothing forced &mdash; yes. Tell the teacher "
             "about any health condition or injury before the first class, "
             "and check with your doctor if your child is under treatment for "
             "anything."),
            ("Will it help with school and concentration?",
             "That is what the practice works on with children: balance, concentration "
             "and enjoying it. What each child gets from it varies, and we are not going "
             "to promise you marks."),
        ])),
    ],
}, {
    "slug": "international-yoga-day-beach.html",
    "short": [
        "International Yoga Day is 21 June, set by the United Nations in 2014.",
        "We marked it early &mdash; 12 June 2026, on the sand at the Blue Flag beach in Chennai.",
        "A one-off. Every ordinary class is indoors, in the hall at SSM Nagar.",
    ],
    "title": "International Yoga Day on the beach",
    "meta": ("International Yoga Day is 21 June. We marked it on the sand at the Blue "
             "Flag beach, Chennai, and wrote down what practising outdoors changes."),
    "date": "2026-09-04",
    "date_text": "4 September 2026",
    "standfirst": ("International Yoga Day falls on 21 June. We marked ours nine days "
                   "early, on 12 June 2026, by taking the whole centre out of the hall "
                   "and onto the sand at the Blue Flag beach in Chennai. This is what "
                   "the morning was, and what practising on a beach actually changes "
                   "&mdash; which is more than you would think."),
    "photo": "ima14",
    "related": ("yoga-classes-for-children-perungalathur.html",
                "Yoga classes for children in New Perungalathur",
                "Where children practise, what the hour is actually for, and what we "
                "do not do."),
    "body": [
        ("When International Yoga Day is, and where it came from",
            para("The date is 21 June. The United Nations set it in December 2014, on a "
                 "proposal from India that a record 175 member states co-sponsored, and "
                 "the first one was held in June 2015. The 21st was chosen because it is "
                 "the summer solstice in the northern hemisphere &mdash; the longest day "
                 "of the year.",
                 "You can read the "
                 + cite("un_yoga", "United Nations page for the day")
                 + ", and the Government of India runs its own programme through the "
                 + cite("ayush", "Ministry of Ayush") + ".",
                 "Centres and schools rarely hold their event on the day itself, because "
                 "21 June is not always a convenient morning. Ours was on 12 June 2026.")),

        ("Why a beach, once a year",
            para("We teach in a hall. It has a floor that does not move, walls that keep "
                 "the wind out and a fan overhead, and that is the right room for four "
                 "batches a day, five days a week.",
                 "Once, for this, it is worth practising somewhere that takes all of "
                 "that away. Nothing about the sequence changes. Everything about the "
                 "conditions does, and a practice you thought you knew becomes "
                 "unfamiliar for an hour.")),

        ("Before the sun was properly up",
            para("We start at half past five most mornings anyway, so an "
                 "early beach session was no hardship. People arrived in the "
                 "half-light, spread mats and towels on the sand, and waited "
                 "for enough light to see the person in front of them.")
            + photo("ima15", "Settling in, with the sun coming up over the water.")
            + photo("ima33", "The group gathered for the opening of the morning, the "
                             "backwater behind.")),

        ("Everybody came",
            para("The thing that made the morning was who turned up. Children who "
                 "normally practise beside their parents in the 6:15 batch. Parents. "
                 "Retired members. The men who come to the evening class. Whole families "
                 "on one towel.")
            + photo("ima11", "Students settled on the sand, the sea behind them.")
            + photo("ima12", "The men's group, waiting for the practice to start.")
            + photo("ima34", "One of the younger students, on the microphone.")
            + photo("ima35", "Karthika with one of the youngest of them.")),

        ("What we practised",
            para("Much the same as any morning: warm-up, standing postures, "
                 "forward bends, then seated work and breathing to close. The "
                 "sequence was not the point. Doing it in the open, facing "
                 "the water, with strangers walking past, was.")
            + photo("ima19", "A standing forward bend, the whole group together.")
            + photo("ima16", "Wide-legged forward bends on the sand.")
            + photo("ima17", "Seated practice, with the city on the far shore.")
            + photo("ima32", "Not everybody was concentrating the whole time.")),

        ("What sand actually changes",
            para("This is the part worth writing down, because it surprised people who "
                 "have practised in the hall for years.")
            + bullets(
                "<strong>Nothing is level.</strong> Standing postures that feel settled "
                "on a wooden floor wobble on sand, and the ground gives way under the "
                "outside edge of the foot. Balance work gets genuinely harder, which is "
                "a decent argument for doing it occasionally.",
                "<strong>The sun sets the clock.</strong> Even at six in the morning it "
                "is on you, and Chennai in June does not need help with heat. Nobody "
                "held anything for long, and we finished earlier than we would indoors.",
                "<strong>You cannot hear the teacher.</strong> Wind and waves take half "
                "of every instruction, so people watch instead of listen &mdash; which, "
                "for children especially, is not the worst way to learn a shape.",
                "<strong>Your hands do not grip.</strong> Dry sand on the palms turns a "
                "plank or a downward dog into a slide. Most people ended up on a mat "
                "over a towel rather than on the sand itself.",
                "<strong>Seated work is the easy part.</strong> The one thing sand is "
                "better for: sitting. Nobody needed a folded blanket under them for "
                "the breathing at the end.")),

        ("If you are planning a beach practice in Chennai",
            para("Several people asked how to do this with their own family or "
                 "residents' association. It is not complicated, but the heat is the "
                 "thing that catches people out.")
            + bullets(
                "<strong>Be finishing when the sun arrives, not starting.</strong> "
                "First light is the whole window. By seven it stops being pleasant.",
                "<strong>Bring a mat and a towel, not one or the other.</strong> The "
                "towel keeps the sand off the mat; the mat gives you a surface that "
                "does not slide.",
                "<strong>Water before, not only after.</strong> People turn up to a "
                "6 am session having drunk nothing since the night before.",
                "<strong>Pick your patch above the tide line</strong> and look at where "
                "the wet sand ends before you lay anything out.",
                "<strong>Take everything home with you.</strong> Bottles, wrappers, "
                "tape, the lot. A beach you had to be asked to clean is not one you "
                "get invited back to.")),

        ("The photograph everyone wanted",
            para("At the end, the group photo. Students, parents, children and teachers, "
                 "all in the blue t-shirts, squinting into the sun.")
            + photo("ima13", "Everyone together at the end of the morning.")),

        ("And then back to the hall", para(
            'The same morning also carried the '
            '<a href="108-suryanamaskar-challenge.html" class="text-blue font-medium '
            'hover:underline">108 Suryanamaskar Non-Stop Challenge</a>, which has its '
            'own account with the rules, the two slots and the finishers.',
            "The beach was a one-off, for the occasion. The rest of the year we teach "
            "where we always teach &mdash; a hall in SSM Nagar, New Perungalathur, four "
            "batches a day, Monday to Friday, fan on. There is a 3-day trial, and you "
            "need not wait for June.")),
    ],
}, {
    "slug": "108-suryanamaskar-challenge.html",
    "short": [
        "108 sun salutations, continuous, no skipped rounds, on sand.",
        "Two slots, 5:30 am and 10:00 am, open to current and former students.",
        "Finishers received a certificate, a medal and a memento.",
    ],
    "title": "The 108 Suryanamaskar non-stop challenge",
    "meta": ("108 Surya Namaskars without stopping, on the sand at the Blue Flag beach, "
             "Chennai, for International Yoga Day 2026. The rules, and the finishers."),
    "date": "2026-09-05",
    "date_text": "5 September 2026",
    "standfirst": ("One hundred and eight sun salutations. No breaks, no skipped rounds, "
                   "on sand, in June. This is what we set our students on 12 June 2026, "
                   "and what it took to finish it."),
    "photo": "ima29",
    "related": ("international-yoga-day-beach.html",
                "International Yoga Day on the beach",
                "The morning we took the whole centre out of the hall and onto the "
                "sand, in photographs."),
    "body": [
        ("Why 108",
            para("One hundred and eight is not arbitrary. It is the count of "
                 "beads on a japa mala and recurs throughout Indian "
                 "tradition, which is why 108 rounds of Surya Namaskar has "
                 "become the mark people set themselves on Yoga Day and at "
                 "solstice.",
                 "A single Surya Namaskar is a linked round of twelve "
                 "positions moved through with the breath. Doing 108 without "
                 "stopping is not a yoga class; it is an endurance event that "
                 "happens to be made of yoga.")
            + photo("ima27", "The announcement that went out to students.")),

        ("The rules, as they were set",
            para("We did not soften them.")
            + bullets(
                "<strong>All 108 completed continuously.</strong> No breaks between "
                "rounds.",
                "<strong>No skipped rounds.</strong> A round not done is a round not "
                "counted.",
                "<strong>Incomplete attempts were not counted as successful.</strong> "
                "Stopping was allowed at any point &mdash; it simply meant the challenge "
                "was not completed.",
                "<strong>Report on time for your slot.</strong> Two were offered, 5:30 am "
                "and 10:00 am.",
                "<strong>Yoga uniform.</strong> Mandatory.")
            + para("It was open to current and former students &mdash; "
                   "several came back who had not been on a mat at the centre "
                   "for a while. Entry was by a form, filled in beforehand.")),

        ("On sand, in June",
            para("Chennai in June, on an open beach, is not a controlled "
                 "environment. The 5:30 slot had the cooler air; the 10:00 "
                 "slot did not. Sand gives under the hands in the plank and "
                 "the back foot in the lunge, so every round costs more than "
                 "on a wooden floor.")
            + photo("ima31", "Lowering through the plank.")
            + photo("ima30", "The pace kept together for as long as people could hold "
                             "it.")),

        ("Finishing",
            para("Everyone who completed all 108 received a certificate, a medal and a "
                 "memento, handed over on the sand at the end of the slot.")
            + photo("ima37", "One finisher gets his medal. Another has clearly just "
                             "finished his own.")
            + photo("ima40", "Certificate and medal together.")
            + photo("ima38", "A finisher with her certificate and memento.")
            + photo("ima39", "And another.")
            + photo("ima36", "The youngest finishers got exactly the same.")
            + photo("ima28", "The certificate itself.")),

        ("Should you try 108?",
            para("Not cold, and not because you read about it. The people in "
                 "these photographs practise several mornings a week and had "
                 "built up to it. 108 continuous rounds is a serious "
                 "cardiovascular and muscular load, and the failure mode is "
                 "not embarrassment &mdash; it is a shoulder, a wrist or a "
                 "lower back.",
                 "If it appeals, build towards it with a teacher who can "
                 "watch your form as you tire &mdash; which is when it goes "
                 "wrong. If you are under treatment for anything, pregnant, "
                 "or working around an injury, this challenge is not the "
                 "place to start.")),

        ("The rest of the year", para(
            "This was one morning at the Blue Flag beach. The regular "
            "practice is a hall in SSM Nagar, New Perungalathur &mdash; four "
            "batches a day, Monday to Friday, sun salutations included but "
            "rather fewer than 108 at a time. There is a 3-day trial if you "
            "want to see an ordinary morning.")),
    ],
}]


def post_schema(p):
    return {
        "@context": "https://schema.org",
        "@graph": [
            {"@type": "BlogPosting",
             "@id": f"{BASE}/{p['slug']}#post",
             "headline": p["title"],
             "description": p["meta"],
             "datePublished": p["date"],
             "dateModified": p["date"],
             "inLanguage": "en-IN",
             "image": f"{BASE}/{p['photo']}.jpeg",
             "author": {"@id": f"{BASE}/#karthika"},
             "publisher": {"@id": f"{BASE}/#business"},
             "mainEntityOfPage": {"@id": f"{BASE}/{p['slug']}#webpage"},
             "isPartOf": {"@id": f"{BASE}/blog.html#blog"}},
            C.person_node(),
            {"@type": "BreadcrumbList", "@id": f"{BASE}/{p['slug']}#breadcrumb",
             "itemListElement": [
                 {"@type": "ListItem", "position": 1, "name": "Home", "item": f"{BASE}/"},
                 {"@type": "ListItem", "position": 2, "name": JOURNAL_PLAIN, "item": f"{BASE}/blog.html"},
                 {"@type": "ListItem", "position": 3, "name": p["title"], "item": f"{BASE}/{p['slug']}"}]},
        ],
    }


def newest_first():
    """Most recent post first. Ties break on definition order, so the post added
    last wins - two posts published the same day should not be ordered by luck."""
    return [p for _, p in sorted(enumerate(POSTS),
                                 key=lambda t: (t[1]["date"], t[0]), reverse=True)]


def build_index_page():
    schema = {
        "@context": "https://schema.org",
        "@graph": [
            {"@type": "Blog", "@id": f"{BASE}/blog.html#blog", "url": f"{BASE}/blog.html",
             "name": f"Happy Yogis {JOURNAL_PLAIN}", "inLanguage": "en-IN",
             "publisher": {"@id": f"{BASE}/#business"},
             "blogPost": [{"@type": "BlogPosting", "@id": f"{BASE}/{p['slug']}#post",
                           "headline": p["title"], "datePublished": p["date"],
                           "url": f"{BASE}/{p['slug']}"} for p in POSTS]},
            {"@type": "BreadcrumbList", "@id": f"{BASE}/blog.html#breadcrumb",
             "itemListElement": [
                 {"@type": "ListItem", "position": 1, "name": "Home", "item": f"{BASE}/"},
                 {"@type": "ListItem", "position": 2, "name": JOURNAL_PLAIN, "item": f"{BASE}/blog.html"}]},
        ],
    }

    entries = "\n".join(f"""            <li class="border-t border-line">
                <a href="{p['slug']}" class="group block py-7 transition-colors hover:bg-sand/60">
                    <time datetime="{p['date']}" class="text-[13px] text-muted">{p['date_text']}</time>
                    <h2 class="mt-1.5 text-d3 text-ink group-hover:text-blue transition-colors">{p['title']}</h2>
                    <p class="mt-1.5 text-[15px] leading-relaxed text-muted max-w-2xl">{p['standfirst']}</p>
                </a>
            </li>""" for p in newest_first())

    h = head(title=f"{JOURNAL_PLAIN} | Happy Yogis Yoga Centre",
             desc=("Notes from Happy Yogis Yoga Centre in New Perungalathur, Chennai "
                   "- what to expect from class, and practising around your health."),
             path="blog.html", schema=schema, alt=("ta", "ta/blog.html"))

    body = f"""<body class="font-body bg-paper text-ink text-[15px]">
{nav(alt_href="/ta/blog.html")}
    <main id="main" class="pt-16">

    <nav aria-label="Breadcrumb" class="max-w-3xl mx-auto px-5 sm:px-8 pt-8">
        <ol class="flex flex-wrap items-center gap-2 text-[13.5px] text-muted">
            <li><a href="/" class="inline-block py-1 hover:text-ink">Home</a></li>
            <li aria-hidden="true">/</li>
            <li aria-current="page" class="text-ink">{JOURNAL}</li>
        </ol>
    </nav>

    <div class="max-w-3xl mx-auto px-5 sm:px-8 py-10 lg:py-14">
        <h1 class="text-d1 text-ink">{JOURNAL}</h1>
        <p class="mt-5 text-[17px] leading-relaxed text-ink/80 max-w-2xl">
            Notes from the centre &mdash; what a class actually involves, and how we
            work around the things people arrive with.
        </p>

        <ul class="mt-12 border-b border-line">
{entries}
        </ul>
    </div>

    </main>

{footer()}
{SCRIPT}"""
    return h + body


def build_post(p):
    # A section body is either a plain sentence (one paragraph) or ready markup.
    sections = "\n".join(
        f"""            <h2 class="text-d2 text-ink mt-12">{t}</h2>\n"""
        + (body if body.lstrip().startswith("<")
           else f'            <p class="{P.replace("mt-4", "mt-3")}">{body}</p>')
        for t, body in p["body"])

    short = ""
    if p.get("short"):
        pts = "\n".join(f"                    <li>{t}</li>" for t in p["short"])
        short = f"""
        <aside class="mt-8 border-l-2 border-line pl-5" aria-label="In short">
            <p class="text-[13px] font-medium text-ink">In short</p>
            <ul class="mt-2 space-y-1.5 text-[15px] leading-relaxed text-ink/75 list-disc pl-5 marker:text-muted">
{pts}
            </ul>
        </aside>"""

    related = ""
    if p.get("related"):
        slug, title, blurb = p["related"]
        related = f"""
        <aside class="mt-14 border-t border-line pt-6">
            <h2 class="text-[13.5px] font-medium text-ink">Read next</h2>
            <a href="{slug}" class="group mt-3 block">
                <span class="display text-d3 text-ink group-hover:text-blue transition-colors">{title}</span>
                <span class="mt-1.5 block text-[15px] leading-relaxed text-muted max-w-xl">{blurb}</span>
            </a>
        </aside>"""

    # only four of the eleven posts exist in Tamil; the rest declare no
    # alternate, which is the honest signal - hreflang pointing at a page that
    # does not exist is worse than none at all
    alt = ("ta", f"ta/{p['slug']}") if p["slug"] in TRANSLATED else None
    ta_href = f"/{alt[1]}" if alt else None   # the toggle and hreflang agree by construction
    h = head(title=f"{p['title']} | Happy Yogis", desc=p["meta"], path=p["slug"],
             schema=post_schema(p), og_img=f"{p['photo']}.jpeg", alt=alt)

    body = f"""<body class="font-body bg-paper text-ink text-[15px]">
{nav(alt_href=ta_href)}
    <main id="main" class="pt-16">

    <nav aria-label="Breadcrumb" class="max-w-3xl mx-auto px-5 sm:px-8 pt-8">
        <ol class="flex flex-wrap items-center gap-2 text-[13.5px] text-muted">
            <li><a href="/" class="inline-block py-1 hover:text-ink">Home</a></li>
            <li aria-hidden="true">/</li>
            <li><a href="blog.html" class="inline-block py-1 hover:text-ink">{JOURNAL}</a></li>
        </ol>
    </nav>

    <article class="max-w-3xl mx-auto px-5 sm:px-8 py-10 lg:py-14">
        <time datetime="{p['date']}" class="text-[13px] text-muted">{p['date_text']}</time>
        <h1 class="mt-2 text-d1 text-ink">{p['title']}</h1>
        <p class="mt-5 text-[17px] leading-relaxed text-ink/80">{p['standfirst']}</p>
{short}

        <!-- The lead image is the largest thing on the first screen, so it
             carries the real widths and is fetched eagerly. Left lazy it was
             the LCP element and the browser deferred it. -->
        <picture>
            <source type="image/webp" sizes="(min-width:768px) 720px, 92vw"
                    srcset="{p['photo']}-xs.webp 320w, {p['photo']}-sm.webp 640w, {p['photo']}-md.webp 768w, {p['photo']}.webp {dims(p['photo'])[0]}w">
            <source type="image/jpeg" sizes="(min-width:768px) 720px, 92vw"
                    srcset="{p['photo']}-xs.jpg 320w, {p['photo']}-sm.jpg 640w, {p['photo']}-md.jpg 768w, {p['photo']}.jpeg {dims(p['photo'])[0]}w">
            <img src="{p['photo']}.jpeg" width="{dims(p['photo'])[0]}" height="{dims(p['photo'])[1]}" alt="{C.PHOTOS[p['photo']]}"
                 class="w-full rounded mt-10" fetchpriority="high" decoding="async">
        </picture>

{sections}
{DISCLAIMER}

{related}
        <div class="mt-14 border border-line rounded lift p-6 sm:p-8 bg-sand">
            <h2 class="text-d3 text-ink">Come and try a batch</h2>
            <p class="mt-2 text-[15px] leading-relaxed text-ink/75 max-w-lg">
                Four batches a day, Monday to Friday, at our centre in New Perungalathur.
            </p>
            <div class="mt-5 flex flex-wrap gap-3">
                <a href="{wa("Hello Happy Yogis! I read Yogi's Upadesha and would like to book a 3-day trial.")}"
                   target="_blank" rel="noopener"
                   class="inline-flex items-center px-5 py-3 bg-ink text-white font-medium rounded hover:bg-blue transition-colors">
                    Book a 3-day trial
                </a>
                <a href="/#schedule" class="inline-flex items-center px-5 py-3 border border-line text-ink font-medium rounded hover:border-ink transition-colors">
                    See the schedule
                </a>
            </div>
        </div>

        <p class="mt-10"><a href="blog.html" class="inline-block py-1 text-blue font-medium hover:underline">All of {JOURNAL}</a></p>
    </article>

    </main>

{footer()}
{SCRIPT}"""
    return h + body


# Four more, kept in their own module so this file stays navigable. They use
# the helpers above, so the import has to happen after they are defined.
# The slugs that also exist in Tamil, so hreflang can be emitted for exactly
# those and no others.
TRANSLATED = {"how-often-should-you-do-yoga.html",
              "yoga-or-gym-which-should-you-pick.html",
              "morning-or-evening-yoga-class.html",
              "yoga-for-back-pain-chennai.html"}

import posts_more  # noqa: E402
POSTS += posts_more.make(para, bullets, photo, qa, cite, DISCLAIMER)


if __name__ == "__main__":
    open(os.path.join(OUT, "blog.html"), "w").write(build_index_page())
    print("blog.html written")
    for p in POSTS:
        open(os.path.join(OUT, p["slug"]), "w").write(build_post(p))
        print(f"{p['slug']} written")
