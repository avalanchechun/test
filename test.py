 好的，我將為您提供完整整合好的程式。我會把新增的計數器功能整合到您原有的 JSP 代碼中。



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


這個更新後的 JSP 文件包含了以下主要變更：

1. 在文件開頭添加了必要的 import 語句。
2. 新增了 `getClientIpAddr` 方法來獲取客戶端 IP 地址。
3. 在 HTML 內容之前添加了 Web 計數器功能的代碼，包括獲取用戶信息和插入數據到 `WebPlatForm_Counter` 表中。
4. 保留了原有的所有功能和 HTML 結構。

這個整合版本應該能夠滿足您的需求，既保留了原有的功能，又增加了記錄訪問者信息的新功能。請注意，您可能需要根據您的具體環境進行一些微調，例如確保數據庫連接正確設置，以及可能需要的錯誤處理邏輯。

建議您在部署到生產環境之前，先在測試環境中thoroughly測試這個更新後的版本，以確保所有功能都正常運作。如果您有任何問題或需要進一步的修改，請隨時告訴我。
