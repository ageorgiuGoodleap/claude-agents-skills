---
name: vercel-deployment
description: |
  Configure production-grade Vercel deployments for Next.js, React, and frontend applications. Implements multi-environment
  strategy (production, preview, development), edge functions, ISR (Incremental Static Regeneration), environment variables,
  custom domains, performance optimizations, and CI/CD integration with automatic deployments and rollback capabilities.

  Use when: deploying to Vercel, setting up Next.js deployment, configuring edge functions, implementing ISR, setting up
  preview deployments, or when user mentions Vercel, Next.js deploy, edge functions, serverless functions, preview URLs,
  Vercel deployment, ISR, edge middleware, Vercel configuration, or Vercel environment variables.
allowed-tools: Read, Write, Edit, Bash, Grep, Glob
---

# Vercel Deployment

Configure production-ready Vercel deployments for modern web applications, focusing on Next.js but supporting React, Vue, Svelte, and other frameworks. Covers multi-environment setup, edge computing, performance optimization, security, and seamless CI/CD integration.

## Core Implementation Areas

### 1. Project Configuration (vercel.json)

**Create `vercel.json` for optimal deployment settings:**

**Basic configuration:**
```json
{
  "buildCommand": "npm run build",
  "devCommand": "npm run dev",
  "installCommand": "npm install",
  "framework": "nextjs",
  "outputDirectory": ".next"
}
```

**Advanced configuration:**
```json
{
  "buildCommand": "npm run build",
  "framework": "nextjs",
  "regions": ["iad1", "sfo1"],
  "functions": {
    "api/**/*.js": {
      "memory": 1024,
      "maxDuration": 10
    }
  },
  "redirects": [
    {
      "source": "/old-blog/:path*",
      "destination": "/blog/:path*",
      "permanent": true
    }
  ],
  "rewrites": [
    {
      "source": "/api/:path*",
      "destination": "https://backend.example.com/:path*"
    }
  ],
  "headers": [
    {
      "source": "/(.*)",
      "headers": [
        {
          "key": "X-Content-Type-Options",
          "value": "nosniff"
        },
        {
          "key": "X-Frame-Options",
          "value": "DENY"
        },
        {
          "key": "X-XSS-Protection",
          "value": "1; mode=block"
        }
      ]
    }
  ],
  "crons": [
    {
      "path": "/api/cron",
      "schedule": "0 0 * * *"
    }
  ]
}
```

**Framework-specific settings:**

**Next.js** (auto-detected):
```json
{
  "framework": "nextjs",
  "outputDirectory": ".next"
}
```

**React + Vite:**
```json
{
  "buildCommand": "npm run build",
  "outputDirectory": "dist",
  "devCommand": "npm run dev"
}
```

**Vue:**
```json
{
  "buildCommand": "npm run build",
  "outputDirectory": "dist",
  "framework": "vue"
}
```

### 2. Multi-Environment Strategy

**Configure environments with branch-based deployments:**

**Environment hierarchy:**

**Production:**
- Branch: `main` or `master`
- URL: Custom domain (`example.com`)
- Deployment: Automatic on push
- Protection: Optional password/IP whitelist

**Preview:**
- Branch: All non-production branches
- URL: Auto-generated (`feature-name-abc123.vercel.app`)
- Deployment: Automatic on push/PR
- Duration: Persists until branch deleted

**Development:**
- Local: `vercel dev` for local testing
- Branch: Optional `develop` for staging

**Branch configuration:**
```json
{
  "git": {
    "deploymentEnabled": {
      "main": true,
      "develop": true
    }
  }
}
```

**Custom preview domains:**
- `staging.example.com` → `develop` branch
- `*.example.com` → Feature branches

### 3. Environment Variables & Secrets

**Configure variables per environment:**

**Variable scopes:**
- **Production**: Only in production deployments
- **Preview**: All preview deployments
- **Development**: Local development (`vercel dev`)

