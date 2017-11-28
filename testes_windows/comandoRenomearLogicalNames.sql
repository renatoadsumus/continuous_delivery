ALTER DATABASE DEV_INFG_CelulaQualidade_DSV MODIFY FILE (NAME=N'INFG_CelulaQualidade_DSV_data', NEWNAME=N'DEV_INFG_CelulaQualidade_DSV_data')
GO
ALTER DATABASE DEV_INFG_CelulaQualidade_DSV MODIFY FILE (NAME=N'INFG_CelulaQualidade_DSV_log', NEWNAME=N'DEV_INFG_CelulaQualidade_DSV_log')
GO
ALTER DATABASE DEV_INFG_CelulaQualidade_DSV set recovery simple;
GO