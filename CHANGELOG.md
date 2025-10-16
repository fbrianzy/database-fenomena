# Changelog

All notable changes to this project will be documented in this file.

## [3.0.0] - 2025-10-16 - Dashfena GitHub-Sync Revamp 

### Added 

- Modular Flask structure with separated layers: routes, services, utils, and middlewares.
- Admin routes isolated in routes/admin/ for better maintenance and access control.
- Server preflight test to check environment variables (GitHub Token, Owner, Repo, Branch) before startup.
- Real-time synchronization with GitHub repository (database-fenomena) displaying the latest sync time.
- Enhanced admin panel for CSV-based CRUD operations.
- Improved UI/UX: smoother loading animation, typing effect, and no blink during initialization.
- Dynamic server status indicators for Running, Stopped, and Restarting.
- Automatic removal of trailing slashes in routes for cleaner URLs.
- Active navigation link detection in navbar.

### Changed 

- Base template refactored to use Tailwind CSS 3 and Font Awesome 6.
- Navbar made more responsive for mobile screens with balanced padding and spacing.
- Scrollbar hidden for clean appearance.
- Optimized GitHub data loader to fetch only recent files per category folder.
- Improved home statistics to include month-over-month comparison and positive growth indicator.
- Refactored all routes to follow consistent blueprint registration order and prefixing.
- Reduced redundant imports and streamlined service calls.

### Fixed 

- Removed blinking effect during page load.
- Resolved duplicated category entries from multiple CSV reads.
- Fixed active navbar detection on /fenomena page.
- Addressed CSRF token mismatch between localhost and IP-based hosts.
- Added missing datetime and requests imports in legacy modules.
- Corrected `url_for` path and static file references.

### Performance 

- Optimized GitHub API requests and caching.
- Reduced redundant reloads after CSV upload.
- Faster dashboard render times and smoother transitions.

### Security 

- Enhanced CSRF validation and session token consistency.
- Added request logging for suspicious activity.
- Sanitized inputs and improved header handling for safer user interaction.

### Folder Structure
```text
app/
 ├── __init__.py
 ├── config/
 ├── routes/
 │   ├── admin/
 │   ├── api/
 │   └── fenomena/
 ├── services/
 ├── utils/
 ├── templates/
 ├── static/
 └── middlewares/
run.py
wsgi.py
CPanel/
 ├── components/
 ├── services/
 ├── utils/
 └── app.py
```

## [2.0.0] - 2025-10-05 - Major Refactoring

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

## [1.0.0] - 2025-08-30 - Initial Release

### Added
- Basic Flask application
- CSV data loading from GitHub
- Trend visualization
- Fenomena data table
- Admin panel
- GitHub integration
- Data filtering
- Sample data fallback
