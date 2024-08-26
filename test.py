 當然，我很樂意為您提供完整的程式碼。我會整合之前的修改，並確保包含所有必要的部分。



```jsp

<%@ page contentType="text/html; charset=UTF-8" %>
<%@ page import="java.sql.*" %>
<%@ page import="java.net.*" %>
<%!
    public static String WS_ID_FIX( String wsid, String product ) {
        String ret=wsid;
        wsid = wsid.toUpperCase().trim();
        product = product.toUpperCase().trim();
        if ( wsid.compareTo("F2")==0 )  return "QC";
        if ( wsid.compareTo("F3")==0 )  {
            if ( product.compareTo("PCIE")==0 || product.compareTo("SATA")==0 ) {
                return "CSB";
            }
            return "BN";
        }
        if ( wsid.compareTo("F4")==0 )  {
            if ( product.compareTo("PATA")==0||product.compareTo("PCIE")==0|| product.compareTo("SATA")==0 ) {
                return "ICT";
            }
            if ( product.compareTo("USB")==0 ) {
                return "LT";
            }
            return "UP";
        }
        if ( wsid.compareTo("F5")==0 )  {
            if ( product.compareTo("PATA")==0||product.compareTo("PCIE")==0|| product.compareTo("SATA")==0 ) {
                return "PF1";
            }
        }
        if ( wsid.compareTo("F6")==0 )  {
            return "FQC";
        }
        if ( wsid.compareTo("F7")==0 )  {
            return "F1";
        }
        if ( wsid.compareTo("F8")==0 )  {
            return "QC";
        }
        if ( wsid.compareTo("F9")==0 )  {
            return "BN";
        }
        if ( wsid.compareTo("F10")==0 )  {
            return "ORT";
        }

        return ret;
    }

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
// First database connection (assumed to be your existing connection)
Connection conn1 = null;
// Second database connection (for WebPlatForm database)
Connection conn2 = null;

try {
    // Initialize your first database connection (keep your existing code)
    Class.forName("com.microsoft.jdbc.sqlserver.SQLServerDriver");
    String url1 = "jdbc:microsoft:sqlserver://YOUR_SERVER1:1433;DatabaseName=YOUR_DB1";
    String user1 = "your_username1";
    String password1 = "your_password1";
    conn1 = DriverManager.getConnection(url1, user1, password1);

    // Initialize the second database connection
    Class.forName("com.microsoft.sqlserver.jdbc.SQLServerDriver");
    String url2 = "jdbc:sqlserver://YOUR_SERVER2:1433;databaseName=WebPlatForm";
    String user2 = "your_username2";
    String password2 = "your_password2";
    conn2 = DriverManager.getConnection(url2, user2, password2);

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
    String clicks_link = "LogSummary";
    String clicks_user = user;
    
    try {
        PreparedStatement pstmt = conn2.prepareStatement(
            "INSERT INTO [dbo].[WebPlatForm_Counter] ([IP], [USER], [REPORT], [CLICK_TIME]) " +
            "VALUES (?, ?, ?, GETDATE())");
        pstmt.setString(1, ip);
        pstmt.setString(2, clicks_user);
        pstmt.setString(3, clicks_link);
        pstmt.executeUpdate();
        pstmt.close();
    } catch (SQLException e) {
        out.println("Error inserting into WebPlatForm_Counter: " + e.getMessage());
    }

    String WO = request.getParameter("WO");
    if (WO == null) {
        WO = "";
    }
    String SkipDouble = request.getParameter("SkipDouble");
    if (SkipDouble == null || SkipDouble.length() == 0) {
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
</head>
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
                    WO:&nbsp;<input type=text name="WO" value="<%=WO%>">
                    移除重複CTL_ID:&nbsp;<select name="SkipDouble">
                        <option value="1" <%=SkipDouble.compareTo("1")==0 ? "selected":""%>>Y</option>
                        <option value="0" <%=SkipDouble.compareTo("1")!=0 ? "selected":""%>>N</option>
                    </select>
                    <input type="submit" name="search" value="doSearch">
                </form>
                <%
                if ( WO.length()>10 ) {
                    String pWS_ID="";
                    String moYM = "PELogSr_20"+WO.substring(4,8);
                    
                    String sql = "use TIPTOP;select * from csfzr109 where PRODUCT_NUM='"+WO+"' ";
                    
                    Statement stmt = conn1.createStatement();
                    ResultSet rs=stmt.executeQuery(sql);
                    int quantity=1;
                    String product = "";
                    if ( rs.next() ) {
                        quantity = rs.getInt("QUANTITY");
                        product = rs.getString("PRODUCT");
                        String wostatus = rs.getString("CLOSE_STATUS");
                        if ( wostatus.indexOf("3")!=-1 ) {
                            wostatus="close";
                        }
                        else {
                            wostatus="open";
                        }
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
                    
                    sql = "select * from LogSystem.dbo.mfg_test_summary where WO='"+WO+"' and SkipDouble="+SkipDouble+" order by ws_id,cnt desc,id_01";
                    
                    java.text.DecimalFormat dformat = new java.text.DecimalFormat("0.00");
                    rs=stmt.executeQuery(sql);
                    while (rs.next()) {
                        String WS_ID = rs.getString("WS_ID");
                        String ID_01 = rs.getString("ID_01");
                        int cnt = rs.getInt("cnt");
                        if ( pWS_ID.compareTo(WS_ID)!=0 ) {
                            if ( pWS_ID.length()!=0 ) {
                %>
                            </table></div>
                <%				
                            }
                %>
                        <div style="width: 200px; display: inline-block;vertical-align:top;">
                        <table id="customers" >
                            <tr><th align="center" colspan=3 ><%=WS_ID_FIX( WS_ID, product )%></th></tr>
                <%		   }
                %>			
                        <tr>
                        <td align="center" ><a href=".\ErrDetail.jsp?WO=<%=WO%>&WS_ID=<%=WS_ID%>&ID_01=<%=ID_01%>&SkipDouble=<%=SkipDouble%>"><%=ID_01%></td>
                        <td align="center" ><%=cnt%></td>
                        <td align="center" ><%=dformat.format((100.0*cnt)/quantity)%>%</td>
                        </tr>
                <%
                        pWS_ID = WS_ID;
                    }
                %>
                        </table>
                        <br>&nbsp;
                        </div>
                <%		
                    stmt.close();
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

<%
} catch(Exception e) {
    out.println("Error: " + e.getMessage());
} finally {
    // Close both connections
    try {
        if(conn1 != null) conn1.close();
        if(conn2 != null) conn2.close();
    } catch(SQLException e) {
        out.println("Error closing connections: " + e.getMessage());
    }
}
%>

```

這個完整的 JSP 代碼包含了以下主要部分：

1. 必要的 import 語句和方法定義（WS_ID_FIX 和 getClientIpAddr）。
2. 兩個數據庫連接的初始化（conn1 和 conn2）。
3. 使用 conn2 來執行 WebPlatForm_Counter 表的插入操作。
4. 原有的 HTML 結構和表單。
5. 使用 conn1 來執行主要的數據查詢和顯示邏輯。
6. 所有必要的 CSS 樣式和 JavaScript 引用。
7. 適當的錯誤處理和連接關閉邏輯。

要使用這個代碼，你需要：

1. 替換 `YOUR_SERVER1`、`your_username1`、`your_password1` 為你的第一個數據庫（現有的）的連接詳情。
2. 替換 `YOUR_SERVER2`、`your_username2`、`your_password2` 為 WebPlatForm 數據庫的連接詳情。
3. 確保 `_title` 變量在某處被定義（可能在包含的文件中）。
4. 確保 "Navigation.jsp" 和 "Foot.jsp" 文件存在於
