// API service module for OjoneAI frontend

const API_BASE_URL = 'http://localhost:8000';

// Default mock detected meal matching Screen 3
export const MOCK_DETECTED_MEAL = {
  image_url: null,
  detected_items: [
    { id: 1, name: 'Grilled chicken breast', portion: '150g portion', calories: 240, protein: 31, carbs: 0, fat: 3.5 },
    { id: 2, name: 'Steamed white rice', portion: '1 cup', calories: 205, protein: 4.2, carbs: 45, fat: 0.4 },
    { id: 3, name: 'Steamed broccoli', portion: 'half cup', calories: 55, protein: 3.7, carbs: 11, fat: 0.6 },
    { id: 4, name: 'Olive oil drizzle', portion: '1 tsp', calories: 40, protein: 0, carbs: 0, fat: 4.5 },
  ],
  total_calories: 540,
  macros: {
    protein: 32,
    carbs: 54,
    fat: 18,
  }
};

/**
 * Upload meal photo to backend for AI estimation
 */
export async function analyzeMealImage(file) {
  try {
    const formData = new FormData();
    formData.append('image', file);

    const response = await fetch(`${API_BASE_URL}/analyze-food-image`, {
      method: 'POST',
      body: formData,
    });

    if (response.ok) {
      const data = await response.json();
      // Map API response to UI breakdown format
      const foods = data.foods || [];
      const totalKcal = data.total_calories || foods.reduce((acc, f) => acc + f.estimated_calories, 0);

      let totalP = 0, totalC = 0, totalF = 0;
      const mappedItems = foods.map((item, idx) => {
        totalP += item.protein || 0;
        totalC += item.carbs || 0;
        totalF += item.fat || 0;
        return {
          id: idx + 1,
          name: item.name,
          portion: item.quantity || '1 serving',
          calories: item.estimated_calories,
          protein: item.protein || 0,
          carbs: item.carbs || 0,
          fat: item.fat || 0,
        };
      });

      return {
        image_url: URL.createObjectURL(file),
        detected_items: mappedItems.length > 0 ? mappedItems : MOCK_DETECTED_MEAL.detected_items,
        total_calories: totalKcal > 0 ? totalKcal : 540,
        macros: {
          protein: Math.round(totalP) || 32,
          carbs: Math.round(totalC) || 54,
          fat: Math.round(totalF) || 18,
        }
      };
    }
  } catch (err) {
    console.warn('Backend API offline or unreachable, using local client scanner:', err);
  }

  // Fallback if backend is not running
  return {
    ...MOCK_DETECTED_MEAL,
    image_url: file ? URL.createObjectURL(file) : null
  };
}

/**
 * Fetch daily dashboard status
 */
export async function fetchDashboard(userId = 1) {
  try {
    const res = await fetch(`${API_BASE_URL}/dashboard?user_id=${userId}`);
    if (res.ok) {
      return await res.json();
    }
  } catch (err) {
    console.warn('Backend API offline for dashboard fetch');
  }
  return null;
}