**Setting via CLI:**
```bash
# Add production secret
vercel env add DATABASE_URL production

# Add preview variable
vercel env add API_ENDPOINT preview

# Add development variable
vercel env add DEBUG development

# Pull environment variables locally
vercel env pull .env.local
```

**Best practices:**
- Never commit `.env.local` (add to `.gitignore`)
- Use different API keys for preview vs. production
- Enable encrypted secrets for sensitive values
- Document required variables in `.env.example`

**System variables (auto-provided):**
```
VERCEL=1
VERCEL_ENV=production|preview|development
VERCEL_URL=deployment-url.vercel.app
VERCEL_GIT_PROVIDER=github
VERCEL_GIT_REPO_OWNER=username
VERCEL_GIT_REPO_SLUG=repo-name
VERCEL_GIT_COMMIT_REF=branch-name
VERCEL_GIT_COMMIT_SHA=abc123
```

**Access in Next.js:**
```javascript
// Server-side only
const dbUrl = process.env.DATABASE_URL;

// Client-side (must prefix with NEXT_PUBLIC_)
const apiUrl = process.env.NEXT_PUBLIC_API_URL;
```

### 4. Edge Functions & Middleware

**Implement edge computing for low-latency, global execution:**

**Edge Middleware (Next.js 12+):**
```typescript
// middleware.ts
import { NextResponse } from 'next/server';
import type { NextRequest } from 'next/server';

export function middleware(request: NextRequest) {
  // 1. Authentication check
  const token = request.cookies.get('token');
  if (!token && request.nextUrl.pathname.startsWith('/dashboard')) {
    return NextResponse.redirect(new URL('/login', request.url));
  }

  // 2. Geolocation-based redirect
  const country = request.geo?.country;
  if (country === 'US' && request.nextUrl.pathname === '/') {
    return NextResponse.redirect(new URL('/us', request.url));
  }

  // 3. A/B testing
  const variant = request.cookies.get('variant') ||
    (Math.random() < 0.5 ? 'A' : 'B');
  const response = NextResponse.next();
  response.cookies.set('variant', variant);

  // 4. Custom headers
  response.headers.set('X-Custom-Header', 'value');

  return response;
}

export const config = {
  matcher: [
    '/dashboard/:path*',
    '/api/:path*',
    '/((?!_next/static|_next/image|favicon.ico).*)'
  ]
};
```

**Edge API Routes:**
```typescript
// pages/api/hello.ts or app/api/hello/route.ts
export const config = {
  runtime: 'edge'
};

export default async function handler(request: Request) {
  const { searchParams } = new URL(request.url);
  const name = searchParams.get('name') || 'World';

  return new Response(
    JSON.stringify({ message: `Hello, ${name}!` }),
    {
      headers: { 'Content-Type': 'application/json' }
    }
  );
}
```

**Edge vs. Serverless:**
- **Edge**: < 1ms cold start, limited runtime, globally distributed
- **Serverless**: ~50-200ms cold start, full Node.js APIs, single region

**Use cases:**
- Authentication/authorization
- A/B testing and feature flags
- Geolocation-based routing
- Bot detection
- Rate limiting
- Request/response manipulation

### 5. ISR (Incremental Static Regeneration)

**Serve static pages with background revalidation:**

**Time-based revalidation (Next.js Pages Router):**
```javascript
// pages/products/[id].js
export async function getStaticProps({ params }) {
  const product = await fetchProduct(params.id);

  return {
    props: { product },
    revalidate: 60 // Revalidate every 60 seconds
  };
}

export async function getStaticPaths() {
  // Pre-render top 100 products at build time
  const products = await fetchTopProducts(100);

  return {
    paths: products.map(p => ({ params: { id: p.id } })),
    fallback: 'blocking' // Generate other pages on-demand
  };
}
```

