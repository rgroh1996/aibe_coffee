# AIBE Coffee List App

AIBE Coffee List App is a Python Kivy GUI application for managing coffee orders, user debts, and cleaning credits in a coffee room/office environment. The app includes SQLite database backend, QR code payment integration, and optional Shelly smart plug voltage logging for coffee machine monitoring.

Always reference these instructions first and fallback to search or bash commands only when you encounter unexpected information that does not match the info here.

## Working Effectively

### Initial Setup (Required for fresh clones)
- Check Python version: `python3 --version` (Python 3.12+ recommended, minimum 3.9)
- Install system dependencies: `sudo apt-get update && sudo apt-get install -y python3-kivy python3-pandas python3-numpy python3-requests python3-qrcode qrencode`
  - Package installation takes 30-45 seconds. NEVER CANCEL.
- Initialize database: `cd tools && python3 init_database.py` (takes ~0.03 seconds)
- Validate setup: `cd .. && python3 main.py -- --noshelly` (use Ctrl+C to exit after confirming GUI loads)

### Running the Application
- **Standard run with hardware**: `python3 main.py` (requires Shelly smart plug connected at 192.168.33.1)
- **Run without hardware**: `python3 main.py -- --noshelly` (recommended for development/testing)
- **Application startup time**: 2-3 seconds for GUI initialization
- **Clean shutdown**: Use Ctrl+C or close the GUI window

### Development and Testing
- **Database operations**: Run from tools/ directory for relative path compatibility
  - Initialize: `cd tools && python3 init_database.py`
  - View contents: `cd tools && python3 print_database.py`
  - Database file location: `database/aibe_coffee.db` (auto-created by init script)
- **Import validation**: Test all major imports with `python3 -c "import kivy, sqlite3, pandas, qrcode; print('All imports successful')"`

## Validation Scenarios

### End-to-End Application Testing
ALWAYS validate functionality after making changes by running these scenarios:

1. **Database Initialization Test**:
   - Delete existing database: `rm -rf database/`
   - Initialize fresh: `cd tools && python3 init_database.py`
   - Verify creation: `ls -la database/` (should show aibe_coffee.db)

2. **Application Startup Test**:
   - Run: `python3 main.py -- --noshelly`
   - Verify GUI loads without errors
   - Check for "Shelly not connected" message (expected with --noshelly)
   - Confirm QR code generation message appears

3. **User Workflow Test** (when GUI is interactive):
   - Navigate through main screen, user selection, coffee selection
   - Test new user creation functionality
   - Verify debt tracking and payment screens
   - Test cleaning credit system

## Critical Technical Details

### Dependency Management
- **System packages only**: Use apt-get for all dependencies. pip installations fail due to network timeouts.
- **Windows incompatibility**: pypiwin32 requirement fails on Linux - this is expected and normal
- **Essential packages**: kivy, pandas, numpy, requests, qrcode must be available via system packages

### Hardware Integration
- **Shelly smart plug**: Optional device at 192.168.33.1 for voltage logging
- **--noshelly flag**: ALWAYS use when Shelly device unavailable (development/CI environments)
- **Network timeouts**: Application gracefully handles hardware connection failures

### Project Structure Navigation
Key directories and files:
- `main.py`: Application entry point with Kivy app initialization
- `backend/`: Data management (data_manager.py) and hardware logging (shelly_log.py)  
- `frontend/`: All GUI screens (main, user, coffee selection, payment, cleaning)
- `tools/`: Database utilities (init_database.py, print_database.py)
- `database/`: SQLite database storage (auto-created)
- `products.json`: Coffee menu and pricing configuration
- `cleaning.json`: Cleaning tasks and credit configuration

### Database Schema
Tables created by init_database.py:
- `users`: User accounts and debt tracking
- `consumed`: Transaction history for coffee purchases
- `debt_paid`: Payment history
- `cleaning`: Cleaning task credits and history

## Timeout and Build Information

### Command Timing Expectations
- **Database initialization**: < 0.1 seconds - DO NOT set long timeouts
- **Package installation**: 30-45 seconds - Set timeout to 60+ seconds, NEVER CANCEL
- **Application startup**: 2-5 seconds - Normal timeout sufficient
- **GUI validation**: 15-30 seconds for manual testing - Use timeout to auto-exit

### No CI/CD or Linting
- **No automated testing**: Repository has no test files or CI configuration
- **No linting tools**: No flake8, black, or other code style tools configured
- **No build process**: Pure Python application, no compilation required

## Common Issues and Solutions

### Import Errors
- **Missing qrcode**: Install `python3-qrcode` via apt
- **Missing pandas**: Install `python3-pandas` via apt  
- **Missing kivy**: Install `python3-kivy` via apt
- **pypiwin32 failure**: Expected on Linux, ignore this error

### Application Errors
- **"Shelly not connected"**: Use `-- --noshelly` flag for development
- **GUI won't start**: Ensure DISPLAY environment variable set (export DISPLAY=:99)
- **Database errors**: Run init_database.py from tools/ directory

### Development Tips
- **Always use system packages**: apt-get installations work reliably
- **Test with --noshelly**: Avoid hardware dependencies during development
- **Database from tools/**: Run database scripts from tools/ directory for correct paths
- **Quick validation**: Use timeout commands to auto-exit long-running processes

## Quick Reference Commands

```bash
# Fresh setup
sudo apt-get update && sudo apt-get install -y python3-kivy python3-pandas python3-numpy python3-requests python3-qrcode
cd tools && python3 init_database.py

# Run application  
python3 main.py -- --noshelly

# Check database
cd tools && python3 print_database.py

# Validate all imports
python3 -c "import kivy, sqlite3, pandas, qrcode; print('All imports successful')"
```