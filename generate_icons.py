"""
Generate PWA icons for mobile app
"""
from PIL import Image, ImageDraw, ImageFont
import os

def create_icon(size, output_path):
    """Create a simple icon with SiteLenz logo"""
    # Create image with gradient background
    img = Image.new('RGB', (size, size), color='#2c3e50')
    draw = ImageDraw.Draw(img)
    
    # Draw gradient effect (dark blue to lighter blue)
    for i in range(size):
        color = (44 + i//10, 62 + i//8, 80 + i//6)
        draw.rectangle([0, i, size, i+1], fill=color)
    
    # Draw camera icon (simplified)
    camera_size = size // 2
    camera_x = (size - camera_size) // 2
    camera_y = (size - camera_size) // 2
    
    # Camera body
    draw.rounded_rectangle(
        [camera_x, camera_y, camera_x + camera_size, camera_y + camera_size],
        radius=size//10,
        fill='#3498db',
        outline='white',
        width=max(2, size//100)
    )
    
    # Camera lens
    lens_size = camera_size // 2
    lens_x = camera_x + (camera_size - lens_size) // 2
    lens_y = camera_y + (camera_size - lens_size) // 2
    draw.ellipse(
        [lens_x, lens_y, lens_x + lens_size, lens_y + lens_size],
        fill='#2c3e50',
        outline='white',
        width=max(2, size//150)
    )
    
    # Inner lens
    inner_size = lens_size // 2
    inner_x = lens_x + (lens_size - inner_size) // 2
    inner_y = lens_y + (lens_size - inner_size) // 2
    draw.ellipse(
        [inner_x, inner_y, inner_x + inner_size, inner_y + inner_size],
        fill='#3498db'
    )
    
    # Save
    img.save(output_path, 'PNG', quality=95)
    print(f"Created: {output_path}")

if __name__ == '__main__':
    # Create static directory if it doesn't exist
    os.makedirs('static', exist_ok=True)
    
    # Generate icons
    create_icon(192, 'static/icon-192.png')
    create_icon(512, 'static/icon-512.png')
    
    print("\n✅ PWA icons generated successfully!")
    print("   📁 static/icon-192.png")
    print("   📁 static/icon-512.png")
