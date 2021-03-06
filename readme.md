# Тестовое задание для "ООО Фабрика Решений" 
## Задание

Задача: спроектировать и разработать API для системы опросов пользователей.

Функционал для администратора системы:

- авторизация в системе (регистрация не нужна)
- добавление/изменение/удаление опросов. Атрибуты опроса: название, дата старта, дата окончания, описание. После создания поле "дата старта" у опроса менять нельзя
- добавление/изменение/удаление вопросов в опросе. Атрибуты вопросов: текст вопроса, тип вопроса (ответ текстом, ответ с выбором одного варианта, ответ с выбором нескольких вариантов)

Функционал для пользователей системы:

- получение списка активных опросов
- прохождение опроса: опросы можно проходить анонимно, в качестве идентификатора пользователя в API передаётся числовой ID, по которому сохраняются ответы пользователя на вопросы; один пользователь может участвовать в любом количестве опросов
- получение пройденных пользователем опросов с детализацией по ответам (что выбрано) по ID уникальному пользователя

Использовать следующие технологии: Django 2.2.10, Django REST framework.

Результат выполнения задачи:
- исходный код приложения в github (только на github, публичный репозиторий)
- инструкция по разворачиванию приложения (в docker или локально)
- документация по API

## Документация по API

| URL                                        | Метод  | Параметры                               | Ответ                                                   |
|--------------------------------------------|--------|-----------------------------------------|---------------------------------------------------------|
| /surveys                                   | GET    | -                                       | Вернет список опросов                                   |
| /surveys/`id`                              | GET    | id опроса                               | Вернет конкретный опрос                                 |
| /surveys                                   | POST   | name, start_date, end_date, description | Создание опроса                                         |
| /surveys/`id`                              | DELETE | -                                       | Удалит опрос                                            |
| /surveys/active                            | GET    | -                                       | Вернет список активных опросов                          |
| /surveys/`id`/start                        | POST   | id опроса, user                         | Вернет ID запущенного опроса, на который можно отвечать |
| /surveys/?search=`запрос`                  | GET    | текст `запроса`                         | Поиск по name и description                             |
| /questions                                 | GET    | -                                       | Вернет список вопросов                                  |
| /questions/`id`                            | GET    | `id` опроса                             | Вернет конкретный вопрос                                |
| /questions                                 | POST   | text, survey, question_type             | Создание вопроса                                        |
| /questions/`id`                            | DELETE | -                                       | Удалит вопрос                                           |
| /questions?search=`запрос`                 | GET    | -                                       | Поиск по text                                           |
| /questions?question_type=`тип`&survey=`id` | GET    | -                                       | Фильтрация по question_type и ID опроса                 |
| /answers                                   | GET    | -                                       | Вернет список вопросов на ответы                        |
| /answers/`id`                              | GET    | id опроса                               | Вернет конкретный вопрос                                |
| /answers                                   | POST   | text, question                          | Создавние вопроса                                       |
| /answers/`id`                              | DELETE | -                                       | Удалит вопрос                                           |
| /answers?search=`запрос`                   | GET    | -                                       | Поиск по text                                           |
| /answers?question=`id`                     | GET    | -                                       | Фильтр по ID вопроса                                    |
| /started/`?user=id`                        | GET    | id                                      | Получение ответов пользователя                          |
| /started/`id`                              | GET    | id                                      | Получение ответов по ID                                 |
| /started/`id`/answer                       | GET    | question,answer,text,user               | Занести ответ в опрос                                   |

На всех "списочных страницах" присутствует пагинация.

## Инструкция по разворачиванию приложения

1) Клонируем репозиторий: `git clone https://github.com/kiriharu/fabrique_test`
2) Запускаем приложение: `docker-compose up -d`
3) Приложение будет доступно на 8000 порту в Debug-моде.