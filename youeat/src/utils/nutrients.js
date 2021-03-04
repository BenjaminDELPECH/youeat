export const fullNutrientsGroupList = (linkNutrientFoodsParam, nutrients) => {
  const linkNutrientFoods = linkNutrientFoodsParam
  nutrients = nutrients.filter(e => e.nutrientGroup !== null)
  let linkNutrientsFoodByGroup = []

  let nutrientGroupList = []
  for (let i = 0; i < linkNutrientFoods.length; i++) {
    const linkNutrientFood = linkNutrientFoods[i];
    let {nutrient} = linkNutrientFood
    nutrient = nutrients.find(e => e.id.toString() === nutrient.id.toString())
    if (nutrient !== undefined) {
      const {nutrientGroup} = nutrient
      if (nutrientGroup !== null) {
        const isAlreadyInList = nutrientGroupList.map(e => e.id)
          .indexOf(nutrientGroup.id) !== -1
        if (!isAlreadyInList) {
          nutrientGroupList.push(nutrientGroup)
        }
      }
    }
  }
  for (let i = 0; i < nutrientGroupList.length; i++) {
    const {id: nutrientGroupId, position: nutrientGroupOrder, deployedDefault} = nutrientGroupList[i];
    const nutrientListOfGroup = nutrients
      .filter(e => e.nutrientGroup.id === nutrientGroupId)
    const nutrientIdListOfGroup = nutrientListOfGroup
      .flatMap(e => e.id)
    const linkNutrientFoodListOfGroup = linkNutrientFoods.filter(e => {
      return nutrientIdListOfGroup.indexOf(e.nutrient.id) !== -1
    })
    const nutrientIdList = extractNutrientIdList(linkNutrientFoodListOfGroup);
    const nutrientGroupTitle = nutrientListOfGroup.find(e => e.nutrientGroupTitle === true)
    linkNutrientsFoodByGroup.push({
      "nutrientGroupOrder": nutrientGroupOrder,
      "deployedDefault": deployedDefault,
      "nutrientTitleId": nutrientGroupTitle ? nutrientGroupTitle.id : null,
      "nutrientIdList": nutrientIdList
    })
  }


  return linkNutrientsFoodByGroup.sort((a, b) => a.nutrientGroupOrder - b.nutrientGroupOrder)
}

const extractNutrientIdList = (linkNutrientFoodListOfGroup) => {
  let nutrientIdList = []
  for (let j = 0; j < linkNutrientFoodListOfGroup.length; j++) {
    const {nutrient} = linkNutrientFoodListOfGroup[j]
    const nutrientId = nutrient.id
    const isInNutrientIdList = nutrientIdList.indexOf(nutrientId) !== -1
    if (!isInNutrientIdList) {
      nutrientIdList.push(nutrientId)
    }
  }
  return nutrientIdList
}


export function generateNutrientsSumValueList(linkNutrientsFood, linkMealFoodSet) {
  let nutrientSumValues = []
  linkMealFoodSet.forEach(linkMealFood => {
    const elemFoodId = linkMealFood.food.id
    const nutrientIdProcessed = []
    linkNutrientsFood
      .filter(e => e.food.id === elemFoodId)
      .forEach(function (elem) {
        if (nutrientIdProcessed.indexOf(elem.nutrient.id) === -1) {
          nutrientIdProcessed.push(elem.nutrient.id)
          nutrientSumValues = updateNutrientSumValues(nutrientSumValues, linkMealFood, linkMealFoodSet, elemFoodId, elem);
        }
      });
  });
  return nutrientSumValues;
}