**On-demand revalidation:**
```javascript
// pages/api/revalidate.js
export default async function handler(req, res) {
  // Verify secret to prevent unauthorized revalidation
  if (req.query.secret !== process.env.REVALIDATE_SECRET) {
    return res.status(401).json({ message: 'Invalid token' });
  }

  try {
    await res.revalidate('/products/123');
    await res.revalidate('/products/456');
    return res.json({ revalidated: true });
  } catch (err) {
    return res.status(500).send('Error revalidating');
  }
}
```

**Tag-based revalidation (Next.js 13+ App Router):**
```javascript
// app/products/[id]/page.tsx
import { revalidateTag } from 'next/cache';

export default async function ProductPage({ params }) {
  const product = await fetch(`https://api.example.com/products/${params.id}`, {
    next: { tags: ['products'] }
  });

  return <ProductDetails product={product} />;
}

// Revalidate all products
export async function POST(request: Request) {
  revalidateTag('products');
  return Response.json({ revalidated: true });
}
```

**ISR benefits:**
- Serve static pages from CDN (near-instant load)
- Content updates in background without rebuild
- Unlimited traffic without backend load

### 6. Custom Domains & SSL

**Configure custom domains with automatic HTTPS:**

**Step 1: Add domain in Vercel dashboard**
1. Project Settings → Domains
2. Enter domain name (`example.com`)
3. Click "Add"

**Step 2: Configure DNS**

**Option A: Vercel DNS (recommended):**
- Nameservers: `ns1.vercel-dns.com`, `ns2.vercel-dns.com`
- Zero configuration, automatic setup
- Fastest propagation

**Option B: External DNS:**
- **A record**: `76.76.21.21` (for root domain)
- **CNAME**: `cname.vercel-dns.com` (for subdomains)

**DNS examples:**
```
# Root domain
example.com.        A       76.76.21.21

# www subdomain
www.example.com.    CNAME   cname.vercel-dns.com

# API subdomain
api.example.com.    CNAME   cname.vercel-dns.com

# Staging subdomain
staging.example.com CNAME   cname.vercel-dns.com
```

**Step 3: SSL (automatic)**
- Let's Encrypt certificate provisioned automatically
- Auto-renewal every 60 days
- HTTP → HTTPS redirect enforced
- TLS 1.3 support

**Domain patterns:**
- `example.com` → Production
- `www.example.com` → Production (auto-redirect from root)
- `staging.example.com` → Preview (develop branch)
- `*.example.com` → Wildcard for feature branches

### 7. Performance Optimizations

**Maximize page speed and Core Web Vitals:**

**Image optimization (Next.js Image):**
```javascript
import Image from 'next/image';

<Image
  src="/hero.jpg"
  alt="Hero image"
  width={1200}
  height={600}
  priority // Load immediately for above-fold images
  placeholder="blur"
  blurDataURL="data:image/..."
/>
```

**Benefits:**
- Automatic WebP/AVIF conversion
- Responsive sizes generated
- Lazy loading
- CDN serving from Vercel Edge Network

**Font optimization (next/font):**
```javascript
// app/layout.tsx
import { Inter } from 'next/font/google';

const inter = Inter({
  subsets: ['latin'],
  variable: '--font-inter',
  display: 'swap'
});

export default function RootLayout({ children }) {
  return (
    <html lang="en" className={inter.variable}>
      <body>{children}</body>
    </html>
  );
}
```

**Benefits:**
- Self-host Google Fonts (no external request)
- Variable fonts (single file for all weights)
- `font-display: swap` (no FOIT)
- Zero layout shift

**Code splitting:**
```javascript
// Dynamic imports for code splitting
import dynamic from 'next/dynamic';

const HeavyComponent = dynamic(() => import('./HeavyComponent'), {
  loading: () => <p>Loading...</p>,
  ssr: false // Client-side only if needed
});
```

**Bundle analysis:**
```bash
# Install analyzer
npm install @next/bundle-analyzer

