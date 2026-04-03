# TODO: Fix "Confirm Configuration" Login Issue on List Pages

## Status: In Progress [11/20 steps complete]

## Steps from Approved Plan

### Phase 1: Apple List Pages (4 files)
- [✅] 1. Edit `templates/apple/laptop.html`: Remove login check in `buyNow()`, add NetID/email modal fields, update submitOrder()`
- [✅] 2. Edit `templates/apple/desktop.html`: Remove login check in `handleAction()` buy path, add NetID/email modal, update submitOrder()
- [✅] 3. Edit `templates/apple/ipad.html`: Remove login check in `handleAction()`, add NetID/email modal, update submitOrder()`
- [✅] 4. Edit `templates/apple/accessories.html`: Remove login check in `buyNow()`, add NetID/email modal, update submitOrder()`

### Phase 2: Dell List Pages (5 files)  
- [✅] 5. Edit `templates/dell/notebook.html`: Remove login check in `buyNow(modelName, index)`, add NetID/email modal, update submitOrder()`
- [✅] 6. Edit `templates/dell/laptop.html`: Remove login check, add NetID/email modal, update submitOrder()`
- [✅] 7. Edit `templates/dell/desktop.html`: Remove login check, add NetID/email modal, update submitOrder()`
- [ ] 8. Edit `templates/dell/monitor.html`: Remove login check  
- [ ] 9. Edit `templates/dell/accessories.html`: Remove login check

### Phase 3: Lenovo List Pages (2 files)
- [ ] 10. Edit `templates/lenovo/laptop.html`: Remove login check in `buyNow()`
- [ ] 11. Edit `templates/lenovo/desktop.html`: Remove login check

### Phase 4: Modal Standardization (7 files missing NetID/email)
- [ ] 12. `apple/laptop.html`: Add NetID/email inputs + submitOrder() data
- [ ] 13. `apple/desktop.html`: Add NetID/email  
- [ ] 14. `apple/ipad.html`: Add NetID/email
- [ ] 15. `dell/notebook.html`: Add NetID/email
- [ ] 16. `dell/laptop.html`: Add NetID/email  
- [ ] 17. `dell/desktop.html`: Add NetID/email
- [ ] 18. `lenovo/laptop.html`: Add NetID/email

### Phase 5: Testing & Completion
- [ ] 19. Test all list pages: Click "Confirm Configuration" → Modal shows NetID/email → Submit succeeds
- [ ] 20. Update this TODO.md as ✅ complete → attempt_completion

**Next Step:** Start Phase 1 with `templates/apple/laptop.html`

