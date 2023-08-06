import openpyxl
import pandas as pd
import clearing
from rich import print
from rich.console import Console
from rich.table import Table


def display_invoice_report():
    console = Console()
    clearing.clear()
    sales_report = pd.read_excel("invoices.xlsx")
    table_stock = Table(show_header=False, header_style="bold blue")
    table_stock.add_row("-----------------------------------SALES REPORT-----------------------------------")
    console.print(table_stock)
    print(sales_report)
    print("-"*36, "END-OF-REPORT", "-"*36)
    console = Console()
