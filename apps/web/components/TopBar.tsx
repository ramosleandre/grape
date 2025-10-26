'use client';

import Image from 'next/image';
import Link from 'next/link';

interface TopBarProps {
  projectName?: string;
}

export default function TopBar({ projectName = 'My Knowledge Graph' }: TopBarProps) {
  return (
    <div className="w-full h-16 bg-white border-b border-[#E5E7EB] flex items-center justify-between px-6">
      {/* Left: Logo and Breadcrumb */}
      <div className="flex items-center gap-4">
        <Link href="/" className="flex items-center">
          <Image
            src="/grape_logo.png"
            alt="Grape Logo"
            width={32}
            height={32}
            className="cursor-pointer"
          />
        </Link>
        <div className="flex items-center gap-2 text-sm text-[#6B7280]">
          <Link href="/" className="hover:text-[#1C1C1C] transition-colors">
            Dashboard
          </Link>
          <span>/</span>
          <span className="text-[#1C1C1C] font-medium">{projectName}</span>
        </div>
      </div>

      {/* Right: AI-Assisted Editing Command Input (Placeholder) */}
      <div className="flex-1 max-w-md ml-8">
        <input
          type="text"
          placeholder="AI-assisted editing command (e.g., 'select nodes related to ontology')"
          className="w-full h-10 px-4 text-sm border border-[#E5E7EB] rounded-lg focus:outline-none focus:ring-2 focus:ring-[#E57373] focus:border-transparent placeholder:text-[#6B7280]"
          disabled
        />
      </div>
    </div>
  );
}
