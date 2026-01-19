# Expense Tracker Desktop

![Python](https://img.shields.io/badge/python-3.11%2B-blue)
![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20macOS-lightgrey)
![Status](https://img.shields.io/badge/status-in%20development-yellow)
![License](https://img.shields.io/badge/license-MIT-green)
![Offline](https://img.shields.io/badge/offline--first-yes-success)

## Description

Offline-first desktop application to track personal and recurring expenses, with categories, analytics, and future local AI integration.

## Features

- Add and manage personal and recurring expenses
- Predefined and custom categories
- Attach PDF receipts to expenses
- View expense history
- Analyze spending with charts and comparisons
- Offline-first for privacy
- Clean, extensible architecture

## Getting Started

### Prerequisites

- Python 3.11+
- pip (Python package manager)

### Project structure

```expense-tracker-desktop/
├─ data/
│  └─ expenses.db
├─ domain/
│  ├─ models.py
├─ persistence/
│  ├─ category_repository.py
│  ├─ expense_repository.py
│  ├─ db.py
│  └─ recurring_expense_repository.py
├─ resources/
│  ├─ default_categories.json
├─ services/
│   ├─ category_service.py
│   ├─ expense_service.py
│   └─ recurring_expense_service.py
└─ ui/
    ├─ app.py
    ├─ expense_form.py
    ├─ expense_list.py
    ├─ month_selector.py
    └─ toolbar.py
```

### Installation

1. Clone the repository:

```bash
git clone https://github.com/<your-username>/expense-tracker-desktop.git
```

2. Navigate to the project folder:

```bash
cd expense-tracker-desktop
```

3. Install required packages:

```bash
pip install -r requirements.txt
```

### Running the Application

```bash
python main.py
```

This will initialize the database and load base categories.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Future Improvements

- Automatic PDF parsing to extract expenses
- Local AI suggestions for categorization and insights
- Enhanced charts and analytics
- Cross-platform UI improvements
- Multi language support
