/**
 * Created by berm on 19-12-16.
 */
function getPing() {
    var xml_http = new XMLHttpRequest();
    xml_http.open("GET", "/live/ping/key/Lqdie4ARBhbJtawrmTBCkenmhb9rvqgRzWN/time/0/", false);
    xml_http.send();
    var ping = xml_http.responseText;
    ping = parseInt(ping);
    document.getElementById("PingOutput").innerHTML = 'Latency: ' + ping + ' MS';
}
$( document ).ready(function() {
    updatePing();
});
function updatePing() {
    setInterval(getPing, 1000);
}
