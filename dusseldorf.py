import heapq
import math
import time
import tracemalloc
from typing import Dict, List, Tuple

coords = {
    'Uni_Klinikum': (51.1882, 6.7902),
    'Marien_Hospital': (51.2674, 6.7701),
    'Evangelisches_KH': (51.2088, 6.7795),
    'Krankenhaus_Elbroich': (51.1447, 6.8651),
    'Sana_Benrath': (51.1653, 6.8669),
    
    'Hauptbahnhof': (51.2205, 6.7928),
    'Altstadt_Rathaus': (51.2255, 6.7715),
    'Medienhafen': (51.2131, 6.7641),
    'Flughafen_DUS': (51.2809, 6.7572),
    'Benrath_Schloss': (51.1616, 6.8715),
}

class DusseldorfGraph:
    
    def __init__(self):
        self.edges: Dict[str, List[Tuple[str, float]]] = {}
        self.coords: Dict[str, Tuple[float, float]] = {}
        self.hospitals: Dict[str, Tuple[float, float]] = {}
    
    def add_node(self, node_id: str, lat: float, lon: float, is_hospital: bool = False):
        if node_id not in self.edges:
            self.edges[node_id] = []
        self.coords[node_id] = (lat, lon)
        if is_hospital:
            self.hospitals[node_id] = (lat, lon)
    
    def add_edge(self, u: str, v: str, weight: float):
        self.edges.setdefault(u, []).append((v, weight))
        self.edges.setdefault(v, []).append((u, weight))
    
    def neighbors(self, node: str) -> List[Tuple[str, float]]:
        return self.edges.get(node, [])
    
    def get_coords(self, node: str) -> Tuple[float, float]:
        return self.coords.get(node, (0, 0))
    
    def find_nearest_hospital(self, start: str) -> Tuple[str, float]:
        start_coords = self.get_coords(start)
        nearest = None
        min_dist = float('inf')
        
        for hospital, hosp_coords in self.hospitals.items():
            dist = math.hypot(
                start_coords[0] - hosp_coords[0],
                start_coords[1] - hosp_coords[1]
            )
            if dist < min_dist:
                min_dist = dist
                nearest = hospital
        
        return nearest, min_dist


def dijkstra(graph: DusseldorfGraph, start: str, target: str) -> Tuple[float, List[str], float, float]:
    tracemalloc.start()
    start_time = time.time()
    
    pq = [(0, start)]
    distances = {start: 0}
    previous = {start: None}
    visited = set()
    nodes_explored = 0
    
    while pq:
        current_dist, current = heapq.heappop(pq)
        
        if current in visited:
            continue
        visited.add(current)
        nodes_explored += 1
        
        if current == target:
            break
        
        for neighbor, weight in graph.neighbors(current):
            new_dist = current_dist + weight
            if neighbor not in distances or new_dist < distances[neighbor]:
                distances[neighbor] = new_dist
                previous[neighbor] = current
                heapq.heappush(pq, (new_dist, neighbor))
    
    path = []
    node = target
    while node is not None:
        path.append(node)
        node = previous.get(node)
    path.reverse()
    
    end_time = time.time()
    current_mem, peak_mem = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    
    return (distances.get(target, float('inf')), path, 
            (end_time - start_time) * 1000, peak_mem / 1024, nodes_explored)


