import os

def generate_index_html(root_dir, output_file="index.html"):
    html_content = [
        "<html>",
        "<head>",
        "<title>HTML File Index</title>",
        '<meta name="viewport" content="width=device-width, initial-scale=1">',
        "<style>",
        "body { font-family: Arial, sans-serif; background: #f8f9fa; margin: 0; padding: 0; }",
        ".container { max-width: 700px; margin: 40px auto; background: #fff; border-radius: 10px; box-shadow: 0 2px 8px rgba(0,0,0,0.08); padding: 32px; }",
        "h1 { color: #2c3e50; text-align: center; }",
        "ul { list-style: none; padding: 0; }",
        "li { margin: 16px 0; }",
        "a { color: #007bff; text-decoration: none; font-size: 1.1em; }",
        "a:hover { text-decoration: underline; }",
        "</style>",
        "</head>",
        "<body>",
        '<div class="container">',
        "<h1>HTML File Index</h1>",
        "<ul>"
    ]

    for dirpath, _, filenames in os.walk(root_dir):
        rel_dir = os.path.relpath(dirpath, root_dir)
        if rel_dir == ".":
            rel_dir = ""
        for filename in filenames:
            if filename.endswith(".html") and filename != output_file:
                file_link = os.path.join(rel_dir, filename).replace("\\", "/")
                html_content.append(f'<li><a href="{file_link}">{file_link}</a></li>')

    html_content.extend([
        "</ul>",
        "</div>",
        "</body>",
        "</html>"
    ])

    with open(os.path.join(root_dir, output_file), "w", encoding="utf-8") as f:
        f.write("\n".join(html_content))

if __name__ == "__main__":
    generate_index_html(".")
