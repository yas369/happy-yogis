import os
#!/usr/bin/env python3
"""Build and validate the JSON-LD @graph for index.html, then inject it."""
import json
import re

# The site root, derived from this file's location so a clone works
# wherever it sits. HAPPY_YOGIS_ROOT overrides it if ever needed.
_SITE = os.environ.get("HAPPY_YOGIS_ROOT") or os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

BASE = "https://happyyogis.in"
PHONE = "+91-99942-47450"

SERVICES = [
    ("Beginner Yoga", "Foundation yoga for new students, taught step by step at a comfortable pace."),
    ("Weight Loss Yoga", "Fat-reduction and metabolism-focused yoga sessions for sustainable results."),
    ("Meditation & Pranayama", "Guided meditation and breathing practice for inner calm and mental clarity."),
    ("Flexibility & Mobility", "Targeted stretching and mobility routines to improve posture and flexibility."),
    ("Women Wellness Yoga", "Wellness-focused yoga for women, including PCOD, thyroid and hormonal balance."),
    ("Senior Citizen Yoga", "Safe, low-impact yoga for elders to maintain mobility and joint health."),
    ("Stress Relief & Relaxation", "Relaxation-focused yoga practice for modern stress management."),
    ("Corporate Wellness", "On-site and online wellness sessions for companies and teams in Chennai."),
    ("Kids Yoga", "Fun yoga for children that builds focus, confidence and healthy habits early."),
]

FAQS = [
    ("What makes Happy Yogis different from other yoga centres?",
     "Happy Yogis focuses on a power yoga approach combined with flexibility training, stability improvement, stress relief, and overall wellness. We focus on building a supportive wellness community rather than forcing rigid discipline."),
    ("Who can join the yoga classes?",
     "Our classes are suitable for beginners, working professionals, women, seniors, kids, and therapy-focused individuals looking to improve their health and wellbeing."),
    ("What are the most common reasons people join Happy Yogis?",
     "Most students join to improve their mental wellness, physical health, flexibility, stress management, and overall lifestyle balance."),
    ("How soon can students notice results?",
     "Many students begin noticing improvements in their mental wellbeing and overall energy levels within the second week of regular practice."),
    ("What type of yoga teaching style do you follow?",
     "We focus on gentle, therapeutic, and guided yoga practices that help students improve comfortably at their own pace."),
    ("Do students need to bring yoga mats?",
     "Students can safely keep their yoga mats at the centre itself for convenience."),
    ("Do you provide any yoga uniforms or dress code?",
     "Yes. Every student will be provided with a set of Happy Yogis t-shirts to wear during classes."),
    ("Will beginners feel pressured during classes?",
     "Not at all. Students are never forced into yoga practices. We focus on creating a comfortable and encouraging community environment for everyone."),
    ("Can anyone join the classes?",
     "Yes. Every abled body is welcome to join the classes and begin their wellness journey with us."),
    ("What kind of transformations have students experienced?",
     "Students have experienced improved flexibility, better physical health, reduced stress, and stronger mental wellbeing through consistent practice."),
    ("How can I enroll in the classes?",
     "You can easily enroll by contacting the Happy Yogis WhatsApp number provided on the website."),
    ("Do you focus only on physical fitness?",
     "No. Along with physical fitness, we strongly focus on mental wellness, stress relief, emotional balance, and overall holistic wellbeing."),
]