def a_star(graph: DusseldorfGraph, start: str, target: str) -> Tuple[float, List[str], float, float, int]:
    tracemalloc.start()
    start_time = time.time()
    
    def heuristic(node: str) -> float:
        lat1, lon1 = graph.get_coords(node)
        lat2, lon2 = graph.get_coords(target)
        lat_dist = (lat1 - lat2) * 111
        lon_dist = (lon1 - lon2) * 85
        return math.hypot(lat_dist, lon_dist)
    
    open_set = []
    heapq.heappush(open_set, (0, start))
    
    came_from = {}
    g_score = {start: 0}
    f_score = {start: heuristic(start)}
    
    visited = set()
    nodes_explored = 0
    
    while open_set:
        _, current = heapq.heappop(open_set)
        
        if current in visited:
            continue
        visited.add(current)
        nodes_explored += 1
        
        if current == target:
            break
        
        for neighbor, weight in graph.neighbors(current):
            tentative_g = g_score[current] + weight
            if neighbor not in g_score or tentative_g < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g
                f_score[neighbor] = tentative_g + heuristic(neighbor)
                heapq.heappush(open_set, (f_score[neighbor], neighbor))
    
    path = []
    node = target
    while node in came_from:
        path.append(node)
        node = came_from[node]
    path.append(start)
    path.reverse()
    
    end_time = time.time()
    current_mem, peak_mem = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    
    return (g_score.get(target, float('inf')), path, 
            (end_time - start_time) * 1000, peak_mem / 1024, nodes_explored)

def build_duesseldorf_graph() -> DusseldorfGraph:
    g = DusseldorfGraph()
    
    nodes = {
        'Uni_Klinikum': (51.1882, 6.7902),
        'Marien_Hospital': (51.2674, 6.7701),
        'Evangelisches_KH': (51.2088, 6.7795),
        'Elbroich_KH': (51.1447, 6.8651),
        'Sana_Benrath': (51.1653, 6.8669),
        
        'Hbf': (51.2205, 6.7928),
        'Altstadt': (51.2255, 6.7715),
        'Medienhafen': (51.2131, 6.7641),
        'Flughafen': (51.2809, 6.7572),
        'Benrath': (51.1616, 6.8715),
        'Oberkassel': (51.2333, 6.7600),
        'Bilk': (51.1950, 6.7820),
        'Eller': (51.1816, 6.8285),
        
        'Kennedydamm': (51.2350, 6.7800),
        'Corneliusstr': (51.2110, 6.7750),
        'Ko_Bogen': (51.2260, 6.7800),
    }
    
    for node_id, (lat, lon) in nodes.items():
        is_hospital = node_id in ['Uni_Klinikum', 'Marien_Hospital', 'Evangelisches_KH', 
                                   'Elbroich_KH', 'Sana_Benrath']
        g.add_node(node_id, lat, lon, is_hospital)
    
    edges = [
        ('Hbf', 'Bilk', 2.5),
        ('Hbf', 'Ko_Bogen', 2.0),
        ('Hbf', 'Corneliusstr', 1.2),
        ('Hbf', 'Uni_Klinikum', 1.8),
        
        ('Altstadt', 'Ko_Bogen', 0.8),
        ('Altstadt', 'Oberkassel', 1.2),
        ('Altstadt', 'Medienhafen', 1.5),
        
        ('Ko_Bogen', 'Kennedydamm', 1.0),
        ('Kennedydamm', 'Marien_Hospital', 2.0),
        ('Marien_Hospital', 'Flughafen', 4.5),
        
        ('Bilk', 'Uni_Klinikum', 1.0),
        ('Bilk', 'Eller', 3.5),
        ('Eller', 'Elbroich_KH', 2.0),
        ('Eller', 'Sana_Benrath', 3.0),
        ('Elbroich_KH', 'Sana_Benrath', 1.8),
        ('Sana_Benrath', 'Benrath', 0.5),
        
        ('Uni_Klinikum', 'Medienhafen', 2.2),
        ('Uni_Klinikum', 'Evangelisches_KH', 1.5),
        ('Evangelisches_KH', 'Corneliusstr', 0.6),
        ('Evangelisches_KH', 'Medienhafen', 1.0),
    ]
    
    for u, v, w in edges:
        g.add_edge(u, v, w)
    
    return g

