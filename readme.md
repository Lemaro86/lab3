### Домен услуги:

1. GET список. В списке услуг возвращается id заявки-черновика этого пользователя для страницы заявки в статусе черновик 
2. GET одна запись
3. POST добавление
4. PUT изменение
5. DELETE удаление
> 6 POST добавления в заявку-черновик. Заявка создается пустой, указывается автоматически создатель, дата создания и статус, остальные поля указываются через PUT или смену статуса

### Домен заявки:

1. GET список (кроме удаленных и черновика, модератор и создатель через логины)
2. GET одна запись (поля заявки + ее услуги). При получении заявки возвращется список ее услуг с картинками
3. PUT изменение (если есть доп поля заявки)
4. PUT сформировать создателем ??
> 5. PUT завершить/отклонить модератором. При одобрении/отклонении заявки проставляется модератор и дата завершения
6. DELETE удаление

### Домен м-м:

> 1. DELETE удаление из заявки
>
> 2. PUT изменение количества/значения в м-м (если есть доп поля м-м)

### Домен пользователь:

> 1. POST регистрация
> 
> 2. POST аутентификация
> 
> 3. POST деавторизация