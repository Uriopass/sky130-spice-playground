import re

# This regex looks for a closing parenthesis ) followed by spaces,
# and then a float number. It matches and captures the float portion.
float_after_paren_pattern = re.compile(r"\)\s+([0-9]*\.[0-9]+)")

# Replace 'input.txt' with the path to your actual file
with open('lol.txt', 'r') as infile:
    mean = 0
    c = 0
    for line in infile:
        # Strip line to avoid confusion with trailing whitespace
        line = line.strip()

        # If line doesn't contain a parenthesis tuple, skip it
        if '(' not in line or ')' not in line:
            continue
        c += 1
        # Search for the pattern in the line
        match = float_after_paren_pattern.search(line)
        if match:
            # The first captured group is our desired float
            mean += float(match.group(1))



    print(mean/c)