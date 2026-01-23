# Frontend CI Pipeline Quick Reference

## 🚀 Pipeline Overview

```
Code Quality (ESLint + Prettier + TypeScript)
    ↓
Tests & Coverage (Vitest)
    ↓
Build Validation
    ↓
Docker Build (Push only, if Dockerfile exists)
    ↓
CI Success Summary
```

## ⚡ Quick Commands

### Run Locally Before Push
```bash
# Full check (recommended)
npm run lint && \
npm run format:check && \
npx tsc --noEmit && \
npm run test:coverage

# Individual checks
npm run lint                    # ESLint
npm run format:check            # Prettier
npx tsc --noEmit               # TypeScript
npm test                        # Tests
npm run test:coverage          # Coverage
npm run build                   # Build
```

### Fix Issues
```bash
npm run lint:fix                # Auto-fix linting
npm run format                  # Auto-format code
```

## 📊 Pipeline Jobs

| Job | Duration | Runs On | Purpose |
|-----|----------|---------|---------|
| Code Quality | ~1 min | All events | Linting, formatting, types |
| Tests & Coverage | ~2 min | All events | Unit/integration tests |
| Build | ~1 min | All events | Production bundle |
| Docker Build | ~2 min | Push only | Container validation |

**Total Time**: ~4-6 minutes

## ✅ Success Criteria

- ✅ ESLint passes (no errors)
- ✅ Prettier formatting correct
- ✅ TypeScript compiles without errors
- ✅ All tests pass
- ✅ Coverage ≥ 70%
- ✅ Production build succeeds
- ✅ Docker image builds (if Dockerfile exists)

## 🔧 Configuration

### Environment Variables
```yaml
NODE_VERSION: '18'
COVERAGE_THRESHOLD: 70
```

### Triggers
- Push to: `main`, `develop`, `feature/**`
- Pull requests to: `main`, `develop`, `feature/**`
- Only when `automotive-frontend/` files change
- Manual: GitHub Actions UI

## 📦 Artifacts

| Artifact | Retention | Contains |
|----------|-----------|----------|
| frontend-test-results | 30 days | Coverage reports |
| frontend-build | 7 days | Production dist/ folder |

## 🚨 Troubleshooting

### Pipeline Fails on Linting
```bash
# Check locally
npm run lint

# Auto-fix
npm run lint:fix
npm run format
```

### Pipeline Fails on Type Checking
```bash
# Check locally
npx tsc --noEmit

# Fix TypeScript errors in your code
```

### Pipeline Fails on Tests
```bash
# Run tests locally
npm test

# With coverage
npm run test:coverage

# Specific test file
npm test -- VehicleCard.test.tsx

# Watch mode
npm test -- --watch
```

### Pipeline Fails on Coverage
```bash
# Check current coverage
npm run test:coverage

# View HTML report
# Open coverage/index.html in browser

# Find uncovered lines
npm run test:coverage -- --reporter=verbose
```

### Pipeline Fails on Build
```bash
# Test build locally
npm run build

# Check for build errors
# Fix import errors, missing dependencies, etc.

# Preview build
npm run preview
```

## 📈 Coverage Reports

- **Codecov**: Automatic upload on test job
- **PR Comments**: Coverage diff with Vitest coverage report action
- **Artifacts**: HTML report available for download

## 💡 Tips

1. **Run checks locally** before pushing to save CI minutes
2. **Use `--fix` flags** to auto-fix issues
3. **Check coverage locally** to avoid surprises
4. **Test build** before pushing
5. **Review PR comments** for coverage changes

## 🎯 Quick Fixes

```bash
# Fix everything at once
npm run format && \
npm run lint:fix && \
npm run test:coverage && \
npm run build

# If tests fail, run verbose
npm test -- --reporter=verbose

# If coverage fails, check report
npm run test:coverage
# Open coverage/index.html
```

## 🔄 Workflow

1. **Write code**
2. **Run local checks** (see Quick Commands)
3. **Commit & push**
4. **Monitor pipeline** in GitHub Actions
5. **Review PR comments** (coverage, etc.)
6. **Merge when green** ✅

## 📚 Documentation

- **Full Guide**: `.github/workflows/README.md`
- **Testing Guide**: `TESTING.md`
- **Quick Commands**: `QUICK_COMMANDS.md`
- **Linting Setup**: `LINTING_SETUP.md`

## 🔍 Common Issues

### "Module not found" in tests
```bash
# Install dependencies
npm ci

# Clear cache
rm -rf node_modules
npm ci
```

### "Type error" in build
```bash
# Check TypeScript config
cat tsconfig.json

# Run type check
npx tsc --noEmit
```

### "Coverage below threshold"
```bash
# Check which files need coverage
npm run test:coverage

# Add tests for uncovered files
# Focus on files with <70% coverage
```

## 🚀 Performance Tips

### Optimize Build Size
```bash
# Check bundle size
npm run build
du -sh dist

# Analyze bundle
npm install -D rollup-plugin-visualizer
# Add to vite.config.js
```

### Speed Up Tests
```bash
# Run tests in parallel (default)
npm test

# Run specific test suite
npm test -- VehicleCard

# Skip slow tests during development
npm test -- --exclude=slow.test.tsx
```

## 🐳 Docker (Optional)

If you have a Dockerfile:

```bash
# Build locally
docker build -t automotive-frontend:local .

# Run container
docker run -d -p 3000:80 automotive-frontend:local

# Test
curl http://localhost:3000

# Stop
docker stop $(docker ps -q --filter ancestor=automotive-frontend:local)
```

## 📊 Metrics to Monitor

- **Build Size**: Should stay under 500KB (gzipped)
- **Test Coverage**: Maintain ≥ 70%
- **Build Time**: Should be under 2 minutes
- **Test Time**: Should be under 3 minutes

## 🎓 Best Practices

1. **Write tests first** (TDD approach)
2. **Keep components small** (easier to test)
3. **Mock external dependencies** (faster tests)
4. **Use TypeScript strictly** (catch errors early)
5. **Format on save** (consistent code style)

---

**Need Help?** Check the full documentation in `.github/workflows/README.md`
