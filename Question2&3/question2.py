import streamlit as st
import numpy as np
import heapq
import time
import matplotlib.pyplot as plt

GRID_SIZE = 70

def generate_grid(density):
    grid = np.zeros((GRID_SIZE, GRID_SIZE))
    
    if density == 'Low':
        prob = 0.1
    elif density == 'Medium':
        prob = 0.2
    else:
        prob = 0.3
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            if np.random.rand() < prob:
                grid[i][j] = 1
                
    return grid

def astar(grid, start, goal):
    start_time = time.time()
    
    rows, cols = grid.shape
    open_set = []
    heapq.heappush(open_set, (0, start))
    
    came_from = {}
    g_score = {start: 0}
    
    nodes_explored = 0
    
    while open_set:
        _, current = heapq.heappop(open_set)
        nodes_explored += 1
        
        if current == goal:
            break
        x, y = current
        
        neighbors = [
            (x+1, y),
            (x-1, y),
            (x, y+1),
            (x, y-1)
        ]
        
        for nx, ny in neighbors:
            if 0 <= nx < rows and 0 <= ny < cols and grid[nx][ny] == 0:

                tentative = g_score[current] + 1

                if (nx,ny) not in g_score or tentative < g_score[(nx,ny)]:
                    g_score[(nx,ny)] = tentative

                    h = abs(nx-goal[0]) + abs(ny-goal[1])
                    f = tentative + h

                    heapq.heappush(open_set,(f,(nx,ny)))
                    came_from[(nx,ny)] = current
    path = []
    node = goal
    while node in came_from:
        path.append(node)
        node = came_from[node]
        
    path.append(start)
    path.reverse()
    end_time = time.time()
    return path, nodes_explored, end_time - start_time

def plot_grapH(grid, path, start, goal):
    fig, ax = plt.subplots()

    ax.imshow(grid, cmap="gray_r")

    if path:
        xs = [p[1] for p in path]
        ys = [p[0] for p in path]
        ax.plot(xs, ys)

    ax.scatter(start[1], start[0], marker="o")
    ax.scatter(goal[1], goal[0], marker="x")

    return fig

st.title("UGV Battlefield Path Planning")

density = st.selectbox("Obstacle Density",["Low","Medium","High"])

start_x = st.number_input("Start X",0,69,0)
start_y = st.number_input("Start Y",0,69,0)

goal_x = st.number_input("Goal X",0,69,60)
goal_y = st.number_input("Goal Y",0,69,60)

if st.button("Generate Battlefield & Find Path"):

    grid = generate_grid(density)

    start = (start_x,start_y)
    goal = (goal_x,goal_y)

    grid[start] = 0
    grid[goal] = 0

    path, explored, runtime = astar(grid,start,goal)

    fig = plot_grapH(grid,path,start,goal)

    st.pyplot(fig)

    st.subheader("Measures of Effectiveness")

    st.write("Path Length:",len(path))
    st.write("Nodes Explored:",explored)
    st.write("Computation Time:",runtime,"seconds")