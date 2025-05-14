def unary_addition(tape):
    """
    Simulates a Turing Machine that adds two unary numbers separated by '+'.
    It simply replaces '+' with '1', thus appending the second unary number.
    """

    # Convert input string to list for mutable operations
    tape = list(tape)

    # Step through the tape
    head = 0
    while head < len(tape):
        if tape[head] == '+':
            tape[head] = '1'  # Replace '+' with '1' to simulate addition
            break
        head += 1

    # Return the updated tape as a string
    return ''.join(tape)

# Example
input_tape = "111+11"
output_tape = unary_addition(input_tape)

print("Input:", input_tape)
print("Output:", output_tape)