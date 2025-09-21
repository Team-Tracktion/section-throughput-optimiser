import "./globals.css";
import { AuthProvider } from "../hooks/use-auth";
import { Analytics } from "@vercel/analytics/react";

import { Suspense } from "react";

export const metadata = {
  title: "Railway Control System",
  description: "Intelligent decision-support system for train operations",
  generator: "Railway Control System",
};

export default function RootLayout({ children }) {
  return (
    <html lang="en" className="dark">
      <body className="font-sans">
        <Suspense fallback={<div>Loading...</div>}>
          <AuthProvider>{children}</AuthProvider>
          <Analytics />
        </Suspense>
      </body>
    </html>
  );
}
