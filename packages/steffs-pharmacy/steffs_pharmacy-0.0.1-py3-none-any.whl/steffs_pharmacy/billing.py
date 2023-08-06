import time
import clearing
from datetime import datetime
from rich.console import Console
from rich.table import Table
import tabulate
import openpyxl


def billing_invoice_generation(cart):
    total = 0
    console = Console()
    clearing.clear()
    while True:
        print("\n")
        table_main = Table(show_header=False, header_style="bold blue",
                           title="Billing & Invoice", title_justify="center")

        header = cart[0].keys()
        rows = [x.values() for x in cart]
        table_main.add_row(tabulate.tabulate(rows, header))
        console.print(table_main)
        try:
            billing_user_input = input(
                "Do you want to continue with the billing ? (y/n)")
            if billing_user_input.lower() == "y":
                # Creating the invoice
                # create a company name and information
                company_name = 'Steff''s Pharmacy.'
                company_address = '007 James Bond St.'
                company_city = 'Melbourne'
                # declare ending message
                message = 'Thanks for shopping with us today!'

                # create a top border
                print('#' * 50)
                # print company information first using format
                table = Table(show_header=False, header_style="bold blue",
                              title="INVOICE", title_justify="center")
                table.add_row('\t\t{}'.format(company_name.title()))
                table.add_row('\t\t{}'.format(company_address.title()))
                table.add_row('\t\t{}'.format(company_city.title()))
                # create a top border
                table.add_row('-' * 50)
                # print out header for section of items
                table.add_row('\tProduct Name\t   Quantity\tPrice')
                # create a print statement for each item
                for i in cart:
                    table.add_row(
                        '\t{}\t-{}-\t{} AUD'.format(i['med_name'], i['med_qty'], i['med_price']*i['med_qty']))
                # print a line between sections
                table.add_row('=' * 50)
                # print out header for section of total
                table.add_row('\t\t\tTotal')
                # calculate total price and print out
                for i in cart:
                    total = total + (float(i['med_price'])*i['med_qty'])
                table.add_row('\t\t\t${}'.format(total))
                # print a line between sections
                table.add_row('=' * 50)
                # output thank you message
                table.add_row('\n\t{}\n'.format(message))
                console.print(table)
                # create a bottom border
                print('-' * 50)
                # Creating an Invoice file in project folder
                now = datetime.now()
                print(f"Invoice Date ={now}\n")
                dt_string = now.strftime("%d%m%Y%H%M%S")
                invoice_number = 'SP'+dt_string
                print(f"Invoice Number ={invoice_number}\n")
                print('#' * 50)
                invoice_file_name = 'invoice_'+invoice_number
                with open(invoice_file_name, 'w') as f:
                    # create a top border
                    f.write('#' * 50)
                    # print company information first using format
                    f.write('\n\t\t{}'.format(company_name.title()))
                    f.write('\n\t\t{}'.format(company_address.title()))
                    f.write('\n\t\t{}'.format(company_city.title()))
                    # create a top border
                    f.write('\n')
                    f.write('-' * 50)
                    # print out header for section of items
                    f.write('\n\tProduct Name\tQuantity\tPrice\n')
                    # create a print statement for each item
                    for i in cart:
                        f.write(
                            '\t{}\t-{}-\t{} AUD'.format(i['med_name'], i['med_qty'], i['med_price']*i['med_qty']))
                        f.write('\n')
                    # print a line between sections
                    f.write('\n')
                    f.write('=' * 50)
                    # print out header for section of total
                    f.write('\n\t\t\tTotal')
                    # calculate total price and print out
                    f.write('\n\t\t\t${}'.format(total))
                    # print a line between sections
                    f.write('\n')
                    f.write('=' * 50)
                    # output thank you message
                    f.write('\n\t{}\n'.format(message))
                    # create a bottom border
                    f.write('\n')
                    f.write('-' * 50)
                    f.write(f"\nInvoice Date ={now}\n")
                    f.write(f"Invoice Number ={invoice_number}\n")
                    f.write('#' * 50)
                    enter_key = input("Press 'Enter' to continue..")
                    return invoice_number
            elif billing_user_input.lower() == "n":
                print("Returning to the Cutomer Order Menu..")
                time.sleep(1)
                return None
            else:
                raise ValueError
        except ValueError:
            print("Invalid Option !")
            time.sleep(1)
