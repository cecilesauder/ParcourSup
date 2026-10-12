from fractions import Fraction

from parcoursup_prototype.order_call import (
    Applicant,
    choose_with_scholarship_reserve,
    prefix_quota_order,
)


applicants = (
    Applicant("N1", 1, False),
    Applicant("N2", 2, False),
    Applicant("N3", 3, False),
    Applicant("B4", 4, True),
)
rate = Fraction(1, 4)
capacity = 4

call_order = prefix_quota_order(applicants, rate)
selected_set = choose_with_scholarship_reserve(applicants, capacity, rate)

print("Ordre d'appel simplifié (le rang est l'ordre d'envoi) :")
for position, applicant in enumerate(call_order, start=1):
    label = "boursier·e" if applicant.scholarship_holder else "autre"
    print(f"  {position}. {applicant.applicant_id} (rang pédagogique {applicant.rank}, {label})")

print("\nEnsemble choisi par la réserve expérimentale (ce n'est pas un ordre d'appel) :")
for applicant in selected_set:
    label = "boursier·e" if applicant.scholarship_holder else "autre"
    print(f"  {applicant.applicant_id} (rang pédagogique {applicant.rank}, {label})")

print("\nCe cas illustre un rang d'appel déplacé, pas un résultat sur les délais réels.")
