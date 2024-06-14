from PIL import Image
import json

def generate_metadata(image_path, sprite_width, sprite_height, output_json_path):
    # Open the sprite sheet image
    sprite_sheet = Image.open(image_path)
    sheet_width, sheet_height = sprite_sheet.size
    
    # Initialize metadata dictionary
    metadata = {"frames": {}}
    sprite_count = 1

    for y in range(0, sheet_height, sprite_height):
        for x in range(0, sheet_width, sprite_width):
            sprite_name = f"sprite{sprite_count}"
            metadata["frames"][sprite_name] = {
                "frame": {"x": x, "y": y, "w": sprite_width, "h": sprite_height}
            }
            sprite_count += 1

    # Save metadata to JSON file
    with open(output_json_path, 'w') as json_file:
        json.dump(metadata, json_file, indent=4)

    print(f"Metadata has been generated and saved to {output_json_path}")

# Define the path to your sprite sheet image and the dimensions of each sprite
image_path = 'assets\plants\sunflower\sunflower_sheet.png'
sprite_width = 30
sprite_height = 30
output_json_path = 'assets\plants\sunflower\sunflower_sheet.json'

# Generate metadata
generate_metadata(image_path, sprite_width, sprite_height, output_json_path)
