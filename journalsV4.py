import streamlit as st
import pandas as pd

# Set page config with minimal padding
st.set_page_config(
    layout="wide", 
    page_title="WoS-JCR Impact Factor Explorer 2025",
    initial_sidebar_state="collapsed"
)

# Custom CSS to reduce padding at the top and make better use of space
st.markdown("""
<style>
    .block-container {
        padding-top: 3rem;
        padding-bottom: 0rem;
    }
    h1 {
        margin-top: 3 !important;
        padding-top: 0 !important;
    }
    .stMarkdown p {
        margin-bottom: 0.5rem;
    }
    hr {
        margin: 0.5rem 0;
    }
    /* Make the slider more left-oriented */
    .stSlider {
        padding-right: 10%;
    }
</style>
""", unsafe_allow_html=True)

# Title section - moved higher up with less spacing
st.markdown("# WoS-JCR Impact Factor Explorer 2025")
st.markdown("*Navigate journal impact factors from Web of Science with country and research area data from SCImago Journal Rank*")
st.markdown("*Developed by [Abhijit Debnath](https://github.com/theabhijitdn)*")

# Add a thinner horizontal line
st.markdown("<hr style='margin: 0.5rem 0; height: 1px'>", unsafe_allow_html=True)

@st.cache_data
def load_data():
    df = pd.read_csv('JCR_Enriched_With_ISSN_Matching.csv')
    df.rename(columns={
        'JIF 2024': 'IF',
        'JIF Quartile': 'Q',
        'Journal Name': 'Journal',
        'JCR Year': 'Year'
    }, inplace=True)
    df['IF'] = pd.to_numeric(df['IF'], errors='coerce')
    # Split the Areas column into a list
    df['Areas'] = df['Areas'].apply(lambda x: str(x).split('; ') if pd.notna(x) else [])
    return df

data = load_data()

# Layout with 2 columns: filters (25%) and data display (75%)
left_col, right_col = st.columns([1, 3])

with left_col:
    st.header('Filter Options')

    if 'if_min' not in st.session_state:
        st.session_state['if_min'] = float(data['IF'].min())
    if 'if_max' not in st.session_state:
        st.session_state['if_max'] = float(data['IF'].max())
    if 'quartile_filter' not in st.session_state:
        st.session_state['quartile_filter'] = []
    if 'publisher_filter' not in st.session_state:
        st.session_state['publisher_filter'] = []
    if 'country_filter' not in st.session_state:
        st.session_state['country_filter'] = []
    if 'areas_filter' not in st.session_state:
        st.session_state['areas_filter'] = []
    if 'search_term' not in st.session_state:
        st.session_state['search_term'] = ""

    # Journal Search
    search_term = st.text_input("Search Journal by Name", value=st.session_state['search_term'])
    st.session_state['search_term'] = search_term

    # Impact Factor Range - using slider instead of number inputs for better UX
    st.subheader("Impact Factor Range (JIF 2024)")
    
    # Use a slider with custom width to make it more left-oriented
    if_range = st.slider(
        "Impact Factor",
        min_value=float(data['IF'].min()),
        max_value=float(data['IF'].max()),
        value=(float(st.session_state['if_min']), float(st.session_state['if_max'])),
        step=0.1,
        format="%.2f"
    )
    if_min, if_max = if_range
    st.session_state['if_min'] = if_min
    st.session_state['if_max'] = if_max
    
    # Display the current range values in a more compact way
    col1, col2 = st.columns(2)
    with col1:
        st.write(f"Min: {if_min:.2f}")
    with col2:
        st.write(f"Max: {if_max:.2f}")

    # Quartile
    quartile_filter = st.multiselect('JIF Quartile', data['Q'].dropna().unique(), default=st.session_state['quartile_filter'])

    # Publisher
    publisher_filter = st.multiselect('Publisher', data['Publisher'].dropna().unique(), default=st.session_state['publisher_filter'])

    # Country
    country_filter = st.multiselect('Country', data['Country'].dropna().unique(), default=st.session_state['country_filter'])

    # Areas
    # Get all unique areas by flattening the lists
    all_areas = sorted(set([area.strip() for sublist in data['Areas'] for area in sublist if area.strip()]))
    areas_filter = st.multiselect('Areas', all_areas, default=st.session_state['areas_filter'])

# Filter logic
def filter_data(df, if_min, if_max, quartile_filter, publisher_filter, country_filter, areas_filter, search_term):
    filtered = df[
        (df['IF'] >= if_min) & (df['IF'] <= if_max) &
        (df['Q'].isin(quartile_filter) if quartile_filter else True) &
        (df['Publisher'].isin(publisher_filter) if publisher_filter else True) &
        (df['Country'].isin(country_filter) if country_filter else True)
    ]
    
    # Apply search term filter
    if search_term:
        filtered = filtered[filtered['Journal'].str.contains(search_term, case=False)]
    
    # Apply areas filter
    if areas_filter:
        filtered = filtered[filtered['Areas'].apply(lambda x: any(area in x for area in areas_filter))]
    
    return filtered

filtered_data = filter_data(data, if_min, if_max, quartile_filter, publisher_filter, country_filter, areas_filter, search_term)

# Right column for data
with right_col:
    st.subheader('Journal Data')
    
    # Option selector for display method
    display_option = st.radio(
        "Choose display method:",
        ["Data Editor", "Simple Table", "Full Width Table"],
        horizontal=True
    )
    
    if display_option == "Data Editor":
        # Use data_editor with wider column configurations
        st.data_editor(
            filtered_data, 
            use_container_width=True,
            height=600,
            hide_index=True,
            disabled=True,
            column_config={
                "Rank": st.column_config.NumberColumn("Rank", width=100),
                "Journal": st.column_config.TextColumn("Journal", width=500),
                "Year": st.column_config.NumberColumn("Year", width=100),
                "IF": st.column_config.NumberColumn("IF", width=100, format="%.2f"),
                "Q": st.column_config.TextColumn("Q", width=100),
                "Publisher": st.column_config.TextColumn("Publisher", width=200),
                "Country": st.column_config.TextColumn("Country", width=150),
                "Areas": st.column_config.TextColumn("Areas", width=250, disabled=True),
            }
        )
    elif display_option == "Simple Table":
        # Use regular table with full width
        st.table(filtered_data.head(50))  # Show first 50 rows as table
    else:
        # Full width with custom CSS
        st.markdown("""
        <style>
        .dataframe {
            width: 100% !important;
        }
        </style>
        """, unsafe_allow_html=True)
        
        st.dataframe(
            filtered_data,
            use_container_width=True,
            height=600,
            hide_index=True
        )
    
    # Show count with more detailed information
    st.write(f"Showing {len(filtered_data)} journals out of {len(data)} total")
    
