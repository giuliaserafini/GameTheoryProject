from enum import IntEnum
from random import randint

class DeviceType(IntEnum):
    """
    This enumerator describes the device's type.\n
    Only two types are modeled: type A and type B.
    """
    TYPE_A = 1
    TYPE_B = 2

class Gateway(object):
    """
    This class describes an IOT gateway, with its bandwidth, shared among all the devices, and the reachability radius.
    """
    COUNTER = 0 # Autoincrement ID.

    def __init__(self, bandwidth, radius=25):
        """
        Initialize a device given a bandwidth [Mbps] and an optional radius [m].\n
        If the radius is omitted, it is assumed to be equal to 25 m.
        """
        if bandwidth is None or bandwidth <= 0: # The bandwidth must be an integer greater than zero.
            raise ValueError("Bandwidth must be greater than zero.")
        
        if radius is None or radius <= 0: # The radius must be an integer greater than zero. 
            raise ValueError("Radius must be greater than zero.")
        
        Gateway.COUNTER += 1 # Increment the ID.

        # Assign the parameters or initialize to default values.
        self.__ID = Gateway.COUNTER
        self.__bandwidth = bandwidth
        self.__radius = radius
        self.__devices = []

    def connect_device(self, device):
        """
        Connect a device to the gateway, if not already connected.
        """
        if device is None or not isinstance(device, Device): # The device's class must be Device and it has to be not null.
            raise ValueError("The device must be not null.")
        if device not in self.__devices: # The device must not be already connected to the device.
            self.__devices.append(device) # Insert the device.
    
    def disconnect_device(self, device):
        """
        Disconnect a device from the gateway, if it was connected.
        """
        if device is None or not isinstance(device, Device): # The device's class must be Device and it has to be not null.
            raise ValueError("The device must be not null.")
        if device in self.__devices:# The device must be already connected to the device.
            self.__devices.remove(device) # Delete the device.
    
    def get_device_count(self, type):
        """
        Return the number of devices connected to the gateway of the speciefied type.
        """
        # Return the number of devices that their type is equal to the given one.
        return len([device for device in self.__devices if device.type == type])

    def __eq__(self, other):
        # Compare the identifier of two instances.
        return other.ID == self.ID if isinstance(other, Gateway) else False
    
    def __hash__(self):
        # Compute the hash using the ID, bandwidth and radius.
        return hash((self.__ID, self.__bandwidth, self.__radius))
    
    def __repr__(self):
        # The string is 'Gateway15' for a gateway, having 15 as ID.
        return "Gateway" + str(self.__ID)
    
    def __str__(self):
        return self.__repr__()
    
    def __contains__(self, item):
        # Check if a device is connected to the gateway.
        return item in self.__devices
    
    ID = property(lambda self: self.__ID)
    bandwidth = property(lambda self: self.__bandwidth)
    devices_count = property(lambda self: len(self.__devices))
    radius = property(lambda self: self.__radius)

class Displacement(object):
    """
    This class represents a displacement of a device or gateway in a two-dimensional space.\n
    This object is immutable.
    """
    def __init__(self, x, y, element):
        """
        Initialize the object given a position (x, y) and and element.
        """
        # Set the given parameters.
        self.__x = x
        self.__y = y
        self.__element = element
    
    def __eq__(self, other):
        # Compare two instances according the position and the element.
        return  other.x == self.x and \
                other.y == self.y and \
                other.element == self.element if isinstance(other, Displacement) \
                else False
    
    x = property(lambda self: self.__x)
    y = property(lambda self: self.__y)
    element = property(lambda self: self.__element)

