import React from 'react';
import { Flame } from 'lucide-react';

export default function Header({ dateStr = "Fri 5 Sep" }) {
  return (
    <header className="app-top-bar">
      <div className="brand-logo">
        <Flame className="brand-icon" strokeWidth={2.5} />
        <span>OjoneAI</span>
      </div>
      <div className="header-date">
        {dateStr}
      </div>
    </header>
  );
}
