"""Check dataset status"""
import os
from pathlib import Path

dataset_path = Path('dataset')
gestures = ['scroll_up', 'scroll_down', 'swipe_left', 'swipe_right', 
            'pinch_zoom', 'thumb_down_close', 'mute_toggle']

print('\nDataset Status:')
print('='*60)

if not dataset_path.exists():
    print('❌ Dataset folder not found!')
    exit(1)

total = 0
for gesture in gestures:
    folder = dataset_path / gesture
    if folder.exists():
        count = len(list(folder.glob('*.png')))
        total += count
        status = '✓' if count >= 100 else '⚠'
        print(f'{status} {gesture:20} {count:4} images')
    else:
        print(f'❌ {gesture:20} MISSING')

print('='*60)
print(f'Total images: {total}')

if total < 350:
    print('\n❌ Too few images (need at least 350)')
    print('Run: python quick_data_collector.py')
elif total < 700:
    print('\n⚠ Low image count (recommended: 700+)')
    print('Should work but accuracy may be lower')
else:
    print('\n✓ Good dataset size!')
