
"""Compare OCR settings across nutrition labels and flag results for review."""

import argparse
import csv
import json
import tempfile
from pathlib import Path

from confidence import calculate_confidence
from extract_fields import extract_nutrition_fields
from ocr_reader import read_text
from preprocess import make_grayscale, make_larger, make_thresholded
from validate import validate_results


ROOT = Path(__file__).resolve().parent.parent
RAW = ROOT / "data" / "raw"
OUTPUT = ROOT / "data" / "outputs" / "batch_review"

METHODS = [
    ("original_psm6", "original", 6),
    ("original_psm11", "original", 11),
    ("grayscale_psm6", "grayscale", 6),
    ("large_psm6", "large", 6),
    ("large_psm11", "large", 11),
    ("threshold_psm6", "threshold", 6),
    ("threshold_psm11", "threshold", 11),
]


def prepare_images(image_path, temporary_folder):
    """Create the image versions used by the OCR experiments."""
    folder = Path(temporary_folder)

    paths = {
        "original": image_path,
        "grayscale": folder / "grayscale.png",
        "large": folder / "large.png",
        "threshold": folder / "threshold.png",
    }

    make_grayscale(str(image_path), str(paths["grayscale"]))
    make_larger(str(image_path), str(paths["large"]))
    make_thresholded(str(image_path), str(paths["threshold"]))

    return paths


def evaluate_method(method_name, image_path, psm):
    """Run OCR, extract fields, and calculate review metrics."""
    text = read_text(str(image_path), config=f"--psm {psm}")
    fields = extract_nutrition_fields(text)
    warnings = validate_results(fields)

    found = sum(value is not None for value in fields.values())
    extra_warnings = [
        warning for warning in warnings
        if "was not found" not in warning
    ]

    confidence = calculate_confidence(fields, warnings)

    return {
        "method": method_name,
        "text": text,
        "fields": fields,
        "warnings": warnings,
        "fields_found": found,
        "fields_total": len(fields),
        "extra_warnings": extra_warnings,
        "confidence": confidence,
    }


def rank_candidate(candidate):
    """Prefer fewer validation issues, then greater field coverage."""
    return (
        -len(candidate["extra_warnings"]),
        candidate["fields_found"],
    )


def review_priority(candidate, disagreement):
    if candidate["fields_found"] < 6 or candidate["extra_warnings"]:
        return "high"
    if disagreement:
        return "high"
    if candidate["fields_found"] < 9:
        return "medium"
    return "low"


def main():
    parser = argparse.ArgumentParser(
        description="Compare OCR methods on imported nutrition labels"
    )
    parser.add_argument("--start", type=int, default=7)
    parser.add_argument("--end", type=int, default=100)
    args = parser.parse_args()

    if args.start < 1 or args.end < args.start:
        parser.error("Use a valid range, such as --start 7 --end 16")

    OUTPUT.mkdir(parents=True, exist_ok=True)
    rows = []

    for number in range(args.start, args.end + 1):
        label = f"label_{number:02d}"
        image_path = RAW / label / f"{label}.png"

        row = {
            "label": label,
            "status": "",
            "best_method": "",
            "fields_found": 0,
            "fields_total": 11,
            "coverage_percent": 0,
            "confidence_percent": 0,
            "validation_issue_count": 0,
            "method_disagreement": "",
            "review_priority": "",
            "error": "",
        }

        if not image_path.is_file():
            row.update(
                status="missing_image",
                review_priority="check_file",
                error="Image not found",
            )
            rows.append(row)
            print(f"{label}: image not found")
            continue

        try:
            candidates = []
            method_errors = {}

            with tempfile.TemporaryDirectory() as temp_dir:
                paths = prepare_images(image_path, temp_dir)

                for method_name, image_version, psm in METHODS:
                    try:
                        candidate = evaluate_method(
                            method_name, paths[image_version], psm
                        )
                        candidates.append(candidate)
                    except Exception as exc:
                        method_errors[method_name] = (
                            f"{type(exc).__name__}: {exc}"
                        )

            if not candidates:
                raise RuntimeError("All OCR methods failed")

            best = max(candidates, key=rank_candidate)

            # Check whether other methods extracted different values.
            disagreement_fields = []
            for field, selected_value in best["fields"].items():
                if selected_value is None:
                    continue

                other_values = {
                    str(candidate["fields"].get(field))
                    for candidate in candidates
                    if candidate["fields"].get(field) is not None
                }

                if len(other_values) > 1:
                    disagreement_fields.append(field)

            disagreement = bool(disagreement_fields)
            priority = review_priority(best, disagreement)
            coverage = (
                100 * best["fields_found"] / best["fields_total"]
                if best["fields_total"] else 0
            )

            # Save the selected OCR text.
            (OUTPUT / f"{label}_ocr.txt").write_text(
                best["text"], encoding="utf-8"
            )

            # Save all candidate results for comparison.
            comparison = {
                "label": label,
                "best_method": best["method"],
                "disagreement_fields": disagreement_fields,
                "method_errors": method_errors,
                "methods": [
                    {
                        "method": candidate["method"],
                        "fields_found": candidate["fields_found"],
                        "fields": candidate["fields"],
                        "validation_warnings": candidate["warnings"],
                    }
                    for candidate in candidates
                ],
            }

            (OUTPUT / f"{label}_comparison.json").write_text(
                json.dumps(comparison, indent=2, ensure_ascii=False),
                encoding="utf-8",
            )

            result = {
                "label": label,
                "image": str(image_path.relative_to(ROOT)),
                "best_ocr_method": best["method"],
                "fields": best["fields"],
                "validation_status": (
                    "warning" if best["warnings"] else "passed"
                ),
                "validation_warnings": best["warnings"],
                "confidence_score": best["confidence"],
                "review_priority": priority,
                "disagreement_fields": disagreement_fields,
                "note": (
                    "Unverified extraction. Field coverage and confidence "
                    "are not measured accuracy."
                ),
            }

            (OUTPUT / f"{label}_extracted.json").write_text(
                json.dumps(result, indent=2, ensure_ascii=False),
                encoding="utf-8",
            )

            row.update(
                status="processed",
                best_method=best["method"],
                fields_found=best["fields_found"],
                fields_total=best["fields_total"],
                coverage_percent=round(coverage, 2),
                confidence_percent=round(best["confidence"] * 100, 2),
                validation_issue_count=len(best["extra_warnings"]),
                method_disagreement="yes" if disagreement else "no",
                review_priority=priority,
            )

            print(
                f"{label}: {best['method']} | "
                f"{best['fields_found']}/{best['fields_total']} fields | "
                f"review: {priority}"
            )

        except Exception as exc:
            row.update(
                status="error",
                review_priority="check_file",
                error=f"{type(exc).__name__}: {exc}",
            )
            print(f"{label}: ERROR - {exc}")

        rows.append(row)

    report_path = OUTPUT / "review_report.csv"

    with report_path.open("w", newline="", encoding="utf-8-sig") as file:
        writer = csv.DictWriter(file, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)

    processed = [row for row in rows if row["status"] == "processed"]

    print(f"\nProcessed {len(processed)} of {len(rows)} labels.")

    if processed:
        average = sum(
            row["coverage_percent"] for row in processed
        ) / len(processed)
        print(f"Average selected field coverage: {average:.2f}%")

    print("Coverage is NOT accuracy. Results require verification.")
    print(f"Review report: {report_path.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
