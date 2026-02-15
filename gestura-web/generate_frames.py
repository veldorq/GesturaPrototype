"""
Generate placeholder animation frames for Gestura 3D website.
Creates gradient frames that transition from cyan to purple with hand gesture overlay.
"""

import os
from pathlib import Path

try:
    from PIL import Image, ImageDraw, ImageFont, ImageFilter
except ImportError:
    print("Installing Pillow...")
    import subprocess
    subprocess.check_call(["pip", "install", "pillow"])
    from PIL import Image, ImageDraw, ImageFont, ImageFilter

# Configuration
TOTAL_FRAMES = 120
OUTPUT_DIR = Path(__file__).parent / "public" / "frames"
WIDTH = 1920
HEIGHT = 1080

# Gestura colors (RGB)
CYAN = (0, 217, 255)
PURPLE = (123, 97, 255)
NAVY_DARK = (10, 14, 39)
NAVY = (21, 27, 61)

def lerp_color(color1, color2, t):
    """Linear interpolation between two colors"""
    return tuple(int(c1 + (c2 - c1) * t) for c1, c2 in zip(color1, color2))

def create_gradient(width, height, color1, color2, direction='vertical'):
    """Create a gradient image"""
    img = Image.new('RGB', (width, height), color=NAVY_DARK)
    draw = ImageDraw.Draw(img)
    
    if direction == 'vertical':
        for y in range(height):
            t = y / height
            color = lerp_color(color1, color2, t)
            draw.line([(0, y), (width, y)], fill=color)
    else:
        for x in range(width):
            t = x / width
            color = lerp_color(color1, color2, t)
            draw.line([(x, 0), (x, height)], fill=color)
    
    return img

def add_radial_glow(img, center_x, center_y, radius, color, intensity=0.5):
    """Add a radial glow effect"""
    overlay = Image.new('RGBA', img.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    
    for r in range(radius, 0, -10):
        alpha = int(255 * intensity * (1 - r / radius))
        glow_color = (*color, alpha)
        draw.ellipse(
            [center_x - r, center_y - r, center_x + r, center_y + r],
            fill=glow_color
        )
    
    return Image.alpha_composite(img.convert('RGBA'), overlay).convert('RGB')

def add_hand_emoji(img, progress):
    """Add hand gesture with animation"""
    draw = ImageDraw.Draw(img)
    
    # Try to use a large font
    try:
        font = ImageFont.truetype("seguiemj.ttf", 300)  # Windows emoji font
    except:
        try:
            font = ImageFont.truetype("arial.ttf", 300)
        except:
            font = ImageFont.load_default()
    
    # Hand emoji changes through animation
    hand_emojis = ['✋', '🤚', '👋', '🖐️', '✊', '🤜', '👊']
    emoji_index = int(progress * (len(hand_emojis) - 1))
    emoji = hand_emojis[emoji_index]
    
    # Position with animation
    center_x = WIDTH // 2
    y_offset = int(100 * progress)  # Moves down as animation progresses
    center_y = HEIGHT // 2 - 200 + y_offset
    
    # Try to get text bounding box
    try:
        bbox = draw.textbbox((0, 0), emoji, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        text_x = center_x - text_width // 2
        text_y = center_y - text_height // 2
        draw.text((text_x, text_y), emoji, font=font, fill=(255, 255, 255, 255))
    except:
        # Fallback: just draw in center
        draw.text((center_x - 150, center_y - 150), emoji, font=font, fill=(255, 255, 255))
    
    return img

def add_text_overlay(img, text, progress, position='center'):
    """Add text overlay"""
    draw = ImageDraw.Draw(img)
    
    try:
        font = ImageFont.truetype("arial.ttf", 80)
    except:
        font = ImageFont.load_default()
    
    # Opacity based on progress
    if position == 'top':
        opacity = 255 if progress < 0.3 else int(255 * (1 - (progress - 0.3) / 0.2))
    elif position == 'center':
        opacity = 255 if 0.3 < progress < 0.6 else 0
    else:  # bottom
        opacity = 255 if progress > 0.7 else 0
    
    opacity = max(0, min(255, opacity))
    
    if opacity > 0:
        try:
            bbox = draw.textbbox((0, 0), text, font=font)
            text_width = bbox[2] - bbox[0]
            text_x = (WIDTH - text_width) // 2
            
            if position == 'top':
                text_y = 150
            elif position == 'center':
                text_y = HEIGHT // 2 + 200
            else:
                text_y = HEIGHT - 200
            
            draw.text((text_x, text_y), text, font=font, fill=(240, 244, 255, opacity))
        except:
            draw.text((WIDTH // 2 - 200, HEIGHT // 2), text, font=font, fill=(240, 244, 255, opacity))
    
    return img

def generate_frame(frame_num, total_frames):
    """Generate a single frame"""
    progress = frame_num / (total_frames - 1)
    
    # Create base gradient (transitions from cyan to purple)
    color1 = lerp_color(NAVY_DARK, CYAN, progress * 0.3)
    color2 = lerp_color(NAVY, PURPLE, progress * 0.3)
    img = create_gradient(WIDTH, HEIGHT, color1, color2, direction='vertical')
    
    # Add radial glows
    glow_x = WIDTH // 2 + int(300 * (progress - 0.5))
    glow_y = HEIGHT // 2 + int(150 * (progress - 0.5))
    img = add_radial_glow(img, glow_x, glow_y, 400, CYAN, 0.3 * progress)
    
    opposite_x = WIDTH // 2 - int(200 * (progress - 0.5))
    opposite_y = HEIGHT // 2 - int(100 * (progress - 0.5))
    img = add_radial_glow(img, opposite_x, opposite_y, 350, PURPLE, 0.3 * (1 - progress))
    
    # Add hand gesture
    img = add_hand_emoji(img, progress)
    
    # Add text overlays based on progress
    if progress < 0.25:
        img = add_text_overlay(img, "GESTURA", progress / 0.25, position='top')
    elif 0.3 < progress < 0.6:
        img = add_text_overlay(img, "Natural Control", (progress - 0.3) / 0.3, position='center')
    elif progress > 0.7:
        img = add_text_overlay(img, "AI-Powered", (progress - 0.7) / 0.3, position='center')
    
    return img

def main():
    """Generate all frames"""
    print(f"🎬 Generating {TOTAL_FRAMES} frames for Gestura...")
    print(f"📁 Output directory: {OUTPUT_DIR}")
    
    # Create output directory
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    
    # Generate frames
    for i in range(TOTAL_FRAMES):
        frame_path = OUTPUT_DIR / f"frame_{i}.webp"
        
        if frame_path.exists():
            print(f"⏭️  Frame {i}/{TOTAL_FRAMES-1} already exists, skipping...")
            continue
        
        print(f"🎨 Generating frame {i}/{TOTAL_FRAMES-1}...", end='\r')
        
        img = generate_frame(i, TOTAL_FRAMES)
        
        # Save as WebP for better compression
        img.save(frame_path, 'WEBP', quality=85, method=6)
    
    print(f"\n✅ Successfully generated {TOTAL_FRAMES} frames!")
    print(f"📊 Total size: {sum(f.stat().st_size for f in OUTPUT_DIR.glob('*.webp')) / 1024 / 1024:.2f} MB")
    print("\n🚀 Next steps:")
    print("   1. Run: npm install")
    print("   2. Run: npm run dev")
    print("   3. Visit: http://localhost:3000")
    print("\n💡 To replace with AI-generated frames, see README.md")

if __name__ == "__main__":
    main()
