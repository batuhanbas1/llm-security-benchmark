import os
import tokenize
import io

def clean_python_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        source = f.read()

    lines = source.split('\n')
    
    tokens = []
    try:
        g = tokenize.generate_tokens(io.StringIO(source).readline)
        tokens = list(g)
    except tokenize.TokenError:
        return

    to_remove = []
    
    for i, tok in enumerate(tokens):
        tok_type = tok[0]
        string_val = tok[1]
        start_line, start_col = tok[2]
        end_line, end_col = tok[3]
        
        if tok_type == tokenize.COMMENT:
            to_remove.append((start_line, start_col, end_line, end_col))
        elif tok_type == tokenize.STRING:
            is_docstring = False
            prev_tok = tokens[i-1] if i > 0 else None
            
            if prev_tok is None:
                is_docstring = True
            elif prev_tok[0] == tokenize.ENCODING:
                is_docstring = True
            else:
                for j in range(i-1, -1, -1):
                    if tokens[j][0] not in (tokenize.NL, tokenize.COMMENT):
                        if tokens[j][0] in (tokenize.INDENT, tokenize.DEDENT, tokenize.NEWLINE, tokenize.ENCODING):
                            is_docstring = True
                        break
            
            if is_docstring:
                to_remove.append((start_line, start_col, end_line, end_col))

    if not to_remove:
        return

    to_remove.sort(key=lambda x: (x[0], x[1]), reverse=True)

    for start_line, start_col, end_line, end_col in to_remove:
        start_line -= 1
        end_line -= 1
        
        if start_line == end_line:
            lines[start_line] = lines[start_line][:start_col] + lines[start_line][end_col:]
        else:
            lines[start_line] = lines[start_line][:start_col]
            for l in range(start_line + 1, end_line):
                lines[l] = ""
            lines[end_line] = lines[end_line][end_col:]

    new_source = '\n'.join(lines)
    
    with open(filepath, 'w', encoding='utf-8') as f:
         f.write(new_source)

def main():
    root = "."
    for dirpath, _, filenames in os.walk(root):
        if "venv" in dirpath or ".git" in dirpath or "results" in dirpath:
            continue
        for file in filenames:
            if file.endswith(".py") and file != "cleaner.py":
                path = os.path.join(dirpath, file)
                print(f"Cleaning {path}...")
                clean_python_file(path)

if __name__ == "__main__":
    main()