def evaluate_duesseldorf():
    g = build_duesseldorf_graph()
    
    scenarios = [
        {'name': 'Scenario 1: Hbf to Nearest Hospital', 'start': 'Hbf'},
        {'name': 'Scenario 2: Airport to Nearest Hospital', 'start': 'Flughafen'},
        {'name': 'Scenario 3: Medienhafen to Nearest Hospital', 'start': 'Medienhafen'},
        {'name': 'Scenario 4: Benrath to Nearest Hospital', 'start': 'Benrath'},
        {'name': 'Scenario 5: Altstadt to Marien Hospital', 'start': 'Altstadt', 'target': 'Marien_Hospital'},
    ]
    
    results = []
    
    for scenario in scenarios:
        start = scenario['start']
        
        if 'target' in scenario:
            target = scenario['target']
            print("================")
            print(f"{scenario['name']}")
            print("================")
            
            dist_d, path_d, time_d, mem_d, nodes_d = dijkstra(g, start, target)
            print(f"\n[Dijkstra]")
            print(f"  Distance: {dist_d:.2f} km")
            print(f"  Path: {' → '.join(path_d)}")
            print(f"  Time: {time_d:.2f} ms")
            print(f"  Memory: {mem_d:.2f} KB")
            print(f"  Nodes Explored: {nodes_d}")
            
            dist_a, path_a, time_a, mem_a, nodes_a = a_star(g, start, target)
            print(f"\n[A*]")
            print(f"  Distance: {dist_a:.2f} km")
            print(f"  Path: {' → '.join(path_a)}")
            print(f"  Time: {time_a:.2f} ms")
            print(f"  Memory: {mem_a:.2f} KB")
            print(f"  Nodes Explored: {nodes_a}")
            
            if abs(dist_d - dist_a) < 0.01:
                print(f"\nValidation: Both algorithms found the same optimal path")
            else:
                print(f"\nWarning: Distance mismatch - Dijkstra: {dist_d}, A*: {dist_a}")
            
        else:
            print("================")
            print(f"{scenario['name']}")
            print("================")
            
            nearest_hospital, _ = g.find_nearest_hospital(start)
            print(f"\nNearest hospital by straight-line: {nearest_hospital}")
            
            dist_d, path_d, time_d, mem_d, nodes_d = dijkstra(g, start, nearest_hospital)
            print(f"\n[Dijkstra] to {nearest_hospital}")
            print(f"  distance: {dist_d:.2f} km")
            print(f"  path: {' → '.join(path_d)}")
            print(f"  time: {time_d:.2f} ms")
            print(f"  memory: {mem_d:.2f} KB")
            print(f"  nodes explored: {nodes_d}")
            
            dist_a, path_a, time_a, mem_a, nodes_a = a_star(g, start, nearest_hospital)
            print(f"\n[A*] to {nearest_hospital}")
            print(f"  distance: {dist_a:.2f} km")
            print(f"  path: {' → '.join(path_a)}")
            print(f"  time: {time_a:.2f} ms")
            print(f"  memory: {mem_a:.2f} KB")
            print(f"  nodes explored: {nodes_a}")
        
        results.append({
            'scenario': scenario['name'],
            'dijkstra_time': time_d,
            'dijkstra_memory': mem_d,
            'dijkstra_nodes': nodes_d,
            'a_star_time': time_a,
            'a_star_memory': mem_a,
            'a_star_nodes': nodes_a,
        })
    
    print("================")
    print("Comparison")
    print("================")
    print(f"{'Scenario':<35} {'Dijkstra (ms)':<15} {'A* (ms)':<15} {'Speedup':<10}")
    print("-" * 75)
    
    for r in results:
        speedup = r['dijkstra_time'] / r['a_star_time'] if r['a_star_time'] > 0 else 1
        print(f"{r['scenario']:<35} {r['dijkstra_time']:<15.2f} {r['a_star_time']:<15.2f} {speedup:.2f}x")
    
    return results

if __name__ == "__main__":
    evaluate_duesseldorf()
