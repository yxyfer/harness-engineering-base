import { createServer } from "node:http";
import { pageContent } from "../app/content.js";

const port = Number(process.env.PORT || 3000);
const server = createServer((_request, response) => {
  response.writeHead(200, { "content-type": "text/html; charset=utf-8" });
  response.end(`<main><h1>${pageContent.title}</h1><p>${pageContent.description}</p></main>`);
});

server.listen(port, "127.0.0.1", () => {
  const address = server.address();
  console.log(`Example listening on http://127.0.0.1:${address.port}`);
});
