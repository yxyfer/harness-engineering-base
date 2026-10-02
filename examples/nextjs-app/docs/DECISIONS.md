# Reference decisions

## Accepted decisions

- Use one owned shadcn-style Radix foundation, adapted to semantic CSS tokens.
  Radix owns dialog focus/keyboard behavior; native fields/selects need no other
  primitive stack. Existing assets were absent. No component platform is added.
- Paper and Ink share every component; themes change tokens, not page markup.
- Server Components render fixtures; browser-only state is confined to small
  interactive components. No persistence or authentication is simulated as real.
- This standalone package is checked separately; repository aggregation remains
  unsupported. Native tools and all component source remain project-owned.
