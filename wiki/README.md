# LuminoraCore Wiki - README

This folder contains the content for the GitHub Wiki at:
https://github.com/luminoracore/luminoracore/wiki

---

## 📁 Wiki Pages Included

### Essential Pages (Created)
1. **Home.md** - Wiki home page with overview and quick links
2. **Getting-Started.md** - Installation and first steps guide
3. **FAQ.md** - Frequently asked questions
4. **Troubleshooting.md** - Common problems and solutions
5. **Core-Concepts.md** - Deep dive into personalities, blending, compilation

### How to Publish to GitHub Wiki

Since GitHub Wiki is a separate system, you need to copy these files manually:

#### Option 1: Via GitHub Web Interface (Easiest)

1. Go to: https://github.com/luminoracore/luminoracore/wiki
2. Click "New Page"
3. Name the page (e.g., "Home", "Getting-Started", "FAQ")
4. Copy the content from the corresponding `.md` file here
5. Click "Save Page"

#### Option 2: Via Git Clone (Advanced)

```bash
# Clone the wiki repository
git clone https://github.com/luminoracore/luminoracore.wiki.git

# Copy files
cp wiki/*.md luminoracore.wiki/

# Push to wiki
cd luminoracore.wiki
git add .
git commit -m "Add initial wiki pages"
git push origin master
```

---

## 📋 Wiki Structure

### Recommended Page Order

1. **Home** - First page visitors see
2. **Getting Started** - Quick installation guide
3. **Core Concepts** - Understanding personalities, blending, compilation
4. **FAQ** - Common questions
5. **Troubleshooting** - Problem solving

### Future Pages (To Add)

- **Tutorials** - Step-by-step guides
- **API Reference** - Complete API documentation
- **Examples** - Code recipes and patterns
- **Deployment Guide** - Production deployment
- **Advanced Topics** - Custom providers, storage backends
- **Contributing** - How to contribute

---

## ✅ Checklist Before Publishing

- [ ] Review all content for accuracy
- [ ] Test all code examples
- [ ] Verify all links work
- [ ] Check formatting (headings, lists, code blocks)
- [ ] Spell check
- [ ] Update version numbers if needed
- [ ] Add screenshots where helpful
- [ ] Cross-link between pages

---

## 🔗 Important Links to Include

Make sure these links are correct before publishing:

- Main README: `https://github.com/luminoracore/luminoracore/blob/main/README.md`
- Quick Start: `https://github.com/luminoracore/luminoracore/blob/main/QUICK_START.md`
- Installation Guide: `https://github.com/luminoracore/luminoracore/blob/main/INSTALLATION_GUIDE.md`
- Creating Personalities: `https://github.com/luminoracore/luminoracore/blob/main/CREATING_PERSONALITIES.md`
- Cheatsheet: `https://github.com/luminoracore/luminoracore/blob/main/CHEATSHEET.md`
- Contributing: `https://github.com/luminoracore/luminoracore/blob/main/CONTRIBUTING.md`

---

## 📝 Content Guidelines

When adding new wiki pages:

1. **Keep it clear** - Use simple language
2. **Show examples** - Code snippets for every concept
3. **Link internally** - Cross-reference other wiki pages
4. **Update dates** - Add "Last updated: [date]" at bottom
5. **Test code** - All code examples must work
6. **Be consistent** - Use same formatting style

---

## 🎨 Formatting Tips

### Headers
```markdown
# Page Title (H1 - only one per page)
## Section (H2)
### Subsection (H3)
```

### Code Blocks
````markdown
```python
# Python code
from luminoracore import Personality
```

```bash
# Shell commands
luminoracore validate file.json
```
````

### Tables
```markdown
| Column 1 | Column 2 |
|----------|----------|
| Data 1   | Data 2   |
```

### Callouts
```markdown
**✅ Tip:** Helpful information

**⚠️ Warning:** Important notice

**❌ Error:** Common mistake
```

---

## 🔄 Maintenance

### When to Update Wiki

- ✅ New version released
- ✅ New features added
- ✅ Breaking changes
- ✅ Common issues discovered
- ✅ User feedback

### Version History

- **v1.0.0** (October 2025)
  - Initial wiki pages created
  - Home, Getting Started, FAQ, Troubleshooting, Core Concepts

---

_This folder is for wiki content backup and preparation. The actual wiki is published at: https://github.com/luminoracore/luminoracore/wiki_

