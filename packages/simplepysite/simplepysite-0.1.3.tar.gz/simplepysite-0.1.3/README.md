# Simplepysite

This is a super-simple static site generator. You can use it to write markdown files and quickly convert them to nicely-styled html. It is basically just some convenience functions built on top of the markdown library (required). This package will provide you with a very simple template for writing blog-like posts, as well as some simple css. Standard markdown syntax applies, and this is true for images and links.

## Install

Make sure you have activated your virtual environment and use pip:

```
python -m pip install simplepysite
```

## Usage
cd to the directory where you would like to create a site, and run the following:

```
python -m simplepysite
```

This will create a template site for you. The "pages" folder contains the markdown files, and html files will be created wherever this command is run.

If you are working this into a workflow, you can also import it as follows:

```python
from simplepysite.site import establish_site, build_site


establish_site() # creates a pages folder, a sample markdown file, and a generic style.css which can be edited

build_site() # assuming there is a "pages" folder, all markdown files contained therein are converted to html
```