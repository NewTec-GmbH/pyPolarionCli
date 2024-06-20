@echo off

rem The following variables shall be adapted:
set USERNAME="my_username"
set PASSWORD="my_password"
set SERVER="https://my-polarion-instance.com"
set PROJECT="MYPROJECT"
set QUERY="author.id:myname"

echo Please set the variables inside this file.
echo:

rem Define and execute the command
set command=pyPolarionCli --verbose --user %USERNAME% --password %PASSWORD% --server %SERVER% search --project %PROJECT% --query %QUERY%

echo Executing....
echo %command%
echo:
%command%
pause