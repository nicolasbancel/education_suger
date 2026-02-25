import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Conseils de classe",
  description: "Aide à la préparation des conseils de classe",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="fr">
      <body className="bg-gray-50 min-h-screen">
        <header className="bg-white border-b px-6 py-4">
          <h1 className="text-lg font-semibold text-gray-800">
            Préparation des conseils de classe
          </h1>
        </header>
        <main className="max-w-5xl mx-auto px-6 py-8">{children}</main>
      </body>
    </html>
  );
}
