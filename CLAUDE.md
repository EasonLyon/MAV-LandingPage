# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a static HTML landing page repository focused on creating business and marketing landing pages. The project is hosted on GitHub Pages and contains multiple landing page templates and variations.

## Key Architecture

- **Static HTML Pages**: All landing pages are standalone HTML files using Tailwind CSS and modern responsive design
- **Template-Based Structure**: Landing pages follow consistent patterns with sections like hero, problem/solution, features, testimonials, pricing, and CTA
- **Python Generation Scripts**: Two Python utilities for content generation and index management
- **Organized by Purpose**: Files are grouped by project (MAV/, WorldMasterclass/, Template/) and naming conventions indicate versions and AI tools used

## Essential Commands

### Generate HTML Index
```bash
python generate_index.py
```
Creates an index.html file listing all HTML files in the repository with organized folder structure.

### Install Dependencies
```bash
npm install
```
Installs Preline UI components.

## File Structure

- **Landing Pages**: Named with prefixes indicating AI tool used (00-LP for templates, 01-LP for variations)
- **MAV/**: Marketing and sales landing pages
- **WorldMasterclass/**: Educational/workshop landing pages  
- **Template/**: Base templates for new pages
- **generate_index.py**: Creates organized index of all HTML files

## Development Notes

- All HTML pages use Tailwind CSS via CDN
- Common libraries: AOS (animations), Google Fonts (Inter), custom styling
- Pages are mobile-responsive with sticky navigation
- Hosted on GitHub Pages with CNAME configuration
- Git workflow includes staged changes to multiple HTML files typically