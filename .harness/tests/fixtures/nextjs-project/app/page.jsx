import { pageContent } from "./content.js";

export default function Page() {
  return (
    <main>
      <h1>{pageContent.title}</h1>
      <p>{pageContent.description}</p>
    </main>
  );
}
