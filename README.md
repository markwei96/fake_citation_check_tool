# Fake Citation Check Tool

[中文版](./README_CN.md)

A command-line tool to verify whether citations in a `.bib` bibliography file are legitimate by searching their titles on Google Scholar.

## Background

With the rise of AI-generated content, fabricated citations have become a growing concern in academic writing. This tool helps researchers quickly identify potentially fake references by cross-checking each citation title against Google Scholar search results.

## How It Works

1. Parses the input `.bib` file and extracts all citation entries.
2. Searches each citation title on Google Scholar via API (Scrapingdog or Serpapi).
3. Compares the search results with the original title (exact match).
4. Outputs a CSV report marking each entry as **OK** (found) or **Fake** (not found), along with a PDF link if available.

## Project Structure

```
fake_citation_check_tool/
├── main.py          # Entry point, argument parsing and main logic
├── spider.py        # Google Scholar API client (Scrapingdog & Serpapi)
├── bib_process.py   # .bib file parser
└── config.py        # API key configuration
```

## Requirements

- Python 3
- `requests` library

## Installation

```bash
pip install requests
```

## Configuration

Edit `config.py` and replace the placeholder strings with your actual API keys:

```python
SCRAP_API_KEY = {
    "scrapingdog": ["YOUR_SCRAPINGDOG_API_KEY"],
    "serpapi": ["YOUR_SERPAPI_API_KEY"],
}
```

You can provide multiple keys per provider. The tool automatically selects the key with the most remaining credits.

| Provider    | Free Tier                          |
|-------------|------------------------------------|
| Scrapingdog | 1000 credits/month (5 per search)  |
| Serpapi     | 250 searches/month (1 per search)  |

## Usage

```bash
python main.py --bib_file_path <path_to_bib_file> [--output_path <path_to_output_csv>]
```

### Arguments

| Argument          | Required | Default         | Description                  |
|-------------------|----------|-----------------|------------------------------|
| `--bib_file_path` | Yes      | `./ref.bib`     | Path to the `.bib` file      |
| `--output_path`   | No       | `./results.csv` | Path to the output CSV file  |

### Example

```bash
python main.py --bib_file_path ./references.bib --output_path ./check_results.csv
```

### Output Format

The output CSV contains the following columns:

```
Index,Status,Title,PDF link
1,OK,Attention Is All You Need,https://arxiv.org/pdf/...
2,Fake,Some Fabricated Paper Title,
```

## License

MIT
