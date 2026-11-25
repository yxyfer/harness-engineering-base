import {
  EXPERIMENTS,
  type ExperimentDefinition,
  type ExperimentRegistry,
  type ExperimentStage,
} from '../config/experiments';

/**
 * The one decision on whether an experiment is on for a person. Every route,
 * Server Action and screen uses it; nothing else reads the registry's stage.
 *
 * | Person  | testers                  | everyone                 | off |
 * | ------- | ------------------------ | ------------------------ | --- |
 * | tester  | on by default, can opt out | on by default, can opt out | off |
 * | other   | not visible              | off by default, can opt in | off |
 *
 * A billed experiment is never on by default. Only explicit choices are
 * stored, so a person who never chose follows the default as it changes.
 */

export type ExperimentChoices = ReadonlyMap<string, boolean>;

export type ExperimentViewer = {
  readonly tester: boolean;
  /** Explicit choices only. A missing ID means "follow the default". */
  readonly choices: ExperimentChoices;
};

export type Person = {
  readonly id?: string | null;
  readonly email?: string | null;
};

type Environment = Readonly<Record<string, string | undefined>>;

const warned = new Set<string>();

/**
 * Whether a person is a tester. `EXPERIMENT_TESTERS` is a comma-separated
 * list of user IDs or emails, or `*` for everyone. When it is unset, everyone
 * is a tester in development (`next dev`) and nobody is anywhere else.
 * Replace this with a stored role when the list outgrows a variable.
 */
export function isTester(
  person: Person,
  env: Environment = process.env,
  warn: (message: string) => void = console.warn,
): boolean {
  const raw = env.EXPERIMENT_TESTERS?.trim();
  if (!raw) return env.NODE_ENV === 'development';
  const entries = raw
    .split(',')
    .map((entry) => entry.trim().toLowerCase())
    .filter(Boolean);
  if (entries.includes('*')) {
    if (env.NODE_ENV === 'production' && !warned.has('*')) {
      warned.add('*');
      warn(
        'EXPERIMENT_TESTERS=* makes every person a tester: every experiment at the testers stage is on for everyone using this deployment.',
      );
    }
    return true;
  }
  return [person.id, person.email].some(
    (value) => !!value && entries.includes(value.toLowerCase()),
  );
}

function find(id: string, registry: ExperimentRegistry) {
  return registry.find((experiment) => experiment.id === id);
}

/** Whether a person may see an experiment and choose for it. */
export function experimentVisible(
  experiment: ExperimentDefinition,
  viewer: ExperimentViewer,
): boolean {
  if (experiment.stage === 'everyone') return true;
  return experiment.stage === 'testers' && viewer.tester;
}

/** What a person gets when they have not chosen. */
export function experimentDefault(
  experiment: ExperimentDefinition,
  viewer: ExperimentViewer,
): boolean {
  return (
    experiment.stage !== 'off' && viewer.tester && experiment.billed !== true
  );
}

export function experimentActive(
  id: string,
  viewer: ExperimentViewer,
  registry: ExperimentRegistry = EXPERIMENTS,
): boolean {
  const experiment = find(id, registry);
  if (!experiment || !experimentVisible(experiment, viewer)) return false;
  return viewer.choices.get(id) ?? experimentDefault(experiment, viewer);
}

export function activeExperimentIds(
  viewer: ExperimentViewer,
  registry: ExperimentRegistry = EXPERIMENTS,
): Set<string> {
  return new Set(
    registry
      .filter(({ id }) => experimentActive(id, viewer, registry))
      .map(({ id }) => id),
  );
}

export type ExperimentState = {
  readonly id: string;
  readonly name: string;
  readonly description: string;
  readonly stage: ExperimentStage;
  readonly billed: boolean;
  readonly active: boolean;
  /** What this person gets without a choice. */
  readonly byDefault: boolean;
  /** Whether `active` comes from this person's own choice. */
  readonly chosen: boolean;
};

/** The experiments a person can see, for Settings. */
export function experimentStates(
  viewer: ExperimentViewer,
  registry: ExperimentRegistry = EXPERIMENTS,
): ExperimentState[] {
  return registry
    .filter((experiment) => experimentVisible(experiment, viewer))
    .map((experiment) => ({
      id: experiment.id,
      name: experiment.name,
      description: experiment.description,
      stage: experiment.stage,
      billed: experiment.billed === true,
      active: experimentActive(experiment.id, viewer, registry),
      byDefault: experimentDefault(experiment, viewer),
      chosen: viewer.choices.has(experiment.id),
    }));
}

export class ExperimentUnavailableError extends Error {
  constructor(id: string) {
    super(`The experiment "${id}" is not available.`);
    this.name = 'ExperimentUnavailableError';
  }
}

/**
 * Call next to the usual access check in every route and Server Action that
 * runs an experiment, so it cannot be reached when it is off.
 */
export function requireExperiment(
  id: string,
  viewer: ExperimentViewer,
  registry: ExperimentRegistry = EXPERIMENTS,
): void {
  if (!experimentActive(id, viewer, registry))
    throw new ExperimentUnavailableError(id);
}

/**
 * Where explicit choices are kept. The application implements it, usually as
 * a table keyed by person and experiment ID. `null` removes a choice, which
 * returns the person to the default.
 */
export interface ExperimentChoiceStore {
  read(personId: string): Promise<Map<string, boolean>>;
  write(personId: string, id: string, choice: boolean | null): Promise<void>;
}

/** For tests and local prototypes only: choices vanish on restart. */
export function memoryChoiceStore(): ExperimentChoiceStore {
  const rows = new Map<string, Map<string, boolean>>();
  return {
    async read(personId) {
      return new Map(rows.get(personId) ?? []);
    },
    async write(personId, id, choice) {
      const own = rows.get(personId) ?? new Map<string, boolean>();
      if (choice === null) own.delete(id);
      else own.set(id, choice);
      rows.set(personId, own);
    },
  };
}

/** Loads a person's viewer. Choices for unknown or retired IDs are dropped. */
export async function loadViewer(
  store: ExperimentChoiceStore,
  person: Person & { readonly id: string },
  registry: ExperimentRegistry = EXPERIMENTS,
  env: Environment = process.env,
): Promise<ExperimentViewer> {
  const stored = await store.read(person.id);
  const choices = new Map(
    [...stored].filter(([id]) => find(id, registry) !== undefined),
  );
  return { tester: isTester(person, env), choices };
}

/**
 * Saves a person's choice, or clears it with `null`. Refuses an experiment the
 * person cannot see, so a request cannot switch on a hidden one.
 */
export async function chooseExperiment(
  store: ExperimentChoiceStore,
  person: Person & { readonly id: string },
  id: string,
  choice: boolean | null,
  registry: ExperimentRegistry = EXPERIMENTS,
  env: Environment = process.env,
): Promise<void> {
  const experiment = find(id, registry);
  const viewer = { tester: isTester(person, env), choices: new Map() };
  if (!experiment || !experimentVisible(experiment, viewer))
    throw new ExperimentUnavailableError(id);
  await store.write(person.id, id, choice);
}
