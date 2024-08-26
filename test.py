 Certainly! I'll integrate this functionality into your existing JSP code. We'll add this at the beginning of your JSP file, right after the initial declarations and before the HTML content starts. Here's how we can do it:



```jsp

<%@ page import="java.sql.*" %>
<%@ page import="java.net.*" %>
<%!
    public static String getClientIpAddr(HttpServletRequest request) {
        String ip = request.getHeader("X-Forwarded-For");
        if (ip == null || ip.length() == 0 || "unknown".equalsIgnoreCase(ip)) {
            ip = request.getHeader("Proxy-Client-IP");
        }
        if (ip == null || ip.length() == 0 || "unknown".equalsIgnoreCase(ip)) {
            ip = request.getHeader("WL-Proxy-Client-IP");
        }
        if (ip == null || ip.length() == 0 || "unknown".equalsIgnoreCase(ip)) {
            ip = request.getHeader("HTTP_CLIENT_IP");
        }
        if (ip == null || ip.length() == 0 || "unknown".equalsIgnoreCase(ip)) {
            ip = request.getHeader("HTTP_X_FORWARDED_FOR");
        }
        if (ip == null || ip.length() == 0 || "unknown".equalsIgnoreCase(ip)) {
            ip = request.getRemoteAddr();
        }
        return ip;
    }
%>
<%
    String user = request.getParameter("user");
    if (user == null) {
        user = "";
    }
    
    String hostAddress = "";
    try {
        InetAddress addr = InetAddress.getByName(request.getRemoteAddr());
        hostAddress = addr.getHostName();
    } catch (UnknownHostException e) {
        hostAddress = "Unknown";
    }
    
    user += "(" + hostAddress + ")";
    
    String ip = getClientIpAddr(request);
    String clicks_link = "LogSummary"; // Change this to match your JSP page name
    String clicks_user = user;
    
    // Assuming you have a database connection named 'conn' already established
    try {
        PreparedStatement pstmt = conn.prepareStatement(
            "INSERT INTO WebPlatForm.[dbo].[WebPlatForm_Counter] ([IP], [USER], [REPORT], [CLICK_TIME]) " +
            "VALUES (?, ?, ?, GETDATE())");
        pstmt.setString(1, ip);
        pstmt.setString(2, clicks_user);
        pstmt.setString(3, clicks_link);
        pstmt.executeUpdate();
        pstmt.close();
    } catch (SQLException e) {
        out.println("Error inserting into WebPlatForm_Counter: " + e.getMessage());
    }
%>

```


To integrate this into your existing JSP file, you should place this code right after your initial JSP declarations and database inclusion, but before the HTML content begins. Here's where you should insert it:

1. After these lines:
```jsp
<%@ page contentType="text/html; charset=UTF-8" %>
<%@ include file="./maintain/ext/dbinclude.jsp" %>
<%!
    // Your existing declarations
%>
```

2. And before this line:
```jsp
<html>
```

This code will capture the user's IP address, attempt to resolve the hostname, and insert a record into the WebPlatForm_Counter table each time the page is accessed.

Please note a few things:
1. This code assumes you already have a database connection named 'conn' established, which seems to be the case from your existing code.
2. The 'clicks_link' variable is set to "LogSummary". You may want to change this to match the actual name of your JSP page.
3. Error handling is minimal here. In a production environment, you might want to log errors more robustly.
4. This code will slightly increase the load time of your page, as it performs a database insert on each page load.

Remember to test this thoroughly in a non-production environment first to ensure it works as expected with your existing setup.
