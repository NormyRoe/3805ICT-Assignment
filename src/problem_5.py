
###############################################################################################
# Imports
#
###############################################################################################
import math
import time
import tracemalloc


###############################################################################################
# Function: find_pivot
# Description:
# Identifies the point with the lowest y-coordinate
# If there is a tie-breaker, identifies the point with the lowest x-coordinate
#
# Input:    array       An array of co-ordinates
# Output:   tuple       The co-ordinate to be used as the pivot
###############################################################################################
def find_pivot(coordinates):
    """
    Return the pivot

    The pivot is the co-ordinate which has the lowest y-coordinate.  
    If there are multiple with the lowest y-coordinate, then selects the one which also has 
    the lowest x-coordinate.

    """
    # Find the point with the lowest y-coordinate, and in case of ties, the lowest x-coordinate
    pivot = min(coordinates, key=lambda c: (c[1], c[0]))

    return pivot


###############################################################################################
# Function: polar_angle
# Description:
# Calculates the polar angle from one coordinate to a second coordinate.
#
# Input:    integer     The first co-ordinate
#           integer     The second co-ordinate
# Output:   integer     The polar angle between the two co-ordinates
###############################################################################################
def polar_angle(coordinate_1, coordinate_2):
    """
    Return the polar angle (in radians) between coordinate_1 and coordinate_2 relative to the x-axis

    """
    # Calculate the angle
    angle = math.atan2(coordinate_2[1] - coordinate_1[1], coordinate_2[0] - coordinate_1[0])

    # Return the angle
    return angle


###############################################################################################
# Function: calculate_distance
# Description:
# Calculates the squared Euclidean distance between two co-ordinates
#
# Input:    integer     The first co-ordinate
#           integer     The second co-ordinate
# Output:   integer     The squared Euclidean distance between the two co-ordinates
###############################################################################################
def calculate_distance(coordinate_1, coordinate_2):
    """
    Return the squared Euclidean distance between coordinate_1 and coordinate_2

    """
    # Calculate the distance
    distance = (coordinate_2[0] - coordinate_1[0])**2 + (coordinate_2[1] - coordinate_1[1])**2

    # Return the distance
    return distance


###############################################################################################
# Function: sort_coordinates
# Description:
# Sort the coordinates by polar angle, if there is a tie, then use the distance from the pivot
#
# Input:    array       An array of co-ordinates
#           tuple       The pivot co-ordinate
# Output:   array       The sorted array of co-ordinates (excluding the pivot)
###############################################################################################
def sort_coordinates(coordinates, pivot):
    """
    Return an array of sorted co-ordinates, excluding the pivot.

    This function:
        - Sorts the co-ordinates by polar angle from the pivot
        - If there is a tie, then uses the distance from the pivot to determine the sorted order

    """
    # Initalise a new array for the co-ordinates
    pivot_less_coordinates = []

    # For loop through the co-ordinates
    for c in coordinates:

        # If c is not the pivot
        if c != pivot:

            # Add to pivot_less_coordinates
            pivot_less_coordinates.append(c)

    # Sort co-ordinates by polar angle from the pivot with a tie-breaker rule using distance from the pivot
    sorted_coordinates = sorted(pivot_less_coordinates, key=lambda c: (polar_angle(pivot, c), calculate_distance(pivot, c)))

    # Return the sorted co-ordinates
    return sorted_coordinates


###############################################################################################
# Function: cross_product
# Description:
# Compute the cross product of vectors OA and OB to determine the orientation
#
# Input:    tuple       Co-ordinate tuple 1
#           tuple       Co-ordinate tuple 2
#           tuple       Co-ordinate tuple 3
# Output:   integer     The cross-product result
###############################################################################################
def cross_product(coordinate_1, coordinate_2, coordinate_3):
    """
    Return cross product result.

    This function:
        - Computes the cross product of vectors OA and OB to determine the orientation

    """
    # Compute the cross product of vectors Co-ordinates 1,2 and Co-ordindates 1,3 to determine the orientation
    # Cross product > 0 means a left turn, < 0 means right turn, and = 0 means collinear
    cross_prod = (coordinate_2[0] - coordinate_1[0]) * (coordinate_3[1] - coordinate_1[1]) - \
                    (coordinate_2[1] - coordinate_1[1]) * (coordinate_3[0] - coordinate_1[0])

    # Return the cross product
    return cross_prod


