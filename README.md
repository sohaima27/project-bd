# Hotel Management Dashboard

A Streamlit-based web application for exploring and visualizing data from the `hoteldb` MySQL database. The app provides an interactive interface to view hotel reservations, client information, room availability, and more, using SQL queries and Streamlit's native charting capabilities.
## nom de personme responsable au project
sohaima ait houssa
## Features
- **Interactive Dashboard**: Navigate through different sections to view:
  - Reservations with client names and hotel cities.
  - Clients residing in Paris.
  - Number of reservations per client.
  - Number of rooms per room type.
  - Available rooms for a specified date range.
- **Visualizations**: Uses Streamlit's built-in `st.bar_chart` for bar charts and `st.table` for tabular data display.
- **Date Range Filter**: Allows users to select a date range to check room availability.
- **Error Handling**: Displays user-friendly error messages for database connection or query issues.
- **Responsive Design**: Works seamlessly on both light and dark themes with Streamlit's default styling.

## Prerequisites
- **MySQL Server**: A running MySQL server with the `hoteldb` database created and populated.
- **Python**: Version 3.8 or higher.
- **Python Libraries**:
  - `streamlit`
  - `mysql-connector-python`
  - `pandas`

## Installation

1. **Clone the Repository** (if applicable, or create a project directory):
   ```bash
   git clone <repository-url>
   cd hotel-management-dashboard
