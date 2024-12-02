import math
from xml.etree.ElementTree import Element, SubElement, tostring, indent

def generate_svg(data):
    """
    Generate an SVG string with two squares per line representing deltas.

    Parameters:
    - data: List of tuples (text, value_left, value_right).
            Values can be None or between -1 and 1.

    Returns:
    - str: SVG content as a string.
    """
    square_size = 20
    gap = 5
    text_offset = 5
    width = square_size * 2 + gap * 2 + 200  # 200 for text
    height = (square_size + gap) * len(data) + gap

    svg = Element('svg', xmlns="http://www.w3.org/2000/svg", width=str(width), height=str(height))

    # Add white background
    SubElement(svg, 'rect', {
        'x': "0",
        'y': "0",
        'width': str(width),
        'height': str(height),
        'fill': "black"
    })

    for i, (text, value_left, value_right) in enumerate(data):
        if text == "skip_line":
            SubElement(svg, 'line', {
                'x1': "0",
                'y1': str(i * (square_size + gap) + gap + square_size / 2),
                'x2': str(width),
                'y2': str(i * (square_size + gap) + gap + square_size / 2),
                'stroke': "white",
                'stroke-width': "1"
            })
            continue

        y_position = i * (square_size + gap) + gap

        def get_color(value):
            if value is None:
                return "rgb(32, 32, 32)"  # Gray for None
            zero_color = [0, 0, 0]
            green = [0, 255, 0]
            red = [255, 0, 0]
            if 0 <= value < 0.5:
                coeff = (value * 2) ** 0.9
                return f"rgb({int(zero_color[0] * (1 - coeff) + red[0] * coeff)}, {int(zero_color[1] * (1 - coeff) + red[1] * coeff)}, {int(zero_color[2] * (1 - coeff) + red[2] * coeff)})"
            elif -0.5 < value < 0:
                coeff = (-value * 2) ** 0.9
                return f"rgb({int(zero_color[0] * (1 - coeff) + green[0] * coeff)}, {int(zero_color[1] * (1 - coeff) + green[1] * coeff)}, {int(zero_color[2] * (1 - coeff) + green[2] * coeff)})"
            elif value >= 0.5:
                return f"rgb(255, 0, {int((value - 0.5)*255*2)})"
            elif value <= -0.5:
                return f"rgb(0, 255, {int((-value - 0.5) * 255 * 2)})"
            else:
                print(value)
                return "rgb(0, 0, 0)"
        # Colors based on values
        color_left = get_color(value_left)
        color_right = get_color(value_right)

        # Left square
        SubElement(svg, 'rect', {
            'x': str(gap),
            'y': str(y_position),
            'width': str(square_size),
            'height': str(square_size),
            'fill': color_left
        })

        # Right square
        SubElement(svg, 'rect', {
            'x': str(gap + square_size + gap),
            'y': str(y_position),
            'width': str(square_size),
            'height': str(square_size),
            'fill': color_right
        })

        # Text
        SubElement(svg, 'text', {
            'x': str(gap + 2 * (square_size + gap)),
            'y': str(y_position + square_size - text_offset),
            'font-size': "12",
            'font-family': "Arial",
            'fill': "white"
        }).text = text

    indent(svg, '  ')

    return tostring(svg).decode('utf-8')

if __name__ == "__main__":
    # Example usage
    data = [
        ("Row 1", 0.5, -1.0),
        ("Row 1", 0.5, -0.9),
        ("Row 1", 0.5, -0.8),
        ("Row 1", 0.5, -0.7),
        ("Row 1", 0.5, -0.5),
        ("Row 1", 0.5, -0.4),
        ("Row 1", 0.5, -0.1),
        ("Row 1", 0.5, -0.05),
        ("Row 1", 0.5, -0.02),
        ("Row 1", 0.5, -0.01),
        ("Row 1", 0.5, 0.1),
        ("Row 1", 0.5, 0.2),
        ("skip_line", None, None),
        ("Row 1", 0.5, 0.4),
        ("Row 1", 0.5, 0.5),
        ("Row 1", 0.5, 0.7),
        ("Row 1", 0.5, 0.8),
        ("Row 1", 0.5, 1.0),
        ("Row 2", None, 0.8),
        ("Row 3", -0.7, None),
        ("Row 4", None, None)
    ]

    svg_content = generate_svg(data)
    with open("output.svg", "w") as f:
        f.write(svg_content)