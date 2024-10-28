import os

# Define the folder where your plots are located
plot_folder = "fig-lib"
output_file = "index.html"

def generate_html(plot_folder):
    # Start the HTML content
    html_content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Krill Movement Plot Gallery</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                background-color: #f4f4f4;
                margin: 0;
                padding: 0;
            }
            .gallery {
                display: flex;
                flex-wrap: wrap;
                gap: 10px;
                justify-content: center;
                margin-top: 20px;
            }
            .gallery img {
                max-width: 300px;
                height: auto;
                border: 1px solid #ccc;
                box-shadow: 2px 2px 6px rgba(0, 0, 0, 0.1);
            }
        </style>
    </head>
    <body>
        <h1 style="text-align: center;">Krill Movement Plot Gallery</h1>
        <div class="gallery">
    """

    # Loop through the plot folder and add images to the HTML content
    for root, _, files in os.walk(plot_folder):
        for file in files:
            if file.endswith(".png"):
                rel_path = os.path.join(root, file)
                html_content += f'<img src="{rel_path}" alt="{file}">\n'

    # End the HTML content
    html_content += """
        </div>
    </body>
    </html>
    """

    # Write the HTML content to a file
    with open(output_file, "w") as f:
        f.write(html_content)

    print(f"Gallery generated and saved to {output_file}!")

# Run the function to generate the HTML
generate_html(plot_folder)