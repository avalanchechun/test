 Certainly! I'll integrate the new username extraction method into your existing code. Here's the updated version:



```jsp

<%@ page contentType="text/html; charset=UTF-8" %>
<%@ include file="./maintain/ext/dbinclude.jsp" %>
<%@ page import="java.sql.*" %>
<%@ page import="java.net.URLDecoder" %>
<%!
    public static String WS_ID_FIX(String wsid, String product) {
        String ret = wsid;
        wsid = wsid.toUpperCase().trim();
        product = product.toUpperCase().trim();
        if (wsid.equals("F2")) return "QC";
        if (wsid.equals("F3")) {
            if (product.equals("PCIE") || product.equals("SATA")) {
                return "CSB";
            }
            return "BN";
        }
        if (wsid.equals("F4")) {
            if (product.equals("PATA") || product.equals("PCIE") || product.equals("SATA")) {
                return "ICT";
            }
            if (product.equals("USB")) {
                return "LT";
            }
            return "UP";
        }
        if (wsid.equals("F5")) {
            if (product.equals("PATA") || product.equals("PCIE") || product.equals("SATA")) {
                return "PF1";
            }
        }
        if (wsid.equals("F6")) return "FQC";
        if (wsid.equals("F7")) return "F1";
        if (wsid.equals("F8")) return "QC";
        if (wsid.equals("F9")) return "BN";
        if (wsid.equals("F10")) return "ORT";
        return ret;
    }

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

    String WO = request.getParameter("WO");
    WO = (WO != null) ? WO : "";
    String SkipDouble = request.getParameter("SkipDouble");
    if (SkipDouble == null || SkipDouble.isEmpty()) {
        SkipDouble = "1";
    }
%>

<html>
<head>
    <meta charset="utf-8" />
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
    <title><%=_title%></title>
    <link rel="stylesheet" type="text/css" href="./Content/bootstrap/css/bootstrap.min.css" />
    <link rel="stylesheet" type="text/css" href="./Content/sb-admin/sb-admin.min.css">
    <link rel="stylesheet" type="text/css" href="./Content/font-awesome/css/all.css">
    <link rel="stylesheet" href="./css/Phison.css">
    <style>
        #customers {
            font-family: "Trebuchet MS", Arial, Helvetica, sans-serif;
            border-collapse: collapse;
            width: 100%;
        }
        #customers td, #customers th {
            border: 1px solid #ddd;
            padding: 8px;
        }
        #customers tr:nth-child(even){background-color: #f2f2f2;}
        #customers tr:hover {background-color: #ddd;}
        #customers th {
            padding-top: 12px;
            padding-bottom: 12px;
            text-align: center;
            background-color: #4CAF50;
            color: white;
        }
    </style>
</head>
<body class="fixed-nav sticky-footer bg-dark" id="page-top">
    <!-- Navigation-->    
    <%@ include file="Navigation.jsp" %>
    <div class="content-wrapper">
        <div class="container-fluid">
            <ol class="breadcrumb">
                <!-- SiteMap-->
                Home > Log Summary( Search MP log by WO )
            </ol>

            <!-- Content-->
            <div id="body">
                <form method="post" name="mdata" action="LogSummary.jsp">
                    WO:&nbsp;<input type="text" name="WO" value="<%=WO%>">
                    移除重複CTL_ID:&nbsp;<select name="SkipDouble">
                        <option value="1" <%=SkipDouble.equals("1") ? "selected":""%>>Y</option>
                        <option value="0" <%=!SkipDouble.equals("1") ? "selected":""%>>N</option>
                    </select>
                    <input type="submit" name="search" value="doSearch">
                </form>
                <%
                if (WO.length() > 10) {
                    String pWS_ID = "";
                    String moYM = "PELogSr_20" + WO.substring(4, 8);
                    

                    PreparedStatement pstmt = null;
                    ResultSet rs = null;
                    try {
                        String sql = "USE TIPTOP; SELECT * FROM csfzr109 WHERE PRODUCT_NUM = ?";
                        pstmt = conn.prepareStatement(sql);
                        pstmt.setString(1, WO);
                        rs = pstmt.executeQuery();
                        
                        int quantity = 1;
                        String product = "";
                        if (rs.next()) {
                            quantity = rs.getInt("QUANTITY");
                            product = rs.getString("PRODUCT");
                            String wostatus = rs.getString("CLOSE_STATUS");
                            wostatus = (wostatus.indexOf("3") != -1) ? "close" : "open";
                %>
                            工單:&nbsp;<%=rs.getString("PRODUCT_NUM")%><br>
                            數量:&nbsp;&nbsp;<%=rs.getString("QUANTITY")%><br>
                            回貨數量:&nbsp;&nbsp;<%=rs.getString("PRODUCTION_QUANTITY")%><br>
                            Status:&nbsp;&nbsp;<%=wostatus%><br>
                            產品:&nbsp;&nbsp;<%=rs.getString("PRODUCT")%><br>
                            PCBA:&nbsp;&nbsp;<%=rs.getString("PCBA")%><br>
                            IC:&nbsp;&nbsp;<%=rs.getString("IC")%><br>
                            FW Ver:&nbsp;&nbsp;<%=rs.getString("FW_VER")%>-<%=rs.getString("FW_MINOR_CODE")%><br>
                            Flash:&nbsp;&nbsp;<%=rs.getString("FLASH_PROVIDER")%>-<%=rs.getString("Flash_SPEC6")%>-<%=rs.getString("FLASH_CAPACITY")%><br>
                            Flash Package:&nbsp;&nbsp;<%=rs.getString("FLASH_PACKAGE")%>*<%=rs.getString("FLASH_NUM")%><br>
                <%        
                        }
                        
                        sql = "SELECT * FROM LogSystem.dbo.mfg_test_summary WHERE WO = ? AND SkipDouble = ? ORDER BY ws_id, cnt DESC, id_01";
                        pstmt = conn.prepareStatement(sql);
                        pstmt.setString(1, WO);
                        pstmt.setString(2, SkipDouble);
                        rs = pstmt.executeQuery();
                        
                        java.text.DecimalFormat dformat = new java.text.DecimalFormat("0.00");
                        while (rs.next()) {
                            String WS_ID = rs.getString("WS_ID");
                            String ID_01 = rs.getString("ID_01");
                            int cnt = rs.getInt("cnt");
                            if (!pWS_ID.equals(WS_ID)) {
                                if (!pWS_ID.isEmpty()) {
                %>
                        </table></div>
                <%                
                                }
                %>
                        <div style="width: 200px; display: inline-block;vertical-align:top;">
                        <table id="customers">
                            <tr><th align="center" colspan=3><%=WS_ID_FIX(WS_ID, product)%></th></tr>
                <%           }
                            pWS_ID = WS_ID;
                %>            
                            <tr>
                            <td align="center"><a href=".\ErrDetail.jsp?WO=<%=WO%>&WS_ID=<%=WS_ID%>&ID_01=<%=ID_01%>&SkipDouble=<%=SkipDouble%>"><%=ID_01%></a></td>
                            <td align="center"><%=cnt%></td>
                            <td align="center"><%=dformat.format((100.0*cnt)/quantity)%>%</td>
                            </tr>
                <%
                        }
                %>
                        </table>
                        <br>&nbsp;
                        </div>
                <%        
                    } catch (SQLException e) {
                        e.printStackTrace();
                        out.println("<div style='color: red;'>檢索數據時發生錯誤。請稍後再試。</div>");
                    } finally {
                        if (rs != null) try { rs.close(); } catch (SQLException e) { /* ignored */ }
                        if (pstmt != null) try { pstmt.close(); } catch (SQLException e) { /* ignored */ }
                        if (conn != null) try { conn.close(); } catch (SQLException e) { /* ignored */ }
                    }
                }
                %>
            </div>
        </div>
    </div>
    <!-- /.container-fluid-->
    <%@ include file="Foot.jsp" %>    
    <!-- /.content-wrapper-->
    <script src="./Scripts/modernizr-2.6.2.js"></script>
    <script src="./Content/jquery/jquery.min.js"></script>
    <script src="./Content/popper/popper.min.js"></script>
    <script src="./Content/bootstrap/js/bootstrap.min.js"></script>
    <script src="./Content/sb-admin/sb-admin.min.js"></script>
    <script defer src="./Content/font-awesome/js/all.js"></script>

    <script type="text/javascript">
    </script>
</body>
</html>

<%@ include file="./maintain/ext/dbexit.jsp" %>

```


主要的更改如下：

1. 添加了新的 import 語句：
   ```jsp
   <%@ page import="java.net.URLDecoder" %>
   ```

2. 添加了新的 `extractUsername` 方法來從查詢字符串中提取用戶名：
   ```jsp
   public static String extractUsername(String queryString) {
       // ... (method implementation)
   }
   ```

3. 更新了獲取用戶名的代碼：
   ```jsp
   String queryString = request.getQueryString();
   String userName = extractUsername(queryString);
   ```

4. 移除了舊的用戶名獲取代碼：
   ```jsp
   // Removed:
   // String userName = request.getRemoteUser();
   // if (userName == null) {
   //     userName = "Unknown";
   // }
   ```

這些更改確保了程序現在從 URL 中提取用戶名，而不是依賴於 `request.getRemoteUser()`。如果 URL 中沒有用戶名，它將返回 "Unknown"。

其餘的代碼保持不變，包括數據庫操作、HTML 結構和 JavaScript 引用。這個更新應該能夠捕獲您提到的 URL 格式中的用戶名（例如 "phison_me2"），並將其用於日誌記錄目的。

請確保測試這個更新，特別是在不同的 URL 格式和缺少用戶參數的情況下，以確保它按預期工作。
