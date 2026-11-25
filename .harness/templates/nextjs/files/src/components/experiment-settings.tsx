'use client';

import { useTransition } from 'react';
import type { ExperimentState } from '@/core/experiments';

type Props = {
  /** From `experimentStates(viewer)` on the server. */
  experiments: readonly ExperimentState[];
  /**
   * A Server Action that calls `chooseExperiment` and refreshes the page.
   * `null` returns the person to the default.
   */
  choose: (id: string, choice: boolean | null) => Promise<void>;
};

/**
 * The experiments a person can see, each with its switch. Unstyled on
 * purpose: the application gives it its own look.
 */
export function ExperimentSettings({ experiments, choose }: Props) {
  const [pending, startTransition] = useTransition();
  if (experiments.length === 0) return null;
  const set = (id: string, choice: boolean | null) =>
    startTransition(() => choose(id, choice));

  return (
    <ul aria-busy={pending}>
      {experiments.map((experiment) => (
        <li key={experiment.id}>
          <label>
            <input
              type="checkbox"
              checked={experiment.active}
              disabled={pending}
              onChange={(event) => set(experiment.id, event.target.checked)}
            />
            {experiment.name}
          </label>
          <p>{experiment.description}</p>
          {experiment.chosen && experiment.active !== experiment.byDefault ? (
            <button
              type="button"
              disabled={pending}
              onClick={() => set(experiment.id, null)}
            >
              Reset to default ({experiment.byDefault ? 'on' : 'off'})
            </button>
          ) : null}
        </li>
      ))}
    </ul>
  );
}
