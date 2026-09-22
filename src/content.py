#!/usr/bin/env python3
"""Confirmed content for the Happy Yogis site.

Every business fact here was confirmed by the owner in the requirements
interview. Nothing in this file may be invented or inferred:
  - 4 batches (the 8-9am batch was removed; it does not run)
  - opening hours Mon-Fri 05:30-19:00 (classes to 18:00, reception to 19:00)
  - a 3-day trial, with NO price shown anywhere on the site
  - no fees of any kind published
  - no social links (sameAs removed at the owner's instruction)
"""

BASE = "https://happyyogis.in"

# time24 is used by the hero's "next class today" panel.
BATCHES = [
    ("05:30", "5:30 &ndash; 6:15 am", "45 min", "Everyone",
     "The early batch. Mostly people who want it done before the day starts."),
    ("06:15", "6:15 &ndash; 7:15 am", "60 min", "Everyone",
     "Our busiest hour. Mixed ability and mixed ages, from school children to retired members."),
    ("10:00", "10:00 &ndash; 11:00 am", "60 min", "Ladies only",
     "Mid-morning, and women only. Popular with homemakers and anyone on a shift pattern."),
    ("17:00", "5:00 &ndash; 6:00 pm", "60 min", "Everyone",
     "The evening batch. A lot of school and college students come to this one."),
]

OPEN_FROM, OPEN_TO = "05:30", "19:00"
HOURS_TEXT = "Monday to Friday, 5:30 am &ndash; 7:00 pm"
CLOSED_TEXT = "Closed Saturday, Sunday and public holidays"

# The one-off event the beach photographs come from. Confirmed by the owner:
# held on 12 June 2026, ahead of International Yoga Day, at the Blue Flag beach
# in Chennai. No participant is named anywhere on the site - several mementos in
# the photographs carry names, and the site does not repeat them.
EVENT = {
    "name": "International Yoga Day 2026",
    "challenge": "108 Suryanamaskar Non-Stop Challenge",
    "date": "12 June 2026",
    "place": "the Blue Flag beach, Chennai",
}

TRIAL = "3-day trial"        # price is deliberately not published

CLASS_GROUPS = [
    ("Start here", [
        ("Beginner yoga",
         "Where you start if you have never held a pose. Standing postures "
         "and the breath, built slowly, never past what your body will do "
         "that day."),
        ("Flexibility and posture",
         "Hip openers, hamstring work and spinal movement, for desk workers "
         "who arrive with a stiff neck and lower back."),
    ]),
    ("Build strength", [
        ("Weight loss and stamina",
         "A faster practice built on sun salutations and standing sequences, "
         "for losing weight and building stamina."),
        ("Yoga for seniors",
         "Low-impact, with chair and wall support where it helps, for joint "
         "mobility and steadiness."),
    ]),
    ("Breath and mind", [
        ("Meditation and pranayama",
         "Breathing practice and seated meditation. Every batch ends with it; "
         "some students come specifically for it."),
        ("Yoga for women",
         "Adapted around PCOD, thyroid, hormonal health and the menstrual "
         "cycle. The 10:00 am batch is women only."),
    ]),
    ("Beyond the batches", [
        ("Yoga for children",
         "Children practise in the morning and evening batches alongside "
         "their parents &mdash; balance, concentration, and enjoying it."),
        ("Corporate and group sessions",
         "For offices and residential associations, at your premises or "
         "online. Ask us for details."),
    ]),
]

CLASSES = [(n, d) for _, items in CLASS_GROUPS for n, d in items]

HEALTH = [
    ("PCOD and hormonal health", "Practice sequenced around hormonal balance, at a manageable pace."),
    ("Thyroid support", "Breathing and movement chosen with thyroid health in mind."),
    ("Knee and joint pain", "Low-impact work with support, so the knees are not loaded."),
    ("Back and spine", "Posture correction and spinal strengthening for desk workers."),
    ("Pregnancy care", "Prenatal practice, guided carefully and adjusted by stage."),
    ("Stress and sleep", "Breathing and relaxation for students who arrive wound up or sleeping badly."),
]

AREAS = [
    "New Perungalathur", "Old Perungalathur", "SSM Nagar",
    "East Tambaram", "West Tambaram", "Selaiyur",
    "Chromepet", "Vandalur", "Urapakkam", "Guduvanchery", "Medavakkam",
]

AREA_PAGES = [
    ("Yoga classes in Perungalathur", "yoga-classes-perungalathur.html",
     "The centre is in this neighbourhood. Where we are, and what a class looks like."),
    ("Yoga classes near Tambaram", "yoga-classes-tambaram.html",
     "Getting here from Tambaram and Selaiyur, and which batch suits the commute."),
]

