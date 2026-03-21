#!/bin/bash
# Generate Instagram Carousel Post 2 Images
# Theme: 3 Sätze für weniger Schulstress

cd /root/life/elternratgeber-system/marketing/carousel_post_2

echo "🎨 Generiere Karussell-Bilder für Post 2..."

# Slide 1: Cover
infsh app run falai/flux-2-klein-lora --input '{
  "prompt": "Instagram carousel cover design, warm orange and yellow gradient background, friendly flat illustration of parent and child talking peacefully, text '3 Sätze für weniger Schulstress' in bold modern sans-serif font centered, decorative elements like hearts and stars, clean professional social media graphic style, 1080x1350px portrait format",
  "aspect_ratio": "3:4"
}' --output slide_1_cover.png

# Slide 2: Problem (What we say vs what kids hear)
infsh app run falai/flux-2-klein-lora --input '{
  "prompt": "Split screen illustration, left side parent speech bubbles with text 'Das schaffst du schon!' and 'Warum kann Maria das?', right side sad child thinking bubbles with 'Ich bin nicht gut genug', soft pink and blue pastel colors, emotional but not scary, educational infographic style, clean modern design, 1080x1350px",
  "aspect_ratio": "3:4"
}' --output slide_2_problem.png

# Slide 3: Solution 1 (Validation)
infsh app run falai/flux-2-klein-lora --input '{
  "prompt": "Warm illustration of mother comforting child at home, cozy living room setting, peaceful atmosphere, mother saying empathetic words, child feeling understood and relaxed, soft warm lighting, yellow and orange tones, supportive parenting moment, flat illustration style, 1080x1350px portrait",
  "aspect_ratio": "3:4"
}' --output slide_3_solution1.png

# Slide 4: Solutions 2+3 (Checklist style)
infsh app run falai/flux-2-klein-lora --input '{
  "prompt": "Clean checklist infographic design, mint green and white background, two large checkmarks with text areas, helpful parenting tips layout, modern sans-serif typography space, friendly icons and illustrations, educational content design, professional Instagram carousel style, 1080x1350px portrait format",
  "aspect_ratio": "3:4"
}' --output slide_4_solutions.png

# Slide 5: CTA / Follow
infsh app run falai/flux-2-klein-lora --input '{
  "prompt": "Instagram follow CTA design, gradient purple to pink background, large bookmark icon and follow button graphic, arrows pointing to action areas, social media engagement design, modern flat style, text space reserved at bottom, call-to-action layout, clean professional finish, 1080x1350px portrait",
  "aspect_ratio": "3:4"
}' --output slide_5_cta.png

echo "✅ Alle 5 Bilder generiert!"
echo "📁 Location: /root/life/elternratgeber-system/marketing/carousel_post_2/"
ls -la *.png