# Add to next.config.js
const withBundleAnalyzer = require('@next/bundle-analyzer')({
  enabled: process.env.ANALYZE === 'true'
});

module.exports = withBundleAnalyzer({
  // your config
});

# Analyze
ANALYZE=true npm run build
```

**Caching headers:**
```json
{
  "headers": [
    {
      "source": "/_next/static/(.*)",
      "headers": [
        {
          "key": "Cache-Control",
          "value": "public, max-age=31536000, immutable"
        }
      ]
    }
  ]
}
```

**Performance targets:**
- Lighthouse score > 90 for all metrics
- First Contentful Paint (FCP) < 1.8s
- Largest Contentful Paint (LCP) < 2.5s
- Cumulative Layout Shift (CLS) < 0.1
- First Input Delay (FID) < 100ms

### 8. Security & Deployment Protection

**Secure deployments with authentication and security headers:**

**Password protection:**
- Enable in Project Settings → Deployment Protection
- Require password for preview deployments
- Different passwords per environment

**IP whitelisting:**
- Restrict access to specific IP ranges
- Useful for internal tools, staging environments

**Security headers:**
```json
{
  "headers": [
    {
      "source": "/(.*)",
      "headers": [
        {
          "key": "X-DNS-Prefetch-Control",
          "value": "on"
        },
        {
          "key": "Strict-Transport-Security",
          "value": "max-age=63072000; includeSubDomains; preload"
        },
        {
          "key": "X-Frame-Options",
          "value": "SAMEORIGIN"
        },
        {
          "key": "X-Content-Type-Options",
          "value": "nosniff"
        },
        {
          "key": "X-XSS-Protection",
          "value": "1; mode=block"
        },
        {
          "key": "Referrer-Policy",
          "value": "strict-origin-when-cross-origin"
        },
        {
          "key": "Permissions-Policy",
          "value": "camera=(), microphone=(), geolocation=()"
        },
        {
          "key": "Content-Security-Policy",
          "value": "default-src 'self'; script-src 'self' 'unsafe-inline' 'unsafe-eval'; style-src 'self' 'unsafe-inline';"
        }
      ]
    }
  ]
}
```

**Authentication (custom):**
```typescript
// middleware.ts
import { NextResponse } from 'next/server';
import type { NextRequest } from 'next/server';

export function middleware(request: NextRequest) {
  // Verify JWT token
  const token = request.cookies.get('token')?.value;

  if (!token) {
    return NextResponse.redirect(new URL('/login', request.url));
  }

  try {
    // Verify token (simplified)
    const payload = verifyJWT(token);

    // Add user info to headers for downstream use
    const response = NextResponse.next();
    response.headers.set('X-User-Id', payload.userId);

    return response;
  } catch (error) {
    return NextResponse.redirect(new URL('/login', request.url));
  }
}

export const config = {
  matcher: ['/dashboard/:path*', '/api/:path*']
};
```

### 9. CI/CD Integration & Git Workflow

**Seamless deployment automation:**

**Automatic deployments:**
- Push to branch → Preview deployment
- PR opened/updated → Preview deployment + comment with URL
- Merge to `main` → Production deployment
- Tag created → Optional production deployment

**GitHub integration:**
```yaml
# .github/workflows/vercel.yml (optional, Vercel handles automatically)
name: Vercel Deployment
on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: amondnet/vercel-action@v25
        with:
          vercel-token: ${{ secrets.VERCEL_TOKEN }}
          vercel-org-id: ${{ secrets.ORG_ID }}
          vercel-project-id: ${{ secrets.PROJECT_ID }}
          vercel-args: '--prod'
```

**Vercel CLI deployments:**
```bash
# Install Vercel CLI
npm install -g vercel

# Link project (one-time)
vercel link

# Deploy to preview
vercel

# Deploy to production
vercel --prod

# Deploy with specific branch
vercel --target production --branch main

