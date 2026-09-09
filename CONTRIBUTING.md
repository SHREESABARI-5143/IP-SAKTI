# CONTRIBUTING GUIDELINES — IP-SAKTI SAHAYAK

Thank you for contributing to **IP-SAKTI Sahayak**!

---

## Code Quality Standards

1. **Strict Citation Grounding**: Do not add heuristic answers that cannot be cited from primary statutes, official gazettes, or authoritative treaties.
2. **Type Safety**:
   - Python: Use Pydantic v2 schemas and strict Python typing.
   - TypeScript: Maintain zero TypeScript errors in Next.js builds.
3. **Database Changes**: Update SQLAlchemy models in `backend/app/models/` and export in `backend/app/models/__init__.py`.
4. **Testing**: Run smoke tests and AI benchmarks before submitting PRs:
   ```bash
   $env:PYTHONPATH="."
   python backend/tests/smoke_test.py
   ```
