
###############################################################################################
# Imports
#
###############################################################################################
import time
import tracemalloc


###############################################################################################
# Function: normalize
# Description:
# Performs z-score normalization on a series of voice numbers
#
# Input:    series      A series of voice numbers
# Output:   series      A normalized version of the series
###############################################################################################
def normalize(series):
    """
    Performs z-score normalization on a series of voice numbers

    The function:

        - Compute the mean
        - Compute the standard deviation
        - Uses the mean and standard deviation to normalize each value

    Normalization ensures the data has mean 0 and standard deviation 1, which is required 
    before applying the SAX transformation.

    """
    # Step 1: Compute the mean

    # Calculate the mean
    mean = sum(series) / len(series)

    # Step 2: Compute the standard deviation

    # Step 2-1: Compute differences from the mean
    # Create a differences list
    differences = []

    # For loop through the series
    for s in series:

        # Calculate the difference by subtracting the mean from the value
        diff = s - mean

        # Append the difference to the differences list
        differences.append(diff)

    # Step 2-2: Square the differences
    # Create a squared differences list
    differences_squared = []

    # For loop through the differences list
    for d in differences:

        # Calculate the squared difference by squaring the difference
        diff_sqr = d * d

        # Append the squared difference to the squared differences list
        differences_squared.append(diff_sqr)

    # Step 2-3: Compute the variance
    # Calculate the variance
    variance = sum(differences_squared) / len(series)

    # Step 2-4: Compute the standard deviation
    # Calculate the standard deviation
    std = variance ** 0.5

    # Step 3: Normalization - Update each value by subtracting the mean and then dividing by the standard deviation

    # Initialise a normalized series list
    series_normalized = []

    # For loop through the series
    for s in series:

        # Caculate it's new value and round to two decimals
        new_value = round((s - mean) / std, 2)

        # Append the new value to the normalized series list
        series_normalized.append(new_value)

    # Return the normalized series
    return series_normalized



###############################################################################################
# Function: sax_transformation
# Description:
# Converts PAA segment means into a SAX letter string.
#
# Input:    series      A list of PAA segment means (already normalized)
# Output:   string      A string of SAX letters representing the series
###############################################################################################
def sax_transformation(series):
    """
    Converts PAA segment means into a SAX letter string.

    The function:

        - Maps each PAA mean to a letter ('a'-'e') based on SAX breakpoints.
        - Combines all letters into a single string.

    Symbolic Aggregate approXimation (SAX) converts normalized numeric values into symbols
    using breakpoints that divide the Gaussian distribution into equal-sized regions.

    SAX operates on the PAA representation, not the raw or normalized series.

    """

    # Create a list to hold the letters
    list_letters = []

    # For loop through the series
    for s in series:

        # If the value is less than -0.67
        if s < -0.67:

            # Add 'a' to the list of letters
            list_letters.append('a')

        # else if the value is between -0.67 and -0.22
        elif s >= -0.67 and s < -0.22:

            # Add 'b' to the list of letters
            list_letters.append('b')


        # else if the value is between -0.22 and 0.22
        elif s >= -0.22 and s < 0.22:
        
            # Add 'c' to the list of letters
            list_letters.append('c')

        # else if the value is between 0.22 and 0.67
        elif s >= 0.22 and s < 0.67:
                
            # Add 'd' to the list of letters
            list_letters.append('d')

        # Else it is greater than 0.67
        else:

            # Add 'e' to the list of letters
            list_letters.append('e')

    # Combine the letters in to a string
    letters = ''.join(list_letters)

    # Return the letters
    return letters


###############################################################################################
# Function: paa
# Description:
# Breaks a normalized time series into equal-sized segments and 
# computes the mean of each segment.
#
# Input:    series      A normalized series of voice frequency values
# Output:   list        A list of PAA segment means
###############################################################################################
def paa(series, size = 100):
    """
    Computes the Piecewise Aggregate Approximation (PAA) of a normalized time series.

    This function:
        - Divides the normalized series into equal-sized segments.
        - Computes the mean of each segment.
        - Returns a list of segment means.

    PAA reduces the dimensionality of the normalized series and prepares it for SAX conversion.

    """
    # Initialise the segment size
    segment_size = size

    # Initialise a segment array
    segments = []

    # Initialise a paa values array
    paa_values = []

    # Check if the size is too low
    if segment_size < 3:
    
        # Return None
        return None

    # Determine if the series can be split into equal length segments
    if len(series) % segment_size == 0 and len(series) != segment_size:

        # Split the series up based on the segment size
        segments = [series[i:i + segment_size] for i in range(0, len(series), segment_size)]

        # For loop through the segments
        for seg in segments:
        
            # Calculate the segment mean
            seg_mean = round(sum(seg) / len(seg), 2)
        
            # Append the mean to paa values
            paa_values.append(seg_mean)
        
        # Return the paa values
        return paa_values

    # Else it can't be split equally
    else:

        # If the size of the series is the same as the segment size
        if len(series) == segment_size:

            # Recursively call the function trying the size minus 1
            return paa(series, size = segment_size - 1)

        # Else If the segment_size is over 50
        elif segment_size > 50:

            # Recursively call the function trying the size minus 10
            return paa(series, size = segment_size - 10)

        # Else if the segment size is greater than 20 and less than or equal to 50
        elif segment_size > 20 and segment_size <= 50:

            # Recursively call the function trying the size minus 10
            return paa(series, size = segment_size - 5)
        
        # Else the segment_size is 20 or under
        else:

            # Recursively call the function trying the size minus 1
            return paa(series, size = segment_size - 1)


