SocialLoginInformation = {
    "Google": {
        "name": "Google",
        "valid_login_urls": ["https://accounts.google.com/"],
        "valid_login_urls_when_logged_in": ["https://accounts.google.com/"],
        "block_requests_if_logged_in": [],
        "must_have_texts_in_valid_login_urls": [["client_id"]],
        "exclude_url_starts_with": ["google.", "accounts.google.", "account.google.", "consent.google.",
                                    "developers.googleblog.com", "pki.goog", "support.google.", "patent.google.",
                                    "www.google.", "translate.google.", "maps.google.", "trends.google.",
                                    "adwords.google.", "picasa.google.", "books.google.", "edu.google.", "news.google.",
                                    "developers.google.", "mymaps.google.", "workspace.google.", "gsuite.google.",
                                    "mijnaccount.google.", "scholar.google.", "blog.google", "patents.google.",
                                    "googlegroups.", "myaccount.google.com"],
        "extra_texts": ["ورود با حساب گوگل"]
    },
    "Facebook": {
        "name": "Facebook",
        "valid_login_urls": ["https://m.facebook.com/login", "https://facebook.com/login",
                             "https://www.facebook.com/login", "https://www.facebook.com/dialog/oauth"],
        "valid_login_urls_when_logged_in": ["https://facebook.com", "https://www.facebook.com",
                                            "https://m.facebook.com"],
        "block_requests_if_logged_in": ["www.facebook.com/x/oauth/status", "facebook.com/x/oauth/status"],
        "must_have_texts_in_valid_login_urls": [["client_id=", "app_id="]],
        "exclude_url_starts_with": ["facebook.", "www.facebook.", "connect.facebook.", "developers.facebook."],
        "extra_texts": []
    },
    "Apple": {
        "name": "Apple",
        "valid_login_urls": ["https://appleid.apple.com/"],
        "valid_login_urls_when_logged_in": ["https://appleid.apple.com/"],
        "block_requests_if_logged_in": [],
        "must_have_texts_in_valid_login_urls": [["client_id"]],
        "exclude_url_starts_with": ["apple.", "appleid.apple.", "secure.apple.", "secure2.apple.",
                                    "secure2.store.apple.", "support.apple.", "music.apple.", "discussions.apple.",
                                    "www.apple.", "business.apple.", "itunes.apple."],
        "extra_texts": []
    },
    "Linkedin": {
        "name": "Linkedin",
        "valid_login_urls": ["https://www.linkedin.com/uas/login"],
        "valid_login_urls_when_logged_in": ["https://www.linkedin.com/uas/login"],
        "block_requests_if_logged_in": [],
        "must_have_texts_in_valid_login_urls": [["session_redirect=%2Foauth%2Fv2%2Flogin-success"]],
        "exclude_url_starts_with": ["linkedin.", "www.linkedin."],
        "extra_texts": []
    },
    "Microsoft": {
        "name": "Microsoft",
        "valid_login_urls": ["https://login.microsoftonline.com/", "https://login.live.com/"],
        "valid_login_urls_when_logged_in": ["https://login.microsoftonline.com/"],
        "block_requests_if_logged_in": [],
        "must_have_texts_in_valid_login_urls": [["client_id"]],
        "exclude_url_starts_with": ["microsoft.", "www.microsoft."],
        "extra_texts": []
    },
    "Baidu": {
        "name": "Baidu",
        "valid_login_urls": ["https://openapi.baidu.com/"],
        "valid_login_urls_when_logged_in": ["https://openapi.baidu.com/"],
        "block_requests_if_logged_in": [],
        "must_have_texts_in_valid_login_urls": [["client_id"]],
        "exclude_url_starts_with": ["baidu.", "www.baidu."],
        "extra_texts": []
    },
    "Twitter-1.0": {
        "name": "Twitter",
        "valid_login_urls": ["https://api.twitter.com/"],
        "valid_login_urls_when_logged_in": ["https://api.twitter.com/"],
        "block_requests_if_logged_in": [],
        "must_have_texts_in_valid_login_urls": [["oauth_token"]],
        "exclude_url_starts_with": ["twitter.", "www.twitter.", "api.twitter."],
        "extra_texts": []
    }
}
