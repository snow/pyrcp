#! /usr/bin/python2.7

'''Get a GMail SMTP connection

Example:
>>> from cc.firebloom.snowhs.gsmtplib import GSMTP
>>> s = GSMTP('your_google_account', 'your_google_password')
>>> s.sendmail('somebody@neverland.cc',
...            'Hello world!',
...            'This is a message sent by gsmtplib'))
>>> s.quit()
'''

from smtplib import SMTP
from email.mime.text import MIMEText

class GSMTP(SMTP):
    '''This class manages a connection to GMail SMTP server.    
    
    Example:
    >>> from cc.firebloom.snowhs.gsmtplib import GSMTP
    >>> s = GSMTP('your_google_account', 'your_google_password')
    >>> s.sendmail('somebody@neverland.cc',
    ...            'Hello world!',
    ...            'This is a message sent by gsmtplib'))
    >>> s.quit()
    '''
    
    account = ''
    
    def __init__(self, account, password):
        '''Initialize a new instance with Google account and password'''
        
        self.account = account
        
        SMTP.__init__(self, 'smtp.gmail.com', 587)
        self.ehlo()
        self.starttls()
        self.ehlo()
        self.login(self.account, password)
        
    def sendmail(self, to, subject, content):
        '''Shortcut method to send a simple mail.
        
        Args
        ----
        - to      : A list of addresses to send this mail to. A bare string will
                    be treated as a list with 1 address.
        - subject : Mail subject
        - content : Mail body. treated as pure text
            
        Example
        -------
        >>> from cc.firebloom.snowhs.gsmtplib import GSMTP
        >>> s = GSMTP('your_google_account', 'your_google_password')
        >>> s.sendmail('somebody@neverland.cc',
        ...            'Hello world!',
        ...            'This is a message sent by gsmtplib'))
        >>> s.quit()
        
        '''
        mail = MIMEText(content)
        mail['subject'] = subject
        mail['from'] = self.account
        mail['to'] = to
        
        SMTP.sendmail(self, self.account, to, mail.as_string())
