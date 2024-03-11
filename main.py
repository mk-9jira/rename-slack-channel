import os
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from slack_sdk.signature import SignatureVerifier


def try_channel_rename(client, body):
    try:
        client.conversations_rename(
            channel=body['channel_id'],
            name=body['text']
        )
    except SlackApiError:
        return False
    else:
        return True


def handle_slack_event(request):
    # Secretの読み込み
    slack_user_token = os.getenv("SLACK_USER_TOKEN", None)
    signing_secret = os.getenv("SIGNING_SECRET", None)
    
    # リクエストの検証
    verifier = SignatureVerifier(signing_secret)
    body = request.get_data(as_text=True) 
    if not verifier.is_valid_request(body, request.headers):
        raise ValueError("Invalid request/credentials.")
    ''' デバッグ
    else:
        print("Request verification was successed.")
        return
    '''
        
    # 後続処理のためリクエストをデコード
    slack_event_body = request.form
    print(slack_event_body)

    # API clientの作成
    user_client = WebClient(token=slack_user_token)

    # rename処理
    if try_channel_rename(user_client, slack_event_body):
        return {
            "text": "チャンネル名を変更しました！"
        }
    else:
        return {
            "text": "[error]チャンネル名の変更に失敗しました"
        }
