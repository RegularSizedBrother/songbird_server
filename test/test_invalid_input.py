import src.jobs.social_media as social_media1
from src.models.recommendation import Recommendation, db
from src.app import create_testing_app

def test_reserved_strings_valid_users():
    strings = [
        "false",
        "then",
        "constructor",
        "true",
    ]

    for s in strings:
        app = create_testing_app()
        with app.app_context():

            record = Recommendation(handle=s)
            db.session.add(record)
            db.session.commit()

            social_media.process_social_media(record.id, testing=True)

            new_record = Recommendation.query.get(record.id)
            assert new_record.error == None

def test_reserved_strings_invalid_users():
    strings = [
        "undefined",
        "null",
        "NULL",
        "(null)",
        "nil",
        "NIL",
        "None",
        "hasOwnProperty",
        "\\",
        "\\\\"
    ]

    for s in strings:
        app = create_testing_app()
        with app.app_context():

            record = Recommendation(handle=s)
            db.session.add(record)
            db.session.commit()

            social_media.process_social_media(record.id, testing=True)

            new_record = Recommendation.query.get(record.id)
            assert new_record.error == True

def test_numeric_strings():
    strings = [
        "0",
        "1",
        "1.00",
        "$1.00",
        "1/2",
        "1E2",
        "123456789012345678901234567890123456789",
        "1,000.00",
        "1 000.00",
        "1'000.00",
        "1,000,000.00",
    ]

    for s in strings:
        app = create_testing_app()
        with app.app_context():

            record = Recommendation(handle=s)
            db.session.add(record)
            db.session.commit()

            social_media.process_social_media(record.id, testing=True)

            new_record = Recommendation.query.get(record.id)
            assert new_record.error == True

def test_ascii_punct():
    strings = [
        ",./;'[]\-=",
        "<>?:\{}|_+",
        "!@#$%^&*()`~",
    ]

    for s in strings:
        app = create_testing_app()
        with app.app_context():

            record = Recommendation(handle=s)
            db.session.add(record)
            db.session.commit()

            social_media.process_social_media(record.id, testing=True)

            new_record = Recommendation.query.get(record.id)
            assert new_record.error == True

def test_whitespace():
    strings = [
        "	              ​    　",
    ]

    for s in strings:
        app = create_testing_app()
        with app.app_context():

            record = Recommendation(handle=s)
            db.session.add(record)
            db.session.commit()

            social_media.process_social_media(record.id, testing=True)

            new_record = Recommendation.query.get(record.id)
            assert new_record.error == True

def test_unicode():
    strings = [
        "Ω≈ç√∫˜µ≤≥÷",
        "åß∂ƒ©˙∆˚¬…æ",
        "œ∑´®†¥¨ˆøπ“‘",
        "¡™£¢∞§¶•ªº–≠",
    ]

    for s in strings:
        app = create_testing_app()
        with app.app_context():

            record = Recommendation(handle=s)
            db.session.add(record)
            db.session.commit()

            social_media.process_social_media(record.id, testing=True)

            new_record = Recommendation.query.get(record.id)
            assert new_record.error == True

def test_two_byte_chars():
    strings = [
        "田中さんにあげて下さい",
        "パーティーへ行かないか",
        "和製漢語",
        "部落格",
    ]

    for s in strings:
        app = create_testing_app()
        with app.app_context():

            record = Recommendation(handle=s)
            db.session.add(record)
            db.session.commit()

            social_media.process_social_media(record.id, testing=True)

            new_record = Recommendation.query.get(record.id)
            assert new_record.error == True

def test_emojis():
    strings = [
        "😍",
        "👩🏽",
        "👨‍🦰 👨🏿‍🦰 👨‍🦱 👨🏿‍🦱 🦹🏿‍♂️",
        "👾 🙇 💁 🙅 🙆 🙋 🙎 🙍",
        "🐵 🙈 🙉 🙊",
    ]

    for s in strings:
        app = create_testing_app()
        with app.app_context():

            record = Recommendation(handle=s)
            db.session.add(record)
            db.session.commit()

            social_media.process_social_media(record.id, testing=True)

            new_record = Recommendation.query.get(record.id)
            assert new_record.error == True

def test_js_injection():
    strings = [
        "<script>alert(123)</script>",
        "&lt;script&gt;alert(&#39;123&#39;);&lt;/script&gt;",
        "<img src=x onerror=alert(123) />",
        "<svg><script>123<1>alert(123)</script>",
        "\"><script>alert(123)</script>",
        "'><script>alert(123)</script>",
        "><script>alert(123)</script>",
        "</script><script>alert(123)</script>",
        "< / script >< script >alert(123)< / script >",
        "\"onfocus=JaVaSCript:alert(123) autofocus\",",
        "\" onfocus=JaVaSCript:alert(123) autofocus",
        "' onfocus=JaVaSCript:alert(123) autofocus",
        "＜script＞alert(123)＜/script＞",
        "<sc<script>ript>alert(123)</sc</script>ript>",
        "--><script>alert(123)</script>",
        "\";alert(123);t=\"",
        "';alert(123);t='",
    ]

    for s in strings:
        app = create_testing_app()
        with app.app_context():

            record = Recommendation(handle=s)
            db.session.add(record)
            db.session.commit()

            social_media.process_social_media(record.id, testing=True)

            new_record = Recommendation.query.get(record.id)
            assert new_record.error == True

def test_sql_injection():
    strings = [
        "1;DROP TABLE users",
        "1'; DROP TABLE users-- 1",
        "' OR 1=1 -- 1",
        "' OR '1'='1",
    ]

    for s in strings:
        app = create_testing_app()
        with app.app_context():

            record = Recommendation(handle=s)
            db.session.add(record)
            db.session.commit()

            social_media.process_social_media(record.id, testing=True)

            new_record = Recommendation.query.get(record.id)
            assert new_record.error == True

def test_interpolation():
    strings = [
        "$HOME",
        "$ENV{'HOME'}",
        "%d",
        "%s%s%s%s%s",
        "{0}",
        "%*.*s",
        "%@",
    ]

    for s in strings:
        app = create_testing_app()
        with app.app_context():

            record = Recommendation(handle=s)
            db.session.add(record)
            db.session.commit()

            social_media.process_social_media(record.id, testing=True)

            new_record = Recommendation.query.get(record.id)
            assert new_record.error == True

def test_file_inclusion():
    strings = [
        "../../../../../../../../../../../etc/passwd%00",
        "../../../../../../../../../../../etc/hosts",
    ]

    for s in strings:
        app = create_testing_app()
        with app.app_context():

            record = Recommendation(handle=s)
            db.session.add(record)
            db.session.commit()

            social_media.process_social_media(record.id, testing=True)

            new_record = Recommendation.query.get(record.id)
            assert new_record.error == True
