#!/usr/bin/env python
import rospy
import actionlib
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
import random
import copy
import math

class State:

    def __init__(self, route=[], distance= int == 0):
        self.route = route
        self.distance = distance
    def __eq__(self, other):
        for i in range(len(self.route)):
            if (self.route[i] != other.route[i]):
                return False
        return True

    
    def __lt__(self, other):
        return self.distance < other.distance

    def _repr_(self):
        return ('({0},{1})\n'.format(self.route, self.distance))

    
    def copy(self):
        return State(self.route, self.distance)

    
    def deepcopy(self):
        return State(copy.deepcopy(self.route), copy.deepcopy(self.distance))

   
    def update_distance(self, matrix, home):

        
        self.distance = 0
       
        from_index = home
       
        for i in range(len(self.route)):
            self.distance += matrix[from_index][self.route[i]]
            from_index = self.route[i]
        
        self.distance += matrix[from_index][home]


class City:
    
    def __init__(self, index= int, distance= int):
        self.index = index
        self.distance = distance

    
    def __lt__(self, other):
        return self.distance < other.distance


def get_best_solution_by_distance(matrix= [], home= int):
    
    route = []
    from_index = home
    length = len(matrix) - 1
    
    while len(route) < length:
        
        row = matrix[from_index]
       
        cities = {}
        for i in range(len(row)):
            cities[i] = City(i, row[i])
        
        del cities[home]
        for i in route:
            del cities[i]
        
        sorted = list(cities.values())
        sorted.sort()
        
        from_index = sorted[0].index
        route.append(from_index)
    
    state = State(route)
    state.update_distance(matrix, home)
    
    return state



def create_population(matrix= [], home= int, city_indexes= [], size= int):
    
    gene_pool = copy.copy(city_indexes)
    
    gene_pool.pop(home)
    
    population = []
    for i in range(size):
        
        random.shuffle(gene_pool)
        
        state = State(gene_pool[:])
        state.update_distance(matrix, home)
       
        population.append(state)
    
    return population



def crossover(matrix= [], home= int, parents= []):
    
    parent_1 = parents[0].deepcopy()
    parent_2 = parents[1].deepcopy()
    
    part_1 = []
    part_2 = []

    
    a = int(random.random() * len(parent_1.route))
    b = int(random.random() * len(parent_2.route))
    start_gene = min(a, b)
    end_gene = max(a, b)
    
    for i in range(start_gene, end_gene):
        part_1.append(parent_1.route[i])

    
    part_2 = [int(x) for x in parent_2.route if x not in part_1]
    
    state = State(part_1 + part_2)
    state.update_distance(matrix, home)
   
    return state



def mutate(matrix= [], home= int, state= State, mutation_rate= float == 0.01):
    
    mutated_state = state.deepcopy()
    
    for i in range(len(mutated_state.route)):
       
        if (random.random() < mutation_rate):
            
            j = int(random.random() * len(state.route))
            city_1 = mutated_state.route[i]
            city_2 = mutated_state.route[j]
            mutated_state.route[i] = city_2
            mutated_state.route[j] = city_1
    
    mutated_state.update_distance(matrix, home)
    
    return mutated_state



def genetic_algorithm(matrix= [], home= int, population= [], keep= int, mutation_rate= float, generations= int):
    
    for i in range(generations):

        
        population.sort()
        
        parents = []
        for j in range(1, len(population)):
            parents.append((population[j - 1], population[j]))
        
        children = []
        for partners in parents:
            children.append(crossover(matrix, home, partners))
        
        for j in range(len(children)):
            children[j] = mutate(matrix, home, children[j], mutation_rate)

        
        population = population[:keep]
        
        population.extend(children)
   
    population.sort()
    
    return population[0]

def distance(a=[],b=[]):
    dist= math.sqrt(((a[0]-b[0])*(a[0]-b[0]))+(a[1]-b[1])*(a[1]-b[1]))
    return dist
    
