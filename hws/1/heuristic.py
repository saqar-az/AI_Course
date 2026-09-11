from timeit import default_timer as timer
import heapq
import json

class Graph:
    def __init__(self):
        self.graph = {}

    def add_node(self,node):
        if node not in self.graph:
            self.graph[node] = []

    def add_edge(self,from_node,to_node,weight):
        if from_node not in self.graph:
            self.add_node(from_node)
        if to_node not in self.graph:
            self.add_node(to_node)
        self.graph[from_node].append((to_node,weight))

    def get_neighbors(self, node):
        return self.graph[node] if node in self.graph else []    


def heuristic(node):

    with open('data.json') as data:
        data = json.load(data)
        for x in data['heuristic_data']:
            if x['node']==node:
                return x['data']

class Search:

    def bfs(self, graph, start, goal):
     start_time = timer()
     queue = [start]
     explored_set = set()
     explored_nodes_num = 0
     path = {start: [start]}
     total_cost={start:0}

     while queue:
        current_city = queue.pop(0)
        if current_city in explored_set:
            continue

        explored_nodes_num += 1
        explored_set.add(current_city)

        if current_city == goal:
            return path[current_city], explored_nodes_num, timer() - start_time,total_cost[current_city]

        for neighbor, cost in graph.get_neighbors(current_city):
            if neighbor not in explored_set:
                queue.append(neighbor)
                path[neighbor] = path[current_city] + [neighbor]
                total_cost[neighbor]=total_cost[current_city]+cost       

     return "no path available", explored_nodes_num, timer() - start_time,0

    def dfs(self, graph, start, goal):
        start_time = timer()
        stack = [start]
        path = {start: [start]}
        total_cost={start:0}
        explored_set = set()
        explored_nodes_num = 0
        
        while stack:
            current_city = stack.pop()
            if current_city in explored_set:
                continue

            explored_nodes_num += 1
            explored_set.add(current_city)

            if current_city == goal:
                return path[current_city], explored_nodes_num, timer() - start_time,total_cost[current_city]

            for neighbor, cost in graph.get_neighbors(current_city):
                if neighbor not in explored_set:
                    stack.append(neighbor)
                    path[neighbor] = path[current_city] + [neighbor]
                    total_cost[neighbor]=total_cost[current_city]+cost
                         
        return "no path available", explored_nodes_num, timer() - start_time,0
    
    def dls(self, graph, start, goal,depth):
        current_depth=0
        start_time = timer()
        stack = [start]
        path = {start: [start]}
        total_cost={start:0}
        explored_set = set()
        explored_nodes_num = 0

        while stack:
            current_city = stack.pop()
            if current_city in explored_set:
                continue

            if current_depth > depth:
                print("Cutoff failure")
                break
          
            explored_set.add(current_city)
            explored_nodes_num += 1

            if current_city == goal and current_depth<=depth:
                return path[current_city], explored_nodes_num, timer() - start_time,total_cost[current_city]

            for neighbor, cost in graph.get_neighbors(current_city):
                if neighbor not in explored_set:
                    stack.append(neighbor)
                    path[neighbor] = path[current_city] + [neighbor]
                    current_depth+=1
                    total_cost[neighbor]=total_cost[current_city]+cost
        
        return "no path available", explored_nodes_num, timer() - start_time,0

    def greedy(self, graph, start, goal):
     start_time = timer()
     priority_queue = [(0, start)]
     path = {start: [start]}
     total_cost={start:0}
     explored_set = set()
     explored_nodes_num = 0
     
     while priority_queue:
        index, current_city = heapq.heappop(priority_queue)

        if current_city in explored_set:
            continue
            
        explored_set.add(current_city)
        explored_nodes_num += 1

        if current_city == goal:
            return path[current_city], explored_nodes_num, timer() - start_time,total_cost[current_city]
        
        for neighbor, cost in graph.get_neighbors(current_city):
            if neighbor not in explored_set:
                heapq.heappush(priority_queue, (heuristic(neighbor), neighbor))
                path[neighbor] = path[current_city] + [neighbor]
                total_cost[neighbor]=total_cost[current_city]+cost

     return "no path available", explored_nodes_num, timer() - start_time,0
    
    def a(self, graph, start, goal):
     start_time = timer()
     priority_queue = [(0, start)]
     path = {start: [start]}
     total_cost={start:0}
     explored_set = set()
     explored_nodes_num = 0
     
     while priority_queue:
        index, current_city = heapq.heappop(priority_queue)

        if current_city in explored_set:
            continue
            
        explored_set.add(current_city)
        explored_nodes_num += 1

        if current_city == goal:
            return path[current_city], explored_nodes_num, timer() - start_time,total_cost[current_city]
        
        for neighbor, cost in graph.get_neighbors(current_city):
            if neighbor not in explored_set:
                heapq.heappush(priority_queue, (heuristic(neighbor)+cost, neighbor))
                path[neighbor] = path[current_city] + [neighbor]
                total_cost[neighbor]=total_cost[current_city]+cost

     return "no path available", explored_nodes_num, timer() - start_time,0

    def ucs(self, graph, start, goal):
     start_time = timer()
     priority_queue = [(0, start)]
     path = {start: [start]}
     total_cost = {start: 0}
     explored_set = set()
     explored_nodes_num = 0
     
     while priority_queue:
        index, current_city = heapq.heappop(priority_queue)

        if current_city in explored_set:
            continue
            
        explored_set.add(current_city)
        explored_nodes_num += 1

        if current_city == goal:
            return path[current_city], explored_nodes_num, timer() - start_time, total_cost[current_city]

        for neighbor, cost in graph.get_neighbors(current_city):
            if neighbor not in explored_set:
                    total_cost[neighbor]=total_cost[current_city]+cost
                    heapq.heappush(priority_queue, (total_cost[neighbor], neighbor))
                    path[neighbor] = path[current_city] + [neighbor]
       
     return "no path available", explored_nodes_num, timer() - start_time,0    
       
def main():   

    g = Graph()

    with open('data.json') as data:
        data = json.load(data)
        for edge in data['edges']:
            g.add_edge(edge['from'], edge['to'], edge['weight'])


    while(True):
        start = input("Enter the start :").capitalize()
        goal = input("Enter the destination :").capitalize()
        algorithm = input("Choose the search algorithm : BFS or DFS or UCS or DLS or A* or GREEDY or 0 to exit: ").lower()
           
        search=Search()

        match algorithm:
            case "bfs":
                path,explored_nodes_num,time,cost=search.bfs(g,start,goal)
            case "dfs":
                path,explored_nodes_num,time,cost=search.dfs(g,start,goal)
            case "dls":
                depth=int(input("Your chosen depth: "))    
                path,explored_nodes_num,time,cost=search.dls(g, start, goal,depth)
            case "greedy":
                path,explored_nodes_num,time,cost=search.greedy(g,start,goal) 
            case "a*":
                path,explored_nodes_num,time,cost=search.a(g, start, goal)
            case "ucs":
                path,explored_nodes_num,time,cost=search.ucs(g,start,goal)
            case "0" :
                exit(0)

        print("path: ",path,"\nnumber of visited vertices: ",explored_nodes_num,"\ntime: ",time,"\ncost: ",cost)       

if __name__ == "__main__":
    main()