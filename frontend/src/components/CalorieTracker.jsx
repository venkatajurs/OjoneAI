import React from 'react';
import { Pencil } from 'lucide-react';

export default function CalorieTracker({ consumed, goal, macros, onEditGoal }) {
  const percentage = Math.min(100, Math.round((consumed / goal) * 100));

  // Multi-segmented bar ratios
  const totalMacros = (macros.protein * 4) + (macros.carbs * 4) + (macros.fat * 9) || 1;
  const proteinPct = Math.round(((macros.protein * 4) / totalMacros) * percentage);
  const carbsPct = Math.round(((macros.carbs * 4) / totalMacros) * percentage);
  const fatPct = Math.max(0, percentage - proteinPct - carbsPct);

  return (
    <div className="today-summary-section">
      <div className="today-label-row">
        <span className="today-label">Today</span>
        <button className="edit-goal-btn" onClick={onEditGoal} title="Click to edit daily calorie target">
          <Pencil size={12} /> Edit Goal
        </button>
      </div>

      <div className="calorie-number-display">
        <span className="calories-consumed">{consumed.toLocaleString()}</span>
        <span className="calories-goal-text">of {goal.toLocaleString()} kcal goal</span>
      </div>

      {/* Segmented Progress Bar */}
      <div className="segmented-progress-container">
        <div 
          className="progress-segment protein" 
          style={{ width: `${proteinPct}%` }}
          title={`Protein (${macros.protein}g)`}
        />
        <div 
          className="progress-segment carbs" 
          style={{ width: `${carbsPct}%` }}
          title={`Carbs (${macros.carbs}g)`}
        />
        <div 
          className="progress-segment fat" 
          style={{ width: `${fatPct}%` }}
          title={`Fat (${macros.fat}g)`}
        />
      </div>

      {/* Macros Row */}
      <div className="macros-grid">
        <div className="macro-item">
          <span className="macro-value">{macros.protein}g</span>
          <span className="macro-name">Protein</span>
        </div>
        <div className="macro-item">
          <span className="macro-value">{macros.carbs}g</span>
          <span className="macro-name">Carbs</span>
        </div>
        <div className="macro-item">
          <span className="macro-value">{macros.fat}g</span>
          <span className="macro-name">Fat</span>
        </div>
      </div>
    </div>
  );
}
