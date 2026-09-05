import React, { useState } from 'react';

export default function GoalModal({ currentGoal, onSave, onClose }) {
  const [val, setVal] = useState(currentGoal);

  const handleSubmit = (e) => {
    e.preventDefault();
    const num = parseInt(val, 10);
    if (!isNaN(num) && num > 0) {
      onSave(num);
    }
  };

  return (
    <div className="modal-backdrop" onClick={onClose}>
      <div className="goal-modal-card animate-fadeIn" onClick={(e) => e.stopPropagation()}>
        <div className="goal-modal-title">Set Calorie Goal</div>
        <div className="goal-modal-sub">Customize your target daily energy intake</div>

        <form onSubmit={handleSubmit}>
          <input 
            type="number" 
            className="goal-input" 
            value={val} 
            onChange={(e) => setVal(e.target.value)}
            min="500" 
            max="10000"
            step="50"
            autoFocus
          />

          <div className="goal-modal-actions">
            <button type="button" className="cancel-modal-btn" onClick={onClose}>
              Cancel
            </button>
            <button type="submit" className="save-goal-btn">
              Save Goal
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}