FAQS = [
    ("Do I need to be flexible to start?",
     "No. Most people who join cannot touch their toes on day one. "
     "Flexibility is what the practice builds, not what it asks for."),
    ("I have never done yoga before. Which batch should I join?",
     "Any of them. Every batch is mixed ability and the practice is adjusted "
     "person by person. Most beginners pick the 6:15 am or the 5:00 pm batch."),
    ("Can I try before joining properly?",
     "Yes. A 3-day trial lets you sit in on a batch before committing. "
     "Message us on WhatsApp and we will book you in."),
    ("Do I need to bring a mat?",
     "Bring one for the trial if you have it. Once you join you can leave your "
     "mat at the centre rather than carrying it every day."),
    ("Is there a dress code?",
     "Wear something you can move in. Every student is given a Happy Yogis "
     "t-shirt to wear to class."),
    ("Can I switch between online and in-person?",
     "Yes. We teach both, and students move between them as their week allows "
     "&mdash; online sign-ups can come to the centre instead, and the other "
     "way round."),
    ("Are the classes in Tamil or English?",
     "Both. Instructions are given in whichever language the batch is comfortable with."),
    ("Do you teach men as well as women?",
     "Yes. The 5:30 am, 6:15 am and 5:00 pm batches are for everyone. The "
     "10:00 am batch is women only."),
    ("Can my child join?",
     "Yes, children practise alongside their parents in the morning and evening batches."),
    ("I have a knee problem, back pain or PCOD. Can I still practise?",
     "In most cases yes, with the practice adapted. Tell us before you start, "
     "and check with your doctor if you are under treatment for anything."),
    ("How soon will I notice a difference?",
     "Most students say they sleep better and feel less stiff within the first "
     "two or three weeks of practising regularly. Physical changes take longer."),
    ("How do I join?",
     "Message us on WhatsApp or call. We will tell you which batches have room "
     "and book you a trial."),
]

PHOTOS = {
    "ima1":  "Adults and children seated in meditation facing their teacher at Happy Yogis",
    "ima3":  "Student holding downward dog on a mat at the centre",
    "ima4":  "Morning batch seated in meditation at the New Perungalathur centre",
    "ima5":  "Teacher leading a seated breathing practice for a mixed-age group",
    "ima6":  "Students of all ages holding tree pose together",
    "ima7":  "Yoga teacher demonstrating a seated spinal twist",
    "ima8":  "Children practising cobra pose in a class at Happy Yogis",
    "ima9":  "Members of the Happy Yogis community together at a centre event",
    "ima10": "Ladies batch moving through cat-cow stretches",
    # A one-off beach session. Captioned as an event wherever it appears: classes
    # are taught in the hall at SSM Nagar, and a visitor should never come away
    # thinking otherwise.
    "ima11": "Students seated on mats at a Happy Yogis beach session, the sea behind them",
    "ima12": "Men from the centre seated on their mats at the beach session at sunset",
    "ima13": "The Happy Yogis group photographed together at the beach session",
    "ima14": "A student stretching both arms overhead in the morning light at the beach",
    "ima15": "The group seated on mats as the sun comes up over the water",
    "ima16": "Students in a wide-legged forward bend together on the sand",
    "ima17": "A row of students in a seated forward bend, the city skyline behind",
    "ima18": "Members of the men's group sitting together on the sand at the beach session",
    "ima19": "The group holding a standing forward bend on the beach",
    # Indoor practice at the centre
    "ima20": "A student holding a wide-legged seated forward fold on a mat at the centre",
    "ima21": "Two students in cobra pose, chests lifted and heads back",
    "ima22": "Three children folded forward together on one mat",
    "ima23": "A young boy balancing on his hands in a wide-legged arm balance",
    "ima24": "A student in a standing forward bend with the palms flat on the mat",
    "ima25": "A student holding an inverted shoulder-supported pose, legs overhead",
    "ima26": "A student in a seated side split, arms stretched overhead",
    # 108 Suryanamaskar Non-Stop Challenge, 12 June 2026
    "ima27": "The Happy Yogis poster announcing the 108 Suryanamaskar Non-Stop Challenge",
    "ima28": "The certificate given to everyone who completed the 108 challenge",
    "ima29": "A row of students holding the lunge of a sun salutation on the sand",
    "ima30": "Students holding a low lunge together, the backwater behind them",
    "ima31": "A student lowering into the plank of a sun salutation on the sand",
    "ima32": "A young girl on her hands in the sand, smiling at the camera",
    "ima33": "The whole group seated for the opening of the morning, water behind",
    "ima34": "A young student speaking into a microphone at the beach session",
    "ima35": "The teacher with one of the younger students after the challenge",
    "ima36": "A young student receiving her certificate and memento",
    "ima37": "A finisher receiving his medal while another celebrates behind him",
    "ima38": "A finisher receiving her certificate and memento",
    "ima39": "A finisher receiving his certificate and memento",
    "ima40": "A finisher with his medal, receiving his certificate",
}

