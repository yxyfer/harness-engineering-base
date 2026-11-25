import assert from 'node:assert/strict';
import { existsSync } from 'node:fs';
import { join } from 'node:path';
import { test } from 'node:test';
import { fileURLToPath } from 'node:url';
import {
  EXPERIMENT_ID,
  EXPERIMENTS,
  type ExperimentRegistry,
} from '../src/config/experiments';
import {
  activeExperimentIds,
  chooseExperiment,
  ExperimentUnavailableError,
  experimentActive,
  experimentStates,
  isTester,
  loadViewer,
  memoryChoiceStore,
  requireExperiment,
} from '../src/core/experiments';

const appRoot = fileURLToPath(new URL('../', import.meta.url));

const registry: ExperimentRegistry = [
  {
    id: 'early',
    name: 'Early',
    description: 'Testers only.',
    source: 'src/experimental/early',
    owner: 'test',
    stage: 'testers',
  },
  {
    id: 'open',
    name: 'Open',
    description: 'Anyone may opt in.',
    source: 'src/experimental/open',
    owner: 'test',
    stage: 'everyone',
  },
  {
    id: 'paid',
    name: 'Paid',
    description: 'Calls a billed provider.',
    source: 'src/experimental/paid',
    owner: 'test',
    stage: 'testers',
    billed: true,
  },
  {
    id: 'stopped',
    name: 'Stopped',
    description: 'Switched off.',
    source: 'src/experimental/stopped',
    owner: 'test',
    stage: 'off',
  },
];
const none = new Map<string, boolean>();
const tester = { tester: true, choices: none };
const member = { tester: false, choices: none };

test('the registry is well formed and names real entry points', () => {
  const ids = new Set<string>();
  for (const experiment of EXPERIMENTS) {
    assert.match(experiment.id, EXPERIMENT_ID);
    assert.ok(!ids.has(experiment.id), `${experiment.id} is registered twice`);
    ids.add(experiment.id);
    assert.ok(experiment.name && experiment.description && experiment.owner);
    assert.ok(
      ['index.ts', 'index.tsx'].some((entry) =>
        existsSync(join(appRoot, experiment.source, entry)),
      ),
      `${experiment.source} has no index entry point`,
    );
  }
});

test('testers get testers-stage experiments by default; others do not see them', () => {
  assert.equal(experimentActive('early', tester, registry), true);
  assert.equal(experimentActive('early', member, registry), false);
  assert.deepEqual(
    experimentStates(member, registry).map((state) => state.id),
    ['open'],
  );
});

test('everyone-stage experiments are on for testers and opt-in for others', () => {
  assert.equal(experimentActive('open', tester, registry), true);
  assert.equal(experimentActive('open', member, registry), false);
  const optedIn = { tester: false, choices: new Map([['open', true]]) };
  assert.equal(experimentActive('open', optedIn, registry), true);
});

test('a tester can turn an experiment off, and back to the default', () => {
  const off = { tester: true, choices: new Map([['early', false]]) };
  assert.equal(experimentActive('early', off, registry), false);
  const [state] = experimentStates(off, registry);
  assert.deepEqual(
    { active: state.active, byDefault: state.byDefault, chosen: state.chosen },
    { active: false, byDefault: true, chosen: true },
  );
});

test('a billed experiment is never on by default, even for testers', () => {
  assert.equal(experimentActive('paid', tester, registry), false);
  const chosen = { tester: true, choices: new Map([['paid', true]]) };
  assert.equal(experimentActive('paid', chosen, registry), true);
});

test('off wins over every choice, and unknown IDs are off', () => {
  const chosen = {
    tester: true,
    choices: new Map([
      ['stopped', true],
      ['retired', true],
    ]),
  };
  assert.equal(experimentActive('stopped', chosen, registry), false);
  assert.equal(experimentActive('retired', chosen, registry), false);
  assert.deepEqual([...activeExperimentIds(chosen, registry)].sort(), [
    'early',
    'open',
  ]);
  assert.throws(
    () => requireExperiment('stopped', chosen, registry),
    ExperimentUnavailableError,
  );
});

test('testers come from EXPERIMENT_TESTERS, and everyone in development', () => {
  const person = { id: 'u1', email: 'Ada@Example.com' };
  assert.equal(isTester(person, { NODE_ENV: 'development' }), true);
  assert.equal(isTester(person, { NODE_ENV: 'production' }), false);
  assert.equal(
    isTester(person, { EXPERIMENT_TESTERS: 'ada@example.com' }),
    true,
  );
  assert.equal(isTester(person, { EXPERIMENT_TESTERS: 'x, u1' }), true);
  assert.equal(
    isTester(person, {
      EXPERIMENT_TESTERS: 'someone@else',
      NODE_ENV: 'development',
    }),
    false,
  );
  const warnings: string[] = [];
  const env = { EXPERIMENT_TESTERS: '*', NODE_ENV: 'production' };
  assert.equal(
    isTester(person, env, (m) => warnings.push(m)),
    true,
  );
  assert.equal(
    isTester(person, env, (m) => warnings.push(m)),
    true,
  );
  assert.equal(warnings.length, 1, 'warns once per process');
});

test('choices are stored explicitly, cleared, and refused when hidden', async () => {
  const store = memoryChoiceStore();
  const person = { id: 'u1' };
  const env = { EXPERIMENT_TESTERS: 'u1' };
  await chooseExperiment(store, person, 'early', false, registry, env);
  let viewer = await loadViewer(store, person, registry, env);
  assert.equal(experimentActive('early', viewer, registry), false);
  await chooseExperiment(store, person, 'early', null, registry, env);
  viewer = await loadViewer(store, person, registry, env);
  assert.equal(experimentActive('early', viewer, registry), true);

  const stranger = { id: 'u2' };
  await assert.rejects(
    chooseExperiment(store, stranger, 'early', true, registry, env),
    ExperimentUnavailableError,
  );
  await assert.rejects(
    chooseExperiment(store, person, 'retired', true, registry, env),
    ExperimentUnavailableError,
  );
});
