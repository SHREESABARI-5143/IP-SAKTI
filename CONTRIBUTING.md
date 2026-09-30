# Contributing to AYURA (IP-SAKTI Sahayak)

Thank you for your interest in contributing to **AYURA**! We welcome community contributions from software engineers, Ayurvedic scholars, patent attorneys, and legal researchers.

---

## 📜 Guiding Principles

1. **Statutory Authenticity**: Every legal assertion and RAG reference must link directly to an authentic Gazette of India, Acts of Parliament, WIPO/TRIPS convention, or official pharmacopoeial text (AFI/API). **Zero hallucinations or fabricated sections are permitted.**
2. **Inclusive Multilingualism**: Ensure UI elements, terminology, and legal definitions preserve precision across all 7 supported Indic languages.
3. **Clean Serverless Architecture**: Keep frontend bundles lightweight and maintain the 100% free-tier serverless boundaries.

---

## 🛠️ How to Contribute

### 1. Reporting Bugs
- Before creating a bug report, check the [existing issues](https://github.com/SHREESABARI-5143/IP-SAKTI/issues).
- Use the **Bug Report** template to provide step-by-step reproduction instructions, logs, and screenshots.

### 2. Suggesting Enhancements
- Open a **Feature Request** detailing the proposed improvement, why it helps Ayurvedic researchers/regulators, and potential design approaches.

### 3. Submitting Pull Requests (PRs)
Follow this standard git workflow:

1. **Fork the Repository** to your GitHub account.
2. **Clone your Fork**:
   ```bash
   git clone https://github.com/<your-username>/IP-SAKTI.git
   cd IP-SAKTI
   ```
3. **Create a Feature Branch**:
   ```bash
   git checkout -b feature/your-feature-name
   # or
   git checkout -b fix/issue-description
   ```
4. **Develop & Test Locally**:
   - Ensure the Next.js frontend builds cleanly:
     ```bash
     cd frontend && npm run build
     ```
   - Run the automated test suites:
     ```bash
     node test_suite.mjs
     cd ../backend && python test_backend_core.py
     ```
5. **Commit your Changes**:
   Follow [Conventional Commits](https://www.conventionalcommits.org/):
   - `feat: add WIPO PCT prior-art search filter`
   - `fix: resolve Globe icon import in ChatInterface`
   - `docs: update deployment playbook for AWS Lambda`
6. **Push and Open a PR**:
   ```bash
   git push origin feature/your-feature-name
   ```
   Open a Pull Request against the `main` branch. Fill in the provided [Pull Request Template](.github/PULL_REQUEST_TEMPLATE.md).

---

## ⚖️ Legal & Statutory Corpus Contributions

If you are contributing statutory texts or Ayurvedic monograph entries:
- Place structured JSON chunks in `data/` or `backend/corpus/`.
- Must contain: `chunk_id`, `statute`, `section_or_article`, `title`, `text`, `effective_date`, `url` (official government gazette link).
- Never commit copyrighted commercial translations. Use public domain government gazettes.

---

## 🛡️ Code Style & Standards

- **Frontend**: Clean React functional components, Tailwind CSS styling, zero unhandled promise rejections.
- **Backend**: Strict PEP 8 style, Pydantic type annotations for request/response contracts, async/await handlers.

Thank you for helping empower Indian traditional medicine with cutting-edge artificial intelligence!