class Space(object):
    """
    This class models a two-dimensional space where is possible to place devices and gateways.
    """
    def __init__(self, rows, columns):
        """
        Initialize the object given the dimensions: rows and columns.
        Both dimensions must be integers, grater than zero.
        """
        if rows is None or rows <= 0: # The rows must an integer greater than zero.
            raise ValueError("Rows must be greater than zero.")
        if columns is None or columns <= 0: # The columns must an integer greater than zero.
            raise ValueError("Columns must be greater than zero.")

        # Assign the parameters and the default values.
        self.__rows = rows
        self.__columns = columns
        self.__positions = []
    
    def add_element(self, element, x=None, y=None):
        """
        Add an element to the space.\n
        If the position (x, y) is omitted, a random one is generated.\n
        If the element is already placed an exception will be raised.\n
        If the position (x, y) is provided, it must be within the boundaries.\n
        Each device is placed in a position, such that it can connect to at least one gateway.
        """
        # If the space already contains a position with that element, raise an exception.
        if len([displacement for displacement in self.__positions if displacement.element == element]) > 0:
            raise RuntimeError("The element is already placed.")
        # If the position provided is out of boundaries, raise an exception.
        if (x is not None and (x < 0 or x >= self.__columns)) or (y is not None and (y < 0 or y >= self.__rows)):
            raise IndexError("The position (x, y) must be within the boundaries.")
        if x is not None and y is not None:
            # Create a new displacement.
            new_displacement = Displacement(x, y, element)
            # If the position is already taken, raise an exception.
            if len([displacement for displacement in self.__positions if displacement.x == x and displacement.y == y]) > 0:
                raise ValueError("The position ({},{}) is already taken.".format(x, y))
            self.__positions.append(new_displacement) # If all of the previous constrains hold, place the element.
            if isinstance(element, Device): # If the element is a device, than it should be near at least one gateway.
                near_gateways = self.get_near_gateways(element) # Find the nearest gateways of a device.
                if len(near_gateways) == 0: # If it's isolated, remove the displacement inserted before and raise an exception.
                    self.__positions.remove(new_displacement)
                    raise ValueError("The device is not able to connect to any gateway.")
                else:
                    # If there is at least one near gateway, select one from the neighbors and setup the connection.
                    random_gateway_index = randint(0, len(near_gateways) - 1)
                    near_gateways[random_gateway_index].connect_device(element)
            return (x, y) # Return the position of the element.
        else:
            added = False # The element is not initially added.
            # Initialize the position.
            x = 0
            y = 0
            while not added: # While the position was not suitable for the element:
                # Generate a random position.
                x = randint(0, self.__columns - 1)
                y = randint(0, self.__rows - 1)
                try:
                    # Try to add the element.
                    (x, y) = self.add_element(element, x=x, y=y)
                    added = True # Everything gone fine, can exit.
                except ValueError as error: # If the exception was a value error than we have to retry, until we find a valid position.
                    continue
            return (x, y) # Return the position.

    def get_near_gateways(self, element):
        if element is None or len([displacement for displacement in self.__positions if displacement.element == element]) == 0:
            raise ValueError("The element is not present or it's null.")
        gateway_displacements = [displacement for displacement in self.__positions if isinstance(displacement.element, Gateway)]
        element_displacement = [displacement for displacement in self.__positions if displacement.element == element][0]
        near_gateways = []
        for gateway_displacement in gateway_displacements:
            if  (gateway_displacement.x - element_displacement.x) ** 2 + \
                (gateway_displacement.y - element_displacement.y) ** 2 <= gateway_displacement.element.radius ** 2:
                near_gateways.append(gateway_displacement.element)
        return near_gateways


