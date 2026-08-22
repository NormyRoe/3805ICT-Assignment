"""
test_problem_3.py
Pytest file for testing the Assignment's Problem 3.
"""

from src.problem_3 import perform_sax


###############################################################################################
# Test Function: test_case_1_paa_fail_both
# Description:
# Tests what happens when neither the Authorized Voice nor the Test Voice series 
# can be equally split up.
#
# Input:    N/A
# Output:   N/A
###############################################################################################
def test_case_1_paa_fail_both():

    # Print what is being tested
    print("Test Case 1: PAA fails both\n")

    # Create authorized voice and test voice time series
    voice_authorized = [1, 2, 3]
    voice_test = [5, 6, 7]

    # Perform SAX
    perform_sax(voice_authorized, voice_test)
    
    # Print an empty line
    print("\n")

    # Print a separator line
    print("=" * 80)

    # Print an empty line
    print("\n")



###############################################################################################
# Test Function: test_case_2_paa_fail_authorized
# Description:
# Tests what happens when the Authorized Voice cannot be equally split up.
#
# Input:    N/A
# Output:   N/A
###############################################################################################
def test_case_2_paa_fail_authorized():

    # Print what is being tested
    print("Test Case 2: PAA fails for Authorized\n")

    # Create authorized voice and test voice time series
    voice_authorized = [1, 2, 3]
    voice_test = [10, 20, 30, 40, 50, 60]

    # Perform SAX
    perform_sax(voice_authorized, voice_test)

    # Print an empty line
    print("\n")

    # Print a separator line
    print("=" * 80)

    # Print an empty line
    print("\n")



###############################################################################################
# Test Function: test_case_3_paa_fail_test
# Description:
# Tests what happens when the Test Voice cannot be equally split up.
#
# Input:    N/A
# Output:   N/A
###############################################################################################
def test_case_3_paa_fail_test():

    # Print what is being tested
    print("Test Case 3: PAA fails for Test\n")

    # Create authorized voice and test voice time series
    voice_authorized = [10, 20, 30, 40, 50, 60]
    voice_test = [1, 2, 3]

    # Perform SAX
    perform_sax(voice_authorized, voice_test)

    # Print an empty line
    print("\n")

    # Print a separator line
    print("=" * 80)

    # Print an empty line
    print("\n")



###############################################################################################
# Test Function: test_case_4_score_under_75
# Description:
# Tests what happens when the Test Voice similarity score is under 75%
#
# Input:    N/A
# Output:   N/A
###############################################################################################
def test_case_4_score_under_75():

    # Print what is being tested
    print("Test Case 4: Similarity Score under 75%\n")

    # Create authorized voice and test voice time series
    voice_authorized = [10, 20, 30, 40, 50]
    voice_test = [10, 11, 12, 13, 14]

    # Perform SAX
    perform_sax(voice_authorized, voice_test)

    # Print an empty line
    print("\n")

    # Print a separator line
    print("=" * 80)

    # Print an empty line
    print("\n")



###############################################################################################
# Test Function: test_case_5_score_over_75
# Description:
# Tests what happens when the Test Voice similarity score is over 75%
#
# Input:    N/A
# Output:   N/A
###############################################################################################
def test_case_5_score_over_75():

    # Print what is being tested
    print("Test Case 5: Similarity Score over 75%\n")

    # Create authorized voice and test voice time series
    voice_authorized = [10, 20, 30, 40, 50]
    voice_test = [10, 20, 40, 41, 42]

    # Perform SAX
    perform_sax(voice_authorized, voice_test)

    # Print an empty line
    print("\n")

    # Print a separator line
    print("=" * 80)

    # Print an empty line
    print("\n")



###############################################################################################
# Test Function: test_case_6_score_equals_75
# Description:
# Tests what happens when the Test Voice similarity score equals 75%
#
# Input:    N/A
# Output:   N/A
###############################################################################################
def test_case_6_score_equals_75():

    # Print what is being tested
    print("Test Case 6: Similarity Score equals 75%\n")

    # Create authorized voice and test voice time series
    voice_authorized = [10, 20, 30, 40]
    voice_test = [10, 20, 29, 31]

    # Perform SAX
    perform_sax(voice_authorized, voice_test)

    # Print an empty line
    print("\n")

    # Print a separator line
    print("=" * 80)

    # Print an empty line
    print("\n")



###############################################################################################
# Test Function: test_case_7_medium_inputs
# Description:
# Tests what happens when the Authorized Voice and the Test Voice series are medium sized
#
# Input:    N/A
# Output:   N/A
###############################################################################################
def test_case_7_medium_inputs():

    # Print what is being tested
    print("Test Case 7: Authorized Voice and Test Voice inputs are medium sized\n")

    # Create authorized voice and test voice time series
    voice_authorized = list(range(500, 900))
    voice_test = list(range(550, 950))

    # Perform SAX
    perform_sax(voice_authorized, voice_test)

    # Print an empty line
    print("\n")

    # Print a separator line
    print("=" * 80)

    # Print an empty line
    print("\n")



###############################################################################################
# Test Function: test_case_8_large_inputs
# Description:
# Tests what happens when the Authorized Voice and the Test Voice series are large
#
# Input:    N/A
# Output:   N/A
###############################################################################################
def test_case_8_large_inputs():

    # Print what is being tested
    print("Test Case 8: Authorized Voice and Test Voice inputs are large\n")

    # Create authorized voice and test voice time series
    voice_authorized = list(range(1000, 2500))
    voice_test = list(range(1505, 3005))

    # Perform SAX
    perform_sax(voice_authorized, voice_test)

    # Print an empty line
    print("\n")

    # Print a separator line
    print("=" * 80)

    # Print an empty line
    print("\n")




if __name__ == "__main__":
    test_case_1_paa_fail_both()
    test_case_2_paa_fail_authorized()
    test_case_3_paa_fail_test()
    test_case_4_score_under_75()
    test_case_5_score_over_75()
    test_case_6_score_equals_75()
    test_case_7_medium_inputs()
    test_case_8_large_inputs()