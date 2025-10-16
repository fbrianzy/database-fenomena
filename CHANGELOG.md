# Changelog

All notable changes to this project will be documented in this file.

## [2.0.0] - 2024-01-XX - Major Refactoring

### Added
- Professional folder structure with separation of concerns
- Modular configuration system (`app/config/`)
- Dedicated middleware layer (`app/middlewares/`)
- Service layer for business logic (`app/services/`)
- Utility functions layer (`app/utils/`)
- Comprehensive error handling
- Automated testing script (`test_structure.py`)
- Makefile for common commands
- Complete documentation (README.md)
- Environment template (.env.example)

### Changed
- **BREAKING**: Migrated from monolithic `app.py` to modular structure
- **BREAKING**: Migrated from monolithic `admin.py` to separate admin routes
- Split large files into smaller, focused modules
- Improved import organization
- Better separation of concerns

### Fixed
- Fixed missing `datetime` import in `csvLoader.py`
- Fixed missing `datetime` import in `githubApiHelpers.py`
- Fixed missing `requests` import in `github.py` middleware
- Fixed circular import in cache clearing
- Fixed wrong `url_for` patterns in logout route
- Fixed missing `delRow.py` route
- Fixed template paths in admin routes
- Fixed admin blueprint registration order

### File Structure Changes

**Before (Monolithic):**
```
.
├── app.py (1000+ lines)
├── admin.py (800+ lines)
├── error_handlers.py
├── FenomenaCleaner.py
└── templates/
```

**After (Modular):**
```
.
├── app/
│   ├── __init__.py
│   ├── config/        # Configuration modules
│   ├── middlewares/   # Middleware & auth
│   ├── models/        # Data models
│   ├── routes/        # Route handlers
│   │   └── admin/     # Admin routes
│   ├── services/      # Business logic
│   ├── utils/         # Utility functions
│   ├── templates/     # HTML templates
│   └── static/        # Static files
├── run.py             # Entry point
├── test_structure.py  # Automated tests
├── Makefile          # Command shortcuts
└── README.md         # Documentation
```

### Security Improvements
- Enhanced CSRF protection
- Better rate limiting
- Improved session management
- Suspicious request detection and logging
- Input validation improvements

### Performance
- Implemented caching system
- GitHub API rate limit handling
- Optimized data loading
- Reduced redundant imports

### Documentation
- Complete README with setup instructions
- Environment variable documentation
- API endpoint documentation
- Troubleshooting guide
- Code comments and docstrings

---

## [1.0.0] - 2024-XX-XX - Initial Release

### Added
- Basic Flask application
- CSV data loading from GitHub
- Trend visualization
- Fenomena data table
- Admin panel
- GitHub integration
- Data filtering
- Sample data fallback
