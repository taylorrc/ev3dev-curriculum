"""
The Final Project for CSSE120
This is the pc code to run on my laptop
Author: Ryan Taylor
"""

import tkinter
from tkinter import ttk

import mqtt_remote_method_calls as com

import time


class MyDelegateOnThePc(object):
    """ Helper class that will receive MQTT messages from the EV3. """

    def __init__(self, label_to_display_messages_in):
        self.display_label = label_to_display_messages_in

    def package_found(self):
        print("Package Found in Warehouse")


def main():
    """
    A majority of the main() function determines how the GUI should look, including adding images and defining buttons
    to call functions on the ev3.

    :return: None
    """
    root = tkinter.Tk()
    root.title("Amazon.com")

    main_frame = ttk.Frame(root, padding=20, relief='raised')
    main_frame.grid()

    left_side_item = ttk.Label(main_frame, text="Amazon Echo")
    left_side_item.grid(row=0, column=0)

    photo1 = tkinter.PhotoImage(file='Echo.gif')
    button1 = ttk.Button(main_frame, image=photo1)
    button1.image = photo1
    button1.grid(row=2, column=0)
    # Change this lambda statement
    button1['command'] = lambda: print("Amazon's Echo: The worlds newest voice assistant")

    left_order_button = ttk.Button(main_frame, text="Order Now")
    left_order_button.grid(row=3, column=0)
    left_order_button['command'] = lambda: address(mqtt_client, address_entry, 'item1')

    main_label = ttk.Label(main_frame, text="  Welcome to Amazon  ")
    main_label.grid(row=1, column=1)

    main_space = ttk.Label(main_frame, text="--")
    main_space.grid(row=2, column=1)

    right_side_product = ttk.Label(main_frame, text="Fire TV")
    right_side_product.grid(row=0, column=2)

    photo2 = tkinter.PhotoImage(file='Fire-TV.gif')
    button2 = ttk.Button(main_frame, image=photo2)
    button2.image = photo2
    button2.grid(row=2, column=2)
    # Change this lambda statement
    button2['command'] = lambda: print("Amazon's Fire TV: The newest in streaming")

    right_order_button = ttk.Button(main_frame, text="Order Now")
    right_order_button.grid(row=3, column=2)
    right_order_button['command'] = lambda: address(mqtt_client, address_entry, 'item2')

    spacer = ttk.Label(main_frame, text="")
    spacer.grid(row=4, column=2)

    address_entry = ttk.Entry(main_frame, width=20)
    address_entry.grid(row=4, column=1)

    address_button = ttk.Button(main_frame, text="Shipping Address:")
    address_button.grid(row=3, column=1)
    address_button['command'] = lambda: print("Address Found")

    # Button for leaving the GUI
    q_button = ttk.Button(main_frame, text="Leave Amazon")
    q_button.grid(row=5, column=2)
    q_button['command'] = (lambda: quit_program(mqtt_client))

    pc_delegate = MyDelegateOnThePc(spacer)
    mqtt_client = com.MqttClient(pc_delegate)
    mqtt_client.connect_to_ev3()
    # mqtt_client.connect_to_ev3("35.194.247.175")  # Off campus IP address of a GCP broker

    root.mainloop()


def address(mqtt_client, address_entry, item_number):
    """
    This is the main method to ship packages to the different houses.
    Sends messages to the ev3 delegate to grab the package and send it to the house

    :param mqtt_client: Connects to the ev3
    :param address_entry: Allows the ev3 to know which house to deliver to
    :param item_number: Allows the ev3 to determine which package was ordered
    :return: None
    """

    ship_to = address_entry.get()

    if ship_to == "White":
        if item_number == 'item1':
            mqtt_client.send_message("grab_package", ['item1'])
            print("Amazon Echo Ordered")
        if item_number == 'item2':
            mqtt_client.send_message("grab_package", ['item2'])
            print("Fire TV Ordered")

        # mqtt_client.send_message("ship_to", [ship_to])
        print("Shipping to White House")

    elif ship_to == "Blue":
        if item_number == 'item1':
            mqtt_client.send_message("grab_package", ['item1'])
            print("Amazon Echo Ordered")
        if item_number == 'item2':
            mqtt_client.send_message("grab_package", ['item2'])
            print("Fire TV Ordered")

        time.sleep(20)
        mqtt_client.send_message("ship_to", [ship_to])
        print("Shipping to Blue House")

    elif ship_to == "":
        print("Please enter the shipping address")

    else:
        print("Too far from carrier facility. Ship to another address")


def quit_program(mqtt_client):
    """Allows the user to close down the GUI on the computer. Will also close the MQTT connection."""
    print("Have a nice day!")
    mqtt_client.send_message("shutdown")
    mqtt_client.close()
    exit()


main()
