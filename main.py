from src.catalog import insert_yarn, update_yarn, delete_yarn, select_yarn
from src.stock import insert_yarn_stock, update_yarn_stock, delete_yarn_stock, select_yarn_stock

while True:
    print("1. Catalog \n"
          "2. Stock \n"
          "3. Quit")
    choice = input("Choice : ")
    match choice:
        case "1":  # Catalog
            print("==== Catalog ====\n"
                  "1. Add new yarn reference \n"
                  "2. Modify yarn reference \n"
                  "3. Consult yarn reference \n"
                  "4. Delete yarn reference \n"
                  "5. Quit")
            choice = input("Choice : ")
            match choice:
                case "1":  # Add yarn reference
                    print("Enter yarn characteristics")
                    product = input("Product : ")
                    brand = input("Brand : ")
                    dye = input("Dye : ") or None
                    weight = float(input("Weight : "))
                    length = float(input("Length : "))
                    colour = input("Colour : ")
                    material = input("Material : ")
                    misc = input("Misc : ") or None
                    insert_yarn(product, brand, colour, material, weight, length, dye, misc)
                    continue

                case "2":  # Modify yarn reference
                    print("Enter yarn id to modify")
                    catalog_id = input("Product ID : ")
                    availability = input("Availability : ") or None
                    misc = input("Misc : ") or None
                    update_yarn(catalog_id, availability, misc)
                    continue

                case "3":  # Consult yarn reference
                    results = select_yarn()
                    for row in results:
                        print(row)
                    continue

                case "4":  # Delete yarn reference
                    print("Enter yarn id to delete")
                    catalog_id = input("Product ID : ")
                    delete_yarn(catalog_id)
                    continue

                case "5":  # Return
                    continue

        case "2":  # Stock
            print("==== Stock ====\n"
                  "1. Add new yarn to shelf \n"
                  "2. Modify yarn \n"
                  "3. Consult shelf \n"
                  "4. Delete yarn from shelf \n"
                  "5. Quit")
            choice = input("Choice : ")
            match choice:
                case "1":  # Add to stock
                    print("Enter yarn characteristics")
                    catalog_id = input("Catalog ID : ")
                    initial_weight = float(input("Initial Weight : "))
                    dye_lot = input("Dye Lot : ") or None
                    misc = input("Misc : ") or None
                    insert_yarn_stock(catalog_id, initial_weight, dye_lot, misc)
                    continue

                case "2":  # Modify yarn from stock
                    print("Enter yarn id to modify")
                    stock_id = input("Stock ID : ")
                    current_weight = float(input("Current Weight : "))
                    misc = input("Misc : ") or None
                    update_yarn_stock(stock_id, current_weight, misc)
                    continue

                case "3":  # Consult yarn in shelf
                    results = select_yarn_stock()
                    for row in results:
                        print(row)
                    continue

                case "4":  # Delete yarn from shelf
                    print("Enter yarn id to delete")
                    stock_id = input("Stock ID : ")
                    delete_yarn_stock(stock_id)
                    continue

                case "5":
                    continue

        case "3":  # Quitter
            print("Thank you and see you soon!")
            break
