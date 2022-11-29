delete from ApiFuzzRequest;
delete from ApiFuzzResponse;
delete from ApiFuzzDataCase;
delete from ApiFuzzRunSummaryPerCaseSetTable;
delete from ApiFuzzCaseSetRuns;
delete from ApiFuzzCaseSet;
delete from ApiFuzzContext;

drop table RandomImage;
drop table ApiFuzzRequest;
drop table ApiFuzzResponse;
drop table ApiFuzzDataCase;
drop table ApiFuzzRunSummaryPerCaseSetTable;
drop table ApiFuzzCaseSetRuns;
drop table ApiFuzzCaseSet;
drop table ApiFuzzContext;

delete from RandomImage
delete from SeclistChar;
delete from SeclistBLNS;
delete from SeclistPassword;
delete from SeclistPayload;
delete from SeclistSqlInjection;
delete from SeclistUsername;
delete from SeclistXSS;

-- drop table SeclistBLNS;
-- drop table SeclistPassword;
-- drop table SeclistPayload;
-- drop table SeclistSqlInjection;
-- drop table SeclistUsername;
-- drop table SeclistXSS;

