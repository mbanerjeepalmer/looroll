import authenticate
import ingest

token = {
    "access_token": "ya29.A0ARrdaM-oUGhQuyvXAQWsE-OrSOCZQqaFk3OydxFh-yW5h9WXebCS6hcD5kGEeuKV4GVb8cW7U6uTrakwnJsJWlvpmcaEdrecPNWPvSIakGN1-m2meerb4j7aXBmt6fpWnodhwlbW_l6qzt5dWvsxLSiRGgWl",
    "expires_in": 3599,
    "refresh_token": "1//03xnJpkpJifUnCgYIARAAGAMSNwF-L9IrFUllZf0_DxJDEJUsfooihWN7RiAdImQEdKlDiexZPj2ylFYRtmeyG190iT7p0EGtLDs",
    "scope": ["https://www.googleapis.com/auth/gmail.modify"],
    "token_type": "Bearer",
    "expires_at": 1643488292.6039147,
}
message_id = "17ea77884d3f99f4"


def test_get_email():
    client = authenticate.refresh_access_token(token)
    assert type(ingest.get_email(client, message_id)) == dict


def test_write_complete_email_locally():
    client = authenticate.refresh_access_token(token)
    parsed_email = ingest.get_email(client, message_id)
    path = ingest.write_complete_email_locally(parsed_email)
    with open(path, "r") as infile:
        content = infile.read()
    assert len(content) > 0