GALLERY = ["ima13", "ima4", "ima14", "ima6", "ima23", "ima1", "ima15", "ima31",
           "ima21", "ima8", "ima12", "ima5", "ima20", "ima10", "ima16", "ima3",
           "ima26", "ima7", "ima11", "ima9", "ima22", "ima17", "ima25", "ima19",
           "ima24", "ima18"]

# The nine beach photographs. Anywhere one of these is shown large it is
# captioned as a one-off session, never as a regular class.
BEACH = {"ima11", "ima12", "ima13", "ima14", "ima15", "ima16", "ima17", "ima18",
         "ima19", "ima29", "ima30", "ima31", "ima32", "ima33", "ima34", "ima35",
         "ima36", "ima37", "ima38", "ima39", "ima40"}

# Real reviews from the centre's Google Business Profile, supplied by the owner.
# 50 reviews were pasted in, every one five stars. Only the 25 with complete
# written text are quotable: 12 are rating-only, 7 are Google's old
# "Positive / Quality" attribute tags, and 4 are truncated with "... More".
# The 12 below are curated from the complete ones for range - beginners,
# long-term students, children, health and flexibility. Nothing is edited
# beyond collapsing repeated full stops and escaping for HTML.
REVIEW_COUNT_CLAIM = "More than 45 five-star reviews on Google"
REVIEWS_URL = "https://www.google.com/maps/search/?api=1&query=HAPPY+YOGIS+YOGA+CENTRE"

REVIEWS = [
    {"text": "Very good place to kick start if we are new to Yoga for people like me (Am 36). Advance level Yoga is also taught here based on our performance and flexibility. Our Yoga Teacher (Karthika Mam) is very polite and concentrates on each and every students carefully. Capturing their strengths and weak areas and correcting them appropriately. No age limits here and it feels very energetic to perform along with the little kids.",
     "name": "Karthik Chennai", "when": "a year ago"},
    {"text": "I really enjoy taking yoga classes with Karthika mam. She is friendly and explains everything clearly. The classes are very peaceful and help me feel calm , relaxed and more focused. Karthika mam teaches not just poses , but also how to breathe properly and stay mindful. I feel stronger, more flexible, and more positive after each class. Karthika mam makes everyone feel welcome, no matter their level. I am very thankful for the guidance and support I receive in every session. I have personally benefitted a lot in my health and sleeping pattern. I highly recommend KARTHIKA MAM to anyone who wants to improve their body and mind through YOGA",
     "name": "Anitha Jaganathan", "when": "a year ago"},
    {"text": "I had a wonderful experience at this yoga class. The instructor is very kind, patient, and explains each posture clearly, which makes it easy for beginners to follow. The sessions are well-structured and help improve both physical health and mental peace. I can already feel positive changes in my flexibility and overall well-being. The environment is calm, supportive, and motivating. I highly recommend this class to anyone looking to start or continue their yoga journey.",
     "name": "Naga Lakshmi", "when": "5 months ago"},
    {"text": "I&rsquo;ve been a student here since 2023, and it has truly helped me maintain my health much better. The classes are well-structured, and the guidance is clear and supportive. I&rsquo;ve noticed improvements in my flexibility, strength, and overall well-being. It has become an important part of my routine, and I highly recommend it to anyone looking to improve their health through yoga",
     "name": "Vasumathi Bindumadhavan", "when": "5 months ago"},
    {"text": "I had a great refreshing days while I was practicing with her. It helped me a lot to recover my body and mental health. My daughter who is 9 year old says.attending yoga classes made her body flexible and gives her peace of mind.she is very happy to learn from Karthika mam as she makes their classes fun and adventurous I highly recommend Happy yogis",
     "name": "Nithya Ramesh", "when": "a year ago"},
    {"text": "Very good yoga coaching center, Karthika ma&rsquo;am is very friendly and sweet. My flexibility has improved a lot from these classes.",
     "name": "Sailakshmi U", "when": "5 months ago"},
    {"text": "I am attending this class for more than a year. Really helps in maintaining fitness. Mam use to shuffle and make modifications to keep it non monotonous.",
     "name": "Ramanathan Ramu", "when": "a year ago"},
    {"text": "Good Structured Yoga training . It is a good experience to do yoga along with school kids who have very good flexibility",
     "name": "Bharat KVK", "when": "11 months ago"},
    {"text": "Wonderful training given by yoga teacher karthiga Mam. Much appreciated when she is correcting our poses when we are doing incorrectly. Keep rocking Mam.",
     "name": "Sanjay Edgar", "when": "11 months ago"},
    {"text": "Really nice. Thank you for such a refreshing class. I always leave feeling better than when I arrived. I feel stronger and more balanced every time I practice with you. You are a friendly person. Thanks a ton mam.",
     "name": "Arockia Thenmozhi", "when": "4 months ago"},
    {"text": "I absolutely loved my yoga class experience! The instructor was calm, kind, friendly and guided us with care. Every session left me feeling refreshed and focused. Highly recommend it for anyone looking to improve mind and body.",
     "name": "Venkatesh Sampath", "when": "a year ago"},
    {"text": "The class is truly inspiring! The instructor's guidance is clear, calm, and motivating. Every session feels like a reset—calm, focused, and refreshing.",
     "name": "Ramya KA", "when": "a year ago"},
]


