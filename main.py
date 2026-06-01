import pygame
import sys
from pathlib import Path
from search import City, Robotaxi, Node

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)
LIGHT_GRAY = (200, 200, 200)
DARK_GRAY = (64, 64, 64)
BLUE = (0, 100, 255)
BLUE_HOVER = (0, 150, 255)
RED = (255, 0, 0)
GREEN = (0, 200, 0)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)

class Button:
    def __init__(self, x, y, width, height, text, font):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font = font
        self.is_hovered = False
        
    def draw(self, screen):
        color = BLUE_HOVER if self.is_hovered else BLUE
        pygame.draw.rect(screen, color, self.rect)
        pygame.draw.rect(screen, BLACK, self.rect, 2)
        
        text_surface = self.font.render(self.text, True, WHITE)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)
    
    def update(self, mouse_pos):
        self.is_hovered = self.rect.collidepoint(mouse_pos)
    
    def is_clicked(self, mouse_pos):
        return self.rect.collidepoint(mouse_pos)


class AlgorithmScreen:
    def __init__(self, screen_width, screen_height):
        self.width = screen_width
        self.height = screen_height
        self.font_title = pygame.font.Font(None, 48)
        self.font_button = pygame.font.Font(None, 28)
        
        self.algorithms = ["BFS", "DFS", "UCS", "Greedy Search", "A*"]
        self.buttons = []
        self.selected_algorithm = None
        
        button_width = 200
        button_height = 50
        start_y = 200
        button_spacing = 80
        
        for i, algo in enumerate(self.algorithms):
            x = (screen_width - button_width) // 2
            y = start_y + i * button_spacing
            self.buttons.append(Button(x, y, button_width, button_height, algo, self.font_button))
    
    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            for button in self.buttons:
                button.update(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            for i, button in enumerate(self.buttons):
                if button.is_clicked(event.pos):
                    self.selected_algorithm = self.algorithms[i]
                    return True
        return False
    
    def draw(self, screen):
        screen.fill(WHITE)
        title = self.font_title.render("Selecciona un Algoritmo", True, BLACK)
        title_rect = title.get_rect(center=(self.width // 2, 80))
        screen.blit(title, title_rect)
        
        for button in self.buttons:
            button.draw(screen)


class MapScreen:
    def __init__(self, screen_width, screen_height):
        self.width = screen_width
        self.height = screen_height
        self.font_title = pygame.font.Font(None, 48)
        self.font_button = pygame.font.Font(None, 28)
        
        # Buscar archivos .txt
        self.maps = self.find_map_files()
        self.buttons = []
        self.selected_map = None
        
        button_width = 200
        button_height = 50
        start_y = 200
        button_spacing = 80
        
        for i, map_file in enumerate(self.maps):
            x = (screen_width - button_width) // 2
            y = start_y + i * button_spacing
            map_name = map_file.stem
            self.buttons.append(Button(x, y, button_width, button_height, map_name, self.font_button))
    
    def find_map_files(self):
        """Encuentra todos los archivos .txt en la carpeta"""
        project_dir = Path(__file__).parent
        map_files = list(project_dir.glob("*.txt"))
        return sorted(map_files)
    
    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            for button in self.buttons:
                button.update(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            for i, button in enumerate(self.buttons):
                if button.is_clicked(event.pos):
                    self.selected_map = self.maps[i].name
                    return True
        return False
    
    def draw(self, screen):
        screen.fill(WHITE)
        title = self.font_title.render("Selecciona un Mapa", True, BLACK)
        title_rect = title.get_rect(center=(self.width // 2, 80))
        screen.blit(title, title_rect)
        
        for button in self.buttons:
            button.draw(screen)


class VisualizationScreen:
    def __init__(self, screen_width, screen_height, algorithm, map_file):
        self.width = screen_width
        self.height = screen_height
        self.font_small = pygame.font.Font(None, 20)
        self.font_medium = pygame.font.Font(None, 28)
        
        self.algorithm = algorithm
        self.map_file = map_file
        
        # Cargar ciudad
        self.city = City(map_file)
        self.cell_size = min((screen_width - 100) // self.city.width, 
                             (screen_height - 200) // self.city.height)
        
        # Posición del mapa en pantalla
        self.map_x = 50
        self.map_y = 150
        
        # Estado de ejecución
        self.route = []
        self.current_step = 0
        self.finished = False
        self.nodes_expanded = 0
        self.total_cost = 0
        self.passengers_collected = set()
        
        self.execute_algorithm()
    
    def execute_algorithm(self):
        """Ejecuta el algoritmo y obtiene la ruta"""
        algo_map = {
            "BFS": "bfs",
            "DFS": "dfs",
            "UCS": "ucs",
            "Greedy Search": "gs",
            "A*": "a_star"
        }
        
        try:
            # Crear una copia de la ciudad para no modificar la original
            robotaxi = Robotaxi(*(self.city.start), self.city, algo_map[self.algorithm])
            # Si llegó aquí sin excepción, obtener ruta del resultado
            # Nota: los métodos actuales solo imprimen, necesitamos modificarlos
            self.get_route_from_search()
        except Exception as e:
            print(f"Error: {e}")
    
    def get_route_from_search(self):
        """Obtiene la ruta ejecutando el algoritmo de forma controlada"""
        from collections import deque
        import heapq
        
        algo_map = {
            "BFS": "bfs",
            "DFS": "dfs",
            "UCS": "ucs",
            "Greedy Search": "gs",
            "A*": "a_star"
        }
        
        algo = algo_map[self.algorithm]
        
        if algo == "bfs":
            self.route = self.bfs_search()
        elif algo == "dfs":
            self.route = self.dfs_search()
        elif algo == "ucs":
            self.route = self.ucs_search()
        elif algo == "gs":
            self.route = self.gs_search()
        elif algo == "a_star":
            self.route = self.a_star_search()
    
    def bfs_search(self):
        from collections import deque
        queue = deque()
        initial_node = Node(*(self.city.start))
        queue.append(initial_node)
        visited = {initial_node.get_state()}
        
        while queue:
            node_to_expand = queue.popleft()
            self.nodes_expanded += 1
            
            if node_to_expand.get_state() == self.city.goal:
                return self.get_route(node_to_expand)
            
            if node_to_expand.get_position() in self.city.passengers:
                node_to_expand.passengers.add(node_to_expand.get_position())
            
            for direction in ["right", "left", "up", "down"]:
                movement = self.get_next_position(node_to_expand, direction)
                if movement and self.is_valid_move(movement):
                    node = Node(*movement)
                    node.parent = node_to_expand
                    node.passengers = set(node.parent.passengers)
                    node.operator = direction
                    if node.get_state() not in visited:
                        queue.append(node)
                        visited.add(node.get_state())
        
        return []
    
    def dfs_search(self):
        stack = []
        initial_node = Node(*(self.city.start))
        stack.append(initial_node)
        visited = {initial_node.get_state()}
        
        while stack:
            node_to_expand = stack.pop()
            self.nodes_expanded += 1
            
            if node_to_expand.get_state() == self.city.goal:
                return self.get_route(node_to_expand)
            
            if node_to_expand.get_position() in self.city.passengers:
                node_to_expand.passengers.add(node_to_expand.get_position())
            
            for direction in ["down", "up", "left", "right"]:  # Orden inversa para mantener BFS-like order
                movement = self.get_next_position(node_to_expand, direction)
                if movement and self.is_valid_move(movement):
                    node = Node(*movement)
                    node.parent = node_to_expand
                    node.passengers = set(node.parent.passengers)
                    node.operator = direction
                    if node.get_state() not in visited:
                        stack.append(node)
                        visited.add(node.get_state())
        
        return []
    
    def ucs_search(self):
        import heapq
        queue = []
        initial_node = Node(*(self.city.start))
        count_heapq = 0
        heapq.heappush(queue, (initial_node.accumulated_cost, count_heapq, initial_node))
        count_heapq += 1
        visited = {initial_node.get_state()}
        
        while queue:
            _, _, node_to_expand = heapq.heappop(queue)
            self.nodes_expanded += 1
            
            if node_to_expand.get_state() == self.city.goal:
                self.total_cost = node_to_expand.accumulated_cost
                return self.get_route(node_to_expand)
            
            if node_to_expand.get_position() in self.city.passengers:
                node_to_expand.passengers.add(node_to_expand.get_position())
            
            for direction in ["right", "left", "up", "down"]:
                movement = self.get_next_position(node_to_expand, direction)
                if movement and self.is_valid_move(movement):
                    node = Node(*movement)
                    node.parent = node_to_expand
                    node.passengers = set(node.parent.passengers)
                    node.operator = direction
                    node.accumulated_cost = node.parent.accumulated_cost
                    self.update_accumulated_cost(node)
                    if node.get_state() not in visited:
                        heapq.heappush(queue, (node.accumulated_cost, count_heapq, node))
                        count_heapq += 1
                        visited.add(node.get_state())
        
        return []
    
    def gs_search(self):
        import heapq
        queue = []
        initial_node = Node(*(self.city.start))
        count_heapq = 0
        heapq.heappush(queue, (0, count_heapq, initial_node))
        count_heapq += 1
        visited = {initial_node.get_state()}
        
        while queue:
            _, _, node_to_expand = heapq.heappop(queue)
            self.nodes_expanded += 1
            
            if node_to_expand.get_state() == self.city.goal:
                return self.get_route(node_to_expand)
            
            if node_to_expand.get_position() in self.city.passengers:
                node_to_expand.passengers.add(node_to_expand.get_position())
            
            for direction in ["right", "left", "up", "down"]:
                movement = self.get_next_position(node_to_expand, direction)
                if movement and self.is_valid_move(movement):
                    node = Node(*movement)
                    node.parent = node_to_expand
                    node.passengers = set(node.parent.passengers)
                    node.operator = direction
                    if node.get_state() not in visited:
                        h_value = self.heuristic(node)
                        heapq.heappush(queue, (h_value, count_heapq, node))
                        count_heapq += 1
                        visited.add(node.get_state())
        
        return []
    
    def a_star_search(self):
        import heapq
        queue = []
        initial_node = Node(*(self.city.start))
        count_heapq = 0
        heapq.heappush(queue, (0, count_heapq, initial_node))
        count_heapq += 1
        visited = {initial_node.get_state()}
        
        while queue:
            _, _, node_to_expand = heapq.heappop(queue)
            self.nodes_expanded += 1
            
            if node_to_expand.get_state() == self.city.goal:
                self.total_cost = node_to_expand.accumulated_cost
                return self.get_route(node_to_expand)
            
            if node_to_expand.get_position() in self.city.passengers:
                node_to_expand.passengers.add(node_to_expand.get_position())
            
            for direction in ["right", "left", "up", "down"]:
                movement = self.get_next_position(node_to_expand, direction)
                if movement and self.is_valid_move(movement):
                    node = Node(*movement)
                    node.parent = node_to_expand
                    node.passengers = set(node.parent.passengers)
                    node.operator = direction
                    node.accumulated_cost = node.parent.accumulated_cost
                    self.update_accumulated_cost(node)
                    if node.get_state() not in visited:
                        f_value = node.accumulated_cost + self.heuristic(node)
                        heapq.heappush(queue, (f_value, count_heapq, node))
                        count_heapq += 1
                        visited.add(node.get_state())
        
        return []
    
    def get_next_position(self, node, direction):
        match direction:
            case "right":
                return (node.row, node.column + 1)
            case "down":
                return (node.row + 1, node.column)
            case "left":
                return (node.row, node.column - 1)
            case "up":
                return (node.row - 1, node.column)
    
    def is_valid_move(self, pos):
        row, col = pos
        if row < 0 or row >= self.city.height or col < 0 or col >= self.city.width:
            return False
        return self.city.matrix[row][col] != '1'
    
    def update_accumulated_cost(self, node):
        if node.get_position() in self.city.high_flow:
            node.accumulated_cost += 7
        else:
            node.accumulated_cost += 1
    
    def heuristic(self, ref_node):
        node = ref_node.clone()
        goal_passengers = self.city.passengers
        _, _, passengers = node.get_state()
        heuristic_value = 0
        
        for passenger in goal_passengers:
            if passenger not in passengers:
                goal_row, goal_column = passenger
                heuristic_value += abs(node.row - goal_row) + abs(node.column - goal_column)
                node.row = goal_row
                node.column = goal_column
        
        heuristic_value += abs(node.row - self.city.goal_destination[0]) + abs(node.column - self.city.goal_destination[1])
        return heuristic_value
    
    def get_route(self, node):
        route = []
        while node.parent is not None:
            route.append(node.get_state())
            node = node.parent
        route.append(node.get_state())
        route.reverse()
        return route
    
    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if self.current_step < len(self.route) - 1:
                    self.current_step += 1
                    self.finished = self.current_step >= len(self.route) - 1
            elif event.key == pygame.K_r:
                self.__init__(self.width, self.height, self.algorithm, self.map_file)
    
    def draw(self, screen):
        screen.fill(WHITE)
        
        # Título
        title = pygame.font.Font(None, 36).render(f"Algoritmo: {self.algorithm}", True, BLACK)
        screen.blit(title, (self.map_x, 20))
        
        # Dibujar mapa
        self.draw_map(screen)
        
        # Información
        info_x = self.map_x + self.city.width * self.cell_size + 50
        self.draw_info(screen, info_x)
        
        # Instrucciones
        font_small = pygame.font.Font(None, 18)
        instructions = [
            "ESPACIO: Siguiente paso",
            "R: Reiniciar"
        ]
        for i, instruction in enumerate(instructions):
            text = font_small.render(instruction, True, DARK_GRAY)
            screen.blit(text, (self.map_x, self.height - 50 + i * 20))
    
    def draw_map(self, screen):
        font_cell = pygame.font.Font(None, max(16, self.cell_size // 2))
        
        for i in range(self.city.height):
            for j in range(self.city.width):
                x = self.map_x + j * self.cell_size
                y = self.map_y + i * self.cell_size
                rect = pygame.Rect(x, y, self.cell_size, self.cell_size)
                
                # Determinar color
                if (i, j) == self.city.goal_destination:
                    color = RED
                elif (i, j) == self.city.start:
                    color = GREEN
                elif self.city.matrix[i][j] == '1':
                    color = BLACK
                elif (i, j) in self.city.high_flow:
                    color = ORANGE
                elif (i, j) in self.city.passengers:
                    color = YELLOW
                else:
                    color = LIGHT_GRAY
                
                pygame.draw.rect(screen, color, rect)
                pygame.draw.rect(screen, GRAY, rect, 1)
                
                # Dibujar símbolos
                if (i, j) == self.city.goal_destination:
                    text = font_cell.render("X", True, WHITE)
                    text_rect = text.get_rect(center=(x + self.cell_size // 2, y + self.cell_size // 2))
                    screen.blit(text, text_rect)
                elif (i, j) == self.city.start:
                    text = font_cell.render("R", True, WHITE)
                    text_rect = text.get_rect(center=(x + self.cell_size // 2, y + self.cell_size // 2))
                    screen.blit(text, text_rect)
                elif (i, j) in self.city.passengers:
                    text = font_cell.render("P", True, BLACK)
                    text_rect = text.get_rect(center=(x + self.cell_size // 2, y + self.cell_size // 2))
                    screen.blit(text, text_rect)
        
        # Dibujar ruta visitada
        if self.current_step >= 0 and self.current_step < len(self.route):
            for step_idx in range(self.current_step + 1):
                state = self.route[step_idx]
                row, col = state[0], state[1]
                x = self.map_x + col * self.cell_size
                y = self.map_y + row * self.cell_size
                
                if step_idx == self.current_step:
                    # Posición actual del robot (azul)
                    pygame.draw.circle(screen, BLUE, 
                                     (x + self.cell_size // 2, y + self.cell_size // 2), 
                                     self.cell_size // 3)
                else:
                    # Camino visitado (gris claro)
                    pygame.draw.circle(screen, LIGHT_GRAY, 
                                     (x + self.cell_size // 2, y + self.cell_size // 2), 
                                     self.cell_size // 4)
    
    def draw_info(self, screen, x):
        font = pygame.font.Font(None, 24)
        info = [
            f"Paso: {max(0, self.current_step)} / {len(self.route) - 1}",
            f"Nodos expandidos: {self.nodes_expanded}",
            f"Costo total: {self.total_cost}",
            f"Pasajeros: {len(self.route[self.current_step][2]) if self.current_step < len(self.route) else 0}/{self.city.goal_passengers}",
        ]
        
        if self.finished:
            info.append("¡COMPLETADO!")
        
        y = 150
        for text in info:
            surface = font.render(text, True, BLACK)
            screen.blit(surface, (x, y))
            y += 40


class App:
    def __init__(self):
        pygame.init()
        self.screen_width = 1200
        self.screen_height = 700
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("RoboTaxi Search Visualizer")
        self.clock = pygame.time.Clock()
        self.running = True
        
        self.state = "algorithm"  # algorithm, map, visualization
        self.algorithm_screen = AlgorithmScreen(self.screen_width, self.screen_height)
        self.map_screen = None
        self.visualization_screen = None
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            
            if self.state == "algorithm":
                if self.algorithm_screen.handle_event(event):
                    self.state = "map"
                    self.map_screen = MapScreen(self.screen_width, self.screen_height)
            
            elif self.state == "map":
                if self.map_screen.handle_event(event):
                    self.state = "visualization"
                    self.visualization_screen = VisualizationScreen(
                        self.screen_width, 
                        self.screen_height,
                        self.algorithm_screen.selected_algorithm,
                        self.map_screen.selected_map
                    )
            
            elif self.state == "visualization":
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.state = "algorithm"
                        self.algorithm_screen = AlgorithmScreen(self.screen_width, self.screen_height)
                    else:
                        self.visualization_screen.handle_event(event)
    
    def draw(self):
        if self.state == "algorithm":
            self.algorithm_screen.draw(self.screen)
        elif self.state == "map":
            self.map_screen.draw(self.screen)
        elif self.state == "visualization":
            self.visualization_screen.draw(self.screen)
        
        pygame.display.flip()
    
    def run(self):
        while self.running:
            self.handle_events()
            self.draw()
            self.clock.tick(60)
        
        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    app = App()
    app.run()