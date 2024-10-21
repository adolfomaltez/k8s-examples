-- Insert 10000 records into the table
USE [SQLTestAG]
GO
DROP TABLE AG_Test;
GO
CREATE TABLE AG_Test (ID uniqueidentifier, RamdonData varchar(255)) ;
GO
INSERT INTO AG_Test ( ID, RamdonData ) VALUES ( NEWID(), CONVERT(VARCHAR(50), NEWID()) );
GO 100