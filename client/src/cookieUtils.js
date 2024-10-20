// cookieUtils.js
export function getCookie(name) {
    let cookieArr = document.cookie.split("; ");

    for (let i = 0; i < cookieArr.length; i++) {
        let cookiePair = cookieArr[i].split("=");

        if (cookiePair[0] === name) {
            return cookiePair[1];
        }
    }
    return null;
}
