import math

BANDWIDTH   = 10      #bandwidth of the channel (assumption: each gateway has the same bandwidth)
PZERO       = 30          #maximum signal intensity estimated 1 meter from the gateway
PL          = (2+7)/2        #path loss value usually set at a value from 2 to 7
ALPHA       = 1           #threshold value for the difference demand and channel capacity 

#the gateway power is given 
GATEWAY_POWER = {'gateway1': 20, 'gateway2': 30, 'gateway3': 15}  

DEVICE_DEMAND = {'device1': 5, 'device2': 7, 'device3':4, 'device4': 8, 'device5': 2}

#structure of our space (gateways and devices)   
space = [["device1","","",""],                      
         ["device5","device2","",""],
         ["","","device3",""],
         ["","","device4","gateway2"],
         ["gateway1","","",""]]

class Device(object):
    COUNTER = 0

    def __init__(self, demand=10.0):
        Device.COUNTER += 1
        self.__ID = Device.COUNTER
        
        if demand is None or demand <= 0.0:
            raise ValueError("Demand can't be null and must be greater than zero.")
        
        self.__demand = demand * 1E6
    
    def __eq__(self, other):
        return other.ID == self.ID if isinstance(other, Device) else False
    
    def __repr__(self):
        return "Device{}".format(self.__ID)
    
    def __str__(self):
        return self.__repr__()

    ID      = property(lambda self: self.__ID)
    demand  = property(lambda self: self.__demand)

class Gateway(object):
    COUNTER = 0

    def __init__(self, power=10.0, bandwidth=50.0):
        Gateway.COUNTER += 1
        self.__ID = Gateway.COUNTER
        
        if power is None or power <= 0.0:
            raise ValueError("Power can't be null and must be greater than zero.")
        
        if bandwidth is None or bandwidth <= 0.0:
            raise ValueError("Bandwidth can't be null and must be greater than zero.")

        self.__power = power * 1E-3
        self.__bandwidth = bandwidth * 1E6
    
    def __eq__(self, other):
        return other.ID == self.ID if isinstance(other, Gateway) else False
    
    def __repr__(self):
        return "Gateway{}".format(self.__ID)
    
    def __str__(self):
        return self.__repr__()

    ID          = property(lambda self: self.__ID)
    power       = property(lambda self: self.__power)
    bandwidth   = property(lambda self: self.__bandwidth)
    

class Space(object):
    def __init__(self, rows, columns):
        if rows is None or rows <= 0:
            raise ValueError("Rows must be an integer, greater than zero.")
        if columns is None or columns <= 0:
            raise ValueError("Columns must be an integer, greater than zero.")
        self.__rows = rows
        self.__columns = columns
        self.__positions = [[None for _ in range(self.__columns)] for _ in range(self.__rows)]

    def add_element(self, x, y, element):
        if x < 0 or x >= self.__rows:
            raise ValueError("The index x must be between 0 and the number of rows.")
        if y < 0 or y >= self.__columns:
            raise ValueError("The index y must be between 0 and the number of columns.")
        if sum([element in row for row in self.__positions]) > 0:
            raise ValueError("The postion ({},{}) is already taken, or the element is already placed.".format(x, y))
        if element is None or not (isinstance(element, Device) or isinstance(element, Gateway)):
            raise ValueError("The element must be not null and it can be only a device or a gateway.")
        self.__positions[x][y] = element
    
    def get_element_position(self, element):
        for i in range(self.__rows):
            for j in range(self.__columns):
                if self.__positions[i][j] == element:
                    #return (i + 1, j + 1)
                    return ((i + 1) * 50.0, (j + 1) * 50.0)
        return (None, None)
    
    def get_distance(self, element1, element2):
        (x1, y1) = self.get_element_position(element1)
        (x2, y2) = self.get_element_position(element2)
        if x1 is None and y1 is None:
            raise ValueError("The first element is not present.")
        if x2 is None and y2 is None:
            raise ValueError("The second element is not present")
        return math.sqrt(math.pow(x1 - x2, 2) + math.pow(y1 - y2, 2))
    
    def rssi(self, device, gateway):
        if device is None or not isinstance(device, Device):
            raise ValueError("The device must be a device and not null.")
        if gateway is None or not isinstance(gateway, Gateway):
            raise ValueError("The gateway must be a gateway and not null.")
        a = PZERO - 10.0 * PL * math.log10(self.get_distance(device, gateway))
        return PZERO - 10.0 * PL * math.log10(self.get_distance(device, gateway))
    
    def device_gateway_power(self, device, gateway):
        b = gateway.power  / math.pow(10, math.fabs(self.rssi(device, gateway)) / 10.0)
        return gateway.power  / math.pow(10, math.fabs(self.rssi(device, gateway)) / 10.0)
    
    def device_gateway_power_noise(self, device, gateway):
        sum_distances = 0.0
        for i in range(self.__rows):
            for j in range(self.__columns):
                current_element = self.__positions[i][j]
                if current_element != None and isinstance(current_element, Device) and current_element != device:
                    sum_distances += self.get_distance(device, current_element)
        return self.device_gateway_power(device, gateway) / sum_distances
    
    def snr(self, device, gateway):
        return self.device_gateway_power(device, gateway) / self.device_gateway_power_noise(device, gateway)

    def capacity(self, device, gateway):
        return gateway.bandwidth * math.log2(1 + self.snr(device, gateway))
    
    def k(self, device, gateway):
        gap = device.demand - self.capacity(device, gateway)

        if gap <= 0.0:
            return 0.0
        elif gap > 0 and gap <= ALPHA:
            return device.demand / self.capacity(device, gateway)
        else:
            return gap


