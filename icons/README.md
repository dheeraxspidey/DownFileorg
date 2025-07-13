# Custom Folder Icons

This folder contains custom icons (.ico files) for the AI File Organizer folders.

## Required Icon Files

Place these 7 icon files in this folder with these exact names:

1. **education_finance.ico** - For Education and Finance files
2. **movies.ico** - For Movie and Video files  
3. **games.ico** - For Game files
4. **apps.ico** - For Application files
5. **entertainment.ico** - For Entertainment files
6. **career.ico** - For Career related files
7. **others.ico** - For Other/miscellaneous files

## Icon Requirements

- **Format**: .ico files only
- **Size**: 256x256 or 128x128 pixels recommended
- **Quality**: Use high-quality icons for best appearance
- **Naming**: Must match the exact filenames listed above (case-sensitive)

## Where to Get Icons

You can download free icons from:
- [Flaticon](https://www.flaticon.com/) - Convert to .ico
- [IconArchive](https://iconarchive.com/) - Many .ico files available
- [Icons8](https://icons8.com/) - Free icons (convert to .ico)
- [Iconify](https://iconify.design/) - Large collection

## Converting Icons

If you have PNG/SVG icons, you can convert them to .ico format using:
- Online converters (search "PNG to ICO converter")
- GIMP (free image editor)
- Paint.NET with plugins
- IcoFX (icon editor)

## Testing

Run `python folder_icon_manager.py` to:
1. Check which icons are available
2. See which ones are missing
3. Create test folders to preview the icons

## Fallback

If custom icons are not found, the program will automatically use Windows built-in icons as fallback.
