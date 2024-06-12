from star_query_rail_client.models import StarRailDetailCharacters

from .action import (
    bind_cookies,
    get_characters_detail,
    get_info,
    login,
    register,
    unbind_user,
    update_password,
)
from .config import status


def test_register():
    response = register("abb", "testpw")
    print(response)


def test_login():
    login("abb", "testpw")
    return "done"


def test_bind_cookies():
    response = bind_cookies(
        "account_id=284738632; cookie_token=xps99MGUWn1uBjzxvaFAzE1A204d6YQg4m8pmXYO; ltoken=MI2Jka7KoTwRTJNLqkACbGnRFPka8cT1OIzyo8ip; ltuid=284738632; mid=0pmcg2neha_mhy; stoken=v2_7FKkxs_p_orCaJEsw9yVvpyBOjhQxAynLTO8cxW5QjM8VueX2kN35TlnB7YzyfUJkYuAqaZ0nORjKpwMguvByiqqEl2NRiM5Y7OowXaSFKBa3_aljXQ-qXh1n0wMt82y; stuid=284738632; x-rpc-device_fp=38d7f1c0c14f1; x-rpc-device_id=a6f9792d-5dee-3183-b040-96918498ea33"  # noqa: E501
    )
    print(response)
    print("\n")
    return "done"


def test_get_info():
    response = get_info()
    print(response)
    print("\n")
    return "done"


def test_get_characters_detail():
    response: StarRailDetailCharacters = get_characters_detail(0)
    print(response)
    return "done"


def test_unbind_user():
    login("abb", "testpw")
    response = get_info()
    print(response)
    print("\n")
    response = unbind_user()
    print(response)
    print("\n")
    response = get_info()
    print(response)
    print("\n")
    return "done"


def test_update_password():
    login("abb", "testpw")
    response = update_password("testpw2")
    print(response)
    login("abb", "testpw2")
    response = update_password("testpw")
    print(response)
    login("abb", "testpw")
    print("\n")
    return "done"