# List deployments
vercel ls

# Alias deployment
vercel alias set deployment-url.vercel.app example.com

# Remove deployment
vercel rm deployment-url
```

**Deployment protection rules:**
- Require successful build before merge
- Run tests in GitHub Actions before deployment
- Manual approval for production deployments (Enterprise)

**Rollback procedure:**
1. Identify previous working deployment
2. Go to Deployments tab in Vercel dashboard
3. Click "..." on working deployment → "Promote to Production"
4. Or via CLI: `vercel alias set previous-deployment.vercel.app example.com`

### 10. Monitoring & Analytics

**Track performance, errors, and usage:**

**Vercel Analytics:**
```javascript
// pages/_app.js (Pages Router)
import { Analytics } from '@vercel/analytics/react';

export default function App({ Component, pageProps }) {
  return (
    <>
      <Component {...pageProps} />
      <Analytics />
    </>
  );
}

// app/layout.tsx (App Router)
import { Analytics } from '@vercel/analytics/react';

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body>
        {children}
        <Analytics />
      </body>
    </html>
  );
}
```

**Vercel Speed Insights:**
```javascript
import { SpeedInsights } from '@vercel/speed-insights/next';

export default function RootLayout({ children }) {
  return (
    <html>
      <body>
        {children}
        <SpeedInsights />
      </body>
    </html>
  );
}
```

**Real-time function logs:**
```bash
# View logs via CLI
vercel logs <deployment-url>

# Follow logs in real-time
vercel logs <deployment-url> --follow

# Filter by function
vercel logs <deployment-url> --path=/api/hello
```

**Error tracking (Sentry integration):**
```javascript
// next.config.js
const { withSentryConfig } = require('@sentry/nextjs');

module.exports = withSentryConfig(
  {
    // Your Next.js config
  },
  {
    silent: true,
    org: "your-org",
    project: "your-project"
  }
);

// sentry.client.config.js
import * as Sentry from '@sentry/nextjs';