###############################################################################################
# Function: lcs
# Description:
# Returns the Longest Common Subsequence between s1 and s2
#
# Input:    string      The first string of letters to compare
#           string      The second string of letters to compare
# Output:   string      The longest common subsequence
#
# Notes:    Uses dynamic programming to compute the LCS table and then 
#           reconstructs the subsequence.
###############################################################################################
def lcs(s1, s2):
    """
    Computes the Longest Common Subsequence (LCS) between two SAX strings.

    The function:
        - Builds a dynamic programming (DP) table storing LCS lengths.
        - Walks backwards through the DP table to reconstruct the actual subsequence.
        - Returns the LCS as a string.

    LCS is used to measure similarity between two SAX patterns.

    """

    # Store the lengths of both strings
    n = len(s1)
    m = len(s2)

    # Create a DP table filled with zeros
    dp = [[0] * (m + 1) for _ in range(n + 1)]

    # Fill the DP table
    # For loop through s1
    for i in range(1, n + 1):

        # For loop through s2
        for j in range(1, m + 1):

            # If the characters match
            if s1[i - 1] == s2[j - 1]:

                # Extend the subsequence
                dp[i][j] = dp[i - 1][j - 1] + 1

            # Else
            else:

                # Best is max of ignoring one char from either string 
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])

    # Reconstruct the subsequence
    # Create an array to hold the letters
    lcs_letters = []

    # Walk backwards through the DP table
    # While n and m are greater than zero
    while n > 0 and m > 0:

        # If the characters match
        if s1[n - 1] == s2[m - 1]:

            # Append the character to the lcs letters array
            lcs_letters.append(s1[n - 1])

            # Decrease n and m
            n -= 1
            m -= 1

        # Else move in the direction of the larger DP value

        # Else if the DP value above is larger, move upward 
        # (skip a character from s1)
        elif dp[n - 1][m] >= dp[n][m - 1]:

            # Decrease n by 1 to move up
            n -= 1

        # Else move to the left (skip a character from s2)
        else:

            # Decrease m by 1 to move left
            m -= 1

    # Reverse the collected letters to get the correct LCS subsequence order
    lcs_letters.reverse()

    # Create the LCS string
    lcs_string = ''.join(lcs_letters)

    # Return the LCS string
    return lcs_string



###############################################################################################
# Function: similarity_classify
# Description:
# Calculates and Classifies the similarity score for the Test Voice
# This is used to determine whether the Test Voice is matched to the Authorized Voice.
#
# Input:    string      The Test Voice pattern
#           string      The LCS string
# Output:   N/A
#
###############################################################################################
def similarity_classify(sax_test, lcs_string):
    """
    Calculates and Classifies the similarity score for the Test Voice.
    This is used to determine whether the Test Voice is a match to the Authorized Voice.

    The function:
        - Calculates the similarity score for the Test Voice.
        - Determines whether the Test Voice is matched to the Authorized Voice.   

    """

    # Create variables for the length of the provided strings
    length_test = len(sax_test)
    length_lcs = len(lcs_string)

    # Calculate the similarity score rounded to two decimals
    score_sim = round(length_lcs / length_test, 2)

    # Calculate the similarity percentage
    score_percent = score_sim * 100

    # Print step 5
    print("\nStep 5 - Calculate Similarity Score:\n")

    # Print the similarity score
    print("Similarity Score:")
    print(f'{length_lcs}/{length_test} = {score_sim} ({score_percent}%)')


    # Print step 6
    print("\nStep 6 - Matching Result:\n")

    # Print the similarity score
    print("Match Result:")
    # Classify the Similarity Score
    # If the percentage is 75 or higher
    if score_percent >= 75:

        # Print match message
        print("Test Voice is a MATCH for the Authorized Voice")

    # Else percentage is lower than 75
    else:

        # Print no match message
        print("Test Voice is NOT A MATCH for the Authorized Voice")


