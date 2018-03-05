import math

rows = 0
columns = 0
vehicles = 0
rides = 0
startbonus = 0
totalsteps = 0



def distance(x, y):
    return abs(x[0] - y[0]) + abs(x[1] - y[1])

class Vehicle:
    def __init__(self):
        self.currentPos=[0,0]
        self.next_free = 0 #the time at which the vehicle finishes the time.
        self.completedRides = [] #list of finished rides that the vehicle has taken
        self.ride = Ride(0,[0,0],[0,0],0,0) # current ride that it is taking

    def getCurrentPos(self):
        return self.currentPos

    def getCurrentRide(self):
        return self.ride

    def getNextFree(self):
        return self.next_free

    def setNextFree(self, distance):
        self.next_free = distance

    def setRide(self, ride):
        self.ride = ride


    def checkFinish(self): #checks if the ride is out of time/arrives at destination
        if self.next_free == curtime:
            return True
        else:
            return False

    def updatePos(self, x, y):
        self.currentPos = [x, y]


    def __str__(self):
        return "Current Position: %s, Next Free: %s, Completed Rides: %s, Current Ride: %s" % (self.currentPos, self.next_free, self.completedRides, self.ride)








class Ride:
    def __init__(self,ID,startpoint,finishpoint,earlieststart,latestfinish):
        self.ID = ID
        self.startpoint = startpoint
        self.finishpoint = finishpoint
        self.earlieststart = earlieststart
        self.latestfinish = latestfinish
        self.distance = distance(startpoint, finishpoint)

    def getID(self):
        return self.ID

    def getStartPoint(self):
        return self.startpoint

    def getFinishPoint(self):
        return self.finishpoint

    def getEarliestStart(self):
        return self.earlieststart

    def getLastestFinish(self):
        return self.latestfinish

    def __str__(self):
        return "ID: %s" % self.ID




def read_input_file(file):
    input_file = open(file, 'r')
    line = input_file.readline().split()
    rows = int(line[0])
    columns = int(line[1])
    numvehicles = int(line[2])
    rides = int(line[3])
    startbonus = int(line[4])
    totalsteps = int(line[5])
    rides = []
    ride_id = 0;
    for line in input_file.readlines():
        line = line.split()
        ride = Ride(ride_id,[int(line[0]),int(line[1])],[int(line[2]),int(line[3])],int(line[4]),int(line[5]))
        ride_id += 1
        n = 0
        while True:
            if n == len(rides):
                rides += [ride]
                break
            if rides[n].latestfinish >= ride.latestfinish:
                rides.insert(n,ride)
                break
            n += 1
    vehicles = []
    for i in range(numvehicles):
        vehicles += [Vehicle()]
    city_map = Map(startbonus,vehicles,rides,totalsteps)
    return city_map


def create_output_file(mappyboi):
    #print("total length of cars outputted" +str(len(mappyboi.vehicles) + len(mappyboi.finished_vehicles)))
    out_file = open('log', 'w')
    for i in mappyboi.vehicles:
        ln=str(len(i.completedRides))+" "
        for n in i.completedRides:
            print('Completed Rides: %s' % n)
            ln+=str(n)+" "
        out_file.write(ln +'\n')
    print(mappyboi.finished_vehicles)
    for i in mappyboi.finished_vehicles:
        numRides = len(i.completedRides)
        ln=str(numRides)+" "
        #print(ln)
        for n in i.completedRides:
            #print(n)
            ln+=str(n)+" "
        out_file.write(ln +'\n')
    out_file.close()



class Map(object):

    def __init__(self, startbonus, vehicles, rides, totalsteps):

        self.startbonus = startbonus
        self.vehicles = vehicles
        self.rides = rides
        self.totalsteps = totalsteps
        self.curtime = 0
        self.finished_vehicles = []

    def addVehicle(self, vehicle):
        time_till_available = vehicle.getNextFree()
        #print(vehicle)
        if len(self.vehicles) == 0:
            self.vehicles += [vehicle]
        else:
            for i in range(len(self.vehicles)):
                if self.vehicles[i].getNextFree() > time_till_available:
                    #print('if statement works')
                    #right here bois
                    self.vehicles.insert(i+1, vehicle)
                    return
            self.vehicles.insert(0, vehicle)


    def getVehicles(self):
        return self.vehicles

    def getRides(self):
        return self.rides


    def calculate_points(self, car, ride):
        if distance(car.ride.finishpoint, ride.startpoint) + car.next_free < ride.earlieststart:
            points = ride.distance + self.startbonus
        else:
            points = ride.distance
        return points

    def calculate_best_ride(self, vehicle):
        valid_rides = []
        array_pointer = 0
        cv = vehicle
        while True:
            if array_pointer >= min(20,len(self.rides)-1) and len(valid_rides) > 0:
                #print('we broke')
                break
            cr = self.rides[array_pointer]
            #checks if it can reach the ride before its last possible pickup time.
            if distance(cv.ride.finishpoint, cr.startpoint) + cv.next_free < cr.latestfinish - cr.distance:
                valid_rides.append(cr)
            array_pointer +=1
            if array_pointer == len(self.rides) and len(valid_rides) == 0:
                #print("end_vehicle")
                self.finished_vehicles.append(cv)
                return

        best_ride = valid_rides.pop()
        for ride in valid_rides:
            if self.calculate_points(cv, ride) > self.calculate_points(cv, best_ride):
                best_ride = ride
        #roeioeuioeuioeuioo
        wait_time = (distance(cv.ride.finishpoint, best_ride.startpoint)) -  (best_ride.earlieststart - self.curtime)
        if wait_time > 0:
            cv.setNextFree(self.curtime + wait_time + distance(cv.ride.finishpoint, best_ride.startpoint) + best_ride.distance)
        else:
            cv.setNextFree(self.curtime + distance(cv.ride.finishpoint, best_ride.startpoint) + best_ride.distance)
        print('current vehicle next_free %s' % cv.next_free)

        cv.setRide(best_ride)
        self.rides.remove(best_ride)
        #print(best_ride)
        self.addVehicle(cv)

    def incerementTime(self):
        self.curtime +=1


def main():
    city_map = read_input_file("b_should_be_easy.in")
    while city_map.curtime < city_map.totalsteps:
        while len(city_map.vehicles) > 0 and city_map.vehicles[-1].next_free == city_map.curtime:
            if len(city_map.rides) == 0:
                print('len of city_map.rides is 0')
                break
            car = city_map.vehicles.pop()
            print(car)
            if car.ride.distance != 0:
                car.completedRides += [car.ride.ID]
            city_map.calculate_best_ride(car)
            print("length of city map vehicles: ", end='')
            print(len(city_map.vehicles))
        city_map.incerementTime()
    create_output_file(city_map)









if __name__ == "__main__":
    main()
    print('done')