def business_node():
    return {
        "@type": ["LocalBusiness", "HealthAndBeautyBusiness", "SportsActivityLocation"],
        "@id": f"{BASE}/#business",
        "name": "Happy Yogis Yoga Centre",
        "alternateName": "Happy Yogis",
        "description": ("A single yoga centre in SSM Nagar, New Perungalathur, Chennai, "
                        "teaching morning and evening batches for ladies, gents and "
                        "children, plus online classes and health-focused practice. "
                        "Students travel in from Perungalathur, Tambaram, Selaiyur, "
                        "Chromepet, Vandalur and Guduvanchery."),
        "url": f"{BASE}/",
        "logo": {"@type": "ImageObject", "@id": f"{BASE}/#logo", "url": f"{BASE}/logo.png",
                 "width": 320, "height": 362},
        "image": [f"{BASE}/og-image.jpg", f"{BASE}/ima4.jpeg", f"{BASE}/ima6.jpeg"],
        "telephone": "+91-99942-47450",
        "address": {
            "@type": "PostalAddress",
            "streetAddress": "SSM Nagar, New Perungalathur",
            "addressLocality": "Chennai",
            "addressRegion": "Tamil Nadu",
            "postalCode": "600063",
            "addressCountry": "IN",
        },
        "geo": {"@type": "GeoCoordinates", "latitude": 12.8938068, "longitude": 80.1131382},
        "hasMap": ("https://www.google.com/maps/search/?api=1"
                   "&query=SSM+Nagar+New+Perungalathur+Chennai"),
        "openingHoursSpecification": [{
            "@type": "OpeningHoursSpecification",
            "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"],
            "opens": OPEN_FROM, "closes": OPEN_TO,
        }],
        "areaServed": [{"@type": "Place", "name": n} for n in AREAS + ["Chennai"]],
        "knowsLanguage": ["en", "ta"],
        "employee": {"@id": f"{BASE}/#karthika"},
        "availableChannel": {"@type": "ServiceChannel", "serviceType": "Online yoga class",
                             "availableLanguage": ["en", "ta"]},
        "hasOfferCatalog": {
            "@type": "OfferCatalog",
            "name": "Yoga classes at Happy Yogis",
            "itemListElement": [
                {"@type": "Offer", "itemOffered": {
                    "@type": "Service", "name": name, "description": desc,
                    "serviceType": name, "provider": {"@id": f"{BASE}/#business"},
                    "areaServed": {"@type": "City", "name": "Chennai"},
                }} for name, desc in CLASSES
            ],
        },
    }


def person_node():
    return {
        "@type": "Person",
        "@id": f"{BASE}/#karthika",
        "name": "Karthika",
        "jobTitle": "Yoga teacher",
        "image": f"{BASE}/instructor.jpeg",
        "description": ("Teacher at Happy Yogis Yoga Centre, New Perungalathur, with more "
                        "than ten years of yoga practice and teaching experience."),
        "worksFor": {"@id": f"{BASE}/#business"},
        "knowsAbout": ["Hatha Yoga", "Power Yoga", "Pranayama", "Meditation",
                       "Prenatal Yoga", "Therapeutic Yoga"],
    }
