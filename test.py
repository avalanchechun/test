 當然，我理解您需要完整的程式碼。我會提供一個修正了之前問題的完整版本，並考慮到您使用的是較舊的 Tomcat 版本。



```jsp
<%@ page contentType="text/html; charset=UTF-8" %>
<%@ include file="./maintain/ext/dbinclude.jsp" %>
<%@ page import="java.sql.PreparedStatement" %>
<%@ page import="java.sql.Timestamp" %>
<%@ page import="java.sql.DriverManager" %>
<%@ page import="java.sql.Connection" %>
<%@ page import="java.io.FileWriter" %>
<%@ page import="java.io.PrintWriter" %>
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

    private void logError(String message, Exception e, String logPath) {
        PrintWriter logWriter = null;
        try {
            logWriter = new PrintWriter(new FileWriter(logPath, true));
            logWriter.println(new Timestamp(System.currentTimeMillis()) + ": " + message);
            if (e != null) {
                e.printStackTrace(logWriter);
            }
        } catch (Exception logEx) {
            System.err.println("無法寫入錯誤日誌: " + logEx.getMessage());
        } finally {
            if (logWriter != null) {
                logWriter.close();
            }
        }
    }
%>
<%
    String logPath = application.getRealPath("/") + "error_log.txt";
    
    // 記錄使用者資訊
    String userIP = request.getRemoteAddr();
    String userName = request.getRemoteUser();
    if (userName == null) {
        userName = "Unknown";
    }
    String reportName = "LogSummary";
    Timestamp clickTime = new Timestamp(System.currentTimeMillis());

    // 新增資料庫連接資訊
    String dbUrl = "jdbc:sqlserver://192.168.8.44;databaseName=WebPlatForm;encrypt=true;trustServerCertificate=true;";
    String dbUser = "paulchun_huang";
    String dbPassword = "Aa123456";

    // 插入資料到 WebPlatForm_Counter 表格
    String insertSQL = "INSERT INTO WebPlatForm.dbo.WebPlatForm_Counter ([IP], [USER], [REPORT], [CLICK_TIME]) VALUES (?, ?, ?, ?)";
    Connection newConn = null;
    PreparedStatement pstmt = null;
    boolean insertSuccess = false;
    try {
        Class.forName("com.microsoft.sqlserver.jdbc.SQLServerDriver");
        newConn = DriverManager.getConnection(dbUrl, dbUser, dbPassword);
        
        pstmt = newConn.prepareStatement(insertSQL);
        pstmt.setString(1, userIP);
        pstmt.setString(2, userName);
        pstmt.setString(3, reportName);
        pstmt.setTimestamp(4, clickTime);
        int affectedRows = pstmt.executeUpdate();
        insertSuccess = (affectedRows > 0);
    } catch (Exception e) {
        String errorMessage = "插入使用者資訊時發生錯誤: " + e.getMessage();
        logError(errorMessage, e, logPath);
    } finally {
        if (pstmt != null) {
            try {
                pstmt.close();
            } catch (SQLException e) {
                logError("關閉 PreparedStatement 時發生錯誤", e, logPath);
            }
        }
        if (newConn != null) {
            try {
                newConn.close();
            } catch (SQLException e) {
                logError("關閉資料庫連接時發生錯誤", e, logPath);
            }
        }
    }

    // 如果插入失敗，嘗試寫入本地文件
    if (!insertSuccess) {
        PrintWriter logWriter = null;
        try {
            logWriter = new PrintWriter(new FileWriter(application.getRealPath("/") + "user_log.txt", true));
            logWriter.println(clickTime + "," + userIP + "," + userName + "," + reportName);
        } catch (Exception e) {
            logError("無法寫入本地日誌文件", e, logPath);
        } finally {
            if (logWriter != null) {
                logWriter.close();
            }
        }
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

<%        
                pWS_ID = WS_ID;
%>
        <div style="width: 200px; display: inline-block;vertical-align:top;">
        <table id="customers" >
            <tr><th align="center" colspan=3 ><%=WS_ID_FIX( WS_ID, product )%></th></tr>
<%           }
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


這個完整的程式碼包含了以下主要更新：

1. 修改了 `logError` 方法，使其接受日誌文件路徑作為參數。
2. 使用傳統的 try-catch-finally 結構代替 try-with-resources，以確保與舊版 Tomcat 兼容。
3. 在 JSP 的主體部分定義了 `logPath` 變數，使用 `application.getRealPath("/")` 獲取應用程序的根目錄。
4. 保留了原有的所有功能，包括工單查詢和數據顯示。
5. 包含了使用者追蹤功能，連接到 192.168.8.44 上的 WebPlatForm 資料庫。
6. 保留了錯誤處理和日誌記錄功能。

使用這個程式碼時，請注意以下幾點：

1. 確保伺服器上已安裝 Microsoft SQL Server JDBC 驅動程式，並且驅動程式版本與您的 Tomcat 和 Java 版本兼容。
2. 如果遇到 SSL/TLS 相關的問題，可能需要調整連接字串中的 `encrypt` 和 `trustServerCertificate` 參數。
3. 確保應用程式有
