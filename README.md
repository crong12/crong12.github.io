# Chin Rong Ong - Data Science Portfolio

[![Deploy to GitHub Pages](https://github.com/crong12/crong12.github.io/actions/workflows/deploy.yml/badge.svg)](https://github.com/crong12/crong12.github.io/actions/workflows/deploy.yml)

Welcome to my data science portfolio! This repository hosts interactive Python notebooks and data visualizations built with [marimo](https://marimo.io) and deployed to GitHub Pages.

## 🌟 Features

- **Interactive Notebooks**: Fully interactive Python notebooks that run in your browser via WebAssembly
- **No Server Required**: All computations happen client-side - no backend needed!
- **Live Code Editing**: Notebooks support live code editing and execution
- **Beautiful Visualizations**: Interactive charts and visualizations using modern Python libraries

## 📊 Current Projects

### One Piece Dialogue Analysis
An interactive analysis of dialogue patterns and emotional content from episodes 293-774 of the One Piece anime series.

**Features:**
- 📈 Interactive word clouds for each Straw Hat character
- 😊 Emotion analysis and visualization
- 🎨 Custom character-themed visualizations
- 📊 Comparative analysis across characters

## 🚀 Local Development

### Prerequisites

- Python 3.12 or higher
- [uv](https://github.com/astral-sh/uv) package manager

### Installation

1. Clone the repository:
```bash
git clone https://github.com/crong12/crong12.github.io.git
cd crong12.github.io
```

2. Install uv (if you haven't already):
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

3. Run a marimo notebook locally:
```bash
# For apps (run mode with hidden code)
uvx marimo run apps/wordclouds_explorer.py

# For notebooks (edit mode with visible code)
uvx marimo edit notebooks/your_notebook.py
```

### Building the Site Locally

To build the entire site locally:

```bash
# Build all notebooks to static HTML
uv run build.py

# Serve the site locally
python -m http.server -d _site
```

Then visit `http://localhost:8000` in your browser.

## 📁 Project Structure

```
crong12.github.io/
├── apps/                    # marimo apps (run mode - code hidden)
│   ├── public/             # Data files, images, and assets for apps
│   ├── one_piece_analysis.py
│   └── wordclouds_explorer.py
├── notebooks/              # marimo notebooks (edit mode - code visible)
│   └── public/            # Data files and assets for notebooks
├── templates/              # Jinja2 templates for the landing page
│   └── index.html.j2
├── assets/                 # Static assets (images, etc.)
│   └── img/
├── .github/
│   └── workflows/
│       └── deploy.yml     # GitHub Actions workflow
├── build.py               # Build script for exporting notebooks
├── index.html            # Root redirect page
└── README.md
```

## 🛠️ Adding New Content

### Adding a New App (Code Hidden)

1. Create a new marimo file in the `apps/` directory:
```bash
uvx marimo new apps/my_new_app.py
```

2. Add your data files to `apps/public/`

3. In your marimo app, load data using:
```python
import marimo as mo
data_path = mo.notebook_location() / "public" / "my_data.csv"
```

4. Push to GitHub - the app will be automatically built and deployed!

### Adding a New Notebook (Code Visible)

1. Create a new marimo file in the `notebooks/` directory:
```bash
uvx marimo new notebooks/my_analysis.py
```

2. Add your data files to `notebooks/public/`

3. Push to GitHub - automatic deployment will handle the rest!

## 🎨 Customizing the Landing Page

The landing page is generated from `templates/index.html.j2`. To customize:

1. Edit the template file
2. The template has access to:
   - `notebooks`: List of notebook objects with `display_name` and `html_path`
   - `apps`: List of app objects with `display_name` and `html_path`

3. Push changes - the site will rebuild automatically

## 🔄 Deployment

This site uses GitHub Actions for automatic deployment:

1. **Push to main branch** → Triggers the workflow
2. **Build step** → Exports all marimo notebooks to HTML/WebAssembly
3. **Deploy step** → Publishes to GitHub Pages

### Manual Deployment

You can also trigger deployment manually:
1. Go to the "Actions" tab in GitHub
2. Select "Deploy to GitHub Pages"
3. Click "Run workflow"

## 📚 Technologies Used

- **[marimo](https://marimo.io)**: Reactive Python notebooks
- **WebAssembly**: Run Python in the browser
- **GitHub Actions**: CI/CD pipeline
- **GitHub Pages**: Static site hosting
- **Python Libraries**:
  - pandas: Data manipulation
  - altair: Interactive visualizations
  - Pillow: Image processing
  - And more!

## 📖 About marimo

marimo is a next-generation Python notebook that's:
- ✨ **Reactive**: Changes propagate automatically
- 🎯 **Interactive**: Rich UI elements and visualizations
- 🚀 **Git-friendly**: Notebooks are stored as pure Python files
- 🌐 **Shareable**: Export to WebAssembly for browser execution

Learn more at [marimo.io](https://marimo.io)

## 🤝 Connect With Me

- 💼 [LinkedIn](https://linkedin.com/in/ongchinrong12)
- 🐙 [GitHub](https://github.com/crong12)
- 📧 [Email](mailto:ongchinrong12@gmail.com)

## 📝 License

This project is open source and available under the [MIT License](LICENSE).

---

**Note**: The `_archive_jekyll/` directory contains the old Jekyll-based site for reference. The site has been migrated to use marimo for a more interactive experience.