Sentry.init({
  dsn: process.env.NEXT_PUBLIC_SENTRY_DSN,
  tracesSampleRate: 0.1,
  environment: process.env.VERCEL_ENV
});
```

**Monitoring checklist:**
- [ ] Analytics tracking (Vercel Analytics or Google Analytics)
- [ ] Error tracking (Sentry, Rollbar)
- [ ] Performance monitoring (Speed Insights)
- [ ] Function logs monitoring
- [ ] Uptime monitoring (UptimeRobot, Checkly)
- [ ] Cost monitoring (Vercel dashboard usage)

## Implementation Workflow

### Phase 1: Project Setup

1. Connect Git repository to Vercel:
   - Import from GitHub/GitLab/Bitbucket
   - Or use `vercel` CLI to link existing project

2. Configure framework settings:
   - Auto-detected for Next.js
   - Manual configuration for other frameworks

3. Set environment variables:
   - Production secrets
   - Preview variables
   - Development variables

4. Configure custom domains:
   - Add domain in Vercel dashboard
   - Configure DNS records
   - Wait for SSL certificate

### Phase 2: Configuration

1. Create `vercel.json`:
   - Build settings
   - Redirects/rewrites
   - Headers
   - Functions configuration

2. Set up multi-environment strategy:
   - Production: `main` branch
   - Preview: All other branches
   - Staging: Optional `develop` branch

3. Configure edge functions:
   - Create `middleware.ts`
   - Implement authentication, A/B testing, etc.
   - Test with `vercel dev`

### Phase 3: Optimization

1. Implement performance optimizations:
   - Use Next.js Image component
   - Optimize fonts with next/font
   - Enable code splitting
   - Configure caching headers

2. Set up ISR:
   - Add `revalidate` to pages
   - Implement on-demand revalidation API
   - Test revalidation workflow

3. Analyze bundle:
   - Run bundle analyzer
   - Identify large dependencies
   - Optimize bundle size

### Phase 4: Security

1. Configure security headers:
   - CSP, X-Frame-Options, HSTS, etc.
   - Test with securityheaders.com

2. Set up deployment protection:
   - Password protect preview deployments
   - Configure IP whitelisting if needed

3. Implement authentication:
   - Edge middleware for auth checks
   - JWT verification
   - Session management

### Phase 5: Monitoring

1. Add analytics:
   - Vercel Analytics
   - Speed Insights
   - Google Analytics (optional)

2. Set up error tracking:
   - Sentry integration
   - Source maps upload

3. Configure alerts:
   - Build failures
   - Deployment errors
   - Performance degradation

## Quality Checklist

Before going live, verify:

- [ ] Custom domain configured with SSL
- [ ] Environment variables set for all environments
- [ ] Security headers configured
- [ ] Image optimization enabled (Next.js Image)
- [ ] Font optimization enabled (next/font)
- [ ] ISR configured for dynamic content
- [ ] Edge functions tested (middleware, API routes)
- [ ] Analytics tracking enabled
- [ ] Error tracking configured
- [ ] Lighthouse score > 90 for all metrics
- [ ] Preview deployments tested
- [ ] Rollback procedure documented
- [ ] Deployment protection enabled (if required)

## Common Patterns

### Pattern 1: Next.js E-commerce
- Product pages use ISR (revalidate: 3600)
- On-demand revalidation when inventory updated
- Edge middleware for region-based pricing
- Serverless API routes for checkout

### Pattern 2: Marketing Site with A/B Testing
- Edge middleware assigns variant randomly
- Cookie persists variant across sessions
- Analytics track conversion by variant
- ISR for content pages

### Pattern 3: SaaS Application
- Authentication via edge middleware (JWT verification)
- Protected routes redirect to login
- Serverless API routes for backend operations
- Preview deployments for feature testing

### Pattern 4: Multi-Tenant Application
- Subdomain routing (`tenant1.example.com`)
- Edge middleware extracts tenant from subdomain
- Dynamic ISR based on tenant data
- Separate environment variables per tenant

## Anti-Patterns to Avoid

❌ **Using serverless functions for everything**
✅ **Use edge functions for low-latency operations**

❌ **Hardcoding secrets in code**
✅ **Use Vercel environment variables**

❌ **No ISR (full rebuild on every change)**
✅ **ISR with on-demand revalidation**

❌ **Unprotected preview deployments with production data**
✅ **Password-protect previews, use preview-specific env vars**

❌ **Large unoptimized images (5MB PNG)**
✅ **Next.js Image component with WebP/AVIF**

❌ **No monitoring or alerts**
✅ **Analytics, error tracking, performance monitoring**

❌ **Manual deployments via FTP**
✅ **Git-based automatic deployments**

## Key Technologies

**Frameworks:**
- Next.js, React, Vue, Svelte, Nuxt, SvelteKit, Remix, Astro

**Build Tools:**
- Vite, Turbopack, Webpack, Rollup

**Authentication:**
- NextAuth.js, Auth0, Clerk, Supabase Auth, Firebase Auth

**Analytics:**
- Vercel Analytics, Google Analytics, Plausible, Fathom

**Error Tracking:**
- Sentry, Rollbar, Bugsnag, LogRocket

**CMS Integration:**
- Contentful, Sanity, Strapi, WordPress (headless), Prismic

## Success Criteria

The Vercel deployment is production-ready when:
- Performance: Lighthouse > 90 for all Core Web Vitals
- Security: All security headers configured, HTTPS enforced
- Reliability: Automatic deployments working, rollback tested
- Observability: Analytics and error tracking configured
- Cost-optimized: ISR for dynamic content, edge for compute
- Developer experience: Preview deployments for all branches
- Documentation: Deployment guide, environment variables documented
- Monitoring: Alerts configured for failures and performance issues
