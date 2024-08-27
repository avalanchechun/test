我發現雖然無法取得username, 但是使用者的網址上會顯示http://pcdw0904017/rdmplog/LogSummary.jsp?user=phison_me2，因此我只要抓user=後面的東西就行了，幫我改程式吧
String userName = request.getRemoteUser();
if (userName == null) {
    userName = "Unknown";
}

請注意，網址不是我給定的，而是使用者進入這個.jsp網頁的網址。
