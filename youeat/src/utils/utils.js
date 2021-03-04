export function range(start, end) {
  return Array(end - start + 1).fill().map((_, idx) => start + idx)
}

  export function isMobile() {
    const toMatch = [
        /Android/i,
        /webOS/i,
        /iPhone/i,
        /iPad/i,
        /iPod/i,
        /BlackBerry/i,
        /Windows Phone/i
    ];

    return toMatch.some((toMatchItem) => {
        return navigator.userAgent.match(toMatchItem);
    });
}

export const firstLetterOnlyUpperCase=(string)=>{
  return string.charAt(0).toUpperCase() + string.slice(1).toLowerCase()
}


export function refresh() {
  var url = location.origin;
  var pathname = location.pathname;
  var hash = location.hash;

  location = url + pathname + '?application_refresh=' + (Math.random() * 100000) + hash;
}

export function cleanLocalStorage() {
  localStorage.removeItem("token")
  localStorage.removeItem("userId")
}

export function validatePassword(val) {
  var passw = /^[A-Za-z]\w{7,100}$/;
  if (val.match(passw)) {
    return true;
  } else {
    return "Entrez un mot de passe entre 6 et 100 caractères, qui contient au moins un caractère numérique";
  }
}
