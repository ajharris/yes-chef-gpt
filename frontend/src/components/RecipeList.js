import React, { useState, useEffect } from 'react';
import axios from 'axios';

function RecipeList() {
  const [recipes, setRecipes] = useState([]);

  useEffect(() => {
    // Fetch recipes from backend
    axios.get('/api/recipes/ingredients')
      .then(response => {
        setRecipes(response.data);
      })
      .catch(error => {
        console.error("Error fetching recipes", error);
      });
  }, []);

  return (
    <div className="recipe-list">
      <h3>Recipes Based on Your Ingredients</h3>
      <ul>
        {recipes.length > 0 ? (
          recipes.map((recipe, index) => (
            <li key={index}>
              <h4>{recipe.name}</h4>
              <p>{recipe.description}</p>
            </li>
          ))
        ) : (
          <p>No recipes available</p>
        )}
      </ul>
    </div>
  );
}

export default RecipeList;
