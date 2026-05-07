from compiler import parser, lexer

input_file = "input.md"
output_file = "output.html"

with open(input_file, "r", encoding="utf-8") as file:
    markdown_text = file.read()

html_output = parser.parse(markdown_text, lexer=lexer)

with open(output_file, "w", encoding="utf-8") as file:
    file.write(html_output)

print(f"HTML successfully written to {output_file}")