class Device(object):
    COUNTER_A = 0
    COUNTER_B = 0

    def __init__(self, type):
        if type is None or not isinstance(type, DeviceType):
            raise TypeError("The device type must be not null.")

        if type == DeviceType.TYPE_A:
            Device.COUNTER_A += 1
            self.__ID = Device.COUNTER_A
        elif type == DeviceType.TYPE_B:
            Device.COUNTER_B += 1
            self.__ID = Device.COUNTER_B
        else:
            raise ValueError("Unsupported device type.")

        self.__type = type
        self.__gateway_callback = None
    
    def __eq__(self, other):
        return other.ID == self.ID and other.type == self.type if isinstance(other, Device) else False
    
    def __hash__(self):
        return hash((self.__ID, self.__type))

    def __repr__(self):
        return "Device {} Type {}".format(self.__ID, self.__type)
    
    def __str__(self):
        return self.__repr__

    def __bandwidth_variation(self, starting_gateway, destination_gateway):
        n1 = starting_gateway.get_device_count(self.type)
        n2 = destination_gateway.get_device_count(self.type)
        m1 = starting_gateway.devices_count - n1
        m2 = destination_gateway.devices_count - n2
        w1 = starting_gateway.bandwidth
        w2 = destination_gateway.bandwidth
        if n1 + m1 == 1 and n2 + m2 == 0:
            return 0
        elif n1 + m1 == 1 and n2 + m2 > 0:
            return (n2 + 1) * w2 / (n2 + m2 + 1) - (n1 * w1 / (n1 + m1) + n2 * w2 / (n2 + m2))
        elif n1 + m1 > 1 and n2 + m2 == 0:
            return (n1 - 1) * w1 / (n1 + m1 - 1) + (n2 + 1) * w2 / (m2 + n2 + 1) - n1 * w1 / (n1 + m1)
        else:
            return  (n1 - 1) * w1 / (n1 + m1 - 1) + (n2 + 1) * w2 / (n2 + m2 + 1) - n1 * w1 / (n1 + m1) - n2 * w2 / (n2 + m2)

    def gateway_selection(self, space):
        near_gateways = space.get_near_gateways(self)
        current_gateway = [gateway for gateway in near_gateways if self in gateway][0]
        changed = 0
        for near_gateway in near_gateways:
            if near_gateway != current_gateway:
                if self.__gateway_callback != None:
                    self.__gateway_callback(near_gateway, self)
                delta = self.__bandwidth_variation(current_gateway, near_gateway)
                if delta > 0:
                    current_gateway.disconnect_device(self)
                    near_gateway.connect_device(self)
                    current_gateway = near_gateway
                    changed = 1
        return changed
    
    def set_gateway_callback(self, gateway_callback):
        self.__gateway_callback = gateway_callback

    ID = property(lambda self: self.__ID)
    type = property(lambda self: self.__type)

def update_bandwidth(gateways):
    payoff_a = 0
    payoff_b = 0
    for gateway in gateways:
        n = gateway.get_device_count(DeviceType.TYPE_A)
        m = gateway.get_device_count(DeviceType.TYPE_B)
        if n + m == 0:
            continue
        device_bandwidth = gateway.bandwidth / (n + m)
        payoff_a += device_bandwidth * n
        payoff_b += device_bandwidth * m
    print("WA = {0:.2f} WB = {0:.2f}".format(payoff_a, payoff_b))

def main():
    N = 100
    GATEWAYS = 50
    DEVICES = 100
    gateways = [Gateway(100) for _ in range(GATEWAYS)]
    devices_a = [Device(DeviceType.TYPE_A) for _ in range(DEVICES)]
    devices_b = [Device(DeviceType.TYPE_B) for _ in range(DEVICES)]
    devices = devices_a + devices_b
    space = Space(N, N)
    for g in gateways:
        space.add_element(g)
    
    for d in devices:
        space.add_element(d)
    
    not_changed = 0
    last_value = 0
    counter = 0
    while not_changed != len(devices):
        not_changed = 0
        for d in devices:
            if not d.gateway_selection(space):
                not_changed += 1
        update_bandwidth(gateways)
        if not_changed - 2 <= last_value and not_changed <= not_changed + 2:
            counter += 1
            if counter == 30:
                update_bandwidth(gateways)
                return
        else:
            last_value = not_changed
            counter = 0
        print(not_changed)
    
    print("FINITOOOOOO")


if __name__ == "__main__":
    main()