# GeoThai Python Library

[![PyPI - Version](https://img.shields.io/pypi/v/geothai)](https://pypi.org/project/geothai/)
[![PyPI Downloads](https://static.pepy.tech/badge/geothai)](https://pepy.tech/projects/geothai)

Welcome to the **GeoThai Python Library**! This library provides a simple and efficient way to access detailed geographic data for Thailand, including provinces, districts, and subdistricts.

## 🌏 Overview

This Python library allows you to:

- Retrieve information about provinces, districts, and subdistricts in Thailand.
- Filter geographic data based on specific criteria.
- Integrate geographic data into your Python applications with ease.

## 🚀 Installation

You can install the GeoThai Python Library via pip:

```bash
pip install geothai
```

## 📚 Usage

### Importing the Library

```python
from geothai import (
    get_all_provinces,
    get_province_by_code,
    get_provinces_by_criterion,
    Province
)
```

### Retrieving All Provinces

```python
provinces = get_all_provinces()
print(provinces)
```

### Getting a Province by ID

```python
province = get_province_by_code(10)  # Replace 10 with the desired province_id
print(province)
```

### Filtering Provinces by Criteria

```python
criteria: Province = {"name_th": "กรุงเทพมหานคร"}
matching_provinces = get_provinces_by_criterion(criteria)
print(matching_provinces)
```

### Similarly, You Can Access Districts, Subdistricts and Postal Codes

```python
districts = get_all_districts()
subdistricts = get_all_subdistricts()
postal_codes = get_all_postal_codes()
```

## 📂 Project Structure

The project is structured as follows:

- **`geothai/data/`**: Contains the data files for provinces, districts, and subdistricts.
- **`geothai/services/`**: Contains the main services for accessing province, district, and subdistrict data.
- **`geothai/types/`**: Includes type definitions for provinces, districts, subdistricts, and postal codes.
- **`geothai/utils/`**: Includes utility functions like criteria matching for filtering data.

## 🛠 Development

To contribute to the development of this library:

1. Clone the repository:

```bash
git clone https://github.com/GeoThai/python-library.git
```

2. Install the required dependencies:

```bash
pip install -r requirements.txt
```

3. Run the tests:

```bash
pytest
```

## 🤝 Contributing

We welcome contributions to enhance the functionality of this library. Please check the [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines on how to contribute.

## 📄 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## 🙋‍♂️ Contact

If you have any questions, issues, or suggestions, feel free to reach out at [contact@fasu.dev](mailto:contact@fasu.dev).
