import ply.lex as lex
import ply.yacc as yacc
import re

from css import style

# Lexer

tokens = (
    'HASH', 'DASH', 'BOLD', 'ITALIC', 'LINK', 'CODE_BLOCK', 'CODE_INLINE', 'STRIKE',
    'PIPE', 'HR', 'BLOCKQUOTE_MARKER', 'DBL_NEWLINE', 'NEWLINE', 'TEXT', 'IMAGE', 'ORDERED_LIST_MARKER'
)

# Regras

def t_BOLD(t):
    r'\*\*[^\n]+?\*\*'
    t.value = t.value[2:-2]
    return t

def t_ITALIC(t):
    r'\*[^\n]+?\*'
    t.value = t.value[1:-1]
    return t

def t_LINK(t):
    r'\[[^\]\n]+\]\([^)\n]+\)'
    m = re.match(r'\[([^\]]+)\]\(([^)]+)\)', t.value)
    t.value = (m.group(1), m.group(2))
    return t

def t_HASH(t):
    r'^\#+(?=[ \t])'
    t.value = len(t.value)
    return t

def t_DASH(t):
    r'^[ \t]*[-*](?=[ \t])'
    return t

def t_CODE_BLOCK(t):
    r'```[\s\S]*?```'
    content = t.value[3:-3].strip()
    content = content.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
    t.value = content
    return t

def t_CODE_INLINE(t):
    r'`[^`\n]+`'
    t.value = t.value[1:-1]
    t.value = t.value.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
    return t

def t_PIPE(t):
    r'\|'
    return t

def t_STRIKE(t):
    r'\~\~[^\n]+?\~\~'
    t.value = t.value[2:-2]
    return t

def t_IMAGE(t):
    r'\!\[[^\]\n]*\]\([^)\n]+\)'
    m = re.match(r'\!\[([^\]]*)\]\(([^)]+)\)', t.value)
    t.value = (m.group(1), m.group(2))
    return t

def t_ORDERED_LIST_MARKER(t):
    r'^[ \t]*\d+\.[ \t]+'
    return t

def t_DBL_NEWLINE(t):
    r'\n[ \t]*\n+'
    return t

def t_HR(t):
    r'^[ \t]*---[- \t]*'
    return t

def t_BLOCKQUOTE_MARKER(t):
    r'^[ \t]*>[ \t]?'
    return t

def t_NEWLINE(t):
    r'\n'
    return t

def t_TEXT(t):
    r'[^#\*\-\n\[\]\|\`\>\~\!0-9]+'
    t.value = t.value.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
    return t

def t_FALLBACK(t):
    r'[#\*\-\[\]\|\`\>\~\!0-9]'
    t.type = 'TEXT'
    return t

def t_CATCHALL(t):
    r'.'
    t.type = 'TEXT'
    return t

def t_error(t):
    print(f"Illegal character '{t.value[0]}' at line {t.lineno}")
    t.lexer.skip(1)

lexer = lex.lex(reflags=re.MULTILINE)

# Parser

def p_document(p):
    '''document : blocks'''
    p[0] = (
        "<!DOCTYPE html>\n<html>\n"
        "<head>\n"
        "<meta charset=\"UTF-8\"\n>"
        "<title>Compiled Markdown</title>\n"
        f"{style}\n"
        "</head>\n"
        "<body>\n"
        f"{''.join(p[1])}"
        "</body>\n</html>"
    )

def p_blocks(p):
    '''blocks : blocks block
              | block'''
    if len(p) == 3:
        p[1].append(p[2])
        p[0] = p[1]
    else:
        p[0] = [p[1]]

def p_block(p):
    '''block : header
             | list
             | ordered_list
             | paragraph
             | code_block  
             | table
             | hr            
             | blockquote    
             | empty_block'''
    p[0] = p[1]

def p_empty_block(p):
    '''empty_block : DBL_NEWLINE
                   | NEWLINE'''
    p[0] = ""

def p_header(p):
    '''header : HASH inline_elements DBL_NEWLINE
              | HASH inline_elements NEWLINE
              | HASH inline_elements'''
    level = min(p[1], 6)
    p[0] = f"<h{level}>{p[2].strip()}</h{level}>\n"

def p_list(p):
    '''list : list_items'''
    p[0] = f"<ul>\n{''.join(p[1])}</ul>\n"

def p_list_items(p):
    '''list_items : list_items list_item
                  | list_item'''
    if len(p) == 3:
        p[1].append(p[2])
        p[0] = p[1]
    else:
        p[0] = [p[1]]

def p_list_item(p):
    '''list_item : DASH inline_elements DBL_NEWLINE
                 | DASH inline_elements NEWLINE
                 | DASH inline_elements'''
    p[0] = f"  <li>{p[2].strip()}</li>\n"

def p_ordered_list(p):
    '''ordered_list : ordered_list_items'''
    p[0] = f"<ol>\n{''.join(p[1])}</ol>\n"

def p_ordered_list_items(p):
    '''ordered_list_items : ordered_list_items ordered_list_item
                          | ordered_list_item'''
    if len(p) == 3:
        p[1].append(p[2])
        p[0] = p[1]
    else:
        p[0] = [p[1]]

