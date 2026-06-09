import os
# Assuming this is run from /home/daniel_trujillo/reporting-agent/
# import sys; sys.path.append('mcp-server') # Could add this if needed
# from server import write_report_doc

# Simple test harness assuming environment is set up
# We would need to mock the Google API calls to really test this,
# but this script verifies the logic of the parser.

def test_markdown_parser():
    test_content = "# Title\n## Section\n### Subsection\nNormal text"
    
    # Simulate the logic to check cleaning
    cleaned_lines = []
    current_index = 1
    formatting_instructions = []
    
    for line in test_content.split('\n'):
        style = None
        cleaned_line = line
        if line.startswith('# '):
            style = 'HEADING_1'
            cleaned_line = line[2:]
        elif line.startswith('## '):
            style = 'HEADING_2'
            cleaned_line = line[3:]
        elif line.startswith('### '):
            style = 'HEADING_3'
            cleaned_line = line[4:]
        
        line_with_newline = cleaned_line + '\n'
        cleaned_lines.append(line_with_newline)
        
        if style:
            formatting_instructions.append({'style': style, 'range': (current_index, current_index + len(line_with_newline))})
        current_index += len(line_with_newline)
    
    cleaned_content = "".join(cleaned_lines)
    
    print("Cleaned Content:")
    print(repr(cleaned_content))
    print("\nFormatting Instructions:")
    for instr in formatting_instructions:
        print(instr)

    # Verification
    assert cleaned_content == "Title\nSection\nSubsection\nNormal text\n"
    assert formatting_instructions[0]['style'] == 'HEADING_1'
    assert formatting_instructions[1]['style'] == 'HEADING_2'
    assert formatting_instructions[2]['style'] == 'HEADING_3'
    print("\nTest passed!")

if __name__ == "__main__":
    test_markdown_parser()
