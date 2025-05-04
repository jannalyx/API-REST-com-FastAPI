import csv
import os
from typing import Dict, List

def read_csv(file_path: str) -> List[Dict]:
    with open(file_path, mode="r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        return [row for row in reader]

def write_csv(file_path: str, data: List[Dict], fieldnames: List[str]):
    with open(file_path, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)

def read_pedidos_csv(file_path: str) -> List[Dict]:
    pedidos = read_csv(file_path)
    for pedido in pedidos:
        pedido['livros'] = eval(pedido['livros']) 
    return pedidos

def write_pedidos_csv(file_path: str, pedidos: List[Dict], fieldnames: List[str]):
    write_csv(file_path, pedidos, fieldnames)

def contar_registros_csv(caminho_arquivo: str) -> int:
    if not os.path.exists(caminho_arquivo):
        return 0
    with open(caminho_arquivo, mode="r", encoding="utf-8") as arquivo:
        leitor = csv.reader(arquivo)
        next(leitor, None) 
        return sum(1 for _ in leitor)

