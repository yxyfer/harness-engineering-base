# Architecture

Inspect [the current map](../../docs/ARCHITECTURE.md) and existing owners before
adding a component or layer. Update the map when a durable boundary changes.

Keep UI state, meaningful domain rules and external access distinguishable.
Introduce a separate module when it owns a real responsibility; this does not
require a repository interface, service or adapter for every small feature.

Reuse shared knowledge when the common concept is clear. Keep derived state
computed from its owner. A shared modal owns keyboard, focus and dismissal
behaviour; content and visual variants should compose it rather than copy it.

An architecture explanation must link to source and distinguish current, planned
and simulated behaviour. An import graph is supporting evidence, not a complete
explanation of the application.
