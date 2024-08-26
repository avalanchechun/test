 當然，我很樂意為您提供完整的程式碼。我會結合原始代碼和我們的修改，為您呈現一個完整的、經過錯誤處理優化的版本。



```jsp

<%@ page contentType="text/html; charset=UTF-8" %>
<%@ include file="./maintain/ext/dbinclude.jsp" %>
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
        // First, check if the table exists
        DatabaseMetaData dbm = conn.getMetaData();
        ResultSet tables = dbm.getTables(null, "dbo", "WebPlatForm_Counter", null);
        if (tables.next()) {
            // Table exists
            PreparedStatement pstmt = conn.prepareStatement(
                "INSERT INTO WebPlatForm.dbo.WebPlatForm_Counter ([IP], [USER], [REPORT], [CLICK_TIME]) " +
                "VALUES (?, ?, ?, GETDATE())");
            pstmt.setString(1, ip);
            pstmt.setString(2, clicks_user);
            pstmt.setString(3, clicks_link);
            pstmt.executeUpdate();
            pstmt.close();
        } else {
            // Table doesn't exist, log the error
            System.err.println("Table WebPlatForm_Counter does not exist in the WebPlatForm database");
        }
    } catch (SQLException e) {
        // Log the full stack trace
        e.printStackTrace();
        // You might want to log this to a file instead of printing to console
        System.err.println("Error inserting into WebPlatForm_Counter: " + e.getMessage());
    }

    String WO = toString(request.getParameter("WO"));
    String SkipDouble = toString(request.getParameter("SkipDouble"));
    if (SkipDouble.length()==0 ) {
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
                    
                    Statement stmt = conn.createStatement();
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

<%@ include file="./maintain/ext/dbexit.jsp" %>

```


這個完整的程式碼包含了以下幾個主要的改進：

1. 在插入 WebPlatForm_Counter 表之前，先檢查表是否存在。
2. 提供了更詳細的錯誤日誌記錄。
3. 使用 `System.err.println()` 輸出錯誤信息，您可能想要將其替換為更合適的日誌框架。

此外，這個版本還保留了原始程式的所有功能，包括：

- 工單信息的顯示
- 測試摘要的查詢和顯示
- 用戶界面的所有元素

為了確保程式正常運行，您還需要確認以下幾點：

1. `dbinclude.jsp` 中的數據庫連接字符串是正確的。
2. 數據庫用戶有訪問 `WebPlatForm` 數據庫和 `WebPlatForm_Counter` 表的必要權限。
3. `WebPlatForm` 數據庫和 `WebPlatForm_Counter` 表確實存在。

如果 `WebPlatForm_Counter` 表不存在，您可能需要創建它。您可以使用之前提供的 SQL 腳本來創建表。

這個優化後的版本應該能夠更好地處理可能出現的錯誤，並提供更多的診斷信息。如果您在運行這個程式時仍然遇到問題，請提供更多的錯誤信息，我會很樂意幫助您進一步調試。