###############################################################################################
# Function: left_most_coordinate
# Description:
# Find the left-most co-ordinate
#
# Input:    array       An array of co-ordinates
# Output:   tuple       The left-most co-ordinate
###############################################################################################
def left_most_coordinate(coordinates):
    """
    Return the left-most co-ordinate

    """
    # Calculate the left-most co-ordinate
    left_most = min(coordinates, key=lambda p: p[0])

    # Return left_most
    return left_most


###############################################################################################
# Function: graham_scan
# Description:
# Compute the convex hull of a set of 2D points using Graham's Scan algorithm
#
# Input:    array       An array of co-ordinates
# Output:   array       The resulting convex hull (list of co-ordinates)
###############################################################################################
def graham_scan(coordinates):
    """
    Compute the convex hull of a set of 2D points using Graham's Scan algorithm

    """

    # Step 1: Find the pivot co-ordindate
    pivot = find_pivot(coordinates)

    # Step 2: Sort co-ordinates by polar angle with respect to the pivot (with tie-breaker by distance)
    sorted_coordinates = sort_coordinates(coordinates, pivot)

    # Step 3: Initialize the convex hull with the pivot co-ordinate
    convex_hull = [pivot]

    # Step 4: Build the Boundary

    # For loop through the sorted co-ordinates array
    for c in sorted_coordinates:

        # While convex_hull has 2 or more co-ordinates in it
        while len(convex_hull) >= 2:

            # Ensure that the last two co-ordindates in convex_hull and c make a left turn            
            # Get the last two coordinates
            coordinate_1 = convex_hull[-2]
            coordinate_2 = convex_hull[-1]

            # Check the cross_product result
            # Cross product to check orientation:
            # For co-ordinates 1, 2, 3, compute (2-1) x (3-1)
            result = cross_product(coordinate_1, coordinate_2, c)

            # If the angle between the last two coordinates and the current coordinate is a right turn
            if result <= 0:

                # Pop the convex_hull
                convex_hull.pop()

            # Else it is a left turn
            else:

                # Break out of the while loop
                break

        # Add the current co-ordindate to the convex_hull
        convex_hull.append(c)

    # Return the completed convex hull
    return convex_hull


###############################################################################################
# Function: jarvic_march
# Description:
# Compute the convex hull of a set of 2D points using Jarvis March algorithm
#
# Input:    array       An array of co-ordinates
# Output:   array       The resulting convex hull (list of co-ordinates)
###############################################################################################
def jarvis_march(coordinates):
    """
    Compute the convex hull of a set of 2D points using Jarvis March algorithm

    """

    # Step 1: Calculate the leftmost point 
    pivot = left_most_coordinate(coordinates)

    # Step 2: Initialize the convex hull
    convex_hull = []

    # Step 3: Build the Boundary

    # Set the pivot as the current_coordindate
    current_coordinate = pivot

    # While True loop
    while True:

        # Append the current_coordinate to convex_hull
        convex_hull.append(current_coordinate)

        # Set the next_coordinate as the first coordinate in the array
        next_coordinate = coordinates[0]

        # For loop through the coordinates
        for c in coordinates:

            # If c equals current_coordinate
            if c == current_coordinate:

                # Continue with the loop
                continue

            # If next_coordinate equals current_coordinate
            if next_coordinate == current_coordinate:

                # Set next_coordinate as c
                next_coordinate = c

                # Continue with the loop
                continue

            # Get the cross product result
            result = cross_product(current_coordinate, next_coordinate, c)

            # Check if the next point is the farthest counterclockwise point
            if result > 0:

                # Set next_coordinate as c
                next_coordinate = c

            # Else if result equals 0, need collinearity handling
            elif result == 0:

                # If the distance between the current_coordinate and c is greater than 
                # the distance between the current_coordinate and the next_coordinate
                if calculate_distance(current_coordinate, c) > calculate_distance(current_coordinate, next_coordinate):

                    # Set next_coordinate as c
                    next_coordinate = c

        # Update current_coordinate as the current next_coordinate
        current_coordinate = next_coordinate

        # If the current_coordinate is the same as the pivot
        if current_coordinate == pivot:

            # Break out of the while loop
            break

    # Return the completed convex hull
    return convex_hull


