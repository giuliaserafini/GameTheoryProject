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
    COUNTER = 0

    def __init__(self, bandwidth, radius=25):
        if bandwidth is None or bandwidth <= 0:
            raise ValueError("Bandwidth must be greater than zero.")
        
        if radius is None or radius <= 0:
            raise ValueError("Radius must be greater than zero.")
        
        Gateway.COUNTER += 1

        self.__ID = Gateway.COUNTER
        self.__bandwidth = bandwidth
        self.__radius = radius
        self.__devices = []

    def connect_device(self, device):
        if device is None or not isinstance(device, Device):
            raise ValueError("The device must be not null.")
        if device not in self.__devices:
            self.__devices.append(device)
    
    def disconnect_device(self, device):
        if device is None or not isinstance(device, Device):
            raise ValueError("The device must be not null.")
        if device in self.__devices:
            self.__devices.remove(device)
    
    def get_device_count(self, type):
        return len([device for device in self.__devices if device.type == type])

    def __eq__(self, other):
        return other.ID == self.ID if isinstance(other, Gateway) else False
    
    def __hash__(self):
        return hash((self.__ID, self.__bandwidth, self.__radius))
    
    def __repr__(self):
        return "Gateway" + str(self.__ID)
    
    def __str__(self):
        return self.__repr__()
    
    def __contains__(self, item):
        return item in self.__devices
    
    ID = property(lambda self: self.__ID)
    bandwidth = property(lambda self: self.__bandwidth)
    devices_count = property(lambda self: len(self.__devices))
    radius = property(lambda self: self.__radius)

class Displacement(object):
    def __init__(self, x, y, element):
        self.__x = x
        self.__y = y
        self.__element = element
    
    def __eq__(self, other):
        return  other.x == self.x and \
                other.y == self.y and \
                other.element == self.element if isinstance(other, Displacement) \
                else False
    
    x = property(lambda self: self.__x)
    y = property(lambda self: self.__y)
    element = property(lambda self: self.__element)

class Space(object):
    def __init__(self, rows, columns):
        if rows is None or rows <= 0:
            raise ValueError("Rows must be greater than zero.")
        if columns is None or columns <= 0:
            raise ValueError("Columns must be greater than zero.")

        self.__rows = rows
        self.__columns = columns
        self.__positions = []
    
    def add_element(self, element, x=None, y=None):
        if len([displacement for displacement in self.__positions if displacement.element == element]) > 0:
            raise RuntimeError("The element is already placed.")
        if (x is not None and (x < 0 or x >= self.__columns)) or (y is not None and (y < 0 or y >= self.__rows)):
            raise IndexError("The position (x, y) must be within the boundaries.")
        if x is not None and y is not None:
            new_displacement = Displacement(x, y, element)
            if len([displacement for displacement in self.__positions if displacement.x == x and displacement.y == y]) > 0:
                raise ValueError("The position ({},{}) is already taken.".format(x, y))
            self.__positions.append(new_displacement)
            if isinstance(element, Device):
                near_gateways = self.get_near_gateways(element)
                if len(near_gateways) == 0:
                    self.__positions.remove(new_displacement)
                    raise ValueError("The device is not able to connect to any gateway.")
                else:
                    random_gateway_index = randint(0, len(near_gateways) - 1)
                    near_gateways[random_gateway_index].connect_device(element)
            return (x, y)
        else:
            added = False
            x = 0
            y = 0
            while not added:
                x = randint(0, self.__columns - 1)
                y = randint(0, self.__rows - 1)
                try:
                    (x, y) = self.add_element(element, x=x, y=y)
                    added = True
                except ValueError as error:
                    continue
            return (x, y)

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