#given a string and a 2-dim space (matrix with string elements),
#it returns the position row-column of object in space
def position(object, space):
    for row in range(len(space)):
        for column in range(len(space[row])):
            if (space[row][column] is object):
                return [row+1, column+1]
    return [0,0]


#a 2-dim space contains two elements, a and b, and the function returns the euclidean distance between them 
def distance(a, b, space): 
    a_position = position(a, space)
    b_position = position(b, space)
    return math.sqrt(math.pow(a_position[0]-b_position[0],2)+ math.pow(a_position[1]-b_position[1],2))

#Rssi between ei and gj 
def Rssi(device, gateway, space):
    return PZERO-10*PL*math.log10(distance(device, gateway, space))

#P_ei 
def power_device_gateway(device, gateway, space):
    return GATEWAY_POWER[gateway]/math.pow(10, abs(Rssi(device, gateway, space))/10)

#P_noise 
def power_noise(device, gateway, space):
    list_devices = []
    for row in range(len(space)):
        for column in range(len(space[row])):
            object = space[row][column]
            if ("device" in object and object is not device): 
                list_devices.append(object)
    sum_distances = 0
    for element in list_devices:
        sum_distances+=distance(device, element, space)
    return power_device_gateway(device, gateway, space)/sum_distances

def SNR(device, gateway, space):
    return power_device_gateway(device, gateway, space)/power_noise(device, gateway, space)

#C between device ei and gateway gj
def capacity(device, gateway, space):
    return BANDWIDTH*math.log2(1+SNR(device, gateway, space))

def K_i(device, gateway, space):
    gap_demand_capacity = DEVICE_DEMAND[device]-capacity(device, gateway, space)
    if(gap_demand_capacity <= 0):
        return 0
    elif(gap_demand_capacity > 0 and gap_demand_capacity < ALPHA):
        return DEVICE_DEMAND[device]/capacity(device, gateway, space)
    else:
        return gap_demand_capacity

#binary variable which says if the device i is associated to the gateway j, the matrix is a device*gateeway matrix in which is cell is 1 or 0
def device_gateway_assignment(device, gateway, device_gateway_matrix):
    return device_gateway_matrix[int(device.replace('device', '')-1)][int(gateway.replace('gateway', ''))-1]
 

def utility(device, gateway, device_gateway_matrix, space):
    m = 0
    for dev in range(len(device_gateway_matrix)):
        m+=device_gateway_assignment(dev, gateway, device_gateway_matrix)
    return (BANDWIDTH/m)-K_i(device, gateway, space)
    
def main():
    space = Space(5, 6)
    gateways = [Gateway(power=20.0), Gateway(power=30.0), Gateway(power=15.0)]
    devices = [Device(demand=5.0), Device(demand=7.0), Device(demand=4.0), Device(demand=8.0), Device(demand=2.0), Device(demand=3.0)]
    space.add_element(0, 0, devices[0])
    space.add_element(2, 1, devices[1])
    space.add_element(1, 4, devices[2])
    space.add_element(3, 3, devices[3])
    space.add_element(0, 3, devices[4])
    space.add_element(3, 0, devices[5])
    space.add_element(1, 2, gateways[0])
    space.add_element(4, 1, gateways[1])
    space.add_element(3, 4, gateways[2])

    for gateway in gateways:
        for device in devices:
            print("{} - {} SNR: {}".format(device, gateway, space.device_gateway_power(device, gateway)))

if __name__ == "__main__":
    main()