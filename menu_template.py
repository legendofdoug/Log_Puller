import getpass

def project_selection():
    options = {
        1: "project 1",
        2: "project 2",

    }
    print("______________________________________________\n"
          "What project is this for?\n"
          "______________________________________________\n"
          "1. Project 1\n"
          "2. Project 2\n"
     
          "Or just enter the project's name."
          )
    project = input("Enter a number or the project name: ")
    try:
        project = options[int(project)]
    except:
        print ("You didn't enter in a number from the list, so I'm going to assume you manually entered the project name")
    finally:
        print (project)
    return project

def menu_selection():

    menu = input("______________________________________________\n"
          "What do you want to do?  \n"
          "______________________________________________\n"
          "1. Collect Logs for FAI\n"
          "2. Collect All Logs for a QPN\n"
          "3. Collect All Logs for a RACKID\n"
          "4. Collect All Logs for a MBSN\n"
          "5. Collect All Logs with a specific issue.\n"
          "Type quit, or exit to stop.  "
          )
    return menu

def pxe_selection():
    menu = input("______________________________________________\n"
                "Pick a PXE: \n"
                 "______________________________________________\n"
                 "pxe ip 1 \n"
                 "pxe ip 2\n"
    options = {"1": "PXE IP 1",
               "2": "PXE IP 2",

               }

    try:
        return options[menu]
    except:
        print(f"Using full IP: {menu}")
        return menu

def pxe_password_selection(pxe):
    options = {
        "pxe ip 1": "pxe pw 1",

    }
    try:
        return options[pxe]
        return options[pxe]
    except:
        pxe_password = getpass.getpass(f"IP: {pxe} was not found. Please enter it here: ")
        return pxe_password

def pxe_user_selection():
    answer = str.lower(input("Is pxe username root?"))
    if answer == "yes" or answer == "y" or answer == "true":
        pxe_user = "root"
    else:
        pxe_user = getpass.getuser("What is the username you want to use? ")
    return pxe_user