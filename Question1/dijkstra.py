import csv
import heapq
from collections import defaultdict

def build_graph(filename):
    graph = defaultdict(list)
    
    with open(filename, 'r') as f:
        reader = csv.DictReader(f)
        
        for row in reader:
            origin = row['Origin']
            dest = row['Destination']
            dist = int(row['Distance'])
            
            graph[origin].append((dest, dist))
            graph[dest].append((origin,dist))
        
    return graph

def dijkstra(graph, source):
    pq = [(0, source)]
    distances = {city: float('inf') for city in graph}
    distances[source] = 0
    while pq:
        current_distance, current_city = heapq.heappop(pq)
        
        if current_distance > distances[current_city]:
            continue
        
        for neighbor, weight in graph[current_city]:
            distance = current_distance + weight
            
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                heapq.heappush(pq, (distance, neighbor))
    return distances

def main():
    graph = build_graph("Question1/indian-cities-dataset.csv")
    source_city = input("Enter the source city: ")
    distances = dijkstra(graph, source_city)
    
    print(f"Shortest distances from {source_city}:")
    for city, dist in distances.items():
        print(f"{city}: {dist} km")
        
if __name__ == "__main__":
    main()