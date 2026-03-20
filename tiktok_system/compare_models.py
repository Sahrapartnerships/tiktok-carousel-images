#!/usr/bin/env python3
"""
Compare Ideogram V3 vs FLUX-Pro for TikTok carousel
Same prompt theme, optimized for each model
"""

import os
import re
import urllib.request
from pathlib import Path

OUTPUT_DIR = Path('/root/life/elternratgeber-system/tiktok_system/images/model_comparison')
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Load credentials
with open(os.path.expanduser('~/.fal-credentials')) as f:
    content = f.read()
    match = re.search(r'export FAL_KEY="([^"]+)"', content)
    if match:
        os.environ['FAL_KEY'] = match.group(1)

import fal_client

# Same theme: "Stressed child with homework"
# Optimized for each model's strengths

print('=' * 60)
print('🎨 MODEL COMPARISON: Ideogram V3 vs FLUX-Pro')
print('=' * 60)

# IDEOGRAM V3 - Best for: Illustrations, clean design, editorial style
print('\n📐 IDEOGRAM V3 (Optimized for illustration/editorial)')
print('-' * 60)

ideogram_prompt = '''Editorial illustration, modern flat design style. A worried child character sitting at a desk with homework, hands on cheeks looking stressed and overwhelmed. Concerned parent standing behind. Soft coral pink, mint green, cream color palette. Warm cozy home setting with window light. Clean composition, smooth gradients, trendy magazine illustration aesthetic. Emotional storytelling, professional editorial quality.'''

print(f'Prompt:\n{ideogram_prompt}\n')

result_ideo = fal_client.subscribe(
    'fal-ai/ideogram/v3',
    arguments={
        'prompt': ideogram_prompt,
        'aspect_ratio': '3:4',
    },
    with_logs=False
)

url_ideo = result_ideo['images'][0]['url']
req = urllib.request.Request(url_ideo, headers={'User-Agent': 'Mozilla/5.0'})
with urllib.request.urlopen(req, timeout=120) as response:
    img_data = response.read()

path_ideo = OUTPUT_DIR / '01_ideogram_v3.png'
with open(path_ideo, 'wb') as f:
    f.write(img_data)

print(f'✅ Saved: {path_ideo.name}')
print(f'   Size: {len(img_data)/1024:.1f} KB')
print(f'   Cost: ~$0.04')
print(f'   URL: {url_ideo}')

# FLUX-PRO - Best for: Photorealism, cinematic quality, detail
print('\n📸 FLUX-PRO (Optimized for cinematic/detail)')
print('-' * 60)

flux_prompt = '''3D rendered illustration, Pixar Disney animation style, cinematic quality. A cute stylized child character with big expressive eyes sitting at a modern desk, hands on cheeks looking worried and stressed at homework papers. Concerned parent figure in soft-focus background. Soft cinematic lighting, depth of field, bokeh. Coral pink and mint green color palette, warm cozy interior. Professional 3D render, octane quality, trending on ArtStation.'''

print(f'Prompt:\n{flux_prompt}\n')

result_flux = fal_client.subscribe(
    'fal-ai/flux-pro',
    arguments={
        'prompt': flux_prompt,
        'aspect_ratio': '3:4',
    },
    with_logs=False
)

url_flux = result_flux['images'][0]['url']
req = urllib.request.Request(url_flux, headers={'User-Agent': 'Mozilla/5.0'})
with urllib.request.urlopen(req, timeout=120) as response:
    img_data = response.read()

path_flux = OUTPUT_DIR / '02_flux_pro.png'
with open(path_flux, 'wb') as f:
    f.write(img_data)

print(f'✅ Saved: {path_flux.name}')
print(f'   Size: {len(img_data)/1024:.1f} KB')
print(f'   Cost: ~$0.03-0.05')
print(f'   URL: {url_flux}')

print('\n' + '=' * 60)
print('📊 COMPARISON SUMMARY')
print('=' * 60)
print('''
IDEOGRAM V3:
  ✅ Best for: Illustrations, clean design, editorial style
  ✅ Style: Flat design, smooth gradients, trendy
  ✅ Text: Good for layouts with text
  ✅ Speed: Medium
  💰 Cost: ~$0.04/image

FLUX-PRO:
  ✅ Best for: Photorealistic 3D, cinematic, high detail
  ✅ Style: Pixar-like, depth, realistic lighting
  ✅ Detail: Higher fidelity, more realistic
  ✅ Versatility: Wide range of styles
  💰 Cost: ~$0.03-0.05/image
''')

print('\n🎉 Comparison images ready!')
print(f'📁 Location: {OUTPUT_DIR}')