function updateNutrientSumValues(nutrientSumValues, linkMealFood, linkMealFoodSet, elemFoodId, elem) {
  if (linkMealFood.quantity) {
    let {quantity, conversionFactor: conversionFactorObj} = linkMealFood
    if (conversionFactorObj === null) {
      conversionFactorObj = {
        conversionFactor: 1,
        id: 1455,
      }
    }
    const conversionFactorValue = conversionFactorObj.conversionFactor
    let {nutrient, value} = elem
    value = quantity * value * conversionFactorValue
    const indexTarget = nutrientSumValues.findIndex(e => parseInt(e.nutrientId) === parseInt(nutrient.id))
    if (indexTarget !== -1) {
      let newNutrientSumValue = nutrientSumValues[indexTarget];
      const newVal = newNutrientSumValue.sumValue + value
      newNutrientSumValue.sumValue = getNutrientValRounded(newVal)
      nutrientSumValues.splice(indexTarget, 1, newNutrientSumValue)
    } else {
      // let newNutrientSumValue = this.generateNutrientSumValObj(nutrient, value)
      nutrientSumValues.push({
        nutrientId: nutrient.id,
        sumValue: value
      })
    }

  } else {
    console.error(elemFoodId)
  }

  return nutrientSumValues
}

export const getNutrientValRounded = (nutrientVal) => {
  if (nutrientVal > 10) {
    nutrientVal = Math.round(nutrientVal)
  } else if (nutrientVal > 1) {
    nutrientVal = Math.round(nutrientVal * 10) / 10
  } else {
    nutrientVal = Math.round(nutrientVal * 100) / 100
  }
  return nutrientVal;
}

export function getNutrientSumValueByLinkMealFoodSet(linkNutrientsFoods, linkMealFoodSet, nutrientIdSelected, store) {
  linkNutrientsFoods = linkNutrientsFoods.filter(e => e.nutrient.id.toString() === nutrientIdSelected.toString())
  let nutrientSumValues = generateNutrientsSumValueList(linkNutrientsFoods, linkMealFoodSet);
  let nutrientSumValueText = ""
  if (nutrientSumValues.length > 0) {
    let nutrientVal = nutrientSumValues[0].sumValue
    nutrientVal = getNutrientValRounded(nutrientVal);
    nutrientSumValueText += nutrientVal
    nutrientSumValueText += " "
    const nutrientTarget = store.getters['nutrients/getNutrients']
      .find(e => e.id.toString() === nutrientIdSelected.toString())
    const unit = nutrientTarget ? nutrientTarget.unit : ""
    nutrientSumValueText += unit
  } else {
    nutrientSumValueText += "NA"
  }
  return nutrientSumValueText
}


export function getCalory(store) {
  return store.getters["profil/getCalory"]
}


export function extractNeed(store, caloryPerG, propName) {
  const proportion = store.getters['profil/getProfile'][propName] / 100
  const caloryNb = getCalory(store) * proportion
  let besoin = caloryNb / caloryPerG
  besoin = Math.round(besoin, 2)
  return besoin;
}


export function calculateNutrientNeed(store, nutrient) {
  let besoin;
  const nutrientIdStr = nutrient.id.toString();
  if (nutrient.id.toString() === "208") {
    besoin = getCalory(store)
  } else if (nutrientIdStr === "205") {
    const caloryPerG = 4
    besoin = extractNeed(store, caloryPerG, "carbohydrateProportion");
  } else if (nutrientIdStr === "204") {
    const caloryPerG = 9
    besoin = extractNeed(store, caloryPerG, "fatProportion");
  } else if (nutrientIdStr === "203") {
    const caloryPerG = 4
    besoin = extractNeed(store, caloryPerG, "proteinProportion");
  }
  else if(nutrientIdStr==="209"){
    besoin = 291;
  }
  else if (nutrient.unit === "%") {
    besoin = 100;
  } else {
    const weigth = store.getters["profil/getProfile"].poid
    besoin = getBesoinFromnutrient(nutrient, weigth);
  }
  return besoin
}

function getBesoinFromnutrient(nutrient, weigth) {

  const besoin = nutrient.needPerKg ? nutrient.besoin * weigth : nutrient.besoin
  return parseFloat(besoin)
}


export function getLinkNutrientsFoodByMealId(storeLinkNutrientsFood, mealId) {
  const obj = storeLinkNutrientsFood.find(e => e.id.toString() === mealId.toString())
  return obj ? obj.linkNutrientsFood : []
}
