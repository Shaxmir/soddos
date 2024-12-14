$(document).ready(function () {
    $('.btn').click(function () {
        $(this).toggleClass('active'); // Добавляем или удаляем класс 'active' у кнопки
        $('.box').toggleClass('open'); // Добавляем или удаляем класс 'open' у бокса
    });
});