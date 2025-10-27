//services/web/app/layout.tsx
import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";
import Link from "next/link";

const inter = Inter({ subsets: ["latin"] });

export const metadata: Metadata = {
  title: "HR-Lookout",
  description: "Enterprise Human Resources Information System",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className={inter.className}>
        <nav className="bg-gradient-to-r from-slate-900 via-blue-900 to-slate-900 text-white p-4 shadow-2xl border-b border-gray-700">
          <div className="container mx-auto flex items-center justify-between">
            <Link href="/" className="text-2xl font-bold bg-gradient-to-r from-blue-400 to-cyan-400 bg-clip-text text-transparent">
              HR-Lookout
            </Link>
            <div className="space-x-6 flex items-center">
              <Link href="/" className="hover:text-blue-400 transition font-medium">
                Dashboard
              </Link>
              <Link href="/organizations" className="hover:text-blue-400 transition font-medium">
                Organizations
              </Link>
              <Link href="/departments" className="hover:text-blue-400 transition font-medium">
                Departments
              </Link>
              <Link href="/employees" className="hover:text-blue-400 transition font-medium">
                Employees
              </Link>
            </div>
          </div>
        </nav>
        <main className="min-h-screen">
          {children}
        </main>
      </body>
    </html>
  );
}
