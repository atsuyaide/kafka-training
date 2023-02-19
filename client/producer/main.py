import argparse
import os
from datetime import datetime

from dotenv import load_dotenv

import kafka


def load_env() -> None:
    dotenv_path = os.path.join(os.path.dirname(__file__), ".env")
    load_dotenv(dotenv_path)


def type_to_send(bootstrap_servers: str, topic: str) -> None:
    print(f"Connecting to {bootstrap_servers}...")
    producer = kafka.KafkaProducer(bootstrap_servers=bootstrap_servers)
    print("Press Enter to send")
    while True:
        key = str(datetime.now()).encode("utf-8")
        value = input(">> ").encode("utf-8")
        print(f"Sending... topic={topic} key={key} value={value}")
        producer.send(topic=topic, key=key, value=value)


def main() -> None:
    load_env()
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-b",
        "--bootstrap-servers",
        type=str,
        default=os.environ["BOOTSTRAP_SERVERS"],
        help="接続するブローカーの情報",
    )
    parser.add_argument(
        "-t", "--topic", type=str, required=True, help="メッセージを送信するトピック名"
    )
    args = parser.parse_args()

    try:
        type_to_send(bootstrap_servers=args.bootstrap_servers, topic=args.topic)
    except KeyboardInterrupt:
        print("Bye")
    except Exception as e:
        import traceback

        traceback.print_exc(e)


if __name__ == "__main__":
    main()
