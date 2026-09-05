import React from 'react';

export default function WeeklyChart({ currentDay = 'F' }) {
  const days = [
    { label: 'M', height: 45, active: false },
    { label: 'T', height: 55, active: false },
    { label: 'W', height: 40, active: false },
    { label: 'T', height: 60, active: false },
    { label: 'F', height: 75, active: true },
    { label: 'S', height: 30, active: false },
    { label: 'S', height: 20, active: false },
  ];

  return (
    <div className="weekly-chart-container">
      {days.map((item, idx) => (
        <div 
          key={idx} 
          className={`day-column ${item.label === currentDay && item.active ? 'active' : ''}`}
        >
          <div className="bar-track">
            <div 
              className="bar-fill" 
              style={{ height: `${item.height}%` }}
            />
          </div>
          <span className="day-label">{item.label}</span>
        </div>
      ))}
    </div>
  );
}
