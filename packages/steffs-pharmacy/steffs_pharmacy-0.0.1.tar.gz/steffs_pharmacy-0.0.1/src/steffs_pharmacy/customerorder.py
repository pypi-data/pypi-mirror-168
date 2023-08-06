import time
import clearing
from rich import print
from rich.console import Console
from rich.table import Table
from searchdrugs import search_drugs
from placingcustomerorder import placing_customer_order
from billing import billing_invoice_generation
from inventoryupdate import inventory_update
from invoiceupdate import invoice_update


def customer_order(cart):
    console = Console()
    while True:
        clearing.clear()
        # Menu for getting customer order
        print("************************************")
        table = Table(show_header=False, header_style="bold blue",
                      title="CUSTOMER ORDER", title_justify="center")
        table.add_row("1. Search for medicine for customer")
        table.add_row("2. Placing the customer order")
        table.add_row("3. Verify medicines in cart and confirm order")
        table.add_row("4. Clear cart")
        table.add_row("5. Exit to main menu")
        console.print(table)
        print("************************************")
        # capture user input
        try:
            user_option = int(input("Choose an option .. "))
        # Catch  any invalid input
        except ValueError:
            print("Invalid Option !")
            time.sleep(1)
            continue
        if user_option == 1:
            search_drugs()
            time.sleep(1)
        elif user_option == 2:
            cart = placing_customer_order(cart)
            time.sleep(1)
        elif user_option == 3:
            if cart:
                invoice_number = billing_invoice_generation(cart)
                if invoice_number is not None:
                    inventory_update(cart)
                    invoice_update(cart, invoice_number)
                    cart.clear()
            else:
                print("Cart is empty !")
            time.sleep(1)
        elif user_option == 4:
            cart.clear()
            print("Cart Emptied !")
            time.sleep(1)
        elif user_option == 5:
            return cart
