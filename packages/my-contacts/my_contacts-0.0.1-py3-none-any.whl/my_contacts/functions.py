import os
from rich.prompt import Prompt
from rich.prompt import Confirm
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich import print

def menu_prompt():
    """_summary_
        Menu_prompt function clears the screen each time and displays a table with Home Menu options and keyboard keys to access menu
    """   
    #clear screen and create and instance of Console from Rich module
    os.system('cls||clear')
    console = Console()

    print()
    console.print(
        Panel.fit("[magenta]\nPlease make a selection   \nfrom the menu below\n",
        title="[cyan]Home")
    )
    
    #create a table
    table = Table()
 
    #add columns and headings
    table.add_column('Home | Operation', style='cyan', justify='left', no_wrap=True)
    table.add_column('Key', justify='left', style='magenta')

    #add rows with menu options
    table.add_row('Add Contact', 'A')
    table.add_row('Edit Contact', 'E')
    table.add_row('Delete Contact', 'D')
    table.add_row('Display Contact', 'DC')
    table.add_row('Display all Contacts', 'DA')
    table.add_row('Quit Application', 'Q')

    #display table
    console.print(table)

def add_contact_prompt():
    """_summary_
        add_contact_prompt function clears the screen each time and displays a table with Add Contact Menu options and keyboard keys to access menu
    """  
    #clear screen and create and instance of Console from Rich module  
    os.system('cls||clear')
    console = Console()

    print()
    console.print(
        Panel.fit("[magenta]\nPlease make a selection from the\nmenu below\n",
        title="[cyan]Add Contact")
    )
    #create a table
    table = Table()
    
    #add columns and headings
    table.add_column('Add | Operation', style='cyan', justify='left', no_wrap=True)
    table.add_column('Key', justify='left', style='magenta')

    #add rows with menu options
    table.add_row('Add a Contact', 'C')
    table.add_row('Add a Close Contact', 'CC')
    table.add_row('Add a Family Contact Contact', 'FC')
    table.add_row('Add a Work Contact', 'WC')
    table.add_row('Home', 'H')
    table.add_row('Quit Application', 'Q')

    #display table
    console.print(table)


def display_table(list):
    """_summary_
        display_table function recives a list of search results and dsiplays them in a table
    Args:
        list (list): a list of results matching user's search input
    """

    #clear screen and create and instance of Console from Rich module 
    os.system('cls||clear')
    console = Console()

    #create a table
    table = Table(title="Your Contacts")

    #add columns and headings
    table.add_column("Id", style="cyan", no_wrap=True)
    table.add_column("First name", style="magenta")
    table.add_column("Last name", style="magenta")
    table.add_column("Phone", style="green")
    table.add_column("Address", style="green")
    table.add_column("Pet", style="green")
    table.add_column("Favourite Drink", style="green")
    table.add_column("Work Address", style="green")
    table.add_column("Work Phone", style="green")
    table.add_column("Skills", style="green")

    #iterate through list of results to add each row to the table.
    #if / elif used to print each type of contact - Contact, Close Contact, Family Contact, Work Contact
    for idx, val in enumerate(list):
        if len(val) == 5:
            table.add_row(list[idx]['id'], list[idx]['first_name'], list[idx]['last_name'], list[idx]['phone'])
        elif len(val) == 6:
            table.add_row(list[idx]['id'], list[idx]['first_name'], list[idx]['last_name'], list[idx]['phone'],  list[idx]['address'])
        elif len(val) == 8:
            table.add_row(list[idx]['id'], list[idx]['first_name'], list[idx]['last_name'], list[idx]['phone'],  list[idx]['address'], list[idx]['pet'], list[idx]['fav_drink'])
        elif len(val) == 9:
            table.add_row(list[idx]['id'], list[idx]['first_name'], list[idx]['last_name'], list[idx]['phone'],  list[idx]['address'], '', '', list[idx]['work_address'], list[idx]['work_phone'], list[idx]['skills'])

    #display table
    console.print(table)


def continue_prompt():
    """_summary_
        Prompts user to press Enter to continue. Execution is frozen untill keypress
    Returns:
        string: returns user input. Used for ID selection for multipe search results. No need for error
        correction here as its done in the while look with a generator expression
    """  
    
    prompt = Prompt.ask("Press Enter to continue...", default="")

    return prompt

