/**
 * The one registry of experiments. It holds metadata only and imports no
 * application code, so reading it never loads an experiment. A folder under
 * `src/experimental` without an entry here is not reachable anywhere.
 *
 * `npm run new-experiment -- <name>` adds an entry above the marker below.
 * `src/experimental/README.md` explains the lifecycle.
 */
export type ExperimentStage =
  /** Off for everyone, whatever they chose. The kill switch. */
  | 'off'
  /** Testers only, on by default for them; they can turn it off. */
  | 'testers'
  /** Testers as above; everyone else may turn it on in Settings. */
  | 'everyone';

export type ExperimentDefinition = {
  /**
   * Saved with each person's choice. Lower-case words joined by hyphens.
   * Never reuse the ID of a retired experiment: old saved choices remain.
   */
  readonly id: string;
  /** Shown in Settings. */
  readonly name: string;
  /** Shown in Settings: what changes when this is on. */
  readonly description: string;
  /** The folder holding the implementation and its `index` entry point. */
  readonly source: `src/experimental/${string}`;
  /** Who decides to open, promote or retire it. */
  readonly owner: string;
  readonly stage: ExperimentStage;
  /**
   * Spends money or calls a paid provider without a person asking each time.
   * A billed experiment is never on by default, not even for testers.
   */
  readonly billed?: boolean;
};

export type ExperimentRegistry = readonly ExperimentDefinition[];

export const EXPERIMENT_ID = /^[a-z][a-z0-9]*(-[a-z0-9]+)*$/;

export const EXPERIMENTS: ExperimentRegistry = [
  // new experiments above this line
];
