alter login <LOGIN> disable;

set nocount on
     declare @cmd varchar(2000)
     declare killListC cursor for select N'kill '+cast(p.spid as nvarchar)+' -- '+rtrim(ltrim(p.loginame))+' using      
'+p.program_name
                                    from master..sysprocesses p 
                                   inner join master..sysdatabases d on p.dbid=d.dbid and d.name='<BASE DE DADOS>'
                                   order by p.spid
     open killListC
     while ( 1=1 ) 
     begin
       fetch next from killListC into @cmd
       if @@fetch_status <> 0 break
       PRINT @cmd;
       exec ( @cmd );
     end
     close killListC
     deallocate killListC
     GO