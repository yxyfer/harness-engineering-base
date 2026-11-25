'use server';

import { revalidatePath } from 'next/cache';
import { chooseExperiment } from '@/core/experiments';
import { choiceStore, currentPerson } from './experiments';

/** Settings calls this through `ExperimentSettings`; `null` resets. */
export async function chooseExperimentAction(
  id: string,
  choice: boolean | null,
): Promise<void> {
  const person = await currentPerson();
  if (!person) throw new Error('Sign in to choose experiments.');
  await chooseExperiment(choiceStore, person, id, choice);
  revalidatePath('/', 'layout');
}
