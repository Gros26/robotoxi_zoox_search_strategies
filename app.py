from pathlib import Path
from collections import deque
import heapq

#• 0 si es una casilla libre (flujo vehicular bajo)
#• 1 si es un muro
#• 2 si es el punto de partida del vehículo
#• 3 si es una casilla con flujo vehicular alto
#• 4 si es un pasajero
#• 5 si es el destino

class Node():
    def __init__(self, row, column):
        self.parent = None
        self.row = row
        self.column = column
        self.operator = None
        self.passengers = set()
        self.accumulated_cost = 0

    def clone(self):
        new_node = Node(self.row, self.column)
        new_node.parent = self.parent
        new_node.operator = self.operator
        new_node.passengers = self.passengers
        new_node.accumulated_cost = self.accumulated_cost
        return new_node

    def get_state(self):
        return (self.row, self.column, frozenset(self.passengers))

    def print_parent(self):
        return self.parent
    
    def get_position(self):
        return (self.row, self.column)



class City():
    def __init__(self, filename):
        
        #read the file
        #with open(filename) as f:
        file_path = Path(__file__).resolve().parent / filename
        with open(file_path, encoding="utf-8") as f:
            contents = f.read()

        #validation that should only have one starting point
        if contents.count('2') != 1:
            raise Exception('Debe haber solo un punto de partida')

        #validation that should only have one destination point
        if contents.count('5') != 1:
            raise Exception('Debe haber solo un destino')    
        
        self.goal_passengers = contents.count('4')

        #determine width and height of the city
        contents = contents.splitlines() # this returns an array
        self.height = len(contents) # the height is the number of lines
        self.width = max(len(line) for line in contents) # the width is the most largest line in the array
        
        self.matrix = []
        self.passengers = []
        self.high_flow = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                try:
                    if contents[i][j] == '2': 
                        self.start = (i, j) #save my starting point
                        row.append('2')
                    elif contents[i][j] == '3':
                        self.high_flow.append((i, j))
                        row.append('3')
                    elif contents[i][j] == '4':
                        self.passengers.append((i, j))
                        row.append('4')
                    elif contents[i][j] == '5':
                        self.goal_destination = (i, j) # save my destination point
                        row.append('5')
                    else:
                        row.append(contents[i][j])
                except IndexError:
                    row.append('0')
            self.matrix.append(row) #this is a 2D array
    
        self.goal = (self.goal_destination[0], self.goal_destination[1], set(self.passengers))


    def print(self):
        print()
        for i in range(self.height):
            for j in range(self.width):
                if (i, j) == self.goal_destination:
                    print("X", end="")
                elif (i, j) == self.start:
                    print("R", end="")
                elif self.matrix[i][j] == '1':
                    print("█", end="")
                elif self.matrix[i][j] == '3':
                    print("+", end="")
                elif self.matrix[i][j] == '4':
                    print("P", end="")
                else:
                    print(" ", end="")
            print()
        print()

node1 = Node(2,0)        

