from django.conf import settings

from src.badi_utils.i18n import BadiI18n

Log = getattr(settings, "LOG_MODEL")


def log(user, priority, action, status, my_object=None, field=None, text=None):
    """
    برای لاگ کردن است

    Arguments:
        user:
            کاربری که لاگ را رقم زده است
        priority:
            اولویت لاگ است
        action:
            عملیات را مشخص میکند
        status:
            وضعیت موفق یا ناموفق بودن لاگ را مشخص میکند
        my_object:
            در صورتی که لاگ برای یک رکورد از پایگاه داده اتفاق افتاده باشد
            آنرا دریافت میکند
    """
    lg = Log()

    lg.user = user
    lg.priority = priority
    lg.status = status

    if text:
        lg.title = BadiI18n.t('custom')
        lg.description = text
    else:
        if action == 1:
            lg.title = BadiI18n.t('login')
            lg.description = 'کاربر ' + str(user) + ' به سامانه وارد شد.'
        elif action == 2:
            lg.title = BadiI18n.t('logout')
            lg.description = 'کاربر ' + str(user) + ' از سامانه خارج شد.'
        elif action == 3:
            lg.title = 'ایجاد رکورد'
            lg.description = "کاربر " + str(user) + " " + str(my_object._meta.verbose_name) + "'" + str(
                field) + "'" + " را اضافه کرد."
        elif action == 4:
            lg.title = 'ویرایش رکورد'
            lg.description = "کاربر " + str(user) + " " + str(my_object._meta.verbose_name) + "'" + str(
                field) + "'" + " را ویرایش کرد."
        elif action == 5:
            lg.title = 'حذف رکورد'
            lg.description = "کاربر " + str(user) + " " + str(my_object._meta.verbose_name) + "'" + str(
                field) + "'" + " را حذف کرد."

    lg.save()
    return lg
