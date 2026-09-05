from django.core.management.base import BaseCommand
from checker.models import Medicine, Interaction


MEDICINES = [
    dict(name="Paracetamol", brand_names="Crocin, Tylenol, Calpol", category="Painkiller / Fever reducer",
         used_for="Relieves mild to moderate pain (headache, muscle ache, toothache) and reduces fever.",
         common_side_effects="Nausea, mild rash, rarely stomach upset.",
         serious_side_effects="Liver damage in overdose, severe allergic reaction, yellowing of skin/eyes.",
         requires_prescription=False),
    dict(name="Ibuprofen", brand_names="Advil, Brufen", category="NSAID Painkiller",
         used_for="Reduces pain, inflammation, and fever (headaches, arthritis, muscle strains).",
         common_side_effects="Stomach upset, heartburn, dizziness, nausea.",
         serious_side_effects="Stomach bleeding/ulcers, kidney problems, increased risk of heart attack with long-term use.",
         requires_prescription=False),
    dict(name="Aspirin", brand_names="Disprin, Ecosprin", category="NSAID / Blood thinner",
         used_for="Relieves pain and fever; low doses used to prevent blood clots (heart attack/stroke prevention).",
         common_side_effects="Stomach irritation, heartburn, nausea.",
         serious_side_effects="Gastrointestinal bleeding, allergic reaction, Reye's syndrome in children.",
         requires_prescription=False),
    dict(name="Warfarin", brand_names="Coumadin", category="Anticoagulant (blood thinner)",
         used_for="Prevents and treats blood clots in conditions like atrial fibrillation and DVT.",
         common_side_effects="Easy bruising, minor bleeding (gums, nosebleeds).",
         serious_side_effects="Severe internal bleeding, blood in urine/stool.",
         requires_prescription=True),
    dict(name="Amoxicillin", brand_names="Amoxil, Novamox", category="Antibiotic",
         used_for="Treats bacterial infections such as ear infections, throat infections, and UTIs.",
         common_side_effects="Diarrhea, nausea, mild rash.",
         serious_side_effects="Severe allergic reaction (anaphylaxis), severe diarrhea (C. difficile infection).",
         requires_prescription=True),
    dict(name="Cetirizine", brand_names="Zyrtec, Cetrizet", category="Antihistamine",
         used_for="Relieves allergy symptoms like sneezing, runny nose, itchy eyes, and hives.",
         common_side_effects="Drowsiness, dry mouth, fatigue.",
         serious_side_effects="Severe allergic reaction (rare).",
         requires_prescription=False),
    dict(name="Omeprazole", brand_names="Prilosec, Omez", category="Proton pump inhibitor (antacid)",
         used_for="Reduces stomach acid to treat acid reflux, heartburn, and stomach ulcers.",
         common_side_effects="Headache, nausea, stomach pain, diarrhea.",
         serious_side_effects="Increased fracture risk with long-term use, low magnesium levels.",
         requires_prescription=False),
    dict(name="Metformin", brand_names="Glucophage", category="Antidiabetic",
         used_for="Controls blood sugar levels in type 2 diabetes.",
         common_side_effects="Nausea, diarrhea, stomach upset, metallic taste.",
         serious_side_effects="Lactic acidosis (rare but serious), vitamin B12 deficiency with long-term use.",
         requires_prescription=True),
]

INTERACTIONS = [
    dict(m1="Aspirin", m2="Warfarin", severity="avoid",
         combined_effects="Significantly increases the risk of serious bleeding, including internal and gastrointestinal bleeding.",
         explanation="Both drugs reduce the blood's ability to clot through different mechanisms, so combining them has an additive anticoagulant effect.",
         advice="Do not combine without direct medical supervision. If a doctor has prescribed both, dosing and monitoring (INR tests) must be closely managed by them."),
    dict(m1="Ibuprofen", m2="Aspirin", severity="avoid",
         combined_effects="Increased risk of stomach irritation, ulcers, and gastrointestinal bleeding. Ibuprofen may also reduce aspirin's heart-protective effect.",
         explanation="Both are NSAIDs that irritate the stomach lining and affect blood clotting; taking them together compounds these effects.",
         advice="Avoid routine combination. If you take low-dose aspirin for heart protection, ask your doctor before also using ibuprofen for pain."),
    dict(m1="Paracetamol", m2="Ibuprofen", severity="safe",
         combined_effects="Can generally be taken together and are sometimes alternated for stronger pain relief, as they work through different mechanisms.",
         explanation="Paracetamol works mainly in the brain to reduce pain/fever, while ibuprofen reduces inflammation at the site of injury, so their effects don't directly compound risk in the same way NSAID combinations do.",
         advice="Usually fine for short-term use at recommended doses, but confirm with a pharmacist, especially if you have stomach, kidney, or liver issues."),
    dict(m1="Omeprazole", m2="Metformin", severity="safe",
         combined_effects="No significant interaction expected between these two medicines.",
         explanation="They act on different body systems (stomach acid vs. blood sugar) with no major overlapping mechanism.",
         advice="Generally fine to take together as prescribed, but always confirm timing with your doctor if you're on both long-term."),
    dict(m1="Cetirizine", m2="Amoxicillin", severity="caution",
         combined_effects="No major dangerous interaction, but both can occasionally cause drowsiness or stomach upset, which may feel more pronounced together.",
         explanation="They act through unrelated pathways, but overlapping mild side effects (drowsiness, GI upset) can add up.",
         advice="Usually safe together, but monitor for excessive drowsiness or stomach discomfort, and consult a pharmacist if symptoms are bothersome."),
]


class Command(BaseCommand):
    help = "Seed the database with sample medicines and interactions."

    def handle(self, *args, **options):
        created_meds = 0
        med_objs = {}
        for m in MEDICINES:
            obj, created = Medicine.objects.get_or_create(name=m["name"], defaults={**m, "source": "seed"})
            med_objs[m["name"]] = obj
            created_meds += created

        created_inter = 0
        for i in INTERACTIONS:
            m1, m2 = med_objs[i["m1"]], med_objs[i["m2"]]
            _, created = Interaction.objects.get_or_create(
                medicine_1=m1, medicine_2=m2,
                defaults=dict(severity=i["severity"], combined_effects=i["combined_effects"],
                              explanation=i["explanation"], advice=i["advice"], source="seed"),
            )
            created_inter += created

        self.stdout.write(self.style.SUCCESS(
            f"Seeded {created_meds} new medicines and {created_inter} new interactions."
        ))
