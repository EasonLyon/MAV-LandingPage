import os

def generate_index_html(root_dir, output_file="index.html"):
    html_content = [
        "<html>",
        "<head>",
        "<title>HTML File Index</title>",
        '<meta name="viewport" content="width=device-width, initial-scale=1">',
        "<style>",
        "body { font-family: Arial, sans-serif; background: #f8f9fa; margin: 0; padding: 0; }",
        ".container { max-width: 900px; margin: 40px auto; background: #fff; border-radius: 10px; box-shadow: 0 2px 8px rgba(0,0,0,0.08); padding: 32px; }",
        "h1 { color: #2c3e50; text-align: center; }",
        ".folder-section { margin-bottom: 36px; }",
        ".folder-title { font-size: 1.3em; color: #007bff; margin-bottom: 10px; margin-top: 30px; border-left: 4px solid #007bff; padding-left: 12px; }",
        "ul { list-style: none; padding: 0; }",
        "li { margin: 12px 0; }",
        "a { color: #007bff; text-decoration: none; font-size: 1.1em; }",
        "a:hover { text-decoration: underline; }",
        ".file-list { background: #f4f8fb; border-radius: 6px; padding: 16px 20px; box-shadow: 0 1px 4px rgba(0,0,0,0.03); }",
        "</style>",
        "</head>",
        "<body>",
        '<div class="container">',
        "<h1>HTML File Index</h1>"
    ]

    folder_map = {}
    for dirpath, _, filenames in os.walk(root_dir):
        rel_dir = os.path.relpath(dirpath, root_dir)
        is_root = rel_dir == "."
        display_dir = "Root" if is_root else rel_dir

        html_files = []
        for f in filenames:
            if not f.endswith(".html"):
                continue
            if is_root and f == output_file:
                continue
            html_files.append(f)

        if html_files:
            html_files.sort()
            folder_map[display_dir] = [
                os.path.join(rel_dir if not is_root else "", f).replace("\\", "/")
                for f in html_files
            ]

    for folder, files in sorted(folder_map.items()):
        html_content.append(f'<div class="folder-section">')
        html_content.append(f'<div class="folder-title">{folder}</div>')
        html_content.append('<ul class="file-list">')
        for file_link in files:
            html_content.append(f'<li><a href="{file_link}">{os.path.basename(file_link)}</a></li>')
        html_content.append('</ul></div>')

    html_content.extend([
        "</div>",
        "</body>",
        "</html>"
    ])

    with open(os.path.join(root_dir, output_file), "w", encoding="utf-8") as f:
        f.write("\n".join(html_content))

if __name__ == "__main__":
    generate_index_html(".")
