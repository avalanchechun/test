 我理解您需要完整的程式碼。我將為您提供一個完整的、包含所有更改的版本。這個版本將包括所有必要的元素，並整合了用戶記錄功能。



```jsp
<%@ page contentType="text/html; charset=UTF-8" %>
<%@ include file="./maintain/ext/dbinclude.jsp" %>
<%@ page import="java.sql.Timestamp" %>
<%@ page import="java.sql.PreparedStatement" %>
<%@ page import="java.sql.SQLException" %>
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
%>
<%
    String WO = toString(request.getParameter("WO"));
    String SkipDouble = toString(request.getParameter("SkipDouble"));
    if (SkipDouble.length()==0 ) {
        SkipDouble = "1";
    }

    // 記錄使用者資訊
    String userIP = request.getRemoteAddr();
    String userName = request.getRemoteUser();
    if (userName == null) {
        userName = "Unknown";
    }
    String reportName = "LogSummary";
    Timestamp clickTime = new Timestamp(System.currentTimeMillis());

    String insertSQL = "INSERT INTO [192.168.8.44].[WebPlatForm].[dbo].[WebPlatForm_Counter] (IP, [USER], REPORT, CLICK_TIME) VALUES (?, ?, ?, ?)";

    try {
        if (conn == null || conn.isClosed()) {
            throw new SQLException("Database connection is not available.");
        }
        PreparedStatement pstmt = conn.prepareStatement(insertSQL);
        pstmt.setString(1, userIP);
        pstmt.setString(2, userName);
        pstmt.setString(3, reportName);
        pstmt.setTimestamp(4, clickTime);
        int rowsAffected = pstmt.executeUpdate();
        pstmt.close();
        if (rowsAffected == 0) {
            throw new SQLException("Inserting user info failed, no rows affected.");
        }
    } catch (Exception e) {
        out.println("<script>console.error('Error logging user information: " + e.getMessage() + "');</script>");
        // 可以选择是否在页面上显示错误信息
        // out.println("<div style='color: red;'>Error logging user information. Please try again later.</div>");
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
                    
                    Statement stmt = null;
                    ResultSet rs = null;
                    try {
                        stmt = conn.createStatement();
                        rs = stmt.executeQuery(sql);
                        
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
                        rs = stmt.executeQuery(sql);
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
                    } catch (SQLException e) {
                        out.println("<script>console.error('Database error: " + e.getMessage() + "');</script>");
                        out.println("<div style='color: red;'>An error occurred while retrieving data. Please try again later.</div>");
                    } finally {
                        if (rs != null) try { rs.close(); } catch (SQLException e) { /* ignored */ }
                        if (stmt != null) try { stmt.close(); } catch (SQLException e) { /* ignored */ }
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

這個完整的程式碼包含了以下主要更改和功能：

1. 在頁面頂部添加了用戶記錄功能，包括錯誤處理和日誌記錄。

2. 保留了原有的所有功能和結構。

3. 改進了錯誤處理和資源管理，使用 try-catch-finally 塊來確保資源正確關閉。

4. 添加了更多的錯誤檢查和控制台日誌記錄，以幫助診斷潛在問題。

5. 保持了原有的 HTML 結構和樣式。

請確保以下幾點：

1. dbinclude.jsp 文件正確設置並初始化了數據庫連接（conn）。
2. 目標數據庫 ([192.168.8.44].[WebPlatForm].[dbo].[WebPlatForm_Counter]) 存在並且可訪問。
3. 執行此 JSP 的用戶具有適當的數據庫權限。

如果您在實施這個版本時仍然遇到問題，請提供具體的錯誤信息或日誌輸出，這將有助於進一步診斷和解決問題。