###############################################################################################
# Function: perform_sax
# Description:
# Performs Symbolic Aggregate approXimation (SAX) to compare two voice time series
#
# Input:    series      The authorised voice time series
#           series      The test voice time series
# Output:   N/A
###############################################################################################
def perform_sax(authorized, test):
    """
    Performs Symbolic Aggregate approXimation (SAX) to compare two voice time series

    This function:
        - Performs z-score normalization on each series of voice numbers
        - Computes the Piecewise Aggregate Approximation (PAA) of each normalized time series.
        - Transforms each PAA series into a SAX letter string.
   

    """
    # Print the input voice series
    print("Input:\n")
    print("Authorized Voice Series:")
    print(authorized)
    print("Test Voice Series:")
    print(test)

    # Start a timer
    start_time = time.perf_counter()
    
    # Start memory allocation tracing
    tracemalloc.start()

    # Normalize the authorized voice time series
    normalized_authorized = normalize(authorized)

    # Normalize the test voice time series
    normalized_test = normalize(test)

    # Print the process and step 1
    print("\nProcess:\n")
    print("Step 1 - Normalize voice series:\n")

    # Print the normalized voice series
    print("Authorized Voice Normalized:")
    print(normalized_authorized)
    print("Test Voice Normalized:")
    print(normalized_test)

    # Compute PAA for the authorized voice time series
    paa_authorized = paa(normalized_authorized)

    # Compute PAA for the test voice time series
    paa_test = paa(normalized_test)

    # Print step 2
    print("\nStep 2 - Compute PAA:\n")

    # Check the scenarios
    # If both paa variables are None
    if paa_authorized is None and paa_test is None:

        # Print error message
        print("Error: Neither series can be split into equal segments")

    # Else if paa_authorized is None
    elif paa_authorized is None:

        # Print error message
        print("Error: Authorized series cannot be split into equal segments")

    # Else if paa_test is None
    elif paa_test is None:

        # Print error message
        print("Error: Test series cannot be split into equal segments")

    # Else both series have been successfully split
    else:

        # Print the PAA series
        print("Authorized Voice PAA:")
        print(paa_authorized)
        print("Test Voice PAA:")
        print(paa_test)

        # Perform SAX conversion on the Authorized PAA
        sax_authorized = sax_transformation(paa_authorized)

        # Perform SAX conversion on the Test PAA
        sax_test = sax_transformation(paa_test)

        # Print step 3
        print("\nStep 3 - SAX Conversion:\n")

        # Print the SAX patterns
        print("Authorized Voice Pattern:")
        print(sax_authorized)
        print("Test Voice Pattern:")
        print(sax_test)

        # Caculate LCS
        lcs_string = lcs(sax_authorized, sax_test)

        # Print step 4
        print("\nStep 4 - Calculate LCS:\n")

        # Print the LCS string
        print("LCS:")
        print(f'{lcs_string} ({len(lcs_string)} characters match)')

        # Calculate similarity and matching
        similarity_classify(sax_test, lcs_string)

    # End the timer
    end_time = time.perf_counter()
    
    # Get the current and peak memory allocation
    memory_current, memory_peak = tracemalloc.get_traced_memory()
    
    # Stop memory allocation tracing
    tracemalloc.stop()

    # Calculate the length of time it took in milliseconds
    total_time = (end_time - start_time) * 1000

    # Print the time and memory stats
    print(f'\nTotal time: {total_time:.4f} ms')
    print(f'Total memory: {memory_peak} bytes')



###############################################################################################
# Function: problem_3
# Description:
# Entry Point for running Problem 3
# 
#
# Input:    N/A
# Output:   N/A
###############################################################################################
def problem_3():
    """
    Entry point for Problem 3.

    The function:
        - Creates an Authorized Voice time series
        - Creates a Test Voice time series
        - Performs Symbolic Aggregate approXimation (SAX)

    SAX is used to transform a time series into a symbolic representation.  
    This representation is then used with Longest Common Subsequence to compare SAX patterns 
    and determine whether they match.
    
    """
    print("Program started.\n")

    # Create authorized voice and test voice time series
    voice_authorized = [135.3, 138.1, 140.5, 143.0, 146.0, 148.8, 151.0, 153.4, 155.6, 158.0]
    voice_test = [133.2, 137.5, 141.2, 144.0, 146.3, 149.5, 151.2, 153.3, 155.7, 157.5]

    # Perform SAX
    perform_sax(voice_authorized, voice_test)





if __name__ == "__main__":
    problem_3()