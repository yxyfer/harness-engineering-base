import js from "@eslint/js";
import { defineConfig, globalIgnores } from "eslint/config";
import next from "@next/eslint-plugin-next";
import hooks from "eslint-plugin-react-hooks";
import tseslint from "typescript-eslint";

export default defineConfig([
  js.configs.recommended,
  globalIgnores([
    ".next/**",
    "next-env.d.ts",
    ".harness/reports/**",
    ".harness/tmp/**",
  ]),
  {
    files: ["**/*.ts", "**/*.tsx"],
    extends: [tseslint.configs.recommendedTypeChecked],
    languageOptions: {
      parserOptions: {
        projectService: true,
        tsconfigRootDir: import.meta.dirname,
      },
    },
    rules: {
      "@typescript-eslint/no-floating-promises": "error",
      "@typescript-eslint/no-misused-promises": "error",
      "@typescript-eslint/only-throw-error": "error",
      "no-eval": "error",
      "no-new-func": "error",
    },
  },
  {
    files: ["src/**/*.tsx"],
    plugins: { "@next/next": next, "react-hooks": hooks },
    rules: {
      ...next.configs.recommended.rules,
      ...next.configs["core-web-vitals"].rules,
      ...hooks.configs.recommended.rules,
    },
  },
  {
    files: ["src/components/**/*.tsx"],
    rules: {
      "no-restricted-imports": [
        "error",
        {
          patterns: [
            {
              group: ["@/server/*", "**/server/*", "node:*"],
              message:
                "UI receives serializable props; server access belongs in pages.",
            },
          ],
        },
      ],
    },
  },
  {
    files: ["src/domain/**/*.ts"],
    rules: {
      "no-restricted-imports": [
        "error",
        {
          patterns: [
            {
              group: ["react", "next/*", "@/server/*", "node:*"],
              message: "Domain validation is independent of rendering and I/O.",
            },
          ],
        },
      ],
    },
  },
]);
