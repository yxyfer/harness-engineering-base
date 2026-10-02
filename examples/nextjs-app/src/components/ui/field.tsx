import type { ComponentProps } from "react";

export function Field({
  id,
  label,
  error,
  ...props
}: ComponentProps<"input"> & { id: string; label: string; error?: string }) {
  return (
    <div className="field">
      <label htmlFor={id}>{label}</label>
      <input
        id={id}
        aria-invalid={Boolean(error)}
        aria-describedby={error ? `${id}-error` : undefined}
        {...props}
      />
      {error && (
        <p id={`${id}-error`} role="alert" className="field-error">
          {error}
        </p>
      )}
    </div>
  );
}
