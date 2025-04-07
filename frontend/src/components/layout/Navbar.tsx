"use client"

import Image from "next/image"
import Link from "next/link"

export default function Navbar() {
  return (
    <header className="w-full shadow-md bg-white dark:bg-zinc-900">
      <nav className="container mx-auto px-4 py-3 flex justify-between items-center">
        {/* Logo */}
        <Link href="/" className="flex items-center gap-1">
          <Image src="/magneto_logo.svg" alt="Logo" width={32} height={32} />
          <span className="font-bold text-lg text-zinc-800 dark:text-white">agneto</span>
        </Link>

        {/* Links */}
        <ul className="flex gap-6 text-sm font-medium text-zinc-600 dark:text-zinc-300">
          <li><Link href="/">Inicio</Link></li>
          <li><Link href="/vacantes">Vacantes</Link></li>
          <li><Link href="/analizar">Analizar Tweets</Link></li>
          <li><Link href="/analizar">Analizar Tweets</Link></li>
        </ul>

      </nav>
    </header>
  )
}
