import React from 'react';

export default function CoachCard({ consumed, goal }) {
  const remaining = Math.max(0, goal - consumed);
  
  let coachMsg = `Good afternoon. You're on track, ${remaining.toLocaleString()} kcal left before dinner.`;
  if (remaining <= 0) {
    coachMsg = `You've reached your daily calorie goal of ${goal.toLocaleString()} kcal. Great job staying focused!`;
  } else if (remaining < 300) {
    coachMsg = `Almost at your goal! You have ${remaining.toLocaleString()} kcal remaining for a light snack.`;
  }

  return (
    <div className="coach-section">
      <div className="coach-label">Coach</div>
      <div className="coach-message">{coachMsg}</div>
    </div>
  );
}
