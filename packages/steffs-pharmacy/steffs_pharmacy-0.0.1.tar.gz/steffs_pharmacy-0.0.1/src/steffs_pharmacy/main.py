import pandas as pd
import time
import clearing
from searchdrugs import search_drugs
from customerorder import customer_order
from displayinvoicereport import display_invoice_report
from displaystockreport import display_stock_report
from rich import print
from rich.console import Console
from rich.table import Table
#Steffs Pharmacy Main function
def main():
    console = Console()
    cart = []
    while True:
        clearing.clear()
        print("*****************************")
        table = Table(show_header=False, header_style="bold blue",
                      title="MENU", title_justify="center")
        table.add_row("1. Search for Medicine")
        table.add_row("2. Customer Order")
        table.add_row("3. Stock In Hand Report")
        table.add_row("4. Sales Report")
        table.add_row("5. Exit")
        console.print(table)
        print("*****************************")

        try:
            choice = int(input("Choose your Option :"))
        except ValueError:
            print("Invalid Option !")
            time.sleep(2)
            continue
        if choice == 1:
            search_drugs()
        elif choice == 2:
            cart = customer_order(cart)
        elif choice == 3:
            display_stock_report()
        elif choice == 4:
            display_invoice_report()
        elif choice == 5:
            exit()
        else:
            # invalid choice
            print(f'Choice {choice} is invalid')
            continue


main()
