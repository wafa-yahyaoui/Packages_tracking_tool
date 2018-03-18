STATUS = (
    ('IT', 'In Transit'),
    ('DL', 'Delivered'),
    ('OFD', 'Out for delivery'),
    ('RTG', 'Ready togo'),
    ('FA', 'Failed attempt'),
)

STATUS_VIEW = {"IT": "form_content_email_IT",
               "DL": "form_content_email_DL",
               "OFD": "form_content_email_OOD",
               "RTG": "form_content_email_RTG",
               "FA": "form_content_email_FA",
               }
