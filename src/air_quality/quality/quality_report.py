from collections import Counter


def generate_quality_report(
    accepted: list[dict],
    rejected: list[dict],
) -> dict:

    total = len(accepted) + len(rejected)

    rejection_reasons = Counter()
    rejection_stages = Counter()

    for record in rejected:
        rejection_stages[record["stage"]] += 1

        for error in record["errors"]:
            rejection_reasons[error] += 1

    acceptance_rate = (
        len(accepted) / total * 100
        if total > 0
        else 0.0
    )

    report = {
        "total_records": total,
        "accepted_records": len(accepted),
        "rejected_records": len(rejected),
        "acceptance_rate": round(acceptance_rate, 2),
        "rejection_stages": dict(rejection_stages),
        "rejection_reasons": dict(rejection_reasons),
    }

    return report