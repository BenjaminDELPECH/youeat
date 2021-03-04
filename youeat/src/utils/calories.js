export function getCalory(profile) {
    const {taille, poid, age, sexe, activity} = profile;
    let besoinCalorique;
    let weightCoeff;
    let tailleCoeff;
    let ageCoeff;
    let additionalCoeff;
    //homme
    if (sexe === 1) {
      weightCoeff = 13.7516
      tailleCoeff = 500.33
      ageCoeff = 6.7550
      additionalCoeff = 66.473
    } else {
      weightCoeff = 9.5634
      tailleCoeff = 184.96
      ageCoeff = 4.6756
      additionalCoeff = 655.0955
    }
    besoinCalorique = weightCoeff * poid + (tailleCoeff * taille) / 100 - ageCoeff * age + additionalCoeff;
    return Math.round(besoinCalorique * activity, 0);
}
