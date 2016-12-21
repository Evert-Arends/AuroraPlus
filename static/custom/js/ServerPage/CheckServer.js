/**
 * Created by berm on 21-12-16.
 */
function CheckIfServerIsOnline() {
    var xml_http = new XMLHttpRequest();
    xml_http.open("GET", "/live/Online/key/Lqdie4ARBhbJtawrmTBCkenmhb9rvqgRzWN/time/0/", false);
    xml_http.send();
    document.getElementById("ServerOnlineOutput").innerHTML = xml_http.responseText;
}
$( document ).ready(function() {
    CheckIfServerIsOnline();
    UpdateServerOnline();
});
function UpdateServerOnline() {
    setInterval(CheckIfServerIsOnline, 1000);
}