###############################################################################################
# Function: perimeter_length
# Description:
# Computes the length of the perimeter
#
# Input:    array       The convex hull
# Output:   integer     The perimeter length
###############################################################################################
def perimeter_length(convex_hull):
    """
    Compute the length of the perimeter

    """
    # Initialise a total variable
    total = 0

    # For loop through the convex_hull
    for i in range(len(convex_hull)):

        # Grab the x-axis and y-axis values for co-ordinate i.
        x_axis_1, y_axis_1 = convex_hull[i]

        # Grab the x-axis and y-axis values for the next co-ordinate.
        # If i is the last co-ordinate in the list, 
        # then the next one is the first co-ordinate in the list.
        x_axis_2, y_axis_2 = convex_hull[(i + 1) % len(convex_hull)]

        # Calculate the distance between the two co-ordinates and add it to total
        total += math.dist((x_axis_1, y_axis_1), (x_axis_2, y_axis_2))

    # Return the total distance
    return total


###############################################################################################
# Function: print_ascii_map
# Description:
# Prints an ASCII representation of the coordinates and the convex hull boundary
#
# Input:    array       The list of coordinates
#           array       The convex hull
# Output:   N/A
###############################################################################################
def print_ascii_map(coordinates, convex_hull):
    """
    Print an ASCII representation of the coordinate map with the convex hull boundary marked.
    """

    # Step 1: Determine the minimum x-axis value from the coordinates
    min_x = min(c[0] for c in coordinates)

    # Step 2: Determine the maximum x-axis value from the coordinates
    max_x = max(c[0] for c in coordinates)

    # Step 3: Determine the minimum y-axis value from the coordinates
    min_y = min(c[1] for c in coordinates)

    # Step 4: Determine the maximum y-axis value from the coordinates
    max_y = max(c[1] for c in coordinates)

    # Step 5: Create an empty grid using '.' for each cell
    # The number of rows is based on the y-axis range
    # The number of columns is based on the x-axis range
    grid = []
    for _ in range(max_y - min_y + 1):

        # Append a new row filled with '.' characters
        grid.append(["."] * (max_x - min_x + 1))

    # Step 6: Mark all coordinates with '*'
    for (x, y) in coordinates:

        # Convert the coordinate into grid row/column positions
        # Row is inverted because ASCII prints top-to-bottom
        row = max_y - y
        col = x - min_x

        # Mark the coordinate with '*'
        grid[row][col] = "*"

    # Step 7: Mark all convex hull points with '#'
    for (x, y) in convex_hull:

        # Convert the coordinate into grid row/column positions
        row = max_y - y
        col = x - min_x

        # Mark the hull vertex with '#'
        grid[row][col] = "#"

    # Step 8: Draw approximate hull edges using '+'
    for i in range(len(convex_hull)):

        # Get the current hull vertex
        x1, y1 = convex_hull[i]

        # Get the next hull vertex (wrap around using modulo)
        x2, y2 = convex_hull[(i + 1) % len(convex_hull)]

        # Calculate the difference in x-axis values
        dx = x2 - x1

        # Calculate the difference in y-axis values
        dy = y2 - y1

        # Determine how many steps are needed to draw the line
        steps = max(abs(dx), abs(dy))

        # If the two points are identical, skip drawing
        if steps == 0:
            continue

        # Calculate how much x changes per step
        x_inc = dx / steps

        # Calculate how much y changes per step
        y_inc = dy / steps

        # Start drawing from the first hull vertex
        x = x1
        y = y1

        # For loop through each step to draw the line
        for _ in range(steps):

            # Convert the current floating-point position into grid coordinates
            row = max_y - int(round(y))
            col = int(round(x)) - min_x

            # Only draw '+' if the cell is still empty
            if grid[row][col] == ".":

                # Mark the hull edge with '+'
                grid[row][col] = "+"

            # Move to the next position along the line
            x += x_inc
            y += y_inc

    # Step 9: Print the completed grid
    for row in grid:

        # Join each row into a single string separated by spaces
        print(" ".join(row))


