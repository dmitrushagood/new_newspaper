from django.db.models.signals import post_save, m2m_changed  # post_save не используется тут
from django.dispatch import receiver  # импортируем нужный декоратор
from django.core.mail import send_mail
from .models import Post
from django.contrib.auth.models import User

# в декоратор передаётся первым аргументом сигнал, на который будет реагировать эта функция,
# и в отправители надо передать также модель


@receiver(m2m_changed, sender=Post.cats.through)
def new_post(sender, action, instance, **kwargs):
    # если проходит команда post_add, то есть добавляется новость,
    # то выполняются следующие действия:
    if action == 'post_add':

        # для каждого из экземпляров категорий созданной новости
        # (например,если у новости две категории, то для каждой из них)
        for each in instance.cats.all():  # например в данном случае each -> sport, culture
            # потому что модель Category возвращает поле article_category, где как-раз хранятся значения sport и
            # culture instance - это экземпляр модели Category, и когда мы перебираем эти самые экземпляры,
            # то получаем доступ и к остальным полям. Поэтому в данном случае each представляет каждый
            # экземпляр instance

            # теперь мы снова перебираем поля экземпляра instance, который представлен переменной each
            # each.subscribers даёт нам доступ к полю subscribers, и следом вызывая cat.email, мы уже проваливаемся в
            # модель пользователя User к его родительскому классу, к полю email
            for cat in each.subscribers.all():
                # 1) cat = sport
                # 2) cat = culture

                send_mail(
                    subject=f'Здравствуй, {cat.email}. Новая статья в твоём любимом разделе! Заголовок:"{instance.title}"',
                    message=f'Дата создания записи: {instance.created.strftime("%d %m %Y")}, первые 50 символов поста: {instance.text[:50]}',
                    from_email='dmitrushatest@yandex.ru',
                    recipient_list=[cat.email]
                )

                print(cat.email)