def add_contact(id, contact_type, first_name, last_name, phone, address, pet_name, fav_drink, work_address, work_phone, skills):
    """_summary_
    add_contact will receive as arguments all the available variables for all the four types of contacts.
    When the function is called, arguments that arent needed are set to None.
    If statments and booleans based on conrtact type are used to reduce repeition of variables that are used by all the contact
    types - first_name, last_name, phone etc.
    Args:
        id (_type_): string
        contact_type (_type_): string
        first_name (_type_): string
        last_name (_type_): string
        phone (_type_): string or None
        address (_type_): string or None
        pet_name (_type_): string or None
        fav_drink (_type_): string or None
        work_address (_type_): string or None
        work_phone (_type_): string or None
        skills (_type_): string or None

    Returns:
        _type_: dictionary
    """    
    if contact_type == 'Contact' or contact_type == 'Close Contact' or contact_type == 'Family Contact' or contact_type == 'Work Contact':
        contact = {'id': str(id), 'type': contact_type, 'first_name': first_name, 'last_name': last_name, 'phone': phone}

        if contact_type == 'Contact':
            return contact

    if contact_type == 'Close Contact' or contact_type == 'Family Contact' or contact_type == 'Work Contact':
        contact['address'] = address

        if contact_type == 'Close Contact':
            return contact
    
    if contact_type == 'Family Contact':
        contact['pet'] = pet_name
        contact['fav_drink'] = fav_drink

        return contact
    
    if contact_type == 'Work Contact':
        contact['work_address'] = work_address
        contact['work_phone'] = work_phone
        contact['skills'] = skills

        return contact

def empty_database_alert(database, action, title_action):
    """
    Function will give uesr an error when attempting to Edit, Delete, Display or Display all contacts when database is empty.

    Args:
        database (list): Contacts database
        action (string): the action being ettempted - edit delete, display.
        title_action (string): action verb for panel title

    Returns:
        boolean: return search again boolean for outer while loop
    """    
    console = Console()
    if not database:
        os.system('cls||clear')
        search_again = False
        console.print(Panel.fit(f'[magenta]\nYou cannot {action} any contacts.\nYour Contacts Book is empty.\n', title_align='left', title=f'[cyan]{title_action} a Contact'))
        continue_prompt()
        return search_again

    search_again = True
    return True

def validate_name(string):
    """
    Function receives a string to guide user to what input they are entering.
    If string is all white space, will prompt user to enter valid name.
    Returns the string stripped of leading and trailing whitespace.
    Args:
        string (string): Name to prompt user on what data they are inputing

    Returns:
        string: sting with no leading or trailing spaces
    """  

    user_input = input(f'Enter {string} Name >> ')

    while len(user_input) < 1 or user_input.isspace():

        print(f'You need to enter a {string} Name for your Contact!\n')
        user_input = input(f'Enter {string} Name >> ')

    return user_input.strip()
       
def validate_phone():
    """
    User input is stripped of leading and trailing white space.
    user input is copied in a temp variable. then all spaces are removed from string.
    isdigit is used to test whether onl numbers have been entered.
    Once string is just numbers, assign phone temp to phone - phone is a copy of phone temp but
    with the original whitespace inbetween numbers.
    Returns:
        string: returns a string that is numeric only and no leading or trailing whitespace.
        White space is allowed inbetween numbers.
    """    
    phone = input('Enter Phone Number >> ').strip()
    while True:
        phone_temp = phone
        phone_test = phone_temp.replace(' ','')

        if not phone_test.isdigit():
            print('Phone number can only contain numbers!\n')
            phone = input('Enter Phone Number >> ').strip()
        else:
            phone = phone_temp
            break

    return phone


def confirm_edit_delete(action, search_result_from_search, search_result_from_get=None):
    console = Console()
    display_table(search_result_from_search)
    print()
    if len(search_result_from_search) > 1:
        console.print(Panel.fit(f'\nContact Selected - [cyan]{search_result_from_get["id"]}[/cyan]: [magenta]{search_result_from_get["first_name"]} {search_result_from_get["last_name"]}\n',
            title_align='left', title='[cyan]Contact Found!', subtitle_align='left', subtitle=f'[cyan]Confirm {action}?'))
        print()
        confirm = Confirm.ask(f'Are you sure you want to {action} [cyan]{search_result_from_get["id"]}[/cyan]: [magenta]{search_result_from_get["first_name"]} {search_result_from_get["last_name"]}[/magenta] ?')

        return confirm
    else:
        console.print(Panel.fit(f'\nContact Selected - [cyan]{search_result_from_search[0]["id"]}[/cyan]: [magenta]{search_result_from_search[0]["first_name"]} {search_result_from_search[0]["last_name"]}\n', 
            title_align='left', title='[cyan]Contact Found!', subtitle_align='left', subtitle='[cyan]Confirm edit?'))
        print()
        confirm = Confirm.ask(f'Are you sure you want to {action} [cyan]{search_result_from_search[0]["id"]}[/cyan]: [magenta]{search_result_from_search[0]["first_name"]} {search_result_from_search[0]["last_name"]}[/magenta] ?')

        return confirm


