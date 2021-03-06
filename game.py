import rooms
import player

# Create an instance of the room class that the player is in
current_room = rooms.room5()
#instance of the player
user = player.Player()
#used to start the game
choice = ""
#used to track all the rooms the player has solved


def victory():
    print("I hope playing this game has provided you with a sense of pride and accomplishment")
    print("Bye bye world")
    quit()

#Movement functions
def move(direction):
    global current_room
    global user
    """
    The function move works by taking a user input in,
    checking if the input value is valid area to move to,
    then updates the player co ordinates to represent the movement.
    The function then calls update_room to update the current_room instance
    """
    try:
        if direction == "c":
            return "placeholder text"
        elif direction in current_room.directions:
            if direction == "north" or direction == "n":
                user.y += 1
            elif direction == "south" or direction == "s":
                user.y -= 1
            elif direction == "east" or direction == "e":
                user.x += 1
            elif direction == "west" or direction == "w":
                user.x += -1
        # This else is in case the user puts in a value that isn't possible to be moved to
            update_room()
        else:
            print("You cannot move there!\n")
            direction_input  = str(input("Please enter a direction to move from this list:" + str(current_room.directions)))
            usage = direction_input[0]
            move(usage)
    except ValueError:
            print("That value isn't recognised!\n")


def update_room():
    global current_room
    global user
    """
    The update_room function is called after the player has moved in the move function
    update_room goes through all possible 9 co ordinate locations to check if the co ords are the same as the player position
    if room co ords and player co ords are the same, the current_room variable instance is updated to reflect the new room the player is in
    """
    if user.x == 1:
        if user.y == 1:
            current_room = rooms.room7()
        elif user.y == 2:
            current_room=rooms.room4()
        elif user.y==3:
            current_room=rooms.room1()

    elif user.x == 2:
        if user.y == 1:
            current_room=rooms.room8()
        if user.y==2:
            current_room=rooms.room5()
        if user.y==3:
            current_room=rooms.room2()

    elif user.x == 3:
        if user.y == 1:
            current_room = rooms.room9()
        elif user.y == 2:
            current_room = rooms.room6()
        elif user.y == 3:
            current_room = rooms.room3()

    room_inventory()
    print("You have moved to room " + str(current_room.room_name) + "\n")


#Puzzle related functions
def total_solved():
    global current_room
    global user
    """
    This function works by looking at the solved_dict list to see if all the values are "y"
    if this is true it means that all the rooms have been solved
    as such it adds the key item to the user inventory
    it returns true or false to determine if the key item can be used or not
    """
    #https://stackoverflow.com/questions/35253971/how-to-check-if-all-values-of-a-dictionary-are-0-in-python
    solved = all(value == "y" for value in user.solved_dict.values())
    if solved == True:
        print("You solved all the puzzles and are rewarded with a key!")
        user.inventory.append("key")
        return True
    else:
        return False


def solved(user_solution, room_solution):
    global current_room
    global user
    """
    This function takes in the user solution, and the solution that is intended
    it then sees if the intended solution is in the user soloution(to allow for some variation in solution such as a splinter v splinter)
    it then updates the solved_dict value to say the room has been solved
    then it checks if every room has been solved
    """
    if room_solution in user_solution:
        print("You have solved room " + str(current_room.room_name))
        user.solved_dict.pop(str(current_room.room_name), None)
        user.solved_dict[str(current_room.room_name)] = "y"
    elif user_solution == "c":
        return None
    else:
        print("That is not the correct answer sorry!")
        use_item("keyboard")

    total_solved()

def puzzle():
    global current_room
    global user
    """
    This function prints out the puzzle in the current room
    """
    print(current_room.room_puzzle())

#inventory related functions
def use_item(input_item):
    global current_room
    global user
    """
    This function works by taking in input_item and comparing it against if statements
    """
    if input_item == "c":
        return None
    elif input_item == "keyboard":
        user_answer = input(current_room.room_puzzle())
        solved(user_answer, current_room.solution)
    elif input_item in user.inventory:
        if input_item == "map":
            print(user.map())
        elif input_item == "notebook":
            print(user.notebook())
        elif input_item == "key" and current_room.room_name == 6 and "barrel" not in current_room.inventory:
            victory()
        elif input_item == "barrel":
            print("A rather useless barrel")
    else:
        print("That item has no use in this room.")
        item_input = str(input("Please enter an item to use:")).lower()
        input_item = item_input.split(" ")
        use_item(input_item[0])



def room_inventory():
    global current_room
    global user
    """
    This function updates the current_room inventory by opening the inventory file
    it then looks at the specific line for the current room
    and updates the current room inventory variable to the line in the file
    """
    #This function means that the room inventory
    with open('inventory.txt', 'r') as file:
        data = file.readlines()

    current_room.inventory = data[current_room.room_name-1]
    file.close()


