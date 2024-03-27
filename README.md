# Script to scrape research papers.

This is a simple Python script to scrape research papers from the Emergent Mind website and save them to an Excel workbook. The idea is to save papers you come across for easier searching and reading later.

I personally have the workbook saved in my Google Drive so that I can access it from anywhere.

This script could be adapted to use Arxiv directly with minimal changes. Please feel free to submit a PR if you go down that route.

## Setup

You'll need a `.env` file in the root directory:
```sh
cp .env.example .env
```

Then fill in the `GOOGLE_DRIVE_PATH` with the path to your Google Drive folder where you want to save the Excel workbook.

## Usage

To scrape a URL:
```sh
python main.py <url>
```

You can also include a comment for the notes field:
```sh
python main.py <url> --notes "This is a great paper!"
```

Finally, there's a batch script to scrape multiple URLs at once:
```sh
python batch.py
```

Make sure to have a `batch.txt` file with one URL per line.