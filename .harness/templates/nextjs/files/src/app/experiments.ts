import 'server-only';
import { cache } from 'react';
import { loadViewer, memoryChoiceStore } from '@/core/experiments';

// The per-request experiment viewer. Replace the two TODOs once the app has a
// database and sign-in; until then nobody can save a choice and everyone gets
// the defaults (everyone is a tester under `next dev`).

// TODO: `sqlChoiceStore(pool.query.bind(pool))` from '@/core/experiment-store'.
export const choiceStore = memoryChoiceStore();

// TODO: return the signed-in person ({ id, email }) or null.
export async function currentPerson(): Promise<{
  id: string;
  email?: string | null;
} | null> {
  return null;
}

/** Loaded once per request; pass `activeExperimentIds(viewer)` to screens. */
export const currentViewer = cache(async () =>
  loadViewer(choiceStore, await currentPerson()),
);
