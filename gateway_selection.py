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


