import streamlit as st
import requests
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont

# Function to create banner image
def create_banner(title, summary, message, banner_image_url, box_color):
    # Image dimensions
    img_width, img_height = 600, 220

    # Download and resize background image
    response = requests.get(banner_image_url)
    background = Image.open(BytesIO(response.content)).convert("RGB")
    background = background.resize((img_width, img_height))

    # Create drawing object
    draw = ImageDraw.Draw(background)

    # Load fonts with fallback
    try:
        font_title = ImageFont.truetype("arial.ttf", 22)
        font_summary = ImageFont.truetype("arialbd.ttf", 28)
        font_message = ImageFont.truetype("arial.ttf", 18)
    except OSError:
        font_title = ImageFont.truetype("DejaVuSans-Bold.ttf", 22)
        font_summary = ImageFont.truetype("DejaVuSans-Bold.ttf", 28)
        font_message = ImageFont.truetype("DejaVuSans.ttf", 18)

    # Draw title
    draw.text((20, 10), title, font=font_title, fill="white")

    # Draw box with dynamic color
    offer_box = (20, 50, 430, 170)
    draw.rounded_rectangle(offer_box, radius=20, fill=box_color)

    # Add the summary and message text
    draw.text((40, 60), summary, font=font_summary, fill="white")
    draw.text((40, 105), message, font=font_message, fill="white")

    # Save image and return
    output_image = BytesIO()
    background.save(output_image, format="PNG")
    output_image.seek(0)
    return output_image

# Streamlit UI components
st.title("Banner Generator")

# Inputs
title = st.text_input("Title", "Keep your car insurance valid")
summary = st.text_input("Summary", "45% off with NCD")
message = st.text_input("Message", "Compare & select a plan for your car insurance.")
banner_image_url = st.text_input("Banner Image URL", "https://cdn.tngdigital.com.my/resource/2025/1/24/b2d53e8f-93a8-42f4-a1e8-557058a75325.png")

# Color picker for dynamic box color
box_color = st.color_picker("Select Box Color", "#00e600")

# Button to generate banner
if st.button("Generate Banner"):
    # Generate banner with selected parameters
    banner_image = create_banner(title, summary, message, banner_image_url, box_color)
    
    # Display the generated banner
    st.image(banner_image, caption="Generated Banner", use_column_width=True)

    # Provide embed code
    st.subheader("Embed Code")
    embed_code = f'<iframe src="{banner_image_url}" width="600" height="220" frameborder="0"></iframe>'
    st.code(embed_code, language='html')
