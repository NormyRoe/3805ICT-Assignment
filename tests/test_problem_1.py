"""
test_problem_1.py
Pytest file for testing the Assignment's Problem 1.
"""

from src.problem_1 import RoadNetwork, run_algorithm

###############################################################################################
# Function: build_network
# Description:
# Builds the road network for the test cases to use
#
# Input:    N/A
# Output:   Network     The built Road Network
###############################################################################################
def build_network():

    # Create Road Network
    network = RoadNetwork()

    # Create intersections
    network.add_intersection("Buffy Avenue")
    network.add_intersection("Angel Road")
    network.add_intersection("Charmed Drive")
    network.add_intersection("Supernatural Circuit")
    network.add_intersection("Xena Road")
    network.add_intersection("Hercules Avenue")

    # Create directional roads
    network.add_road("Buffy Avenue", "Angel Road", 5)
    network.add_road("Buffy Avenue", "Supernatural Circuit", 10)
    network.add_road("Angel Road", "Charmed Drive", 5)
    network.add_road("Angel Road", "Xena Road", 10)
    network.add_road("Charmed Drive", "Hercules Avenue", 5)
    network.add_road("Charmed Drive", "Xena Road", 10)
    network.add_road("Supernatural Circuit", "Angel Road", 5)
    network.add_road("Supernatural Circuit", "Charmed Drive", 10)
    network.add_road("Xena Road", "Buffy Avenue", 5)
    network.add_road("Xena Road", "Hercules Avenue", 10)
    network.add_road("Hercules Avenue", "Charmed Drive", 5)
    network.add_road("Hercules Avenue", "Supernatural Circuit", 15)

    # Return the created network
    return network

###############################################################################################
# Test Function: test_case_1_nonexistent
# Description:
# Tests with a nonexistent intersection
#
# Input:    N/A
# Output:   N/A
###############################################################################################
def test_case_1_nonexistent():

    # Build the Road Network
    network = build_network()

    # Print what is being tested
    print("Test Case 1: Non-Existent Intersection\n")

    # Run Dijkstra's Algorithm for a specified intersection
    run_algorithm(network, "Harry Street")

    # Print an empty line
    print("\n")

###############################################################################################
# Test Function: test_case_2_first
# Description:
# Tests with the first intersection that was added
#
# Input:    N/A
# Output:   N/A
###############################################################################################
def test_case_2_first():

    # Build the Road Network
    network = build_network()

    # Print what is being tested
    print("Test Case 2: First Intersection Created\n")

    # Run Dijkstra's Algorithm for the specified intersection
    run_algorithm(network, "Buffy Avenue")

    # Print an empty line
    print("\n")


###############################################################################################
# Test Function: test_case_3_other
# Description:
# Tests with a different intersection
#
# Input:    N/A
# Output:   N/A
###############################################################################################
def test_case_3_other():

    # Build the Road Network
    network = build_network()

    # Print what is being tested
    print("Test Case 3: Other Intersection Created\n")

    # Run Dijkstra's Algorithm for a specified intersection
    run_algorithm(network, "Charmed Drive")

    # Print an empty line
    print("\n")


###############################################################################################
# Test Function: test_case_4_unreachable
# Description:
# Tests with a network that contains an intersection that can't be reached
#
# Input:    N/A
# Output:   N/A
###############################################################################################
def test_case_4_unreachable():

    # Build the Road Network
    network = build_network()

    # Add a new intersection
    network.add_intersection("Arrow Lane")

    # Print what is being tested
    print("Test Case 4: Network has Intersection which can't be reached\n")

    # Run Dijkstra's Algorithm for the specified intersection
    run_algorithm(network, "Buffy Avenue")

    # Print an empty line
    print("\n")


###############################################################################################
# Test Function: test_case_5_one_way
# Description:
# Tests with an intersection that only has one road coming in to it, and none going out.
#
# Input:    N/A
# Output:   N/A
###############################################################################################
def test_case_5_one_way():

    # Build the Road Network
    network = build_network()

    # Add a new intersection
    network.add_intersection("Flash Street")

    # Print what is being tested
    print("Test Case 5: Testing from an Intersection which has no outgoing road\n")

    # Create directional road
    network.add_road("Hercules Avenue", "Flash Street", 5)

    # Run Dijkstra's Algorithm for the new intersection
    run_algorithm(network, "Flash Street")

    # Print an empty line
    print("\n")


###############################################################################################
# Test Function: test_case_6_large
# Description:
# Tests with larger network
#
# Input:    N/A
# Output:   N/A
###############################################################################################
def test_case_6_large():

    # Build the Road Network
    network = build_network()

    # Add new intersections
    network.add_intersection("Flash Street")
    network.add_intersection("Arrow Lane")
    network.add_intersection("SuperGirl Street")
    network.add_intersection("Swamp Lane")

    # Create directional roads
    network.add_road("Hercules Avenue", "Flash Street", 5)
    network.add_road("Flash Street", "Arrow Lane", 5)
    network.add_road("Arrow Lane", "Hercules Avenue", 5)
    network.add_road("Arrow Lane", "Supernatural Circuit", 10)
    network.add_road("Charmed Drive", "SuperGirl Street", 4)
    network.add_road("SuperGirl Street", "Angel Road", 4)
    network.add_road("SuperGirl Street", "Hercules Avenue", 4)
    network.add_road("Xena Road", "Swamp Lane", 4)
    network.add_road("Swamp Lane", "Charmed Drive", 4)
    network.add_road("Swamp Lane", "Hercules Avenue", 4)

    # Add an additional 2500 intersections and directional roads in a chain
    for i in range(1, 2501):

        # Name the intersection
        name = f'Intersection {i}'

        # Create the new intersection
        network.add_intersection(name)

        # If the number is 1
        if i == 1:

            # Create the directional road from Flash Street
            network.add_road("Flash Street", name, 5)

        # Else
        else:

            # Create the directional road from the previous one
            network.add_road(f'Intersection {i-1}', name, 5)

        # For every third intersection
        if i % 3 == 0:

            # Add two more directional roads
            network.add_road(name, f'Intersection {i-1}', 5)
            network.add_road(name, f'Intersection {i-2}', 5)
            network.add_road(f'Intersection {i-2}', name, 8)

    # Print what is being tested
    print("Test Case 6: Large Road Network\n")

    # Run Dijkstra's Algorithm for the specified intersection
    run_algorithm(network, "Flash Street")

    # Print an empty line
    print("\n")


if __name__ == "__main__":
    test_case_1_nonexistent()
    test_case_2_first()
    test_case_3_other()
    test_case_4_unreachable()
    test_case_5_one_way()
    test_case_6_large()