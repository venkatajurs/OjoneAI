import React, { useState } from 'react';
import Header from './components/Header';
import CoachCard from './components/CoachCard';
import WeeklyChart from './components/WeeklyChart';
import CalorieTracker from './components/CalorieTracker';
import TodayLog from './components/TodayLog';
import GoalModal from './components/GoalModal';
import UploadModal from './components/UploadModal';
import FoodDetails from './components/FoodDetails';
import { Plus, LayoutGrid, Smartphone } from 'lucide-react';

export default function App() {
  // App state matching the wireframe mockups
  const [viewMode, setViewMode] = useState('interactive'); // 'interactive' or 'grid'
  const [activeScreen, setActiveScreen] = useState('home'); // 'home', 'upload', 'details'
  
  const [goal, setGoal] = useState(2200);
  const [showGoalModal, setShowGoalModal] = useState(false);

  const [logs, setLogs] = useState([
    { id: 1, time: '8:05', name: 'Protein shake', calories: 210, protein: 25, carbs: 5, fat: 2 },
    { id: 2, time: '12:40', name: 'Grilled chicken bowl', calories: 540, protein: 42, carbs: 55, fat: 12 },
    { id: 3, time: '4:10', name: 'Greek yogurt', calories: 150, protein: 15, carbs: 12, fat: 0 },
  ]);

  const [analysisResult, setAnalysisResult] = useState(null);

  // Derived state calculations
  const consumedCalories = logs.reduce((sum, item) => sum + (item.calories || 0), 0);

  const macros = {
    protein: logs.reduce((sum, item) => sum + (item.protein || 0), 0),
    carbs: logs.reduce((sum, item) => sum + (item.carbs || 0), 0),
    fat: logs.reduce((sum, item) => sum + (item.fat || 0), 0),
  };

  // Handlers
  const handleImageAnalyzed = (data) => {
    setAnalysisResult(data);
    setActiveScreen('details');
  };

  const handleAddMealToLog = (meal) => {
    const now = new Date();
    const timeStr = `${now.getHours()}:${now.getMinutes() < 10 ? '0' : ''}${now.getMinutes()}`;

    const newLog = {
      id: Date.now(),
      time: timeStr,
      name: meal.name,
      calories: meal.calories,
      protein: meal.protein,
      carbs: meal.carbs,
      fat: meal.fat,
    };

    setLogs([...logs, newLog]);
    setActiveScreen('home');
    setAnalysisResult(null);
  };

  const handleDeleteLog = (id) => {
    setLogs(logs.filter(it => it.id !== id));
  };

  return (
    <main>
      {/* Top Viewport Navigation Tabs */}
      <div className="app-viewport-switcher">
        <button 
          className={`view-tab-btn ${viewMode === 'interactive' ? 'active' : ''}`}
          onClick={() => setViewMode('interactive')}
        >
          <Smartphone size={14} /> Interactive Flow
        </button>
        <button 
          className={`view-tab-btn ${viewMode === 'grid' ? 'active' : ''}`}
          onClick={() => setViewMode('grid')}
        >
          <LayoutGrid size={14} /> 3-Screen Design Grid
        </button>
      </div>

      {viewMode === 'grid' ? (
        /* Side-by-Side 3 Screen Wireframe View */
        <div className="screens-grid animate-fadeIn">
          {/* Screen 1: Home entry point */}
          <div className="screen-card-wrapper">
            <div className="screen-header-badge">
              <span>1. Home entry point, coach and today's totals</span>
            </div>
            <div className="home-container">
              <Header dateStr="Fri 5 Sep" />
              <CoachCard consumed={1340} goal={2200} />
              <WeeklyChart currentDay="F" />
              <CalorieTracker 
                consumed={1340} 
                goal={2200} 
                macros={{ protein: 62, carbs: 128, fat: 41 }} 
                onEditGoal={() => setShowGoalModal(true)}
              />
              <TodayLog logs={logs} onDeleteLog={handleDeleteLog} />
              <div className="fab-container">
                <button className="fab-btn" onClick={() => setViewMode('interactive')}>
                  <Plus size={22} />
                </button>
              </div>
            </div>
          </div>

          {/* Screen 2: Upload a meal photo */}
          <div className="screen-card-wrapper">
            <div className="screen-header-badge">
              <span>2. Upload a meal photo (web upload)</span>
            </div>
            <UploadModal 
              onClose={() => {}} 
              onImageAnalyzed={(data) => {
                setAnalysisResult(data);
                setViewMode('interactive');
                setActiveScreen('details');
              }}
            />
          </div>

          {/* Screen 3: Food details itemized breakdown */}
          <div className="screen-card-wrapper">
            <div className="screen-header-badge">
              <span>3. Food details itemized breakdown</span>
            </div>
            <FoodDetails 
              analysisData={analysisResult} 
              onBack={() => {}}
              onDiscard={() => {}}
              onAddMeal={(meal) => handleAddMealToLog(meal)}
            />
          </div>
        </div>
      ) : (
        /* Interactive Mobile App View */
        <div className="screen-card-wrapper animate-fadeIn">
          {activeScreen === 'home' && (
            <div className="home-container">
              <Header dateStr="Fri 5 Sep" />
              <CoachCard consumed={consumedCalories} goal={goal} />
              <WeeklyChart currentDay="F" />
              <CalorieTracker 
                consumed={consumedCalories} 
                goal={goal} 
                macros={macros}
                onEditGoal={() => setShowGoalModal(true)}
              />
              <TodayLog logs={logs} onDeleteLog={handleDeleteLog} />
              
              <div className="fab-container">
                <button 
                  className="fab-btn" 
                  onClick={() => setActiveScreen('upload')}
                  title="Upload meal photo"
                >
                  <Plus size={22} />
                </button>
              </div>
            </div>
          )}

          {activeScreen === 'upload' && (
            <UploadModal 
              onClose={() => setActiveScreen('home')}
              onImageAnalyzed={handleImageAnalyzed}
            />
          )}

          {activeScreen === 'details' && (
            <FoodDetails 
              analysisData={analysisResult}
              onBack={() => setActiveScreen('upload')}
              onDiscard={() => {
                setAnalysisResult(null);
                setActiveScreen('home');
              }}
              onAddMeal={handleAddMealToLog}
            />
          )}
        </div>
      )}

      {/* Goal Setting Modal */}
      {showGoalModal && (
        <GoalModal 
          currentGoal={goal}
          onClose={() => setShowGoalModal(false)}
          onSave={(newGoal) => {
            setGoal(newGoal);
            setShowGoalModal(false);
          }}
        />
      )}
    </main>
  );
}
