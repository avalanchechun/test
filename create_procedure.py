CREATE PROCEDURE write_Click @IP nvarchar(30), @UserName nvarchar(30), @Report nvarchar(30)
AS

insert into [192.168.8.44].[WebPlatForm].[dbo].[WebPlatForm_Counter]
(IP,[USER],REPORT,CLICK_TIME)
values 
(@IP,@UserName,@Report,convert(varchar, getdate(), 120))
