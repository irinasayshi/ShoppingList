import pandas as pd
from itertools import chain

shopping_list = [["qty", "unit", "item"]]
new_item = ""
user_imported = ""
recipes = [ {
    "Banana Oatmeal Pancakes" : {
        "bananas" : {"unit" : "tsp", "qty" : 2},
        "eggs"  : {"unit" : "", "qty" : 3},
        "cinnamon" : {"unit" : "tsp", "qty" : .25},
        "oatmeal" : {"unit" : "cup", "qty" : 1},
        "sugar" : {"unit" : "tsp", "qty" : 1}
        }
    }, {
    "Garden Salad" : {
        "cucumber" : {"unit" : "", "qty" : 1},
        "tomatoes" : {"unit" : "", "qty" : 1},
        "red onion" : {"unit" : "", "qty" : .25},
        "avocado" : {"unit" : "", "qty" : 1},
        "salt" : {"unit" : "", "qty" : 1},
        "garlic" : {"unit" : "", "qty" : 2}
        }
    }, {
    "Watermelon Salad" : {
        "watermelon" : {"unit" : "", "qty" : 1},
        "arugula" : {"unit" : "box", "qty" : 1},
        "goat cheese" : {"unit" : "", "qty" : 1}
        }
    }, {
    "Red Curry Carrot Soup" : {
        "onion" : {"unit" : "", "qty" : 1},
        "coconut milk" : {"unit" : "can", "qty" : 1},
        "garlic" : {"unit" : "", "qty" : 1},
        "vegetable broth" : {"unit" : "box", "qty" : 1},
        "carrots" : {"unit" : "", "qty" : 5},
        "sea salt" : {"unit" : "", "qty" : .75},
        "ginger" : {"unit" : "tsp", "qty" : 2},
        "red curry thai" : {"unit" : "", "qty" : 1},
        "lime" : {"unit" : "", "qty" : 1},
        "corn starch" : {"unit" : "tbsp", "qty" : 1}
        }
    }, {
    "Kale Pesto Risotto" : {
        "walnuts" : {"unit" : "cup", "qty" : .5},
        "olive oil" : {"unit" : "tbsp", "qty" : 4},
        "onion" : {"unit" : "", "qty" : 1},
        "aborino rice" : {"unit" : "cup", "qty" : 1},
        "white wine (dry)" : {"unit" : "cup", "qty" : .5},
        "garlic" : {"unit" : "", "qty" : 1},
        "kale" : {"unit" : "cup", "qty" : 2},
        "butter (unsalted)" : {"unit" : "tbsp", "qty" : 2},
        "salt" : {"unit" : "", "qty" : 1},
        "pepper" : {"unit" : "", "qty" : 1},
        "parmesan cheese" : {"unit" : "cup", "qty" : 2}
        }
    }, {
    "Roasted Buttermilk Chicken" : {
        "chicken" : {"unit" : "lb", "qty" : 2},
        "buttermilk" : {"unit" : "cup", "qty" : 2},
        "salt" : {"unit" : "", "qty" : 1}
        }
    }, {
    "Cauliflower Steaks" : {
        "cauliflower" : {"unit" : "", "qty" : 2},
        "salt" : {"unit" : "", "qty" : 1},
        "parmesan cheese" : {"unit" : "cup", "qty" : 1},
        "lemon" : {"unit" : "", "qty" : 1},
        "olive oil" : {"unit" : "", "qty" : 1}
        }
    }
]

# Print out menu options for the shopping list builder
def show_menu():
    print("\n================================================================================================")
    print("What Would you like to buy? Add items to your shopping list at any time or access any menu items by number:\n")
    print("\t(1) Find from Recipe Book - Enter \"RECIPES\"")
    print("\t(2) Import Shopping List - Enter \"IMPORT\"")
    print("\t(3) Download Shopping List - Enter \"DOWNLOAD\"")
    print("\t(4) Show menu - Enter \"MENU\"")
    print("\t(5) Show shopping list - Enter \"LIST\"")
    print("\t(6) Finish - Enter \"DONE\"")
    print("================================================================================================")
    print("\n")

# Append new items to the shopping list in a nested list format (formatted to easily conver to CSV)
def add_to_list(item, unit="", qty=1):
    new_item = [qty, unit, item]
    shopping_list.append(new_item)

# Display current items in the shopping list in a human readable format (does not dedupe). Code loops through shopping list (skips the first index, because that's the header for the CSV). If length is greater than one (the smallest the length can be is 1 because of the hardcoded header in the list), then print the items in the shopping list.
# item[0] - qty
# item[1] - unit
# item[2] - item
def show_shopping_list():
    if len(shopping_list) > 1:
        for n, item in enumerate(shopping_list[1:]):
            # How to handle the output if there is no unit
            if item[1] == "":
                print("{0} - {1}".format(item[0], item[2]))
            # How to handle the output if there is a unit
            else:
                print("{0} {1} - {2}".format(item[0], item[1], item[2]))
    else:
        print("There's nothing in your shopping list yet.")
    print("\n")

