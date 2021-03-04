import gql from "graphql-tag";

const conversion_factor_attrs = gql`
  fragment conversion_factor_attrs on ConversionFactorType{
    id
    conversionFactor
    measure{
      id
      nameFr
    }
  }
`;

export const link_meal_food_attrs = gql`
  fragment link_meal_food_attrs on LinkMealFoodType{
    id
    food{
      id
      nameFr

    }
    meal{
      id
    }
    conversionFactor{
      ...conversion_factor_attrs
    }
    quantity
  }
  ${conversion_factor_attrs}
`;

export const meal_attrs = gql`
  fragment meal_attrs on MealType{
    id
    name
    linkMealFoodSet{
      ...link_meal_food_attrs
    }
    fatherMeal{
      id
      sonMeal{
        id
        name
        linkMealFoodSet{
          ...link_meal_food_attrs
        }
      }
      linkmealroutinepropSet{
        id
        consumptionHour
      }
    }
    objectType{
      id
    }
  }
  ${link_meal_food_attrs}
`;


