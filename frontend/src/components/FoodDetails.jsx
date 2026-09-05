import React, { useState } from 'react';
import { ArrowLeft, Plus, Trash2 } from 'lucide-react';

export default function FoodDetails({ analysisData, onBack, onDiscard, onAddMeal }) {
  const [items, setItems] = useState(analysisData?.detected_items || [
    { id: 1, name: 'Grilled chicken breast', portion: '150g portion', calories: 240, protein: 31, carbs: 0, fat: 3.5 },
    { id: 2, name: 'Steamed white rice', portion: '1 cup', calories: 205, protein: 4.2, carbs: 45, fat: 0.4 },
    { id: 3, name: 'Steamed broccoli', portion: 'half cup', calories: 55, protein: 3.7, carbs: 11, fat: 0.6 },
    { id: 4, name: 'Olive oil drizzle', portion: '1 tsp', calories: 40, protein: 0, carbs: 0, fat: 4.5 },
  ]);

  const totalCalories = items.reduce((acc, item) => acc + (Number(item.calories) || 0), 0);
  
  const totalProtein = Math.round(items.reduce((acc, item) => acc + (Number(item.protein) || 0), 0));
  const totalCarbs = Math.round(items.reduce((acc, item) => acc + (Number(item.carbs) || 0), 0));
  const totalFat = Math.round(items.reduce((acc, item) => acc + (Number(item.fat) || 0), 0));

  const removeItem = (id) => {
    setItems(items.filter(it => it.id !== id));
  };

  const handleSaveToLog = () => {
    onAddMeal({
      name: items.length > 0 ? items[0].name + (items.length > 1 ? ` + ${items.length - 1} items` : '') : 'Logged meal',
      calories: totalCalories,
      protein: totalProtein || 32,
      carbs: totalCarbs || 54,
      fat: totalFat || 18,
      items: items
    });
  };

  return (
    <div className="food-details-container animate-fadeIn">
      <div className="food-details-header">
        <button className="back-btn" onClick={onBack}>
          <ArrowLeft size={18} /> Food details
        </button>
      </div>

      {/* Hero Banner Image */}
      <div className="food-hero-banner">
        {analysisData?.image_url ? (
          <img src={analysisData.image_url} alt="Meal preview" />
        ) : (
          <div style={{
            width: '100%',
            height: '100%',
            background: 'linear-gradient(135deg, #B58448 0%, #D4A853 50%, #8C6228 100%)',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            color: '#FFFFFF',
            fontWeight: 700,
            letterSpacing: 1
          }}>
            MEAL PHOTO PREVIEW
          </div>
        )}
      </div>

      <div className="detected-section">
        <div className="detected-heading">Detected items</div>

        <div className="detected-items-list">
          {items.map((item) => (
            <div key={item.id} className="food-item-row">
              <div className="food-item-info">
                <span className="food-item-title">{item.name}</span>
                <span className="food-item-portion">{item.portion}</span>
              </div>
              <div style={{ display: 'flex', alignItems: 'center', gap: 12 }}>
                <span className="food-item-calories">{item.calories}</span>
                <button 
                  onClick={() => removeItem(item.id)}
                  style={{ background: 'none', border: 'none', color: '#94A3B8', cursor: 'pointer' }}
                  title="Remove item"
                >
                  <Trash2 size={14} />
                </button>
              </div>
            </div>
          ))}
        </div>

        {/* Total calories */}
        <div className="total-summary-row">
          <span className="total-label-text">Total</span>
          <span className="total-value-text">{totalCalories}</span>
        </div>

        {/* Macro bar */}
        <div className="food-macro-summary">
          <div className="macro-pill-bar">
            <div style={{ width: '35%', background: '#2563EB' }} />
            <div style={{ width: '45%', background: '#06B6D4' }} />
            <div style={{ width: '20%', background: '#94A3B8' }} />
          </div>
          <div className="macro-labels-line">
            <span>Protein <strong style={{ color: '#0F172A' }}>{totalProtein || 32}g</strong></span>
            <span>Carbs <strong style={{ color: '#0F172A' }}>{totalCarbs || 54}g</strong></span>
            <span>Fat <strong style={{ color: '#0F172A' }}>{totalFat || 18}g</strong></span>
          </div>
        </div>

        {/* Action Buttons */}
        <div className="food-details-actions">
          <button className="btn-discard" onClick={onDiscard}>
            Discard
          </button>
          <button className="btn-save-log" onClick={handleSaveToLog}>
            Add to today's log
          </button>
        </div>
      </div>
    </div>
  );
}
