delete from ApiFuzzRequestFileUpload;
delete from ApiFuzzRequest;
delete from ApiFuzzResponse;
delete from ApiFuzzDataCase;
delete from ApiFuzzRunSummaryPerCaseSetTable;
delete from ApiFuzzCaseSetRuns;
delete from ApiFuzzCaseSet;
delete from ApiFuzzContext;

drop table ApiFuzzRequestFileUpload;
drop table ApiFuzzRequest;
drop table ApiFuzzResponse;
drop table ApiFuzzDataCase;
drop table ApiFuzzRunSummaryPerCaseSetTable;
drop table ApiFuzzCaseSetRuns;
drop table ApiFuzzCaseSet;
drop table ApiFuzzContext;

SELECT SUM("pgsize") FROM "dbstat" WHERE name='RandomImage';
SELECT SUM("pgsize") FROM "dbstat" WHERE name='SeclistBLNS';
SELECT SUM("pgsize") FROM "dbstat" WHERE name='SeclistPassword';

SELECT (COUNT(*) *  -- The number of rows in the table
     ( 24 +        -- The length of all 4 byte int columns
       12 +        -- The length of all 8 byte int columns
       128 ) / 1024)    -- The estimate of the average length of all string columns
FROM RandomImage;

SELECT ((COUNT(*) *  -- The number of rows in the table
     ( 24 +        -- The length of all 4 byte int columns
       12 +        -- The length of all 8 byte int columns
       128 )) / 1024) / 1024    -- The estimate of the average length of all string columns
FROM SeclistPassword;

SELECT (COUNT(*) *  -- The number of rows in the table
     ( 24 +        -- The length of all 4 byte int columns
       12 +        -- The length of all 8 byte int columns
       128 ) / 1024 * 1024)      -- The estimate of the average length of all string columns
FROM SeclistBLNS;

SELECT (COUNT(*) *  -- The number of rows in the table
     ( 24 +        -- The length of all 4 byte int columns
       12 +        -- The length of all 8 byte int columns
       128 ) / 1024)       -- The estimate of the average length of all string columns
FROM SeclistPayload;

SELECT (COUNT(*) *  -- The number of rows in the table
     ( 24 +        -- The length of all 4 byte int columns
       12 +        -- The length of all 8 byte int columns
       128 )/ 1024) / 1024    -- The estimate of the average length of all string columns
FROM SeclistSqlInjection;

SELECT (COUNT(*) *  -- The number of rows in the table
     ( 24 +        -- The length of all 4 byte int columns
       12 +        -- The length of all 8 byte int columns
       128 )/ 1024) / 1024      -- The estimate of the average length of all string columns
FROM SeclistUsername;

SELECT (COUNT(*) *  -- The number of rows in the table
     ( 24 +        -- The length of all 4 byte int columns
       12 +        -- The length of all 8 byte int columns
       128 )/ 1024) / 1024     -- The estimate of the average length of all string columns
FROM SeclistXSS;

-- delete from RandomImage
-- delete from SeclistChar;
-- delete from SeclistBLNS;
-- delete from SeclistPassword;
-- delete from SeclistPayload;
-- delete from SeclistSqlInjection;
-- delete from SeclistUsername;
-- delete from SeclistXSS;

-- drop table RandomImage;
-- drop table SeclistBLNS;
-- drop table SeclistPassword;
-- drop table SeclistPayload;
-- drop table SeclistSqlInjection;
-- drop table SeclistUsername;
-- drop table SeclistXSS;