business = {
    "@type": ["LocalBusiness", "HealthAndBeautyBusiness", "SportsActivityLocation"],
    "@id": f"{BASE}/#business",
    "name": "Happy Yogis Yoga Centre",
    "alternateName": "Happy Yogis",
    "description": ("Yoga centre in New Perungalathur, Chennai offering online and offline yoga "
                    "classes for ladies, gents and kids, including beginner yoga, weight-loss yoga, "
                    "meditation, prenatal care and therapeutic wellness programmes."),
    "url": f"{BASE}/",
    "logo": {"@type": "ImageObject", "@id": f"{BASE}/#logo",
             "url": f"{BASE}/logo.png", "width": 320, "height": 362,
             "caption": "Happy Yogis Yoga Centre logo"},
    "image": [f"{BASE}/og-image.jpg", f"{BASE}/ima4.jpeg", f"{BASE}/ima1.jpeg"],
    "telephone": PHONE,
    "currenciesAccepted": "INR",
    "address": {
        "@type": "PostalAddress",
        "streetAddress": "SSM Nagar, New Perungalathur",
        "addressLocality": "Chennai",
        "addressRegion": "Tamil Nadu",
        "postalCode": "600063",
        "addressCountry": "IN",
    },
    "geo": {"@type": "GeoCoordinates", "latitude": 12.8938068, "longitude": 80.1131382},
    "hasMap": "https://www.google.com/maps/search/?api=1&query=SSM+Nagar+New+Perungalathur+Chennai",
    # Site's own contact section states Mon-Fri 5:30 AM - 6:00 PM, closed Sat/Sun.
    "openingHoursSpecification": [{
        "@type": "OpeningHoursSpecification",
        "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"],
        "opens": "05:30", "closes": "18:00",
    }],
    "areaServed": [
        {"@type": "Place", "name": n} for n in
        ["New Perungalathur", "Perungalathur", "Tambaram", "Chromepet",
         "Guduvanchery", "Selaiyur", "Medavakkam", "Chennai"]
    ],
    "knowsLanguage": ["en", "ta"],
    "sameAs": [
        "https://instagram.com/happyyogis",
        "https://facebook.com/happyyogis",
        "https://youtube.com/happyyogis",
    ],
    "employee": {"@id": f"{BASE}/#karthika"},
    "availableChannel": {
        "@type": "ServiceChannel",
        "serviceType": "Online yoga class",
        "availableLanguage": ["en", "ta"],
    },
    "hasOfferCatalog": {
        "@type": "OfferCatalog",
        "name": "Yoga programmes at Happy Yogis",
        "itemListElement": [
            {"@type": "Offer", "itemOffered": {
                "@type": "Service", "name": name, "description": desc,
                "serviceType": name,
                "provider": {"@id": f"{BASE}/#business"},
                "areaServed": {"@type": "City", "name": "Chennai"},
            }} for name, desc in SERVICES
        ],
    },
}

karthika = {
    "@type": "Person",
    "@id": f"{BASE}/#karthika",
    "name": "Karthika",
    "jobTitle": "Lead Yoga Instructor",
    "image": f"{BASE}/instructor.jpeg",
    "description": ("Lead yoga instructor at Happy Yogis with more than 10 years of practice and "
                    "teaching experience in yoga and holistic wellness."),
    "worksFor": {"@id": f"{BASE}/#business"},
    "knowsAbout": ["Hatha Yoga", "Power Yoga", "Pranayama", "Meditation",
                   "Prenatal Yoga", "Therapeutic Yoga"],
}

website = {
    "@type": "WebSite",
    "@id": f"{BASE}/#website",
    "url": f"{BASE}/",
    "name": "Happy Yogis Yoga Centre",
    "inLanguage": "en-IN",
    "publisher": {"@id": f"{BASE}/#business"},
}

webpage = {
    "@type": "WebPage",
    "@id": f"{BASE}/#webpage",
    "url": f"{BASE}/",
    "name": "Yoga Classes in Chennai | Happy Yogis Yoga Centre",
    "description": ("Yoga classes in Chennai for ladies, gents and kids at New Perungalathur. "
                    "Beginner, weight-loss, prenatal and therapy yoga."),
    "isPartOf": {"@id": f"{BASE}/#website"},
    "about": {"@id": f"{BASE}/#business"},
    "primaryImageOfPage": {"@id": f"{BASE}/#logo"},
    "inLanguage": "en-IN",
}

faqpage = {
    "@type": "FAQPage",
    "@id": f"{BASE}/#faq",
    "mainEntity": [
        {"@type": "Question", "name": q,
         "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in FAQS
    ],
}

graph = {"@context": "https://schema.org",
         "@graph": [business, karthika, website, webpage, faqpage]}

payload = json.dumps(graph, indent=2, ensure_ascii=False)
assert json.loads(payload), "schema must parse"
assert "</script" not in payload, "must not break out of the script tag"

block = ('    <!-- Structured data: LocalBusiness + Person + WebSite + WebPage + FAQPage -->\n'
         '    <script type="application/ld+json">\n' + payload + '\n    </script>\n')

path = f"{_SITE}/index.html"
html = open(path).read()
assert "application/ld+json" not in html, "an ld+json block already exists"
html = html.replace("</style>\n</head>", "</style>\n\n" + block + "</head>", 1)
open(path, "w").write(html)
print(f"injected {len(payload)} bytes of JSON-LD; "
      f"{len(SERVICES)} services, {len(FAQS)} FAQ entries")
