import difflib
import re
from collections import Counter
import time

def injection_found(segmentsA, segmentsB):
    """Simulates an injection detection by comparing two segment lists.
    Returns True if an 'X' segment in segmentsA aligns with an 'A' segment in segmentsB,
    indicating a potential 'injection' of discrepancies."""
    i, j = 0, 0  # indices for iterating through segmentsA and segmentsB
    while i < len(segmentsA) and j < len(segmentsB):
        A = segmentsA[i]
        B = segmentsB[j]
        # Check segment types and decide to advance in list or detect an injection
        if A[0] == 'A' and B[0] == 'A':
            i += 1
            j += 1
        elif A[0] == 'A' and B[0] == 'X':
            i += 1
            j += 1
        elif A[0] == 'X' and B[0] == 'A':
            return True  # Injection detected
        elif A[0] == 'X' and B[0] == 'X':
            i += 1
            j += 1
    return False

def split_string(string1, string2):
    """Splits the first string into two parts based on the length of the second string.
    Returns a list of two segments."""
    x = len(string2)
    return [string1[:x], string1[x:]]

def last_char_indices(segments):
    """Calculates indices of the last character for each segment in the segment list.
    Returns a list of these indices."""
    indices = []
    cumulative_length = 0
    for segment in segments:
        cumulative_length += len(segment)
        indices.append(cumulative_length - 1) 
    return indices

def merge_and_maximize_elements(array1, array2):
    """Combines two lists and keeps the maximum count of each unique element.
    Returns a new list with maximized elements."""
    counter1, counter2 = Counter(array1), Counter(array2)
    merged_result = []
    for key in set(counter1.keys()).union(counter2.keys()):
        max_count = max(counter1.get(key, 0), counter2.get(key, 0))
        merged_result.extend([key] * max_count)
    return merged_result

def balance_and_correct_segments(segmentsA, segmentsB):
    """Balances and adjusts discrepancies between two segment lists to facilitate further analysis.
    Adjusts the segment lengths to match each other and corrects empty segments."""
    max_index = len(merge_and_maximize_elements(last_char_indices(segmentsA), last_char_indices(segmentsB)))
    for i in range(max_index):
        # Correct segment mismatches by splitting and adjusting based on length differences
        if i == len(segmentsA) or len(segmentsB[i]) > len(segmentsA[i]):
            split_segments = split_string(segmentsB[i], segmentsA[i])
            segmentsB = segmentsB[:i] + split_segments + segmentsB[i+1:]
            if len(segmentsA[i]) == 0:
                segmentsA[i], segmentsB[i] = 'X', 'A'
        elif i == len(segmentsB) or len(segmentsB[i]) < len(segmentsA[i]):
            split_segments = split_string(segmentsA[i], segmentsB[i])
            segmentsA = segmentsA[:i] + split_segments + segmentsA[i+1:]
            if len(segmentsB[i]) == 0:
                segmentsB[i], segmentsA[i] = 'X', 'A'
        elif len(segmentsA[i]) == 0 and len(segmentsB[i]) == 0:
            segmentsA[i], segmentsB[i] = 'X', 'X'
    return segmentsA, segmentsB

def highlight_string_differences(string1, string2):
    """Highlights differences between two strings using difflib.
    Compares string1 with string2 and string1 with string3 to extract difference segments."""
    matcher12 = difflib.SequenceMatcher(None, string1, string2)
    
    segment_list1 = []
    # Create segments from diff operations
    for operation12, start112, end112, start212, end212 in matcher12.get_opcodes():
        if operation12 == 'replace' or operation12 == 'delete':
            segment_list1.append('X'*(end112-start112))
        elif operation12 == 'insert':
            segment_list1.append('')
        elif operation12 == 'equal':
            segment_list1.append('A'*(end112-start112))

    return segment_list1

def propagate_x_sequences(seq1, seq2):
    """Propagates 'X' markers in sequences to indicate continuous discrepancies."""
    i = 0
    while i < len(seq1) - 1:
        if 'X' in seq1[i] or 'X' in seq2[i]:
            x_sequence_length = 0
            if 'X' in seq1[i+1]:
                x_sequence_length += len(seq1[i])
            if 'X' in seq2[i+1]:
                x_sequence_length += len(seq2[i])
            if x_sequence_length != 0:
                seq1[i], seq1[i+1] = 'X' * len(seq1[i]), 'X' * len(seq1[i+1])
                seq2[i], seq2[i+1] = 'X' * len(seq2[i]), 'X' * len(seq2[i+1])
        i += 1
    return seq1, seq2
    
def isInjection(originalPage, truePage, falsePage, negativeLogic=False):
    start_time_ns = time.perf_counter_ns()

    # Highlight differences
    segments12 = highlight_string_differences(originalPage, truePage)
    segments13 = highlight_string_differences(originalPage, falsePage)
    
    # Normalize segments
    balanced_segments12, balanced_segments13 = balance_and_correct_segments(segments12, segments13)

    # Propagate segments
    balanced_segments12, balanced_segments13 = propagate_x_sequences(balanced_segments12, balanced_segments13)
    
    # Find unique orange segments
    if negativeLogic: result = injection_found(balanced_segments12, balanced_segments13)
    else: result = injection_found(balanced_segments13, balanced_segments12)
    print("Result (isInjection):", result)

    end_time_ns = time.perf_counter_ns()
    duration = (end_time_ns - start_time_ns)
    print(f"Execution time: {duration} nanoseconds")

    return result, duration