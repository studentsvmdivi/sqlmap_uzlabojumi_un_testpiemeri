import difflib
import time

def check_string_differences(s1, s2, s3):
    # Compare s1 with s2 and s1 with s3 using difflib to get differences as opcodes.
    opcodes1 = difflib.SequenceMatcher(None, s1, s2).get_opcodes()
    opcodes2 = difflib.SequenceMatcher(None, s1, s3).get_opcodes()

    i, j = 0, 0  # indices for opcodes1 and opcodes2
    potential_injection = False
    discrepancy_detected = False

    # Loop through both sets of opcodes as long as there are opcodes to process
    while i < len(opcodes1) or j < len(opcodes2):
        # Retrieve operation type and endpoint from opcodes lists
        op1, end1 = get_opcode_info(opcodes1, i)
        op2, end2 = get_opcode_info(opcodes2, j)
        
        # Analyze operations to detect discrepancies or potential injections
        if op1 == 'equal' and op2 == 'equal':
            # Reset flags if sequences align again after a discrepancy
            if potential_injection and not discrepancy_detected:
                return True
            potential_injection = False
            discrepancy_detected = False
        elif op1 == 'equal' and op2 != 'equal':
            discrepancy_detected = True
        elif op1 != 'equal' and op2 == 'equal':
            potential_injection = True
        elif op1 != 'equal' and op2 != 'equal':
            potential_injection = False
            discrepancy_detected = True

        # Increment indices based on which segment ends first
        i, j = increment(i, j, end1, end2)
    
    # Final evaluation of detected patterns
    injection_detected = (potential_injection and not discrepancy_detected)
    return injection_detected

def increment(i, j, end1, end2):
    """Increment indices based on comparison of end positions."""
    if end1 < end2:
        i += 1
    elif end1 > end2:
        j += 1
    else:
        i += 1
        j += 1
    return i, j

def get_opcode_info(opcodes, index):
    """Retrieve operation and endpoint from opcode list at a given index."""
    if index < len(opcodes):
        op = opcodes[index][0]
        end = opcodes[index][2]
    else:
        op = 'equal'  # default to 'equal' if beyond list range
        end = opcodes[-1][2]  # use the last end point if index is out of range
    return op, end

def isInjection(originalPage, truePage, falsePage, negativeLogic=False):
    """Determine if an injection-like pattern exists between the text comparisons."""
    start_time_ns = time.perf_counter_ns()

    # Check for differences, potentially reversing roles of s2 and s3 based on negativeLogic flag
    if negativeLogic: result = check_string_differences(originalPage, truePage, falsePage)
    else: result = check_string_differences(originalPage, falsePage, truePage)
    print("Result (isInjection):", result)

    # Calculate and print the function execution time
    end_time_ns = time.perf_counter_ns()
    duration = (end_time_ns - start_time_ns)
    print(f"Execution time: {duration} nanoseconds")

    return result, duration
