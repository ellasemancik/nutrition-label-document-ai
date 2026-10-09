
import argparse
import hashlib
import io
import json
import re
import time
from pathlib import Path

import requests
from PIL import Image, ImageOps


# Project folders
ROOT = Path(__file__).resolve().parents[1]
RAW_DIR = ROOT / "data" / "raw"
MANIFEST = ROOT / "data" / "import_manifest.jsonl"

# Open Food Facts
SEARCH_URL = "https://world.openfoodfacts.org/api/v2/search"
IMAGE_BASE = "https://images.openfoodfacts.org/images/products"

# Replace with your own contact email
USER_AGENT = "NutritionLabelDocumentAI/1.0 (your-email@example.com)"

session = requests.Session()
session.headers.update({"User-Agent": USER_AGENT})


def existing_labels():
    numbers = []

    for folder in RAW_DIR.glob("label_*"):
        if not folder.is_dir():
            continue

        match = re.fullmatch(r"label_(\d+)", folder.name)

        if match:
            numbers.append(int(match.group(1)))

    return numbers


def existing_imports():
    codes = set()
    hashes = set()

    if MANIFEST.exists():
        with MANIFEST.open("r", encoding="utf-8") as file:
            for line in file:
                if not line.strip():
                    continue

                record = json.loads(line)

                if record.get("barcode"):
                    codes.add(record["barcode"])

                if record.get("sha256"):
                    hashes.add(record["sha256"])

    return codes, hashes


def get_nutrition_image_url(product):
    code = str(product.get("code", ""))
    images = product.get("images") or {}

    # Look for an English nutrition image
    nutrition = images.get("nutrition_en")

    if isinstance(nutrition, dict):
        revision = nutrition.get("rev")

        if revision is not None and code.isdigit():
            padded = code.zfill(13)

            folder = "/".join([
                padded[:3],
                padded[3:6],
                padded[6:9],
                padded[9:]
            ])

            return (
                f"{IMAGE_BASE}/{folder}/"
                f"nutrition_en.{revision}.full.jpg"
            )

    # Fallback to the selected image URL
    selected = product.get("selected_images") or {}
    nutrition = selected.get("nutrition") or {}
    display = nutrition.get("display") or {}

    return display.get("en")


def search_products(page):
    params = {
        "countries_tags_en": "united-states",
        "states_tags": "en:nutrition-photo-selected",
        "fields": (
            "code,product_name,images,selected_images"
        ),
        "page_size": 20,
        "page": page,
        "sort_by": "nothing"
    }

    for attempt in range(2):
        try:
            response = session.get(
                SEARCH_URL,
                params=params,
                timeout=40
            )

            response.raise_for_status()

            return response.json().get("products", [])

        except requests.RequestException as error:
            print(
                f"Page {page}, attempt {attempt + 1}/2: "
                f"{error}"
            )

            if attempt == 0:
                print("Waiting 15 seconds...")
                time.sleep(15)

    return None


def download_image(url):
    try:
        response = session.get(url, timeout=30)
        response.raise_for_status()

        if len(response.content) > 15_000_000:
            return None

        image = Image.open(io.BytesIO(response.content))
        image = ImageOps.exif_transpose(image)
        image = image.convert("RGB")

        # Skip very small images
        if min(image.size) < 200:
            return None

        return image

    except (requests.RequestException, OSError):
        return None


def image_bytes(image):
    buffer = io.BytesIO()
    image.save(buffer, format="PNG")
    return buffer.getvalue()


def import_labels(count, max_pages):
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    MANIFEST.parent.mkdir(parents=True, exist_ok=True)

    codes, hashes = existing_imports()

    next_number = max(existing_labels(), default=0) + 1
    imported = 0
    failed_pages = 0

    print(f"Looking for {count} new nutrition labels...\n")

    for page in range(1, max_pages + 1):
        if imported >= count:
            break

        products = search_products(page)

        if products is None:
            failed_pages += 1

            if failed_pages >= 3:
                print("Too many failed searches. Stopping.")
                break

            continue

        failed_pages = 0

        if not products:
            print("No more products returned.")
            break

        available = sum(
            1 for product in products
            if get_nutrition_image_url(product)
        )

        print(
            f"Page {page}: {len(products)} products, "
            f"{available} nutrition images"
        )

        for product in products:
            if imported >= count:
                break

            code = str(product.get("code", ""))

            if not code or code in codes:
                continue

            image_url = get_nutrition_image_url(product)

            if not image_url:
                continue

            image = download_image(image_url)

            if image is None:
                continue

            data = image_bytes(image)
            digest = hashlib.sha256(data).hexdigest()

            if digest in hashes:
                continue

            # Find the next unused label number
            while (RAW_DIR / f"label_{next_number:02d}").exists():
                next_number += 1

            label_id = f"label_{next_number:02d}"
            folder = RAW_DIR / label_id

            folder.mkdir()

            image_path = folder / f"{label_id}.png"
            image_path.write_bytes(data)

            record = {
                "label_id": label_id,
                "barcode": code,
                "product_name": product.get("product_name"),
                "source": "Open Food Facts",
                "image_url": image_url,
                "product_url": (
                    f"https://world.openfoodfacts.org/product/{code}"
                ),
                "sha256": digest,
                "annotation_status": "unverified"
            }

            with MANIFEST.open("a", encoding="utf-8") as file:
                file.write(json.dumps(record) + "\n")

            codes.add(code)
            hashes.add(digest)

            imported += 1
            next_number += 1

            print(f"[{imported}/{count}] Imported {label_id}")

            # Be respectful of the image server
            time.sleep(1)

        time.sleep(7)

    print("\nImport finished!")
    print(f"New labels imported: {imported}")
    print(f"Saved to: {RAW_DIR}")
    print(f"Manifest: {MANIFEST}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--count",
        type=int,
        default=10
    )

    parser.add_argument(
        "--max-pages",
        type=int,
        default=30
    )

    args = parser.parse_args()

    if args.count < 1 or args.max_pages < 1:
        parser.error("Arguments must be at least 1")

    import_labels(args.count, args.max_pages)
