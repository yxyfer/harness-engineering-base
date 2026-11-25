import type { ExperimentChoiceStore } from './experiments';

/**
 * Explicit experiment choices in a SQL table, one row per person and
 * experiment. Apply `experimentChoicesTable()` with the application's own
 * migration tool; this module never creates tables itself.
 */
export type Query = (
  text: string,
  values: readonly unknown[],
) => Promise<{ rows: readonly Record<string, unknown>[] }>;

const IDENTIFIER = /^[a-z_][a-z0-9_]*(\.[a-z_][a-z0-9_]*)?$/;

function checked(table: string): string {
  if (!IDENTIFIER.test(table))
    throw new Error(`"${table}" is not a plain table name.`);
  return table;
}

/** The migration for the table, PostgreSQL syntax. */
export function experimentChoicesTable(table = 'experiment_choices'): string {
  return `create table if not exists ${checked(table)} (
  person_id text not null,
  experiment_id text not null,
  enabled boolean not null,
  updated_at timestamptz not null default now(),
  primary key (person_id, experiment_id)
);`;
}

/**
 * A choice store over any client that runs parameterised SQL, such as
 * `pool.query` from `pg` or a Neon client. A missing row means "follow the
 * default", so clearing a choice deletes its row.
 */
export function sqlChoiceStore(
  query: Query,
  table = 'experiment_choices',
): ExperimentChoiceStore {
  const name = checked(table);
  return {
    async read(personId) {
      const { rows } = await query(
        `select experiment_id, enabled from ${name} where person_id = $1`,
        [personId],
      );
      return new Map(
        rows.map((row) => [String(row.experiment_id), row.enabled === true]),
      );
    },
    async write(personId, id, choice) {
      if (choice === null) {
        await query(
          `delete from ${name} where person_id = $1 and experiment_id = $2`,
          [personId, id],
        );
        return;
      }
      await query(
        `insert into ${name} (person_id, experiment_id, enabled) values ($1, $2, $3)
on conflict (person_id, experiment_id) do update set enabled = excluded.enabled, updated_at = now()`,
        [personId, id, choice],
      );
    },
  };
}
