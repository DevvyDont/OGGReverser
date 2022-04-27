@echo off
cd target
for %%f in (*.mf) do (
    ..\bin\multify.exe -x -f %%f
)