*current status: in-development*

# Board Game Web-scraping: Finding the best 2-player Games

## Description:
Scraping the weekly 2-player "boardgames" sub-reddit posts for the past year, we will count and visualize which games are mentioned the most frequently.

<img src="./imgs/larger_img.png">

#### Tools
1. Web-scraping:
   Scrapy, Requests
2. Data Cleaning: Pandas
3. Text parsing: Spacy, NLTK, SciKitLearn
4. Visualization: Matplotlib, Seaborn, Plotly 


## Project layout

main.py - main program

/data: stored data as csv after extracting from website json objects

/imgs: figures, plots, readme images

/src: mini-modules to be imported into the main program

/tests: what are tests?

## How to Run

Clone the repository then once inside the repository, use the following shell commands in order.

```bash
$: conda env create -f environment.yml

$: conda activate env

$: python main.py

```
