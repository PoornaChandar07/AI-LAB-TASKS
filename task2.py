import random
import copy

# Calculate total path cost
def calculate_cost(graph, path):
    cost = 0
    for i in range(len(path) - 1):
        cost += graph[path[i]][path[i + 1]]
    cost += graph[path[-1]][path[0]]  # Return to start
    return cost

# Generate neighbors by swapping two cities
def get_neighbors(path):
    neighbors = []
    for i in range(1, len(path)):
        for j in range(i + 1, len(path)):
            neighbor = path.copy()
            neighbor[i], neighbor[j] = neighbor[j], neighbor[i]
            neighbors.append(neighbor)
    return neighbors

# Hill Climbing Algorithm
def hill_climbing_tsp(graph):
    V = len(graph)
    current_path = list(range(V))  # Initial path: [0, 1, 2, ..., V-1]
    random.shuffle(current_path)   # Randomize the initial path
    current_cost = calculate_cost(graph, current_path)

    while True:
        neighbors = get_neighbors(current_path)
        next_path = current_path
        next_cost = current_cost

        for neighbor in neighbors:
            cost = calculate_cost(graph, neighbor)
            if cost < next_cost:
                next_path = neighbor
                next_cost = cost

        # If no better neighbor, stop (local minimum)
        if next_cost >= current_cost:
            break

        current_path = next_path
        current_cost = next_cost

    return current_path, current_cost

# Example usage
if __name__ == "__main__":
    graph = [[0, 10, 15, 20],
             [10, 0, 35, 25],
             [15, 35, 0, 30],
             [20, 25, 30, 0]]
    
    best_path, best_cost = hill_climbing_tsp(graph)
    print("Best path found:", best_path)
    print("Cost of path:", best_cost)