# Write shopping list to a text file. Loop through every item in the shopping list and append each list to a txt file in a human readable format.
def download_list(file_name):
    # Use pandas to easily sum like ingredients + units
    # Pop out the first index to its own var. To be used as the header in the dataframe
    headers = shopping_list.pop(0)
    # Save the shopping list as a dataframe and set the column headers
    df = pd.DataFrame(shopping_list, columns = headers)
    # Convert the qty column to all integers; they can be a mix of strings/ints
    df["qty"] = df["qty"].apply(pd.to_numeric)
    # Group the same ingredient + unit and then aggregate by the qty column.
    sl = pd.DataFrame(df.groupby(["item", "unit"], as_index=False).agg({"qty":"sum"}))
    # Loop through the dataframe and write to txt file.
    with open(file_name, "w") as shopping_list_file:
        # Function iterrows loops through each row of a dataframe.
        for index, row in sl.iterrows():
            # If the unit is not empty, then add a trailing space.
            if len(row["unit"]) != 0:
                row["unit"] = row["unit"] + " "
            # Format the qty row to a string to strip out trailing .0 in floats
            row["qty"] = str(row["qty"])
            row["qty"] = row["qty"].rstrip('0').rstrip('.')
            # Write the contents of the shopping list to a file
            write_to_file = "{1} {2}- {0}".format(row["item"], row["qty"], row["unit"])
            shopping_list_file.write(write_to_file + "\n")
        print("Shopping list", file_name, "has been downloaded.\n")

# Import shopping list from an existing file. Convert a string back to a list of ["qty", "unit", "item"]
def import_list(file_name):
    with open(file_name, "r") as shopping_list_file:
        # For each line in the shopping list file, strip the line from the txt file and save it to a list
        data = [line.strip() for line in shopping_list_file]
        # For each item in the list, split it at the dash and create individual lists. Then split the string in the first index at the space
        for d in data:
            s1 = d.lower()
            s1 = s1.split("-")
            s2 = [s1[0].split(), s1[-1]]
            # Because the second split creates a list inside of a list, chain the inner list to the outer list.
            s3 = list(chain.from_iterable(i if isinstance(i, list) else [i] for i in s2))
            # If the length of s3 is 2, the unit is missing. Insert an empty string at index 1. Strip the leading space in front of index 2.
            if len(s3) == 2:
                s3.insert(1, "")
                s3[2] = s3[2].strip()
                shopping_list.append(s3)
            else:
                s3[2] = s3[2].strip()
                shopping_list.append(s3)
        print("Shopping list", file_name, "has been imported.\n")

# Display the available recipes that user can import into the shopping list.
def show_recipes():
    for i, r in enumerate(recipes):
        i += 1
        for name in r:
            print("(" + str(i) + ")", name.title())

# Match the recipe_choice input to an existing recipe, push ingredient and units
def push_ingredients(pi):
    # Loop through recipes with access to the int and value
    for i, rcp in enumerate(recipes):
        # Set index as i + 1 to later find the correct recipe if user inputed by number
        index = i + 1
        # Loop through each recipe check to see if there is a user input match
        for r in rcp:
            if r == pi or index == pi:
                # When recipe match is found, loop through the recipe and access the ingredients
                print("Ingredients for {0} have been added to the shopping list\n\n".format(r.title()))
                for x in recipes[i]:
                    for ni, ingredients in enumerate(recipes[i][x]):
                        # Loop through ingredients to access the amount and unit. Push to shopping list.
                        unit = recipes[i][x][ingredients]["unit"]
                        qty = recipes[i][x][ingredients]["qty"]
                        add_to_list(ingredients, unit, qty)

# Run function to start shopping list
show_menu()

while True:
    # Ask for user to choose from the menu or add what you are buying
    print("Enter what you are buying or choose item from menu: ")
    new_item = input("- ").lower()

    # Take in user input based on menu options and show appropriate action
    # If user is done, end program
    if new_item == "RECIPES" or new_item == "Recipe" or new_item == "recipe" or new_item == "1":
        print("Select which recipe ingredients to import:")
        # Show list of RECIPES
        show_recipes()
        # Take user input by name (convert to lower to avoid case sensitivity) or number
        recipe_choice = input("- ").title()
        try:
            recipe_choice = int(recipe_choice)
        except ValueError:
            pass
        # Find the matching recipe name from recipe book and push to shopping list
        push_ingredients(recipe_choice)
        # TO DO: ADD A CANCEL OPTION
    elif new_item == "IMPORT" or new_item == "Import" or new_item == "import" or new_item == "2":
            # Give the file name
            print("Name the file (example: shopping_list.txt)")
            file_name = input("- ")
            # Download the list to the computer and end program
            import_list(file_name)
            user_imported = True
    elif new_item == "DOWNLOAD" or new_item == "Download" or new_item == "download" or new_item == "3":
        # Ensure user has at least 1 item to download
        if len(shopping_list) < 2:
            print("Your shopping list is empty, add items to shopping list first.")
        else:
            # Use the same file the user imported
            if user_imported == True:
                download_list(file_name)
                break
            else:
                # Give the file a name
                print("Name the file (example: shopping_list.txt)")
                file_name = input("- ")
                download_list(file_name)
                break
    # Show menu to the user again
    elif new_item == "MENU" or new_item == "Menu" or new_item == "menu" or new_item == "4":
        show_menu()
    # Show what is currently in the shopping list
    elif new_item == "LIST" or new_item == "List" or new_item == "list" or new_item == "5":
        show_shopping_list()
    # Done quits the program, does not save anything
    elif new_item == "DONE" or new_item == "Done" or new_item == "done" or new_item == "6":
        break
    elif len(new_item) == 0:
        print("Add at least one shopping item or choose an option from the menu.")
    else:
        new_qty = input("How Much? ")
        new_unit = input("Unit? ")

        add_to_list(new_item, new_unit, new_qty)
