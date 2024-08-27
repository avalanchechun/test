 當然，我會為您提供完整的程式碼。我會整合之前的代碼和新的修改，以確保所有功能都包含在內。



```jsp

<%@ page contentType="text/html; charset=UTF-8" %>
<%@ page import="java.sql.*" %>
<%@ include file="./maintain/ext/dbinclude.jsp" %>
<%!
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
        if (wsid.compareTo("F6") == 0) return "FQC";
        if (wsid.compareTo("F7") == 0) return "F1";
        if (wsid.compareTo("F8") == 0) return "QC";
        if (wsid.compareTo("F9") == 0) return "BN";
        if (wsid.compareTo("F10") == 0) return "ORT";
        return ret;
    }

    public void logUserInfo(Connection conn, String ip, String user, String page) {
        String sql = "INSERT INTO WebPlatForm.dbo.user_logs (ip, username, page, click_time) VALUES (?, ?, ?, GETDATE())";
        try (PreparedStatement pstmt = conn.prepareStatement(sql)) {
            pstmt.setString(1, ip);
            pstmt.setString(2, user);
            pstmt.setString(3, page);
            pstmt.executeUpdate();
        } catch (SQLException e) {
            e.printStackTrace();
        }
    }
%>
<%
    String WO = toString(request.getParameter("WO"));
    String SkipDouble = toString(request.getParameter("SkipDouble"));
    if (SkipDouble.length() == 0) {
        SkipDouble = "1";
    }

    // Log user info
    String userIp = request.getRemoteAddr();
    String username = (String) session.getAttribute("username");
    logUserInfo(conn, userIp, username, "LogSummary");
%>

<!DOCTYPE html>
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
                if (WO.length() > 10) {
                    String pWS_ID = "";
                    String moYM = "PELogSr_20" + WO.substring(4, 8);

                    String sql = "use TIPTOP;select * from csfzr109 where PRODUCT_NUM='" + WO + "' ";

                    Statement stmt = conn.createStatement();
                    ResultSet rs = stmt.executeQuery(sql);
                    int quantity = 1;
                    String product = "";
                    if (rs.next()) {
                        quantity = rs.getInt("QUANTITY");
                        product = rs.getString("PRODUCT");
                        String wostatus = rs.getString("CLOSE_STATUS");
                        if (wostatus.indexOf("3") != -1) {
                            wostatus = "close";
                        } else {
                            wostatus = "open";
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

                    sql = "select * from LogSystem.dbo.mfg_test_summary where WO='" + WO + "' and SkipDouble=" + SkipDouble + " order by ws_id,cnt desc,id_01";

                    java.text.DecimalFormat dformat = new java.text.DecimalFormat("0.00");
                    rs = stmt.executeQuery(sql);
                    while (rs.next()) {
                        String WS_ID = rs.getString("WS_ID");
                        String ID_01 = rs.getString("ID_01");
                        int cnt = rs.getInt("cnt");
                        if (pWS_ID.compareTo(WS_ID) != 0) {
                            if (pWS_ID.length() != 0) {
                %>
                        </table></div>
                <%                
                            }
                %>
                        <div style="width: 200px; display: inline-block;vertical-align:top;">
                        <table id="customers">
                            <tr><th align="center" colspan=3><%=WS_ID_FIX(WS_ID, product)%></th></tr>
                <%           
                        }
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
</body>
</html>

<%@ include file="./maintain/ext/dbexit.jsp" %>

```


這個完整的 JSP 文件包含了以下主要變更和功能：

1. 添加了 `logUserInfo` 方法來記錄用戶信息到數據庫。

2. 在頁面加載時調用 `logUserInfo` 方法，記錄用戶的 IP 地址、用戶名和頁面名稱。

3. 移除了之前用於記錄用戶信息的 JavaScript 代碼。

4. 保留了原有的所有功能，包括工單搜索、數據顯示等。

5. 使用了準備好的語句（PreparedStatement）來防止 SQL 注入攻擊。

6. 保留了原有的 HTML 結構和樣式。

要使用這個更新後的代碼，請確保：

1. 在您的 SQL Server 數據庫中存在 `WebPlatForm.dbo.user_logs` 表，且具有適當的列（ip, username, page, click_time）。

2. `dbinclude.jsp` 文件中的數據庫連接擁有向 `user_logs` 表插入數據的權限。

3. 用戶登錄時正確地將 `username` 設置在 session 中。

如果您需要進行任何調整或有任何問題，請隨時告訴我。
