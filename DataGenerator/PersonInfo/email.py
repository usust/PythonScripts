import random

from faker import Faker


def generate_unique_emails(count):
    fake = Faker()
    emails = set()
    domains = [
        "gmail.com", "yahoo.com", "hotmail.com", "outlook.com", "live.com",
        "icloud.com", "protonmail.com", "aol.com", "msn.com", "mail.com",
        "zoho.com", "gmx.com", "yandex.com", "qq.com", "163.com", "126.com",
        "sina.com", "sohu.com", "foxmail.com", "aliyun.com", "yeah.net",
        "tom.com", "189.cn", "139.com", "21cn.com", "hotmail.co.uk",
        "btinternet.com", "mail.ru", "inbox.ru", "list.ru", "bk.ru",
        "web.de", "t-online.de", "orange.fr", "wanadoo.fr", "laposte.net",
        "libero.it", "virgilio.it", "alice.it", "cox.net", "charter.net",
        "earthlink.net", "juno.com", "comcast.net", "verizon.net", "att.net",
        "bellsouth.net", "bigpond.com", "btconnect.com", "cfl.rr.com", "frontier.com",
        "mac.com", "me.com", "mailinator.com", "rocketmail.com", "safe-mail.net",
        "wow.com", "y7mail.com", "yahoo.co.in", "yahoo.co.jp", "yahoo.co.uk",
        "yahoo.com.au", "yahoo.ca", "yahoo.fr", "yahoo.de", "yahoo.it",
        "yahoo.es", "yahoo.com.sg", "ymail.com", "zoznam.sk", "freemail.hu",
        "centrum.cz", "seznam.cz", "o2.pl", "wp.pl", "interia.pl", "onet.pl",
        "student.university.edu", "alumni.university.edu", "companyname.com",
        "enterprise.org", "business.net", "ngo.org", "government.gov", "edu.cn",
        "school.edu", "college.edu", "university.edu", "researchlab.org",
        "consultingfirm.com", "lawfirm.net", "medcenter.org", "hospital.net",
        "techstartup.io", "devteam.co", "opensource.org", "cloudservice.net",
        "freemail.org", "temporarymail.com", "throwawaymail.com", "disposablemail.com",
        "mytempemail.com", "temp-mail.org", "spamgourmet.com", "maildrop.cc",
        "guerrillamail.com", "10minutemail.com", "sharklasers.com",
        "posteo.de", "tutanota.com", "lavabit.com", "countermail.com", "mailbox.org",
        "runbox.com", "fastmail.com", "hushmail.com", "startmail.com",
        "zoemail.com", "mailfence.com", "kolabnow.com", "posteo.net",
        "disroot.org", "autistici.org", "safe-mail.net", "mailbox.org",
        "mail.comcast.net", "protonmail.ch", "cock.li", "seznam.cz",
        "freenet.de", "bluewin.ch", "hispeed.ch", "gawab.com", "rediffmail.com",
        "inbox.lv", "latnet.lv", "mail.ee", "mail.bg", "abv.bg",
        "netscape.net", "hotmail.fr", "outlook.fr", "mail.kz", "rambler.ru",
        "bk.ru", "list.ru", "inbox.ru", "mail.ru"
    ]

    while len(emails) < count:
        username = fake.user_name()
        domain = random.choice(domains)
        email = f"{username}@{domain}"
        emails.add(email.lower())
    return list(emails)


if __name__ == "__main__":
    unique_emails = generate_unique_emails(10223)
    with open("电子邮箱地址.txt", "w", encoding="utf-8") as f:
        for email in unique_emails:
            f.write(email+"\n")
            print(email)
