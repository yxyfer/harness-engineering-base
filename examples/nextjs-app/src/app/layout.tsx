import type { Metadata } from "next";
import Link from "next/link";
import { ThemeSwitch } from "@/components/theme-switch";
import "./globals.css";

export const metadata: Metadata = {
  title: "Workroom · Synthetic reference",
  description:
    "A synthetic Next.js work-item foundation. No live integrations.",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" data-theme="paper">
      <body>
        <a className="skip-link" href="#main">
          Skip to content
        </a>
        <div className="shell">
          <aside className="sidebar">
            <Link className="brand" href="/">
              w<span>Workroom</span>
            </Link>
            <p className="eyebrow">Reference workspace</p>
            <nav aria-label="Main navigation">
              <Link href="/">
                Work items <span>03</span>
              </Link>
              <Link href="/components">
                Component kit <span>↗</span>
              </Link>
            </nav>
            <div className="sidebar-note">
              <span className="dot" />
              Synthetic environment
              <p>
                Owned components.
                <br />
                No connected services.
              </p>
            </div>
          </aside>
          <div className="workspace">
            <header className="topbar">
              <span>Workspace / Foundation</span>
              <ThemeSwitch />
            </header>
            <div className="demo-banner">
              SYNTHETIC DATA{" "}
              <span>
                Local SQLite and synthetic sessions · external SSO untested
              </span>
            </div>
            <main id="main">{children}</main>
            <footer>
              Next.js reference foundation{" "}
              <span>Step 11 · disposable local demonstration</span>
            </footer>
          </div>
        </div>
      </body>
    </html>
  );
}