###############################################################################################
# Function: print_info
# Description:
# Prints the supplied information for the supplied algorithm
#
# Input:    string      Which algorithm was used
#           stack       The completed convex_hull stack
#           float       The time it took for the algorithm to run
#           float       The peak memory usage for the algorithm
#           array       The list of coordinates
# Output:   N/A
###############################################################################################
def print_info(algorithm, convex_hull, time, memory, coordinates):
    """
    Print the supplied information for the supplied algorithm.

    This function:
        - Prints which algorithm was used
        - Prints how long it took the algorithm to run
        - Prints how much memory the algorithm used
        - Prints the length of the fence perimeter
        - Prints the Fence Perimeter vertices
        - Prints an ASCII map showing the convex hull boundary
        
    """
    # Print the algorithm's name
    print(f'\nConvex Hull using the {algorithm} algorithm:\n')

    # Print the algorithm's time
    print(f"Time {algorithm} took: {time:.4f} ms ")
    
    # Print the algorithm's memory usage
    print(f"{algorithm} had a peak memory usage of: {memory} bytes")

    # If convex_hull does not form a polygon
    if len(convex_hull) < 3:

        # Print a message
        print("Error: No valid convex hull (polygon) can be created using these co-ordinates.")

        # Return out of the function
        return

    # Else convex_hull contains co-ordinates
    else:

        # Calculate the Perimeter Fence Length
        length = perimeter_length(convex_hull)

        # Print the Perimeter Fence Length
        print(f'Perimeter Fence Length: {length:.2f} units')

        # Print the Perimeter Fence Vertices order
        print("Perimeter Fence Vertices: ")

        print(convex_hull)

        # Visual representation of the coordinates with the boundary marked
        print("Coordinate map with convex hull boundary marked: ")

        print_ascii_map(coordinates, convex_hull)


###############################################################################################
# Function: run_algorithms
# Description:
# Runs both Graham's Scan and Jarvis March algorithms on the supplied co-ordinates
#
# Input:    series      The authorised voice time series
#           series      The test voice time series
# Output:   N/A
###############################################################################################
def run_algorithms(coordinates):
    """
    Runs both Graham's Scan and Jarvis March algorithms against the supplied coordinates.

    This function:
        - Prints the supplied coordinates
        - Tracks the performance timing for each algorithm
        - Tracks the memory allocation for each algorithm
        - Prints out the information for each algorithm       
   
    """
    # Print the co-ordinates
    print("Co-ordinates: ")

    print(coordinates)

    # Start a timer
    grahams_start_time = time.perf_counter()
    
    # Start memory allocation tracing
    tracemalloc.start()

    # Perform Graham's Scan
    grahams_hull = graham_scan(coordinates)

    # End the timer
    grahams_end_time = time.perf_counter()
    
    # Get the current and peak memory allocation
    grahams_memory_current, grahams_memory_peak = tracemalloc.get_traced_memory()
    
    # Stop memory allocation tracing
    tracemalloc.stop()

    # Calculate the length of time it took in milliseconds
    grahams_total_time = (grahams_end_time - grahams_start_time) * 1000

    # Print the information for Graham's Scan
    print_info("Graham's Scan", grahams_hull, grahams_total_time, grahams_memory_peak, coordinates)

    # Start a timer
    jarvis_start_time = time.perf_counter()
        
    # Start memory allocation tracing
    tracemalloc.start()
    
    # Perform Graham's Scan
    jarvis_hull = jarvis_march(coordinates)
    
    # End the timer
    jarvis_end_time = time.perf_counter()
        
    # Get the current and peak memory allocation
    jarvis_memory_current, jarvis_memory_peak = tracemalloc.get_traced_memory()
        
    # Stop memory allocation tracing
    tracemalloc.stop()
    
    # Calculate the length of time it took in milliseconds
    jarvis_total_time = (jarvis_end_time - jarvis_start_time) * 1000
    
    # Print the information for Jarvis March
    print_info("Jarvis March", jarvis_hull, jarvis_total_time, jarvis_memory_peak, coordinates)



###############################################################################################
# Function: problem_5
# Description:
# Entry Point for running Problem 5
# 
#
# Input:    N/A
# Output:   N/A
###############################################################################################
def problem_5():
    """
    Entry point for Problem 5.

    The function:
        - Creates co-ordinates to run the algorithms on
        - Calls the run_algorithms function with the co-ordinates    

    """

    print("Program started.\n")

    # Create Co-ordinates
    coordinates = [(3, 4), (5, 2), (1, 1), (8, 5), (7, 9), (2, 6), (4, 7), (9, 3), (6, 1), (0, 3)]

    # Run the algorithms
    run_algorithms(coordinates)

    


if __name__ == "__main__":
    problem_5()