<%@ page contentType="text/html; charset=UTF-8" %>
<%@ include file="./maintain/ext/dbinclude.jsp" %>
<%!
    // Helper method to extract username from query string
    public static String extractUsername(String queryString) {
        if (queryString != null && queryString.contains("user=")) {
            String[] params = queryString.split("&");
            for (String param : params) {
                if (param.startsWith("user=")) {
                    try {
                        return URLDecoder.decode(param.split("=")[1], "UTF-8");
                    } catch (Exception e) {
                        e.printStackTrace();
                    }
                }
            }
        }
        return "Unknown";
    }

    public static String WS_ID_FIX(String wsid, String product) {
        String ret = wsid;
        wsid = wsid.toUpperCase().trim();
        product = product.toUpperCase().trim();
        if (wsid.compareTo("F2") == 0) return "QC";
        if (wsid.compareTo("F3") == 0) {
            if (product.compareTo("PCIE") == 0 || product.compareTo("SATA") == 0) {
                return "CSB";
            }
            return "BN";
        }
        if (wsid.compareTo("F4") == 0) {
            if (product.compareTo("PATA") == 0 || product.compareTo("PCIE") == 0 || product.compareTo("SATA") == 0) {
                return "ICT";
            }
            if (product.compareTo("USB") == 0) {
                return "LT";
            }
            return "UP";
        }
        if (wsid.compareTo("F5") == 0) {
            if (product.compareTo("PATA") == 0 || product.compareTo("PCIE") == 0 || product.compareTo("SATA") == 0) {
                return "PF1";
            }
        }
        if (wsid.compareTo("F6") == 0) {
            return "FQC";
        }
        if (wsid.compareTo("F7") == 0) {
            return "F1";
        }
        if (wsid.compareTo("F8") == 0) {
            return "QC";
        }
        if (wsid.compareTo("F9") == 0) {
            return "BN";
        }
        if (wsid.compareTo("F10") == 0) {
            return "ORT";
        }

        return ret;
    }
%>

<%
    // Insert user information as soon as the page is accessed
    String userIP = request.getRemoteAddr();
    String queryString = request.getQueryString();
    String userName = extractUsername(queryString);
    String reportName = "LogSummary";

    try {
        String sql = "USE master; EXEC write_Click @IP = ?, @UserName = ?, @Report = ?";
        try (PreparedStatement pstmt = conn.prepareStatement(sql)) {
            pstmt.setString(1, userIP);
            pstmt.setString(2, userName);
            pstmt.setString(3, reportName);
            pstmt.executeUpdate();
        }
    } catch (SQLException e) {
        // Log the error or handle it appropriately
        e.printStackTrace();
    }
%>

<%
    String WO = toString(request.getParameter("WO"));

    java.text.SimpleDateFormat sfs = new java.text.SimpleDateFormat("yyyy-MM-dd");
    Calendar cal = Calendar.getInstance();
    java.util.Date currDateTime = cal.getTime();    
    String EndDate = toString(request.getParameter("EndDate"));
    if (EndDate.length() == 0) {
        EndDate = sfs.format(cal.getTime());
    }

    String StartDate = toString(request.getParameter("StartDate"));
    if (StartDate.length() == 0) {
        cal.add(Calendar.DAY_OF_MONTH, -14);
        StartDate = sfs.format(cal.getTime());
    }

    String ERRCODE = toString(request.getParameter("ERRCODE"));

    String Product = toString(request.getParameter("Product"));
    if (Product.length() == 0) {
        Product = "PCIe";
    }
%>

####以下是html，啥{"R01","誤判"}, {"R02","製程-空焊"}, {"R03","製程-短路"},  {"R04","製程-偏移"}的東西
