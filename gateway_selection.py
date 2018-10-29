import math

BANDWIDTH = 10      #bandwidth of the channel (assumption: each gateway has the same bandwidth)
PZERO = 1           #maximum signal intensity estimated 1 meter from the gateway
PL = (2+7)/2        #path loss value usually set at a value from 2 to 7
ALPHA = 1           #threshold value for the difference demand and channel capacity 

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
    COUNT = 0

class Gateway(object):
    COUNT = 0

    def __init__(self):
        Gateway.COUNT += 1
        self.__ID = Gateway.COUNT
    
    ID = property(lambda self: self.__ID)

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
        if self.__positions[x][y] is None or sum([element in row for row in self.__positions]) > 0:
            raise ValueError("The postion ({},{}) is already taken, or the element is already placed.".format(x, y))
        else:
            self.__positions[x][y] = element
    
    def get_element_position(self, element):
        for i in range(self.__rows):
            for j in range(self.__columns):
                if self.__positions[i][j] == element:
                    return (i, j)
        return (None, None)
        



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
    


if __name__ == "__main__":
    for _ in range(10):
        a = Gateway()
        print(a.ID)