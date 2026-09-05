import React from 'react';
import { Trash2 } from 'lucide-react';

export default function TodayLog({ logs, onDeleteLog }) {
  return (
    <div className="log-section">
      <div className="log-title">Today's log</div>
      
      {logs.length === 0 ? (
        <div style={{ color: '#94A3B8', fontSize: '13px', fontStyle: 'italic', padding: '12px 0' }}>
          No meals logged yet today. Click + to add your food photo.
        </div>
      ) : (
        <div className="log-list">
          {logs.map((item) => (
            <div key={item.id} className="log-item">
              <span className="log-item-time">{item.time}</span>
              <span className="log-item-name">{item.name}</span>
              <span className="log-item-calories">{item.calories}</span>
              {onDeleteLog && (
                <button 
                  className="log-item-delete" 
                  onClick={() => onDeleteLog(item.id)}
                  title="Remove log item"
                >
                  <Trash2 size={14} />
                </button>
              )}
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
