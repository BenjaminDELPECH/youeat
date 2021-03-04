from users.models import Profile



def calculateNeeds(activity, poid, totalCalories):
    # 0.8g/kg is recommanded for an normal
    # 2g/kg is recommended for most active
    # version 1 of Nutrients Stats support 7 levels of activity
    # so the step value between 0.8 to 2 will be  (2 - 0.8) / 6 = 0.2
    proteinNeedPerKg = 0.8 + (activity - 1) * 0.2
    proteinActivityFactorCoeff = proteinNeedPerKg / 0.8
    proteinTotalGramNeed = proteinNeedPerKg * poid

    # graisses mono insaturees doivent representer 25% de l'apport calorique total
    # graisses polyinsaturees peuvent representee 6.5%
    # satures, entre 8 et 10%
    # 25 + 6.5 + 8 = 40
    monoInsaturedTotalGramNeed = (totalCalories * 0.25) / 9
    polyinsaturedTotalGramNeed = (totalCalories * 0.065) / 9
    saturedTotalGramNeed = (totalCalories * 0.08) / 9
    lipidTotalGramNeed = monoInsaturedTotalGramNeed + polyinsaturedTotalGramNeed + saturedTotalGramNeed
    # Glucid will be the rest
    # 4 calories for one gram
    totalGlucidGramNeed = (totalCalories - lipidTotalGramNeed * 9 - proteinTotalGramNeed * 4) / 4
    return lipidTotalGramNeed, monoInsaturedTotalGramNeed, polyinsaturedTotalGramNeed, proteinActivityFactorCoeff, proteinTotalGramNeed, saturedTotalGramNeed, totalGlucidGramNeed

def handleProfilContext(profil):
    activity = profil.activity
    poid = profil.poid
    men = profil.sexe == 1
    weightCoeff = 13.75 if men else 9.56
    heigthCoeff = 5 if men else 1.85
    ageCoeff = 6.77 if men else 4.67
    additional = 66.5 if men else 655
    activityCoeff = 1.05 + ((activity / 10) - 0.1)
    basalMetabolism = additional + (weightCoeff * profil.poid) + (heigthCoeff * profil.taille) - (
            ageCoeff * profil.age)
    totalCalories = basalMetabolism * activityCoeff
    return activity, poid, profil, totalCalories

def calculateProfilProperties(info):
    totalCalories = 2100
    poid = 70
    activity = 3
    if info.context.user.id:
        user_id = info.context.user.id
        profil = Profile.objects.get(user_id=user_id)
        activity, poid, profil, totalCalories = handleProfilContext(profil)
    return activity, poid, totalCalories


