$directoyPath="./.data/postgres";
if(!(Test-Path -path $directoyPath))  
{  
    New-Item -ItemType directory -Path $directoyPath
    Write-Host "Postgres data path has been created successfully at: " $directoyPath  -ForegroundColor green
}
else
{
    Write-Host "Postgres data path exists $directoyPath " -ForegroundColor green
}


&docker run -it --rm --name mypostgres -e POSTGRES_USER=postgres -e POSTGRES_PASSWORD=password `
        -v ${PWD}/.data/postgres:/var/lib/postgresql/data -p 5432:5432 postgres:13.0