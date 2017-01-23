/**
 * Created by berm on 21-12-16.
 */
function CheckIfServerIsOnline(key) {
    var ServerKey = key;
    var xml_http = new XMLHttpRequest();
    if (ServerKey != "") {
        xml_http.open("GET", "/live/Online/key/" + ServerKey + "/time/0/", false);
        console.log(ServerKey);
    } else {
        xml_http.open("GET", "/live/Online/key/" + ServerKey + "/time/0/", false);

    }
    xml_http.send();
    document.getElementById("ServerOnlineOutput").innerHTML = xml_http.responseText;
}

function UpdateServerOnline(key) {
    setInterval(CheckIfServerIsOnline(key), 1000);
}