class Robotaxi():
    def __init__(self, y, x, city, search=None):
        self.column = x
        self.row = y
        self.city = city
        self.matrix = city.matrix
        self.update_sensors()
        self.h(node1)
        if search:
            match search:
                case "bfs":
                    return self.bfs()
                case "dfs":
                    return self.dfs()
                case "ucs":
                    return self.ucs()
        

    def position(self):
        return (self.row, self.column)
    
    def move(self, y, x):
        self.matrix[self.row][self.column] = '0'
        self.matrix[y][x] = '2'
        self.row = y
        self.column = x
        self.update_sensors()

    def update_sensors(self):
        self.left = self.column - 1 >= 0 and self.matrix[self.row][self.column - 1] != '1'
        self.up = self.row - 1 >= 0 and self.matrix[self.row - 1][self.column] != '1'
        self.right = self.column + 1 <= (len(self.matrix[self.row]) - 1) and self.matrix[self.row][self.column + 1] != '1'
        self.down = self.row + 1 <= (len(self.matrix) - 1) and self.matrix[self.row + 1][self.column] != '1'

    def find_position(self, to_move):
        match to_move:
            case "right":
                return (self.row, self.column + 1)
            case "down":
                return (self.row + 1, self.column)
            case "left":
                return (self.row, self.column - 1)
            case "up":
                return (self.row - 1, self.column)


    def bfs(self):
        queue = deque()
        initial_node = Node(*(self.position())) 
        queue.append(initial_node)
        visited = {initial_node.get_state()}
        count = 0

        while(True):
            count += 1

            if not queue: 
                raise Exception(f"No hay solución, los pasos hasta aqui fueron: {count}")
            
            node_to_expand = queue.popleft()
            self.move(*(node_to_expand.get_position()))
            self.update_sensors()

            if node_to_expand.get_state() == self.city.goal:
                print(self.get_route(node_to_expand))
                return print(f"Lo encontrooooo: {node_to_expand.get_state()}, expandio {count} nodos")

            if node_to_expand.get_position() in self.city.passengers:
                node_to_expand.passengers.add(node_to_expand.get_position())

            paths = []
            if self.right:
                movement = self.find_position("right")
                node = Node(*(movement))
                node.parent = node_to_expand
                node.passengers = set(node.parent.passengers)
                node.operator = "right"
                if node.get_state() not in visited:
                    paths.append(node)
                visited.add(node.get_state())
            if self.left:
                movement = self.find_position("left")
                node = Node(*(movement))
                node.parent = node_to_expand
                node.passengers = set(node.parent.passengers)
                node.operator = "left"
                if node.get_state() not in visited:
                    paths.append(node)
                visited.add(node.get_state())
            if self.up:
                movement = self.find_position("up")
                node = Node(*(movement))
                node.parent = node_to_expand
                node.passengers = set(node.parent.passengers)
                node.operator = "up"
                if node.get_state() not in visited:
                    paths.append(node)
                visited.add(node.get_state())
            if self.down:
                movement = self.find_position("down")
                node = Node(*(movement))
                node.parent = node_to_expand
                node.passengers = set(node.parent.passengers)
                node.operator = "down"
                if node.get_state() not in visited:
                    paths.append(node)
                visited.add(node.get_state())

            queue.extend(paths)

    def dfs(self):
        stack = []
        initial_node = Node(*(self.position())) 
        stack.append(initial_node)
        visited = {initial_node.get_state()}
        count = 0

        while(True):
            count += 1

            if not stack: 
                raise Exception(f"No hay solución, los pasos hasta aqui fueron: {count}")
            
            node_to_expand = stack.pop()
            self.move(*(node_to_expand.get_position()))
            self.update_sensors()

            if node_to_expand.get_state() == self.city.goal:
                print(self.get_route(node_to_expand))
                return print(f"Lo encontrooooo: {node_to_expand.get_state()}, expandio {count} nodos")

            if node_to_expand.get_position() in self.city.passengers:
                node_to_expand.passengers.add(node_to_expand.get_position())


            if self.right:
                movement = self.find_position("right")
                node = Node(*(movement))
                node.parent = node_to_expand
                node.passengers = set(node.parent.passengers)
                node.operator = "right"
                if node.get_state() not in visited:
                    stack.append(node)
                visited.add(node.get_state())
            if self.left:
                movement = self.find_position("left")
                node = Node(*(movement))
                node.parent = node_to_expand
                node.passengers = set(node.parent.passengers)
                node.operator = "left"
                if node.get_state() not in visited:
                    stack.append(node)
                visited.add(node.get_state())
            if self.up:
                movement = self.find_position("up")
                node = Node(*(movement))
                node.parent = node_to_expand
                node.passengers = set(node.parent.passengers)
                node.operator = "up"
                if node.get_state() not in visited:
                    stack.append(node)
                visited.add(node.get_state())
            if self.down:
                movement = self.find_position("down")
                node = Node(*(movement))
                node.parent = node_to_expand
                node.passengers = set(node.parent.passengers)
                node.operator = "down"
                if node.get_state() not in visited:
                    stack.append(node)
                visited.add(node.get_state())

    def ucs(self): #uniform cost search
        queue = []
        initial_node = Node(*(self.position())) 
        count_heapq = 0  #This is a counter for tie-breaker
        count = 0 #This is the node expand counter
        #priority = 0 #This is the algorith counter
        """ uso de heapq
        # Agregar elementos (prioridad, dato)
        heapq.heappush(cola, (3, "Tarea baja"))
        heapq.heappush(cola, (1, "Tarea crítica"))
        heapq.heappush(cola, (2, "Tarea media"))

        # Extraer el elemento de mayor prioridad (el valor numérico más bajo)
        prioridad, tarea = heapq.heappop(cola)
        print(f"Procesando: {tarea} (Prioridad: {prioridad})")
        # Salida: Procesando: Tarea crítica (Prioridad: 1)"""
        heapq.heappush(queue, (initial_node.accumulated_cost, count_heapq, initial_node))
        count_heapq += 1
        visited = {initial_node.get_state()}

        while True:
            count += 1

            if not queue: 
                raise Exception(f"No hay solución, los pasos hasta aqui fueron: {count}")
            
            _, _,node_to_expand = heapq.heappop(queue)
            self.move(*(node_to_expand.get_position()))
            self.update_sensors()

            if node_to_expand.get_state() == self.city.goal:
                print(self.get_route(node_to_expand)) #Improvement: here it can return the node, and then in the function call we use this returned node
                return print(f"Lo encontrooooo: {node_to_expand.get_state()}, expandio {count} nodos")

            if node_to_expand.get_position() in self.city.passengers:
                node_to_expand.passengers.add(node_to_expand.get_position())


            if self.right:
                movement = self.find_position("right")
                node = Node(*(movement))
                node.parent = node_to_expand
                node.passengers = set(node.parent.passengers)
                node.operator = "right"
                node.accumulated_cost = node.parent.accumulated_cost
                self.update_accumulated_cost(node)
                if node.get_state() not in visited:
                    heapq.heappush(queue, (node.accumulated_cost, count_heapq, node))
                    count_heapq += 1
                visited.add(node.get_state())

            if self.left:
                movement = self.find_position("left")
                node = Node(*(movement))
                node.parent = node_to_expand
                node.passengers = set(node.parent.passengers)
                node.operator = "left"
                node.accumulated_cost = node.parent.accumulated_cost
                self.update_accumulated_cost(node)
                if node.get_state() not in visited:
                    heapq.heappush(queue, (node.accumulated_cost, count_heapq, node))
                    count_heapq += 1
                visited.add(node.get_state())

            if self.up:
                movement = self.find_position("up")
                node = Node(*(movement))
                node.parent = node_to_expand
                node.passengers = set(node.parent.passengers)
                node.operator = "up"
                node.accumulated_cost = node.parent.accumulated_cost
                self.update_accumulated_cost(node)
                if node.get_state() not in visited:
                    heapq.heappush(queue, (node.accumulated_cost, count_heapq, node))
                    count_heapq += 1
                visited.add(node.get_state())

            if self.down:
                movement = self.find_position("down")
                node = Node(*(movement))
                node.parent = node_to_expand
                node.passengers = set(node.parent.passengers)
                node.operator = "down"
                node.accumulated_cost = node.parent.accumulated_cost
                self.update_accumulated_cost(node)
                if node.get_state() not in visited:
                    heapq.heappush(queue, (node.accumulated_cost, count_heapq, node))
                    count_heapq += 1
                visited.add(node.get_state())


    def update_accumulated_cost(self, node: Node):
        if node.get_position() in self.city.high_flow:
            node.accumulated_cost += 7
        else:
            node.accumulated_cost += 1

        
    
    def get_route(self, node: Node):
        route = []
        while node.parent != None:
            route.append(node.get_state())
            node = node.parent

        route.append(node.get_state())
        route.reverse()

        return route

    #h(n)
    def h(self, ref_node: Node):
        #The idea is the sum of the distances from the car to the passengers and then to the destination
        #i'm going to make a basic implementation, but this can be better if we select the passenger nearest to the car in each iteration
        node = ref_node.clone()
        goal_passengers = self.city.passengers
        _, _, passengers = node.get_state()
        heuristic = 0

        for passenger in goal_passengers:
            if passenger not in passengers:
                goal_row, goal_column = passenger
                heuristic += self.manhattan_distance(node.row, node.column, goal_row, goal_column)
                node.row = goal_row
                node.column = goal_column
        heuristic += self.manhattan_distance(node.row, node.column, *(self.city.goal_destination))



    def manhattan_distance(self, init_row, init_column, goal_row, goal_column):
        return abs(init_row - goal_row) + abs(init_column - goal_column)



    


#verify that the matrix is ​​not modified after execution it must always be the same

city = City("city1.txt")
print(city.matrix)
city.print()
print("Robotaxi 1")
robotaxi = Robotaxi(*(city.start), city, "bfs")
print("Robotaxi 2")
robotaxi2 = Robotaxi(*(city.start), city, "dfs")
print("Robotaxi 3")
robotaxi3 = Robotaxi(*(city.start), city)
print("Robotaxi 4")
robotaxi4 = Robotaxi(*(city.start), city, "ucs")

