import authenticate

token = {
    "access_token": "ya29.A0ARrdaM-oUGhQuyvXAQWsE-OrSOCZQqaFk3OydxFh-yW5h9WXebCS6hcD5kGEeuKV4GVb8cW7U6uTrakwnJsJWlvpmcaEdrecPNWPvSIakGN1-m2meerb4j7aXBmt6fpWnodhwlbW_l6qzt5dWvsxLSiRGgWl",
    "expires_in": 3599,
    "refresh_token": "1//03xnJpkpJifUnCgYIARAAGAMSNwF-L9IrFUllZf0_DxJDEJUsfooihWN7RiAdImQEdKlDiexZPj2ylFYRtmeyG190iT7p0EGtLDs",
    "scope": ["https://www.googleapis.com/auth/gmail.modify"],
    "token_type": "Bearer",
    "expires_at": 1643488292.6039147,
}


def test_user_oauth():
    assert type(authenticate.user_oauth()[0]) == str


def dummy_request(client=None, protected_url=None):
    if client is None:
        client = authenticate.set_up_oauth_client(token=token)
    if protected_url is None:
        protected_url = "https://www.googleapis.com/gmail/v1/users/me/messages"
    r = client.get(protected_url)
    return r.json()



def test_write_token_to_json(tmpdir):
    outfile = tmpdir.join("gmail_token.json")
    authenticate.write_token_to_json(token, path=str(outfile))
    contents = outfile.read()
    assert type(contents) == str
