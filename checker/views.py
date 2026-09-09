from django.shortcuts import render
from django.db.models import Q

from .models import Medicine, Interaction
from .ai_helper import ai_available, generate_medicine_info, generate_interaction_info


def home(request):
    return render(request, "checker/home.html", {"ai_on": ai_available()})


def _get_or_create_medicine(name):
    """DB-first lookup; falls back to AI generation and caches the result."""
    name = name.strip()
    if not name:
        return None, False

    medicine = Medicine.objects.filter(name__iexact=name).first()
    if medicine:
        return medicine, False

    # try matching a brand name too
    medicine = Medicine.objects.filter(brand_names__icontains=name).first()
    if medicine:
        return medicine, False

    if not ai_available():
        return None, False

    data = generate_medicine_info(name)
    if not data or not data.get("used_for") or "not recognized" in data.get("used_for", "").lower():
        return None, False

    medicine = Medicine.objects.create(
        name=name.title(),
        category=data.get("category", ""),
        used_for=data.get("used_for", ""),
        common_side_effects=data.get("common_side_effects", ""),
        serious_side_effects=data.get("serious_side_effects", ""),
        requires_prescription=bool(data.get("requires_prescription", False)),
        source="ai",
    )
    return medicine, True


def medicine_lookup(request):
    query = request.GET.get("q", "").strip()
    medicine = None
    ai_generated = False
    not_found = False

    if query:
        medicine, ai_generated = _get_or_create_medicine(query)
        not_found = medicine is None

    return render(
        request,
        "checker/medicine_lookup.html",
        {
            "query": query,
            "medicine": medicine,
            "ai_generated": ai_generated,
            "not_found": not_found,
            "ai_on": ai_available(),
        },
    )


def _get_interaction(med1, med2):
    return Interaction.objects.filter(
        Q(medicine_1=med1, medicine_2=med2) | Q(medicine_1=med2, medicine_2=med1)
    ).first()


def interaction_check(request):
    name1 = request.GET.get("med1", "").strip()
    name2 = request.GET.get("med2", "").strip()

    context = {"name1": name1, "name2": name2, "ai_on": ai_available()}

    if not name1 or not name2:
        return render(request, "checker/interaction_check.html", context)

    med1, _ = _get_or_create_medicine(name1)
    med2, _ = _get_or_create_medicine(name2)

    if not med1 or not med2:
        context["lookup_failed"] = True
        context["missing"] = []
        if not med1:
            context["missing"].append(name1)
        if not med2:
            context["missing"].append(name2)
        return render(request, "checker/interaction_check.html", context)

    context["med1"] = med1
    context["med2"] = med2

    interaction = _get_interaction(med1, med2)
    ai_generated = False

    if not interaction and ai_available():
        data = generate_interaction_info(med1.name, med2.name)
        if data and data.get("combined_effects"):
            interaction = Interaction.objects.create(
                medicine_1=med1,
                medicine_2=med2,
                severity=data.get("severity", "caution"),
                combined_effects=data.get("combined_effects", ""),
                explanation=data.get("explanation", ""),
                advice=data.get("advice", ""),
                source="ai",
            )
            ai_generated = True

    context["interaction"] = interaction
    context["ai_generated"] = ai_generated
    context["no_data"] = interaction is None

    return render(request, "checker/interaction_check.html",context)
