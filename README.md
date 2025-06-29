# WoS-JCR Impact Factor Explorer 2023

## Description
A web application that enables users to explore and analyze journal impact factors from Web of Science (WoS) Journal Citation Reports, enhanced with country and research area data from SCImago Journal Rank (SJR).

## URL
https://wos-jcr-2025.streamlit.app/ 

## Features
- **Interactive Journal Search**
  - Real-time search with auto-complete suggestions
  - Dynamic filtering of journal names

- **Advanced Filtering Options**
  - Impact Factor Range (JIF 2024)
  - Journal Quartile (Q1-Q4)
  - Publisher
  - Country of Publication
  - Research Areas

- **Flexible Data Display**
  - Interactive Data Editor
  - Compact Table View
  - Full-Width Table Display
  - Customizable column widths

- **Data Export**
  - Download filtered results as CSV
  - Preserve all metadata in exports

## Installation

### Prerequisites
- Python 3.8 or higher
- Git

### Setup
```bash
# Clone the repository
git clone https://github.com/yourusername/wos-jcr-explorer.git
cd wos-jcr-explorer

# Create and activate virtual environment (optional but recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the application
streamlit run app.py
```

### Requirements
```
streamlit
pandas
numpy
openpyxl
xlrd
requests
```

## Usage

1. **Launch the Application**
   ```bash
   streamlit run app.py
   ```

2. **Search for Journals**
   - Type journal name in the search box
   - Click on suggestions to auto-fill

3. **Apply Filters**
   - Set Impact Factor range using the slider
   - Select multiple options for Quartile, Publisher, Country
   - Choose relevant research areas

4. **View and Export Data**
   - Switch between different view modes
   - Download filtered results using the export button

## Data Structure

The application uses an Excel file with the following schema:
```
- Journal Name: str
- IF (Impact Factor): float
- Q (Quartile): str
- Publisher: str
- Country: str
- Areas: list[str]
- Year: int
```

## Project Structure
```
wos-jcr-explorer/
├── app.py
├── requirements.txt
├── README.md
├── .streamlit/
│   └── config.toml
└── data/
    └── JCR_Enriched_With_ISSN_Matching.xlsx
```

## Contributing
1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## Developer
Developed by [Abhijit Debnath](https://github.com/theabhijitdn)

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details

## Acknowledgments
- Web of Science for Journal Citation Reports data
- SCImago for Journal & Country Rank data
- Streamlit team for the excellent framework

## Support
For support, email your-email@example.com or open an issue in the repository.

---

**Note:** Replace placeholder URLs, usernames, and email addresses with your actual information before publishing.
