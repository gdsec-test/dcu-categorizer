from iris_helper import IrisHelper
from settings import dbstring
from regex_helper import ListHelper

#i = IrisHelper(dbstring)


def cleanup():
    address = ['sh.baidu.com', 'notices.nr-online.com', 'legal-notification.com', 'woody.ch', 'justdeals.com',
                   'certifiedmart.com', 'marcon-media.de', 'newsletter.kopp-verlag.de', 'brandshop.com', 'law360.com',
                   'ogrupo.org.br', 'domainerschoice.com', '163.com', 'peakindustry.com', 'woody.ch', 'foxmail.com',
                   'sina.cn', 'sina.com', 'appleitunesguide.com', 'notice.bizcn.com']
    garbage = []
    for a in address:
        trash = i.trash_man(a)
        for t in trash:
            garbage.append(t[0])

    print garbage


def categorize():

    l = ListHelper()

    phish_keys = ['phishing', 'phish']
    malware_keys = ['malware', 'virus']
    netabuse_keys = ['botnet', 'intrusion', 'scan', 'attempted login', 'login attempted']
    spam_keys = ['spam', 'spoof', 'spoofed']
    garbage_keys = ['copyright', 'trademark', 'infringement']

    data = [(33289088, u'FRAUD and HARASSMENT that Funds ISIS'),
            (33289417, u'Fraud domain http://www.holdingsbrighton.com'),
            (33290092, u'Fwd: Action required: Please verify your email address/Is someone using my email? Email 4'),
            (33290660, u'Malicious site removal request [3MdEqgRA]'), (33290718, u'belgiumbrand.club: SPAM - We need your cooperation'),
            (33290987, u'Abuse: ID THEFT.'), (33291012, u'website'), (33291117, u'Fraudulent Site'), (33291121, u'SPAM /phishing brinksiinc.com'),
            (33291135, u'Phishing at your domain'), (33291227, u'RE: Report multiple spear phishing e-mails'),
            (33291235, u'Abuse from 50.62.160.34'), (33291241, u'Fw: Important')]


    test = [(123, u'phish'), (456, u'virus'), (789, u'spam'), (012, u'rando')]

    phish_cat = l.reg_logic(test, phish_keys)
    m_list = phish_cat[1]
    phish_cat = phish_cat[0]


   # print i.data_pull()


    #ToDo setup regex seperated by category for use in this function

    return phish_cat, m_list

if __name__ == '__main__':
    print categorize()