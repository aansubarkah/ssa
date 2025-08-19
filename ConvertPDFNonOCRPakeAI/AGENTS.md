AGENTS.md for SSA (ConvertPDFNonOCRPakeAI)

Build/lint/test
- Build: npm run build (tailwind + oneliner). CSS only: npm run build-css. One-liner HTML: npm run build-oneliner. Dev watch: npm run dev.
- Lint: none configured. If adding ESLint/Prettier, define npm scripts and update this file.
- Tests: none configured. Playwright is available; place specs in tests/. Run: npx playwright test. Single test: npx playwright test tests/file.spec.js -g "test name".

Code style
- JS runtime: Node CommonJS in build scripts; browser code is vanilla JS in single-file HTML. Do not introduce new deps without adding to package.json.
- Imports: require("module") in Node; in browser use IIFE/modules consistent with existing files. Keep relative paths explicit.
- Formatting: 2 spaces, keep current semicolon style, lines < 100 chars. Do not add comments unless requested.
- Types: JS dynamic; validate inputs; prefer const/let; avoid global leakage; pure functions where possible.
- Naming: camelCase for vars/functions, PascalCase for classes, UPPER_SNAKE_CASE for constants; filenames kebab-case for scripts.
- Errors: Wrap fs/network/UI actions with try/catch; return user-safe messages; never log secrets or API keys.
- Security: API keys stored via XOR in localStorage; never expose keys; avoid innerHTML with untrusted data; sanitize user inputs.
- Build scripts: keep CommonJS; follow existing patterns in build-oneliner.js and build-local-converter.js.
- Assets: commit production artifacts per docs; avoid committing node_modules and generated intermediates; respect .gitignore.
- Tools present: tailwindcss, postcss, playwright. Use npx tailwindcss for CSS builds.
- Cursor/Copilot rules: none found (.cursor/rules, .cursorrules, .github/copilot-instructions.md absent).