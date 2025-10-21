import numpy as np

# Distance matrix between cities
d = np.array([[0, 10, 12, 11, 14],
              [10, 0, 13, 15, 8],
              [12, 13, 0, 9, 14],
              [11, 15, 9, 0, 16],
              [14, 8, 14, 16, 0]])

iteration = 100
n_ants = 5
n_citys = 5

# Parameters
e = 0.5         # Evaporation rate
alpha = 1       # Pheromone importance
beta = 2        # Visibility importance

# Visibility matrix: inverse of distance
visibility = 1 / (d + np.eye(n_citys))  # avoid division by zero
visibility[d == 0] = 0

# Pheromone matrix: initialized uniformly
pheromone = 0.1 * np.ones((n_citys, n_citys))

# Ant routes: each ant has a path of n_citys + 1 (return to start)
rute = np.ones((n_ants, n_citys + 1), dtype=int)

for ite in range(iteration):
    rute[:, 0] = 1  # all ants start at city 1

    for i in range(n_ants):
        visited = set([1])
        for j in range(1, n_citys):
            cur_loc = rute[i, j - 1] - 1
            probs = np.zeros(n_citys)

            for k in range(n_citys):
                if (k + 1) not in visited:
                    probs[k] = (pheromone[cur_loc, k] ** alpha) * (visibility[cur_loc, k] ** beta)

            probs_sum = np.sum(probs)
            if probs_sum == 0:
                next_city = np.random.choice(list(set(range(1, n_citys + 1)) - visited))
            else:
                probs /= probs_sum
                cum_prob = np.cumsum(probs)
                r = np.random.rand()
                next_city = np.where(cum_prob >= r)[0][0] + 1

            rute[i, j] = next_city
            visited.add(next_city)

        rute[i, -1] = 1  # return to start

    # Calculate tour distances
    dist_cost = np.zeros(n_ants)
    for i in range(n_ants):
        s = 0
        for j in range(n_citys):
            s += d[rute[i, j] - 1, rute[i, j + 1] - 1]
        dist_cost[i] = s

    # Find best route
    dist_min_loc = np.argmin(dist_cost)
    dist_min_cost = dist_cost[dist_min_loc]
    best_route = rute[dist_min_loc, :]

    # Pheromone evaporation
    pheromone *= (1 - e)

    # Pheromone update
    for i in range(n_ants):
        for j in range(n_citys):
            from_city = rute[i, j] - 1
            to_city = rute[i, j + 1] - 1
            pheromone[from_city, to_city] += 1.0 / dist_cost[i]

print("Routes of all ants:")
print(rute)
print("\nBest path:", best_route)
print("Cost of the best path:", int(dist_min_cost))
