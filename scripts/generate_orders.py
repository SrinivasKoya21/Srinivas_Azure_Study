"""
generate_orders.py
Simulates a stream of order-event JSON files landing in an ADLS Gen2
container, one file per small batch of orders, mimicking what an
e-commerce checkout system would produce.

Usage:
    python scripts/generate_orders.py --batches 5 --orders-per-batch 40
"""

import argparse
import json
import random
import uuid
from datetime import datetime, timedelta, timezone
from pathlib import Path

from faker import Faker

# azure-storage-file-datalake is only needed if you pass --upload, so it's
# imported lazily inside upload_to_adls() below instead of here. That way
# this script runs for local dataset generation with just `pip install faker`.

fake = Faker()

# Must match the seed data you loaded into Postgres in section 2.2
CUSTOMER_IDS = list(range(1, 16))          # customer_id 1..15
PRODUCT_CATALOG = [
    (1, 89.99), (2, 39.99), (3, 74.50), (4, 199.00), (5, 129.99),
    (6, 34.99), (7, 84.99), (8, 24.99), (9, 149.00), (10, 59.99),
    (11, 129.00), (12, 19.99), (13, 44.99), (14, 34.50), (15, 49.99),
]  # (product_id, unit_price) — mirrors the products table

STATUSES = ["PLACED", "PLACED", "PLACED", "PLACED", "CANCELLED"]  # ~20% cancelled, for DQ practice


def make_order_event() -> dict:
    """Build one realistic (and occasionally intentionally messy) order-event dict."""
    product_id, unit_price = random.choice(PRODUCT_CATALOG)
    quantity = random.randint(1, 4)
    order_ts = datetime.now(timezone.utc) - timedelta(minutes=random.randint(0, 4320))

    event = {
        "order_id": str(uuid.uuid4()),
        "customer_id": random.choice(CUSTOMER_IDS),
        "product_id": product_id,
        "quantity": quantity,
        "unit_price": unit_price,
        "order_status": random.choice(STATUSES),
        "order_timestamp": order_ts.isoformat(),
        "shipping_country": fake.country_code(),
    }

    # Intentionally inject a small amount of dirty data so Phase 3's
    # data-quality expectations have something real to catch.
    roll = random.random()
    if roll < 0.03:
        event["order_id"] = None                      # missing primary key
    elif roll < 0.06:
        event["quantity"] = -1                          # invalid quantity
    elif roll < 0.09:
        event["customer_id"] = 9999                     # orphaned customer_id

    return event


def write_batch_locally(batch: list[dict], out_dir: Path) -> Path:
    out_dir.mkdir(parents=True, exist_ok=True)
    file_name = f"orders_{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%f')}.json"
    file_path = out_dir / file_name
    with file_path.open("w") as f:
        for event in batch:
            f.write(json.dumps(event) + "\n")   # newline-delimited JSON
    return file_path


def upload_to_adls(local_path: Path, account_name: str, container: str, directory: str):
    from azure.storage.filedatalake import DataLakeServiceClient  # lazy import, see note above

    service_client = DataLakeServiceClient(
        account_url=f"https://{account_name}.dfs.core.windows.net",
        credential=None,  # uses `az login` credentials via DefaultAzureCredential if configured;
                           # simplest for this project: use account_key instead, see note below
    )
    fs_client = service_client.get_file_system_client(container)
    dir_client = fs_client.get_directory_client(directory)
    file_client = dir_client.create_file(local_path.name)
    with local_path.open("rb") as f:
        data = f.read()
    file_client.append_data(data, offset=0, length=len(data))
    file_client.flush_data(len(data))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--batches", type=int, default=5, help="how many files to generate")
    parser.add_argument("--orders-per-batch", type=int, default=40)
    parser.add_argument("--local-dir", default="./data/orders_landing")
    parser.add_argument("--upload", action="store_true", help="also upload each file to ADLS")
    parser.add_argument("--account-name", default="")
    parser.add_argument("--container", default="landing")
    parser.add_argument("--directory", default="orders")
    args = parser.parse_args()

    out_dir = Path(args.local_dir)

    for i in range(args.batches):
        batch = [make_order_event() for _ in range(args.orders_per_batch)]
        local_path = write_batch_locally(batch, out_dir)
        print(f"[{i+1}/{args.batches}] wrote {local_path} ({len(batch)} events)")

        if args.upload:
            upload_to_adls(local_path, args.account_name, args.container, args.directory)
            print(f"    uploaded to abfss://{args.container}@{args.account_name}.dfs.core.windows.net/{args.directory}/{local_path.name}")


if __name__ == "__main__":
    main()
