import difflib
import re
from lib.utils.make_strings_equal import make_strings_equal
import time

def find_injection(str1, str2):
    """
    Identifies segments in str1 marked as 'orange' with ANSI escape codes and checks
    if these segments are not marked as orange in str2.
    
    Args:
    - str1 (str): The first string with potentially orange-marked segments.
    - str2 (str): The second string to compare against.
    
    Returns:
    - List[str]: Segments that are orange in str1 and not orange in str2.
    """
    # ANSI escape sequence pattern to remove formatting for clean comparison
    ansi_escape_pattern = re.compile(r'\x1b\[\d+(?:;\d+)*m')
    segments1 = re.split(ansi_escape_pattern, str1)  # Segments of str1 without ANSI codes
    segments2 = re.split(ansi_escape_pattern, str2)  # Segments of str2 without ANSI codes

    return injection_found(segments1, segments2)

def injection_found(segmentsA, segmentsB):
    """
    Compares lengths of corresponding segments between two lists.
    Returns True if a segment in segmentsA is shorter than its corresponding segment in segmentsB,
    suggesting an "injection" or alteration.
    """
    x = False  # Flag to handle complex segment comparison logic
    i, j = 0, 0  # indices for segmentsA and segmentsB
    while i < len(segmentsA) and j < len(segmentsB):
        A = segmentsA[i] if not x else A3  # Continue from remainder if split
        B = segmentsB[j]
        if len(A) < len(B):
            return True  # Injection detected
        elif len(B) < len(A):
            # Split A into three parts if it is longer than B
            A1 = A[:len(B)]
            A2 = A[len(B):len(B) + len(segmentsB[j+1])]
            A3 = A[len(B) + len(segmentsB[j+1]):]
            x = True  # Set flag to use A3 in next loop iteration
            j += 2  # Move to the next segment in segmentsB
            continue
        
        x = False  # Reset flag
        i += 1
        j += 1
    return False

def highlight_line_difference(page1, page2):
    """
    Wraps diff parts in ANSI escape codes to highlight differences.
    Orange is used for deletions or changes from page1, red for parts in page2 replacing those in page1,
    and green for additions in page2.
    Returns a tuple of highlighted lines.
    """
    diff = difflib.SequenceMatcher(None, page1, page2)
    ORANGE, GREEN, RED, RESET = '\033[38;5;208m', '\033[92m', '\033[91m', '\033[0m'
    result_line1, result_line2 = [], []
    for tag, i1, i2, j1, j2 in diff.get_opcodes():
        if tag == 'replace':
            result_line1.append(ORANGE + page1[i1:i2] + RESET)
            result_line2.append(RED + page1[i1:i2] + RESET)
            result_line2.append(GREEN + page2[j1:j2] + RESET)
        elif tag == 'delete':
            result_line1.append(ORANGE + page1[i1:i2] + RESET)
            result_line2.append(RED + page1[i1:i2] + RESET)
        elif tag == 'insert':
            result_line1.append(ORANGE + "\\0" + RESET)
            result_line2.append(GREEN + page2[j1:j2] + RESET)
        elif tag == 'equal':
            result_line1.append(page1[i1:i2])
            result_line2.append(page2[j1:j2])
    return ''.join(result_line1), ''.join(result_line2)

def normalize_lines(lineA, lineB):
    """
    Adjusts lines A and B to make them equal by inserting "\\0" where necessary,
    facilitated by a custom function in an external module.
    """
    return make_strings_equal(lineA, lineB)


def isInjection(originalPage, truePage, falsePage, negativeLogic=False):
    start_time_ns = time.perf_counter_ns()

    dFalsePage, falsePage = highlight_line_difference(originalPage, falsePage)
    dTruePage, truePage = highlight_line_difference(originalPage, truePage)
    print("truePage 2:", truePage)
    print("falsePage 3:", falsePage)
    dTruePage, dFalsePage = normalize_lines(dTruePage, dFalsePage)
    print("dTruePage:", dTruePage)
    print("dFalsePage:", dFalsePage)
    if negativeLogic: result = find_injection(dTruePage, dFalsePage)
    else: result = find_injection(dFalsePage, dTruePage)
    print("Result (isInjection):", result)

    end_time_ns = time.perf_counter_ns()
    duration = (end_time_ns - start_time_ns)
    print(f"Execution time: {duration} nanoseconds")

    return result

#isInjection("ABCDEFG", "ABY1DEFGY2", "ABX1DX2FX3G")