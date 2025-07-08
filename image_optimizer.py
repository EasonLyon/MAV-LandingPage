#!/usr/bin/env python3
"""
Image Optimizer Script
Compresses images for web optimization while maintaining quality
"""

import os
import sys
import json
import shutil
from pathlib import Path
from PIL import Image, ImageOps
import argparse
from datetime import datetime

class ImageOptimizer:
    def __init__(self, backup_dir="backup_images"):
        self.backup_dir = Path(backup_dir)
        self.backup_dir.mkdir(exist_ok=True)
        
        # Compression settings based on file size
        self.compression_tiers = {
            'high': {'quality': 70, 'max_width': 1920, 'max_height': 1080},
            'medium': {'quality': 80, 'max_width': 2400, 'max_height': 1600},
            'light': {'quality': 85, 'max_width': 3000, 'max_height': 2000},
            'skip': {'quality': 90, 'max_width': 4000, 'max_height': 3000}
        }
        
        self.stats = {
            'total_files': 0,
            'processed_files': 0,
            'skipped_files': 0,
            'original_size': 0,
            'compressed_size': 0,
            'files_processed': []
        }
        
    def get_file_size_mb(self, file_path):
        """Get file size in MB"""
        return os.path.getsize(file_path) / (1024 * 1024)
    
    def get_compression_tier(self, file_size_mb):
        """Determine compression tier based on file size"""
        if file_size_mb >= 15:
            return 'high'
        elif file_size_mb >= 5:
            return 'medium'
        elif file_size_mb >= 2:
            return 'light'
        else:
            return 'skip'
    
    def backup_file(self, file_path):
        """Create backup of original file"""
        rel_path = os.path.relpath(file_path)
        backup_path = self.backup_dir / rel_path
        backup_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(file_path, backup_path)
        return backup_path
    
    def optimize_image(self, file_path, dry_run=False):
        """Optimize a single image file"""
        try:
            original_size = self.get_file_size_mb(file_path)
            tier = self.get_compression_tier(original_size)
            
            if tier == 'skip':
                print(f"⏩ Skipping {file_path} ({original_size:.2f}MB - already optimized)")
                self.stats['skipped_files'] += 1
                return
            
            settings = self.compression_tiers[tier]
            
            if dry_run:
                print(f"🔍 Would compress {file_path} ({original_size:.2f}MB) using {tier} compression")
                return
            
            # Backup original
            backup_path = self.backup_file(file_path)
            
            # Open and process image
            with Image.open(file_path) as img:
                # Convert to RGB if necessary
                if img.mode in ('RGBA', 'LA', 'P'):
                    img = img.convert('RGB')
                
                # Auto-orient based on EXIF data
                img = ImageOps.exif_transpose(img)
                
                # Resize if too large
                if img.width > settings['max_width'] or img.height > settings['max_height']:
                    img.thumbnail((settings['max_width'], settings['max_height']), Image.Resampling.LANCZOS)
                
                # Save with compression
                img.save(file_path, 'JPEG', quality=settings['quality'], optimize=True)
            
            new_size = self.get_file_size_mb(file_path)
            compression_ratio = ((original_size - new_size) / original_size) * 100
            
            print(f"✅ Compressed {file_path}")
            print(f"   {original_size:.2f}MB → {new_size:.2f}MB ({compression_ratio:.1f}% reduction)")
            
            self.stats['processed_files'] += 1
            self.stats['original_size'] += original_size
            self.stats['compressed_size'] += new_size
            self.stats['files_processed'].append({
                'file': str(file_path),
                'original_size_mb': original_size,
                'compressed_size_mb': new_size,
                'compression_ratio': compression_ratio,
                'tier': tier,
                'backup_path': str(backup_path)
            })
            
        except Exception as e:
            print(f"❌ Error processing {file_path}: {str(e)}")
    
    def find_images(self, directory="."):
        """Find all image files in directory"""
        image_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.webp'}
        image_files = []
        
        for root, dirs, files in os.walk(directory):
            for file in files:
                if Path(file).suffix.lower() in image_extensions:
                    image_files.append(os.path.join(root, file))
        
        return sorted(image_files)
    
    def generate_report(self):
        """Generate optimization report"""
        if self.stats['processed_files'] == 0:
            print("\n📊 No files were processed")
            return
        
        total_reduction = self.stats['original_size'] - self.stats['compressed_size']
        avg_reduction = (total_reduction / self.stats['original_size']) * 100
        
        print(f"\n📊 Optimization Report")
        print(f"=" * 50)
        print(f"Total files found: {self.stats['total_files']}")
        print(f"Files processed: {self.stats['processed_files']}")
        print(f"Files skipped: {self.stats['skipped_files']}")
        print(f"Original size: {self.stats['original_size']:.2f}MB")
        print(f"Compressed size: {self.stats['compressed_size']:.2f}MB")
        print(f"Space saved: {total_reduction:.2f}MB ({avg_reduction:.1f}% reduction)")
        
        # Save detailed report
        report_path = f"optimization_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(report_path, 'w') as f:
            json.dump(self.stats, f, indent=2)
        print(f"Detailed report saved to: {report_path}")
    
    def run(self, directory=".", dry_run=False, file_pattern=None):
        """Run the optimization process"""
        print(f"🚀 Starting image optimization in: {directory}")
        print(f"Backup directory: {self.backup_dir}")
        
        if dry_run:
            print("🔍 DRY RUN MODE - No files will be modified")
        
        image_files = self.find_images(directory)
        
        if file_pattern:
            image_files = [f for f in image_files if file_pattern in f]
        
        self.stats['total_files'] = len(image_files)
        
        if not image_files:
            print("No image files found!")
            return
        
        print(f"Found {len(image_files)} image files")
        
        for i, file_path in enumerate(image_files, 1):
            print(f"\n[{i}/{len(image_files)}] Processing: {file_path}")
            self.optimize_image(file_path, dry_run)
        
        if not dry_run:
            self.generate_report()

def main():
    parser = argparse.ArgumentParser(description='Optimize images for web use')
    parser.add_argument('directory', nargs='?', default='.', help='Directory to process (default: current)')
    parser.add_argument('--dry-run', action='store_true', help='Show what would be done without making changes')
    parser.add_argument('--pattern', help='Only process files containing this pattern')
    parser.add_argument('--backup-dir', default='backup_images', help='Backup directory (default: backup_images)')
    
    args = parser.parse_args()
    
    optimizer = ImageOptimizer(backup_dir=args.backup_dir)
    optimizer.run(args.directory, dry_run=args.dry_run, file_pattern=args.pattern)

if __name__ == "__main__":
    main()