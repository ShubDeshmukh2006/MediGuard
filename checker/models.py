from django.db import models


class Medicine(models.Model):
    name = models.CharField(max_length=150, unique=True)
    brand_names = models.CharField(max_length=300, blank=True, help_text="Comma-separated common brand names")
    category = models.CharField(max_length=100, blank=True, help_text="e.g. Painkiller, Antibiotic, Antacid")
    used_for = models.TextField(help_text="What condition/symptom this medicine treats")
    common_side_effects = models.TextField(blank=True)
    serious_side_effects = models.TextField(blank=True, help_text="Effects that need urgent medical attention")
    requires_prescription = models.BooleanField(default=False)
    source = models.CharField(
        max_length=20,
        choices=[("seed", "Seed data"), ("ai", "AI-generated"), ("admin", "Manually added")],
        default="seed",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta :
        ordering = ["name"]

    def __str__(self):
        return self.name


class Interaction(models.Model):
    SEVERITY_CHOICES = [
        ("safe", "Generally Safe"),
        ("caution", "Use With Caution"),
        ("avoid", "Avoid Combination"),
    ]

    medicine_1 = models.ForeignKey(Medicine, related_name="interactions_as_first", on_delete=models.CASCADE)
    medicine_2 = models.ForeignKey(Medicine, related_name="interactions_as_second", on_delete=models.CASCADE)
    severity = models.CharField(max_length=10, choices=SEVERITY_CHOICES)
    combined_effects = models.TextField(help_text="What happens if both are taken together")
    explanation = models.TextField(help_text="Why this happens (mechanism)")
    advice = models.TextField(help_text="Practical recommendation: take / avoid / space doses / consult doctor")
    source = models.CharField(
        max_length=20,
        choices=[("seed", "Seed data"), ("ai", "AI-generated"), ("admin", "Manually added")],
        default="seed",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("medicine_1", "medicine_2")

    def __str__(self):
        return f"{self.medicine_1.name} + {self.medicine_2.name}"
