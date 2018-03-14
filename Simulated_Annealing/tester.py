

def get_value(self):
    """Calculate the total length of the closed-circuit path of the current
    state by summing the distance between every pair of adjacent cities.  Since
    the default simulated annealing algorithm seeks to maximize the objective
    function, return -1x the path length. (Multiplying by -1 makes the smallest
    path the smallest negative number, which is the maximum value.)
    
    Returns
    -------
    float
        A floating point value with the total cost of the path given by visiting
        the cities in the order according to the self.cities list
    
    Notes
    -----
        (1) Remember to include the edge from the last city back to the
        first city
        
        (2) Remember to multiply the path length by -1 so that simulated
        annealing finds the shortest path
    """
    import math
    dist_sum = 0
    max_len = len(self.cities)
    curr_idx = 0
    while curr_idx < max_len:
        city1 = self.cities[curr_idx][1]
        for i in range(curr_idx, max_len):
            city2 = self.cities[i][1]
            euc_dist = math.sqrt((city1[0] + city2[0])**2 + (city1[1] + city2[1])**2)
            dist_sum += euc_dist
        curr_idx+=1
    return dist_sum