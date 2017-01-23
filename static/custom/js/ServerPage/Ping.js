/**
 * Created by berm on 19-12-16.
 */
function getPing(key) {
    var ServerKey = key;
    var xml_http = new XMLHttpRequest();
    if (ServerKey != "") {
        xml_http.open("GET", "/live/ping/key/" + ServerKey + "/time/0/", false);
        console.log(ServerKey);
    } else {
        xml_http.open("GET", "/live/ping/key/" + ServerKey + "/time/0/", false);
    }
    xml_http.send();
    var ping = xml_http.responseText;
    ping = parseInt(ping);
    document.getElementById("PingOutput").innerHTML = 'Latency: ' + ping + ' MS';
}
function UpdatePing(key) {
    setInterval(getPing(key), 1000);
}
