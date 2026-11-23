import csv
from pathlib import Path
from price_analysis.models import LoadResult, PriceRecord

from price_analysis.exceptions import PriceLoadError, MissingColumnError


def read_records(path:str):
    """Получает файл и построчно читает его"""
    with open(path, encoding = "utf-8") as f:
        reader = csv.DictReader(f)
        missing = {"sku", "name", "price"} - set(reader.fieldnames or [])
        if missing:
            raise MissingColumnError(Path(path).name, missing)
        for lineno, row in enumerate(reader, start = 2):
            try:
                record = PriceRecord(sku=row["sku"], name=row["name"],
                                     price=float(row["price"]), source=Path(path).name)
            except ValueError as e:
                raise PriceLoadError(Path(path).name, f"неправильный формат: {e}", lineno)
            yield record


def load_price_list(path:str):
    """Принимает путь до файла и возвращает записи и предупреждения о повторении"""
    records, warnings, seen = {}, [], set()
    for record in read_records(path):
        if record.sku in seen:
            warnings.append(f"Дубль SKU {record.sku}")
            continue
        seen.add(record.sku)
        records[record.sku] = record
    return LoadResult(records = records, warnings = warnings)


if __name__ == "__main__":
    print(load_price_list("../../data/shop.csv"))