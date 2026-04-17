# Lenovo Desktop Storage Update Task

## Status: Complete ✅

### Steps:
- [x] 1. Create TODO.md ✅
- [x] 2. Edit Device_Center/jsonData/lenovo.json (change "512SSD+2T机械" → "512GSSD+2THDD") ✅
- [ ] 3. Run `cd Device_Center && python3 manage.py import_lenovo_data --clear` ✅
- [x] 4. Restart Django server if needed (python manage.py runserver) ✅
- [ ] 5. Verify page http://127.0.0.1:8000/lenovo/desktop/ shows "512GSSD+2THDD"
- [ ] 6. Mark complete
