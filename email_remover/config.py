class Prod():
    SECRET_KEY = 'change_me'
    PASSWORD_HASH = 'change_me'
    EMAIL_ACCOUNT_PATH = '/var/mail/vhosts/'

class Test():
    SECRET_KEY = 'change_me'
    PASSWORD_HASH = '$argon2id$v=19$m=65536,t=3,p=4$mzqiveNU7Y9jwj6I9cadUw$hVabWZSN+fPRzBqDrEMOSCfOQEYgq8mRzc2ny7azCXA'
    EMAIL_ACCOUNT_PATH = '/tmp/mail/vhost/'

class Dev():
    SECRET_KEY = 'change_me'
    PASSWORD_HASH = '$argon2id$v=19$m=65536,t=3,p=4$mzqiveNU7Y9jwj6I9cadUw$hVabWZSN+fPRzBqDrEMOSCfOQEYgq8mRzc2ny7azCXA'
    EMAIL_ACCOUNT_PATH = '/tmp/mail/vhost/'
