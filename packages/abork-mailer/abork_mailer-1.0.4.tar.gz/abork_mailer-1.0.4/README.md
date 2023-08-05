# **ABORK_MAIL**
abork_mail is a module for sending emails easily.

## **1. Installation**

```
pip intall abork_mail
```

## **2. Usage**

```
from py_mail.mail import SmtpMail
```

```
mail = SmtpMail(par1=val1, par2=val2, ...)
mail.send()
```

Use the `mail_text_html` parameter instead of `mail_text` if you want to send HTML-content.
