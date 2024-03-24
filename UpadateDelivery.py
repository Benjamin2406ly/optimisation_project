import Delivery
import InitWindow
import random

# while i < len(delivery_array):
def update_delivery(i, delivery_array, initwindows):
    for initwindow in initwindows: 
        if initwindow.delivery is None:
            initwindow.delivery = delivery_array[i]