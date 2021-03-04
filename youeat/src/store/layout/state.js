export const DEFAULT_HEADER_TITLE_VAL = 1;
export const HEADER_ACTION_NORMAL = "normal";
export const HEADER_ACTION_SEARCH = "search";


export default function () {
  return {
    //
    headerTitle:DEFAULT_HEADER_TITLE_VAL,
    headerAction:HEADER_ACTION_NORMAL,
    dialogAction: -1,
    mealIdSelected: -1,
    from:undefined,
    searchPageTabSelected: "meal",
    mealViewTabSelected:"Stats",
    searchMode:false
  }
}
