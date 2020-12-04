Set-Location -Path ./hotelapp

&python ./manage.py migrate

&echo "from users.models import CustomUser; CustomUser.objects.create_superuser('root@example.com', 'password')" | python ./manage.py shell

$DBFILE=Join-Path -Path "$(pwd)" -ChildPath "db.sqlite3"

$SQLFILES=Get-ChildItem –Path "../data" -Recurse -Filter *.sql

foreach ($FILE in $SQLFILES) {
  &python ./manage.py dbshell ".read $FILE"
}

Write-Output 'Done...'

Set-Location -Path ".."