def p_ordered_list_item(p):
    '''ordered_list_item : ORDERED_LIST_MARKER inline_elements DBL_NEWLINE
                         | ORDERED_LIST_MARKER inline_elements NEWLINE
                         | ORDERED_LIST_MARKER inline_elements'''
    p[0] = f"  <li>{p[2].strip()}</li>\n"

def p_paragraph(p):
    '''paragraph : para_content DBL_NEWLINE
                 | para_content'''
    content = p[1].strip()
    if content:
        p[0] = f"<p>{content}</p>\n"
    else:
        p[0] = ""

def p_para_content(p):
    '''para_content : para_content NEWLINE inline_elements
                    | para_content NEWLINE
                    | inline_elements'''
    if len(p) == 4:
        p[0] = p[1] + " " + p[3]
    elif len(p) == 3:
        p[0] = p[1] + " "
    else:
        p[0] = p[1]

def p_inline_elements(p):
    '''inline_elements : inline_elements inline_element
                       | inline_element'''
    if len(p) == 3:
        p[0] = p[1] + p[2]
    else:
        p[0] = p[1]

def p_inline_element(p):
    '''inline_element : TEXT
                      | BOLD
                      | ITALIC
                      | LINK
                      | CODE_INLINE
                      | STRIKE
                      | IMAGE'''
    
    if p.slice[1].type == 'BOLD':
        p[0] = f"<strong>{p[1]}</strong>"
    elif p.slice[1].type == 'ITALIC':
        p[0] = f"<em>{p[1]}</em>"
    elif p.slice[1].type == 'STRIKE':
        p[0] = f"<del>{p[1]}</del>"
    elif p.slice[1].type == 'LINK':
        p[0] = f'<a href="{p[1][1]}">{p[1][0]}</a>'
    elif p.slice[1].type == 'IMAGE':
        p[0] = f'<img src="{p[1][1]}" alt="{p[1][0]}">'
    elif p.slice[1].type == 'CODE_INLINE':
        p[0] = f"<code>{p[1]}</code>"
    else:
        p[0] = p[1]

def p_hr(p):
    '''hr : HR DBL_NEWLINE
          | HR NEWLINE
          | HR'''
    p[0] = "<hr>\n"

def p_blockquote(p):
    '''blockquote : blockquote_lines DBL_NEWLINE
                  | blockquote_lines NEWLINE
                  | blockquote_lines'''
    p[0] = f"<blockquote>\n  <p>{p[1].strip()}</p>\n</blockquote>\n"

def p_blockquote_lines(p):
    '''blockquote_lines : blockquote_lines NEWLINE blockquote_line
                        | blockquote_line'''
    if len(p) == 4:
        p[0] = p[1] + " " + p[3]
    else:
        p[0] = p[1]

def p_blockquote_line(p):
    '''blockquote_line : BLOCKQUOTE_MARKER inline_elements'''
    p[0] = p[2]

def p_code_block(p):
    '''code_block : CODE_BLOCK DBL_NEWLINE
                  | CODE_BLOCK NEWLINE
                  | CODE_BLOCK'''
    p[0] = f"<pre><code>{p[1]}</code></pre>\n"

def p_table(p):
    '''table : table_rows DBL_NEWLINE
             | table_rows NEWLINE
             | table_rows'''
    rows = p[1]
    if not rows:
        p[0] = ""
        return
        
    html = "<table>\n"
    
    has_header = False
    if len(rows) > 1:
        if all(re.match(r'^[\s\-:]+$', cell) for cell in rows[1]):
            has_header = True

    if has_header:
        html += "<thead>\n<tr>\n"
        for cell in rows[0]:
            html += f"  <th>{cell.strip()}</th>\n"
        html += "</tr>\n</thead>\n<tbody>\n"
        
        for row in rows[2:]:
            html += "<tr>\n"
            for cell in row:
                html += f"  <td>{cell.strip()}</td>\n"
            html += "</tr>\n"
        html += "</tbody>\n"
    else:
        html += "<tbody>\n"
        for row in rows:
            html += "<tr>\n"
            for cell in row:
                html += f"  <td>{cell.strip()}</td>\n"
            html += "</tr>\n"
        html += "</tbody>\n"
        
    html += "</table>\n"
    p[0] = html

def p_table_rows(p):
    '''table_rows : table_rows table_row
                  | table_row'''
    if len(p) == 3:
        p[1].append(p[2])
        p[0] = p[1]
    else:
        p[0] = [p[1]]

def p_table_row(p):
    '''table_row : PIPE table_cells PIPE NEWLINE
                 | PIPE table_cells PIPE'''
    p[0] = p[2]

def p_table_cells(p):
    '''table_cells : table_cells PIPE cell_content
                   | cell_content'''
    if len(p) == 4:
        p[1].append(p[3])
        p[0] = p[1]
    else:
        p[0] = [p[1]]

def p_cell_content(p):
    '''cell_content : inline_elements
                    | '''
    p[0] = p[1] if len(p) > 1 else ""

def p_error(p):
    if p:
        print(f"Syntax error at '{p.value}' (type: {p.type}, line: {p.lineno})")
    else:
        print("Syntax error at EOF")

# Build the parser
parser = yacc.yacc()