def pickup_item(input_item):
    if input_item == None:
        return None
    global current_room
    global user
    """
    Pickup item works by looking at a file with all the items in each room
    It then finds out which line is the room the player is currently in
    When the user picks up the item it then rewrites the line to remove the picked up item
    and writes the line back to the file
    """
    line_value = current_room.room_name

    with open('inventory.txt', 'r') as file:
        data = file.readlines()

    current_inventory = str(data[line_value-1])

    if input_item in current_inventory:
        new_inventory = current_inventory.replace(input_item, "")
        data[line_value-1] = new_inventory
        user.inventory.append(input_item)

        with open('inventory.txt', 'w') as file:
            file.writelines(data)

        file.close()
        room_inventory()

    elif input_item == "c":
        return None
    else:
        print("That item isn't in this room sorry!")
        item = input("Please input an item to pick up: ")
        pickup_item(item)


def drop_item(input_item):
    if input_item == None:
        return None
    global current_room
    global user
    """
    drop_item works by seeing if the item is in the player inventory
    If that is true, then it reads a file with all items in rooms
    it then adds the dropped item to the line that represents the current room
    and removes the item from the user inventory
    """
    line_value = current_room.room_name-1

    if input_item in user.inventory:

        with open('inventory.txt', 'r') as file:
            inventory = file.readlines()

        current_inventory = str(inventory[line_value])
        new_inventory = input_item + ", " + current_inventory
        inventory[line_value] = new_inventory
        user.inventory.remove(input_item)

        with open('inventory.txt', 'w') as file:
            file.writelines(inventory)

        file.close()
        room_inventory()

    elif input_item == "c":
        return None
    else:
        print("You do not have that item to drop!")
        item = input("Please input an item to drop: ")
        drop_item(item)

#
def inventory(input):
    if input == None:
        return None
    global current_room
    global user
    """
    This function prints out the player inventory
    """
    if input == "player" or input == "user":
        print(user.inventory)
    elif input == "room":
        with open('inventory.txt', 'r') as file:
            inventory = file.readlines()
            current_inventory = inventory[(current_room.room_name)-1]
            print(current_inventory)
        file.close()
    elif input == "c":
        return None
    else:
        new_input = input("That isn't a recognised command, please input either room or user:")
        inventory(new_input)


def look(item):
    global current_room
    if item == "map":
        print("A map that shows your current location")
    elif item == "notebook":
        print("A notebook with a few pages.\nOn the first page is written: Your task is to go to all rooms and solve all the riddles.\nOnce You have done this you will be given a key and will have to find the keyhole.\nUse this notebook to keep track of the rooms you have solved")
    elif item == "room":
        print(current_room.look)
    elif item == "c":
        return None
    else:
        new_item = input("That isn't a recognised item, please input a recognised item:")
        look(new_item)



def direct():
    global current_room
    global user
    print("List of available exits from this room:")
    print(", ".join(current_room.directions))


def help():
    global current_room
    global user
    """Help function that prints out all available commands"""
    file = open("help.txt", "r")
    print(file.read())
    file.close()



# First open the file to clear all the text in the file
open('inventory.txt', 'w').close()
# Then write all the items in each room to the file line by line
with open('inventory.txt', 'w') as file:
    file.write("\n")
    file.write("\n")
    file.write("\n")
    file.write("\n")
    file.write("map, notebook\n")
    file.write("barrel\n")
    file.write("\n")
    file.write("\n")
    file.write("\n")

#Update the room inventory as soon as the game starts
room_inventory()

#acts as the start of the game
print(current_room.look)

while choice != "q":
    """
    This while loop is the game running
    It takes a user input in to then work out what the corresponding function is to execute the task the user input
    """
    try:
        choice = str(input("Please input what action you would like to do:")).lower()
        choice = choice.split(" ")
        command = choice[0]
        # This try except exists to prevent IndexError incase choice.split does not have 2 values
        try:
            usage = choice[1]
            if usage == "placeholder":
                print("nice try")
                command = "help"
        except IndexError:
            usage = None

        if command == "move" or command == "m":
            move(usage)
        elif command == "inv" or command == "i" or command == "inventory":
            inventory(usage)
        elif command == "puzzle":
            puzzle()
        elif command == "drop" or command == "d":
            drop_item(usage)
        elif command == "pickup" or command == "p" or command == "pickup item":
            pickup_item(usage)
        elif command == "use" or command == "u":
            use_item(usage)
        elif command == "--help":
            help()
        elif command == "look":
            look(usage)
        elif command == "directions":
            direct()
        elif command == "q":
            print("Bye Bye World")
            choice = "q"
        else:
            print("That isn't a valid command, enter --help to see available commands\n")
    except ValueError:
        print("That isn't a valid command, enter --help to see available commands\n")
