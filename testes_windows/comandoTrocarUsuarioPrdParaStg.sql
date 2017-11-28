USE DEV_INFG_CelulaQualidade_DSV
GO
exec sp_dropuser INFG_CelulaQualidade_DSV ;
exec sp_grantdbaccess DEV_INFG_CelulaQualidade_DSV;
exec sp_grantdbaccess DEV_INFG_Jenkins;
exec sp_addrolemember 'db_owner', 'DEV_INFG_CelulaQualidade_DSV';
exec sp_addrolemember 'db_owner', 'DEV_INFG_Jenkins';
exec sp_changedbowner 'sa';
alter login DEV_INFG_CelulaQualidade_DSV enable;
alter login DEV_INFG_CelulaQualidade_DSV with default_database = DEV_INFG_CelulaQualidade_DSV;