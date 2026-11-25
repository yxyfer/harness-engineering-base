import { defineConfig, globalIgnores } from 'eslint/config';
import nextVitals from 'eslint-config-next/core-web-vitals';
import nextTypeScript from 'eslint-config-next/typescript';
import { boundaryZones } from './eslint.boundaries.mjs';

const root = import.meta.dirname;

export default defineConfig([
  ...nextVitals,
  ...nextTypeScript,
  {
    files: ['src/**/*.{ts,tsx}'],
    rules: {
      'import/no-restricted-paths': [
        'error',
        { basePath: root, zones: boundaryZones(root) },
      ],
    },
  },
  globalIgnores([
    '.next/**',
    'out/**',
    'build/**',
    'next-env.d.ts',
    'coverage/**',
    'test-results/**',
    'playwright-report/**',
  ]),
]);
