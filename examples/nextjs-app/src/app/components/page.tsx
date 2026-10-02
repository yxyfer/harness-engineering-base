import { Button } from "@/components/ui/button";
import { Field } from "@/components/ui/field";
import { StateExample, type ExampleState } from "@/components/state-example";

const states: ExampleState[] = [
  "loading",
  "empty",
  "error",
  "no-access",
  "success",
];

export default function ComponentsPage() {
  return (
    <>
      <div className="page-heading">
        <div>
          <p className="eyebrow">Owned foundation</p>
          <h1>
            One kit.
            <br />
            Two expressions.
          </h1>
          <p className="muted">
            Switch Paper / Ink above. Every component keeps the same
            implementation.
          </p>
        </div>
      </div>
      <section className="panel catalogue">
        <h2>Controls and variants</h2>
        <p className="muted">
          Button examples below are presentation-only. Interactive confirmation
          lives on the work-item edit page.
        </p>
        <div className="actions">
          <Button disabled>Primary (disabled)</Button>
          <Button variant="secondary" disabled>
            Secondary (disabled)
          </Button>
          <Button variant="quiet" disabled>
            Quiet (disabled)
          </Button>
        </div>
        <Field
          id="catalogue-title"
          label="Title example"
          defaultValue="A clear next step"
          readOnly
        />
        <Field
          id="catalogue-error"
          label="Invalid title example"
          defaultValue=""
          error="Use at least 3 characters for the title."
          readOnly
        />
      </section>
      <div className="state-grid">
        {states.map((state) => (
          <StateExample key={state} state={state} />
        ))}
      </div>
    </>
  );
}