def movebase_istemci():
    cities = ['Point1', 'Point2', 'Point3','Point4']
    home = 0  
    point1=[2,2]
    point2=[-4,-8]
    point3=[-0.5,-3]
    point4=[0,2]
    city_indexes = [0, 1, 2, 3]
    dist11=distance(point1,point1)
    dist12=distance(point1,point2)
    dist13=distance(point1,point3)
    dist14=distance(point1,point4)
    dist21=distance(point2,point1)
    dist22=distance(point2,point2)
    dist23=distance(point2,point3)
    dist24=distance(point2,point4)
    dist31=distance(point3,point1)
    dist32=distance(point3,point2)
    dist33=distance(point3,point3)
    dist34=distance(point3,point4)
    dist41=distance(point4,point1)
    dist42=distance(point4,point2)
    dist43=distance(point4,point3)
    dist44=distance(point4,point4)

    matrix = [[dist11, dist12, dist13, dist14],
              [dist21, dist22, dist23, dist24],
              [dist31, dist32, dist33, dist34],
              [dist41, dist42, dist43, dist44]]
    population = create_population(matrix, home, city_indexes, 100)
    state = genetic_algorithm(matrix, home, population, 20, 0.01, 100)

    istemci = actionlib.SimpleActionClient('move_base',MoveBaseAction)
    istemci.wait_for_server()
    hedef = MoveBaseGoal()
    hedef.target_pose.header.frame_id = "map"
    i=0
    print(cities[home])
    for i in range(0, len(state.route)):
        print(' > ' + cities[state.route[i]])
    print(' -> ' + cities[home])
    print('\n\nTotal distance: {0} meters'.format(state.distance))
    print()
  
    for i in range(0, len(state.route)):    
        if state.route[i]==0:
            hedef.target_pose.pose.position.x = point1[0]
            hedef.target_pose.pose.position.y = point1[1]
            hedef.target_pose.pose.orientation.w = 1.0
            bekle = istemci.wait_for_result()
            print("Moving to Point1")
            istemci.send_goal(hedef)
            i=i+1
        elif state.route[i]==1:
            hedef.target_pose.pose.position.x = point2[0]
            hedef.target_pose.pose.position.y = point2[1]
            hedef.target_pose.pose.orientation.w = 1.0
            bekle = istemci.wait_for_result()
            print("Moving to Point2")
            istemci.send_goal(hedef)
            i=i+1
        if i==3:
            hedef.target_pose.pose.position.x = point1[0]
            hedef.target_pose.pose.position.y = point1[1]
            hedef.target_pose.pose.orientation.w = 1.0
            bekle = istemci.wait_for_result()
            print("Moving to Point1")
            istemci.send_goal(hedef)
            
        elif state.route[i]==2:
            hedef.target_pose.pose.position.x = point3[0]
            hedef.target_pose.pose.position.y = point3[1]
            hedef.target_pose.pose.orientation.w = 1.0
            bekle = istemci.wait_for_result()
            print("Moving to Point3")
            istemci.send_goal(hedef)
            i=i+1
        if i==3:
            hedef.target_pose.pose.position.x = point1[0]
            hedef.target_pose.pose.position.y = point1[1]
            hedef.target_pose.pose.orientation.w = 1.0
            bekle = istemci.wait_for_result()
            print("Moving to Point1")
            istemci.send_goal(hedef)
            
        elif state.route[i]==3:
            hedef.target_pose.pose.position.x = point4[0]
            hedef.target_pose.pose.position.y = point4[1]
            hedef.target_pose.pose.orientation.w = 1.0
            bekle = istemci.wait_for_result()
            print("Moving to Point4")
            istemci.send_goal(hedef)
            i=i+1
        if i==3:
            hedef.target_pose.pose.position.x = point1[0]
            hedef.target_pose.pose.position.y = point1[1]
            hedef.target_pose.pose.orientation.w = 1.0
            bekle = istemci.wait_for_result()
            print("Moving to Point1")
            istemci.send_goal(hedef)
    	    
    if not bekle:
 	   
        rospy.signal_shutdown("aa")
    else:
        return istemci.get_result()   

if __name__ == '__main__':
    try:
        rospy.init_node('move_base_hedef_gonder')
        result = movebase_istemci()
        if result:
            rospy.loginfo("a")
        else:
            rospy.loginfo("Moving back to home...")
	   
            
    except rospy.ROSInterruptException:
        pass
