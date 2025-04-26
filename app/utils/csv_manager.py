import csv
from typing import Dict, List

def read_csv(file_path: str) -> List[Dict]:
    """Lê um arquivo CSV com codificação UTF-8"""
    with open(file_path, mode="r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        return [row for row in reader]

def write_csv(file_path: str, data: List[Dict], fieldnames: List[str]):
    """Escreve no arquivo CSV com codificação UTF-8"""
    with open(file_path, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)